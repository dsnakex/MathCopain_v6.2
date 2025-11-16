"""
AssignmentEngine - Homework/Exercise assignment management

Handles:
- Creating and publishing assignments
- Generating adaptive exercises per student (ML integration)
- Tracking completion and progress
- Auto-grading and feedback
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import and_

from database.models import (
    Assignment, AssignmentCompletion, Classroom,
    ClassroomEnrollment, User, ExerciseResponse
)
from database.connection import get_session, DatabaseSession
from core.ml import DifficultyOptimizer


class AssignmentEngine:
    """
    Manages homework/exercise assignments for classrooms

    Integrates with ML to provide adaptive difficulty per student
    """

    def __init__(self, teacher_id: int):
        """
        Initialize AssignmentEngine

        Args:
            teacher_id: ID of the teacher creating assignments
        """
        self.teacher_id = teacher_id
        self.difficulty_optimizer = DifficultyOptimizer()

    # ========================================================================
    # ASSIGNMENT CREATION
    # ========================================================================

    def create_assignment(
        self,
        classroom_id: int,
        title: str,
        skill_domains: List[str],
        difficulty_levels: Optional[List[int]] = None,
        exercise_count: int = 10,
        due_date: Optional[datetime] = None,
        description: Optional[str] = None,
        adaptive: bool = True
    ) -> Dict:
        """
        Create a new assignment for a classroom

        Args:
            classroom_id: Classroom ID
            title: Assignment title
            skill_domains: List of domains (e.g., ["addition", "multiplication"])
            difficulty_levels: List of difficulty levels [1-5] or None for adaptive
            exercise_count: Number of exercises per student
            due_date: Due date (defaults to 7 days from now)
            description: Instructions for students
            adaptive: If True, use ML to adapt difficulty per student

        Returns:
            Dict with assignment details

        Raises:
            ValueError: If invalid parameters
        """
        # Validate domains
        valid_domains = [
            'addition', 'soustraction', 'multiplication', 'division',
            'fractions', 'decimaux', 'geometrie', 'mesures', 'proportionnalite'
        ]
        invalid_domains = [d for d in skill_domains if d not in valid_domains]
        if invalid_domains:
            raise ValueError(f"Invalid domains: {invalid_domains}")

        # Default due date: 7 days from now
        if not due_date:
            due_date = datetime.now() + timedelta(days=7)

        # Validate difficulty levels
        if difficulty_levels and not adaptive:
            invalid_levels = [d for d in difficulty_levels if d < 1 or d > 5]
            if invalid_levels:
                raise ValueError(f"Difficulty levels must be 1-5")

        with DatabaseSession() as session:
            # Verify classroom exists and belongs to teacher
            classroom = session.query(Classroom).filter(
                and_(
                    Classroom.id == classroom_id,
                    Classroom.teacher_id == self.teacher_id
                )
            ).first()

            if not classroom:
                raise ValueError("Classroom not found or not yours")

            # Create assignment
            assignment = Assignment(
                classroom_id=classroom_id,
                teacher_id=self.teacher_id,
                title=title,
                description=description,
                skill_domains=skill_domains,
                difficulty_levels=difficulty_levels if not adaptive else None,
                exercise_count=exercise_count,
                due_date=due_date,
                is_published=False  # Draft by default
            )

            session.add(assignment)
            session.flush()  # Get ID

            return {
                'id': assignment.id,
                'title': assignment.title,
                'classroom_id': classroom_id,
                'classroom_name': classroom.name,
                'skill_domains': skill_domains,
                'exercise_count': exercise_count,
                'due_date': due_date.isoformat(),
                'adaptive': adaptive,
                'is_published': False,
                'message': f"✓ Devoir '{title}' créé (brouillon)"
            }

    def publish_assignment(self, assignment_id: int) -> Dict:
        """
        Publish an assignment (make it visible to students)

        Also creates AssignmentCompletion records for all students

        Args:
            assignment_id: Assignment ID

        Returns:
            Dict with publish confirmation
        """
        with DatabaseSession() as session:
            # Get assignment
            assignment = session.query(Assignment).filter(
                and_(
                    Assignment.id == assignment_id,
                    Assignment.teacher_id == self.teacher_id
                )
            ).first()

            if not assignment:
                raise ValueError("Assignment not found")

            if assignment.is_published:
                return {
                    'id': assignment_id,
                    'message': "⚠️ Devoir déjà publié"
                }

            # Get all students in classroom
            students = session.query(User).join(
                ClassroomEnrollment,
                User.id == ClassroomEnrollment.student_id
            ).filter(
                and_(
                    ClassroomEnrollment.classroom_id == assignment.classroom_id,
                    ClassroomEnrollment.status == 'active'
                )
            ).all()

            # Create completion records for each student
            for student in students:
                completion = AssignmentCompletion(
                    assignment_id=assignment_id,
                    student_id=student.id,
                    exercises_total=assignment.exercise_count,
                    exercises_completed=0,
                    status='in_progress'
                )
                session.add(completion)

            # Mark as published
            assignment.is_published = True

            return {
                'id': assignment_id,
                'title': assignment.title,
                'students_assigned': len(students),
                'message': f"✓ Devoir publié pour {len(students)} élèves"
            }

    def update_assignment(
        self,
        assignment_id: int,
        **updates
    ) -> Dict:
        """
        Update assignment details

        Args:
            assignment_id: Assignment ID
            **updates: Fields to update

        Returns:
            Dict with updated assignment
        """
        with DatabaseSession() as session:
            assignment = session.query(Assignment).filter(
                and_(
                    Assignment.id == assignment_id,
                    Assignment.teacher_id == self.teacher_id
                )
            ).first()

            if not assignment:
                raise ValueError("Assignment not found")

            # Update allowed fields
            allowed_fields = [
                'title', 'description', 'skill_domains',
                'difficulty_levels', 'exercise_count', 'due_date'
            ]

            for field, value in updates.items():
                if field in allowed_fields:
                    setattr(assignment, field, value)

            return {
                'id': assignment_id,
                'message': "✓ Devoir mis à jour"
            }

    def delete_assignment(self, assignment_id: int) -> Dict:
        """
        Delete an assignment (and all completions)

        Args:
            assignment_id: Assignment ID

        Returns:
            Dict with confirmation
        """
        with DatabaseSession() as session:
            assignment = session.query(Assignment).filter(
                and_(
                    Assignment.id == assignment_id,
                    Assignment.teacher_id == self.teacher_id
                )
            ).first()

            if not assignment:
                raise ValueError("Assignment not found")

            # Delete (cascade will remove completions)
            session.delete(assignment)

            return {
                'id': assignment_id,
                'message': f"✓ Devoir '{assignment.title}' supprimé"
            }

    # ========================================================================
    # ADAPTIVE EXERCISE GENERATION (ML Integration)
    # ========================================================================

    def generate_student_exercises(
        self,
        assignment_id: int,
        student_id: int
    ) -> List[Dict]:
        """
        Generate personalized exercises for a student using ML

        Adapts difficulty based on student's proficiency

        Args:
            assignment_id: Assignment ID
            student_id: Student ID

        Returns:
            List of exercise definitions
        """
        with get_session() as session:
            assignment = session.query(Assignment).filter(
                Assignment.id == assignment_id
            ).first()

            if not assignment:
                raise ValueError("Assignment not found")

            exercises = []

            for domain in assignment.skill_domains:
                # Use ML to predict optimal difficulty
                if assignment.difficulty_levels is None:
                    # Adaptive mode - use ML
                    try:
                        difficulty, explanation = self.difficulty_optimizer.predict(
                            user_id=student_id,
                            skill_domain=domain,
                            apply_flow_adjustment=True
                        )
                    except:
                        # Fallback to medium difficulty
                        difficulty = 3
                else:
                    # Fixed difficulty - pick from specified levels
                    import random
                    difficulty = random.choice(assignment.difficulty_levels)

                # Generate exercise definition
                exercise = {
                    'domain': domain,
                    'difficulty': difficulty,
                    'type': self._determine_exercise_type(domain),
                    'ml_adapted': assignment.difficulty_levels is None
                }

                exercises.append(exercise)

            # If we need more exercises, duplicate with variations
            while len(exercises) < assignment.exercise_count:
                # Copy existing exercises with slight difficulty variation
                base_ex = exercises[len(exercises) % len(assignment.skill_domains)]
                new_ex = base_ex.copy()
                exercises.append(new_ex)

            return exercises[:assignment.exercise_count]

    def _determine_exercise_type(self, domain: str) -> str:
        """Determine exercise type based on domain"""
        type_mapping = {
            'addition': 'calculation',
            'soustraction': 'calculation',
            'multiplication': 'calculation',
            'division': 'calculation',
            'fractions': 'problem',
            'decimaux': 'problem',
            'geometrie': 'visual',
            'mesures': 'problem',
            'proportionnalite': 'problem'
        }
        return type_mapping.get(domain, 'calculation')

    # ========================================================================
    # COMPLETION TRACKING
    # ========================================================================

    def record_exercise_completion(
        self,
        assignment_id: int,
        student_id: int,
        is_correct: bool,
        time_taken: int
    ) -> Dict:
        """
        Record completion of one exercise in assignment

        Args:
            assignment_id: Assignment ID
            student_id: Student ID
            is_correct: Whether answer was correct
            time_taken: Time in seconds

        Returns:
            Dict with updated progress
        """
        with DatabaseSession() as session:
            completion = session.query(AssignmentCompletion).filter(
                and_(
                    AssignmentCompletion.assignment_id == assignment_id,
                    AssignmentCompletion.student_id == student_id
                )
            ).first()

            if not completion:
                raise ValueError("Assignment completion record not found")

            # Update progress
            completion.exercises_completed += 1

            # Calculate success rate
            # We'll need to query actual exercise responses for accurate rate
            responses = session.query(ExerciseResponse).filter(
                and_(
                    ExerciseResponse.user_id == student_id,
                    ExerciseResponse.created_at >= completion.assignment.created_at
                )
            ).all()

            if responses:
                correct_count = sum(1 for r in responses if r.is_correct)
                completion.success_rate = correct_count / len(responses)

            # Update time spent
            if completion.time_spent_seconds:
                completion.time_spent_seconds += time_taken
            else:
                completion.time_spent_seconds = time_taken

            # Check if completed
            if completion.exercises_completed >= completion.exercises_total:
                completion.status = 'completed'
                completion.completed_at = datetime.now()

            return {
                'assignment_id': assignment_id,
                'student_id': student_id,
                'progress': f"{completion.exercises_completed}/{completion.exercises_total}",
                'success_rate': completion.success_rate,
                'status': completion.status
            }

    def get_assignment_completion(
        self,
        assignment_id: int
    ) -> List[Dict]:
        """
        Get completion status for all students in assignment

        Args:
            assignment_id: Assignment ID

        Returns:
            List of completion dicts
        """
        with get_session() as session:
            completions = session.query(
                AssignmentCompletion,
                User
            ).join(
                User,
                AssignmentCompletion.student_id == User.id
            ).filter(
                AssignmentCompletion.assignment_id == assignment_id
            ).all()

            result = []
            for completion, user in completions:
                result.append({
                    'student_id': user.id,
                    'student_name': user.username,
                    'exercises_completed': completion.exercises_completed,
                    'exercises_total': completion.exercises_total,
                    'progress_percentage': (
                        completion.exercises_completed / completion.exercises_total * 100
                        if completion.exercises_total > 0 else 0
                    ),
                    'success_rate': completion.success_rate,
                    'time_spent_minutes': (
                        completion.time_spent_seconds // 60
                        if completion.time_spent_seconds else 0
                    ),
                    'status': completion.status,
                    'completed_at': (
                        completion.completed_at.isoformat()
                        if completion.completed_at else None
                    )
                })

            return result

    # ========================================================================
    # ASSIGNMENT LISTING & SEARCH
    # ========================================================================

    def list_assignments(
        self,
        classroom_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Dict]:
        """
        List assignments with filters

        Args:
            classroom_id: Filter by classroom (None = all classrooms)
            status: Filter by status ('active', 'past', 'draft')

        Returns:
            List of assignment dicts
        """
        with get_session() as session:
            query = session.query(Assignment).filter(
                Assignment.teacher_id == self.teacher_id
            )

            if classroom_id:
                query = query.filter(Assignment.classroom_id == classroom_id)

            now = datetime.now()

            if status == 'active':
                query = query.filter(
                    and_(
                        Assignment.is_published == True,
                        Assignment.due_date >= now
                    )
                )
            elif status == 'past':
                query = query.filter(
                    and_(
                        Assignment.is_published == True,
                        Assignment.due_date < now
                    )
                )
            elif status == 'draft':
                query = query.filter(Assignment.is_published == False)

            assignments = query.order_by(Assignment.created_at.desc()).all()

            result = []
            for assignment in assignments:
                # Get completion stats
                completions = session.query(AssignmentCompletion).filter(
                    AssignmentCompletion.assignment_id == assignment.id
                ).all()

                completed_count = sum(
                    1 for c in completions
                    if c.status == 'completed'
                )
                avg_success = (
                    sum(c.success_rate for c in completions if c.success_rate) / len(completions)
                    if completions else 0
                )

                result.append({
                    'id': assignment.id,
                    'title': assignment.title,
                    'classroom_id': assignment.classroom_id,
                    'skill_domains': assignment.skill_domains,
                    'exercise_count': assignment.exercise_count,
                    'due_date': assignment.due_date.isoformat(),
                    'is_published': assignment.is_published,
                    'students_assigned': len(completions),
                    'students_completed': completed_count,
                    'avg_success_rate': avg_success,
                    'created_at': assignment.created_at.isoformat()
                })

            return result
