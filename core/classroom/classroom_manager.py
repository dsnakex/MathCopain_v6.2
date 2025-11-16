"""
ClassroomManager - Backend for classroom management

Handles all classroom operations for teachers:
- Create/update/delete classrooms
- Enroll/remove students
- Get classroom overview with real-time stats
- Monitor student progress
- Generate class reports
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from sqlalchemy import func, and_
from sqlalchemy.exc import IntegrityError

from database.models import (
    TeacherAccount, Classroom, ClassroomEnrollment,
    User, ExerciseResponse, SkillProfile,
    Assignment, AssignmentCompletion
)
from database.connection import get_session, DatabaseSession
from core.ml import PerformancePredictor


class ClassroomManager:
    """
    Manages classroom operations for teachers

    Provides complete CRUD operations and analytics
    """

    def __init__(self, teacher_id: int):
        """
        Initialize ClassroomManager for a teacher

        Args:
            teacher_id: ID of the teacher
        """
        self.teacher_id = teacher_id
        self.ml_predictor = PerformancePredictor()

    # ========================================================================
    # CLASSROOM CRUD OPERATIONS
    # ========================================================================

    def create_classroom(
        self,
        name: str,
        grade_level: str,
        school_year: Optional[str] = None,
        max_students: int = 30,
        description: Optional[str] = None
    ) -> Dict:
        """
        Create a new classroom

        Args:
            name: Classroom name (e.g., "CE2 - Classe A")
            grade_level: Grade level (CE1, CE2, CM1, CM2)
            school_year: School year (e.g., "2025-2026")
            max_students: Maximum number of students
            description: Optional description

        Returns:
            Dict with classroom info

        Raises:
            ValueError: If invalid parameters
        """
        # Validate grade level
        valid_grades = ['CE1', 'CE2', 'CM1', 'CM2']
        if grade_level not in valid_grades:
            raise ValueError(f"Invalid grade_level. Must be one of: {valid_grades}")

        # Auto-generate school year if not provided
        if not school_year:
            current_year = datetime.now().year
            school_year = f"{current_year}-{current_year + 1}"

        with DatabaseSession() as session:
            classroom = Classroom(
                teacher_id=self.teacher_id,
                name=name,
                grade_level=grade_level,
                school_year=school_year,
                max_students=max_students,
                description=description,
                is_active=True
            )

            session.add(classroom)
            session.flush()  # Get ID

            return {
                'id': classroom.id,
                'name': classroom.name,
                'grade_level': classroom.grade_level,
                'school_year': classroom.school_year,
                'max_students': classroom.max_students,
                'created_at': classroom.created_at.isoformat(),
                'message': f"✓ Classe '{name}' créée avec succès"
            }

    def update_classroom(
        self,
        classroom_id: int,
        **updates
    ) -> Dict:
        """
        Update classroom information

        Args:
            classroom_id: Classroom ID
            **updates: Fields to update (name, description, max_students, etc.)

        Returns:
            Dict with updated classroom info
        """
        with DatabaseSession() as session:
            classroom = session.query(Classroom).filter(
                and_(
                    Classroom.id == classroom_id,
                    Classroom.teacher_id == self.teacher_id
                )
            ).first()

            if not classroom:
                raise ValueError(f"Classroom {classroom_id} not found or not yours")

            # Update allowed fields
            allowed_fields = ['name', 'description', 'max_students', 'is_active']
            for field, value in updates.items():
                if field in allowed_fields:
                    setattr(classroom, field, value)

            return {
                'id': classroom.id,
                'name': classroom.name,
                'message': "✓ Classe mise à jour"
            }

    def delete_classroom(self, classroom_id: int) -> Dict:
        """
        Delete a classroom (soft delete - sets is_active=False)

        Args:
            classroom_id: Classroom ID

        Returns:
            Dict with confirmation message
        """
        with DatabaseSession() as session:
            classroom = session.query(Classroom).filter(
                and_(
                    Classroom.id == classroom_id,
                    Classroom.teacher_id == self.teacher_id
                )
            ).first()

            if not classroom:
                raise ValueError(f"Classroom {classroom_id} not found")

            # Soft delete
            classroom.is_active = False

            return {
                'id': classroom_id,
                'message': f"✓ Classe '{classroom.name}' archivée"
            }

    def get_classroom(self, classroom_id: int) -> Dict:
        """
        Get classroom details

        Args:
            classroom_id: Classroom ID

        Returns:
            Dict with complete classroom information
        """
        with get_session() as session:
            classroom = session.query(Classroom).filter(
                and_(
                    Classroom.id == classroom_id,
                    Classroom.teacher_id == self.teacher_id
                )
            ).first()

            if not classroom:
                raise ValueError(f"Classroom {classroom_id} not found")

            # Count students
            student_count = session.query(ClassroomEnrollment).filter(
                and_(
                    ClassroomEnrollment.classroom_id == classroom_id,
                    ClassroomEnrollment.status == 'active'
                )
            ).count()

            return {
                'id': classroom.id,
                'name': classroom.name,
                'grade_level': classroom.grade_level,
                'school_year': classroom.school_year,
                'max_students': classroom.max_students,
                'student_count': student_count,
                'description': classroom.description,
                'is_active': classroom.is_active,
                'created_at': classroom.created_at.isoformat()
            }

    def list_classrooms(self, active_only: bool = True) -> List[Dict]:
        """
        List all teacher's classrooms

        Args:
            active_only: If True, only return active classrooms

        Returns:
            List of classroom dicts
        """
        with get_session() as session:
            query = session.query(Classroom).filter(
                Classroom.teacher_id == self.teacher_id
            )

            if active_only:
                query = query.filter(Classroom.is_active == True)

            classrooms = query.order_by(Classroom.created_at.desc()).all()

            result = []
            for classroom in classrooms:
                # Count students
                student_count = session.query(ClassroomEnrollment).filter(
                    and_(
                        ClassroomEnrollment.classroom_id == classroom.id,
                        ClassroomEnrollment.status == 'active'
                    )
                ).count()

                result.append({
                    'id': classroom.id,
                    'name': classroom.name,
                    'grade_level': classroom.grade_level,
                    'student_count': student_count,
                    'max_students': classroom.max_students,
                    'school_year': classroom.school_year
                })

            return result

    # ========================================================================
    # STUDENT ENROLLMENT
    # ========================================================================

    def add_student(
        self,
        classroom_id: int,
        student_username: str
    ) -> Dict:
        """
        Add a student to classroom

        Args:
            classroom_id: Classroom ID
            student_username: Student username

        Returns:
            Dict with enrollment confirmation

        Raises:
            ValueError: If student not found or classroom full
        """
        with DatabaseSession() as session:
            # Verify classroom belongs to teacher
            classroom = session.query(Classroom).filter(
                and_(
                    Classroom.id == classroom_id,
                    Classroom.teacher_id == self.teacher_id,
                    Classroom.is_active == True
                )
            ).first()

            if not classroom:
                raise ValueError("Classroom not found or inactive")

            # Find student
            student = session.query(User).filter(
                User.username == student_username
            ).first()

            if not student:
                raise ValueError(f"Student '{student_username}' not found")

            # Check if classroom is full
            current_students = session.query(ClassroomEnrollment).filter(
                and_(
                    ClassroomEnrollment.classroom_id == classroom_id,
                    ClassroomEnrollment.status == 'active'
                )
            ).count()

            if current_students >= classroom.max_students:
                raise ValueError(f"Classroom is full ({classroom.max_students} students max)")

            # Check if already enrolled
            existing = session.query(ClassroomEnrollment).filter(
                and_(
                    ClassroomEnrollment.classroom_id == classroom_id,
                    ClassroomEnrollment.student_id == student.id
                )
            ).first()

            if existing:
                if existing.status == 'active':
                    raise ValueError(f"Student '{student_username}' already enrolled")
                else:
                    # Reactivate
                    existing.status = 'active'
                    existing.enrolled_at = datetime.now()
                    message = f"✓ {student_username} ré-inscrit dans {classroom.name}"
            else:
                # Create new enrollment
                enrollment = ClassroomEnrollment(
                    classroom_id=classroom_id,
                    student_id=student.id,
                    status='active'
                )
                session.add(enrollment)
                message = f"✓ {student_username} ajouté à {classroom.name}"

            return {
                'classroom_id': classroom_id,
                'student_id': student.id,
                'student_username': student_username,
                'message': message
            }

    def remove_student(
        self,
        classroom_id: int,
        student_id: int,
        status: str = 'withdrawn'
    ) -> Dict:
        """
        Remove student from classroom

        Args:
            classroom_id: Classroom ID
            student_id: Student ID
            status: New status (withdrawn, completed)

        Returns:
            Dict with confirmation
        """
        with DatabaseSession() as session:
            enrollment = session.query(ClassroomEnrollment).filter(
                and_(
                    ClassroomEnrollment.classroom_id == classroom_id,
                    ClassroomEnrollment.student_id == student_id
                )
            ).first()

            if not enrollment:
                raise ValueError("Enrollment not found")

            enrollment.status = status

            return {
                'classroom_id': classroom_id,
                'student_id': student_id,
                'message': f"✓ Élève retiré de la classe"
            }

    def get_classroom_students(
        self,
        classroom_id: int,
        active_only: bool = True
    ) -> List[Dict]:
        """
        Get all students in a classroom with their stats

        Args:
            classroom_id: Classroom ID
            active_only: Only return active enrollments

        Returns:
            List of student dicts with performance metrics
        """
        with get_session() as session:
            query = session.query(
                User,
                ClassroomEnrollment
            ).join(
                ClassroomEnrollment,
                User.id == ClassroomEnrollment.student_id
            ).filter(
                ClassroomEnrollment.classroom_id == classroom_id
            )

            if active_only:
                query = query.filter(ClassroomEnrollment.status == 'active')

            enrollments = query.all()

            students = []
            for user, enrollment in enrollments:
                # Get recent performance (last 30 days)
                thirty_days_ago = datetime.now() - timedelta(days=30)

                recent_exercises = session.query(ExerciseResponse).filter(
                    and_(
                        ExerciseResponse.user_id == user.id,
                        ExerciseResponse.created_at >= thirty_days_ago
                    )
                ).all()

                exercises_completed = len(recent_exercises)
                success_count = sum(1 for ex in recent_exercises if ex.is_correct)
                success_rate = success_count / exercises_completed if exercises_completed > 0 else 0

                # Get last activity
                last_activity = session.query(ExerciseResponse).filter(
                    ExerciseResponse.user_id == user.id
                ).order_by(ExerciseResponse.created_at.desc()).first()

                last_activity_date = last_activity.created_at if last_activity else None

                # Check if at risk (ML prediction)
                at_risk = False
                risk_score = 0.0
                if exercises_completed >= 5:
                    # Use ML to detect at-risk
                    try:
                        # Get average success probability across all domains
                        risk_score = 1.0 - success_rate  # Simple heuristic
                        at_risk = risk_score >= 0.40  # 40% risk threshold
                    except:
                        pass

                students.append({
                    'id': user.id,
                    'username': user.username,
                    'grade_level': user.grade_level,
                    'learning_style': user.learning_style,
                    'enrolled_at': enrollment.enrolled_at.isoformat(),
                    'status': enrollment.status,
                    'exercises_completed': exercises_completed,
                    'success_rate': success_rate,
                    'last_activity': last_activity_date.isoformat() if last_activity_date else None,
                    'at_risk': at_risk,
                    'risk_score': risk_score
                })

            return students

    # ========================================================================
    # CLASSROOM ANALYTICS
    # ========================================================================

    def get_classroom_overview(self, classroom_id: int) -> Dict:
        """
        Get complete classroom overview with real-time analytics

        Args:
            classroom_id: Classroom ID

        Returns:
            Dict with comprehensive classroom statistics
        """
        classroom = self.get_classroom(classroom_id)
        students = self.get_classroom_students(classroom_id)

        if not students:
            return {
                **classroom,
                'students': [],
                'stats': {
                    'total_students': 0,
                    'avg_success_rate': 0.0,
                    'total_exercises': 0,
                    'at_risk_count': 0
                }
            }

        # Calculate class statistics
        total_exercises = sum(s['exercises_completed'] for s in students)
        avg_success_rate = sum(s['success_rate'] for s in students) / len(students)
        at_risk_count = sum(1 for s in students if s['at_risk'])

        # Active students (exercised in last 7 days)
        seven_days_ago = datetime.now() - timedelta(days=7)
        active_students = sum(
            1 for s in students
            if s['last_activity'] and datetime.fromisoformat(s['last_activity']) >= seven_days_ago
        )

        stats = {
            'total_students': len(students),
            'active_students_7d': active_students,
            'avg_success_rate': avg_success_rate,
            'total_exercises': total_exercises,
            'avg_exercises_per_student': total_exercises / len(students),
            'at_risk_count': at_risk_count,
            'at_risk_percentage': at_risk_count / len(students) if students else 0
        }

        return {
            **classroom,
            'students': students,
            'stats': stats
        }

    def get_at_risk_students(
        self,
        classroom_id: int,
        threshold: float = 0.40
    ) -> List[Dict]:
        """
        Identify students at risk of failing

        Args:
            classroom_id: Classroom ID
            threshold: Risk threshold (0-1)

        Returns:
            List of at-risk students with recommendations
        """
        students = self.get_classroom_students(classroom_id)

        at_risk = []
        for student in students:
            if student['at_risk'] and student['risk_score'] >= threshold:
                # Identify struggling domain
                struggling_domain = self._identify_struggling_domain(student['id'])

                at_risk.append({
                    'id': student['id'],
                    'username': student['username'],
                    'risk_score': student['risk_score'],
                    'risk_level': self._classify_risk_level(student['risk_score']),
                    'success_rate': student['success_rate'],
                    'struggling_domain': struggling_domain,
                    'recommendation': self._generate_recommendation(
                        student['risk_score'],
                        struggling_domain
                    )
                })

        # Sort by risk score (highest first)
        at_risk.sort(key=lambda x: x['risk_score'], reverse=True)

        return at_risk

    def _identify_struggling_domain(self, student_id: int) -> str:
        """Identify which domain student struggles most with"""
        with get_session() as session:
            # Get skill profiles
            profiles = session.query(SkillProfile).filter(
                SkillProfile.user_id == student_id
            ).all()

            if not profiles:
                return "unknown"

            # Find lowest proficiency
            lowest = min(profiles, key=lambda p: p.proficiency_level)
            return lowest.skill_domain

    def _classify_risk_level(self, risk_score: float) -> str:
        """Classify risk level"""
        if risk_score >= 0.80:
            return "CRITICAL"
        elif risk_score >= 0.60:
            return "HIGH"
        elif risk_score >= 0.40:
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_recommendation(self, risk_score: float, domain: str) -> str:
        """Generate recommendation based on risk"""
        if risk_score >= 0.80:
            return f"Intervention immédiate requise - Revoir les bases de {domain}"
        elif risk_score >= 0.60:
            return f"Suivi rapproché et exercices de renforcement en {domain}"
        elif risk_score >= 0.40:
            return f"Exercices de révision conseillés en {domain}"
        else:
            return "Continuer avec suivi régulier"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def verify_teacher_access(teacher_id: int, classroom_id: int) -> bool:
    """
    Verify that teacher has access to classroom

    Args:
        teacher_id: Teacher ID
        classroom_id: Classroom ID

    Returns:
        bool: True if teacher owns classroom
    """
    with get_session() as session:
        classroom = session.query(Classroom).filter(
            and_(
                Classroom.id == classroom_id,
                Classroom.teacher_id == teacher_id
            )
        ).first()

        return classroom is not None
