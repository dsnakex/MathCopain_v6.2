"""
CurriculumMapper - Maps exercises to French National Curriculum

Handles:
- Loading official Éducation Nationale competencies (CE1-CM2)
- Mapping exercises to curriculum competencies
- Tracking student progress on official competencies
- Generating curriculum-aligned reports for teachers
- Identifying competency gaps
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
from sqlalchemy import and_, func

from database.models import (
    CurriculumCompetency, StudentCompetencyProgress,
    ExerciseResponse, User, SkillProfile
)
from database.connection import get_session, DatabaseSession


class CurriculumMapper:
    """
    Maps MathCopain exercises to French National Curriculum competencies

    Integrates with official Éducation Nationale standards for CE1-CM2
    """

    def __init__(self):
        """Initialize CurriculumMapper"""
        self.curriculum_data: Dict[str, List[Dict]] = {}
        self._load_curriculum_data()

    # ========================================================================
    # CURRICULUM DATA LOADING
    # ========================================================================

    def _load_curriculum_data(self) -> None:
        """Load curriculum data from JSON files"""
        data_dir = Path(__file__).parent.parent.parent / "data" / "curriculum"

        grade_levels = ['CE1', 'CE2', 'CM1', 'CM2']

        for grade in grade_levels:
            file_path = data_dir / f"EN_competences_{grade}.json"

            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.curriculum_data[grade] = json.load(f)
            else:
                # Will be created later with default data
                self.curriculum_data[grade] = []

    def sync_competencies_to_database(self) -> Dict:
        """
        Sync curriculum JSON data to database

        Should be run once after initial setup or when curriculum updates

        Returns:
            Dict with sync statistics
        """
        with DatabaseSession() as session:
            total_synced = 0
            total_updated = 0

            for grade_level, competencies in self.curriculum_data.items():
                for comp_data in competencies:
                    # Check if competency exists
                    existing = session.query(CurriculumCompetency).filter(
                        CurriculumCompetency.competency_code == comp_data['code']
                    ).first()

                    if existing:
                        # Update existing
                        existing.title = comp_data['title']
                        existing.description = comp_data.get('description')
                        existing.skill_domain = comp_data['domain']
                        existing.difficulty_range = comp_data.get('difficulty_range', [1, 5])
                        total_updated += 1
                    else:
                        # Create new
                        competency = CurriculumCompetency(
                            competency_code=comp_data['code'],
                            title=comp_data['title'],
                            description=comp_data.get('description'),
                            grade_level=grade_level,
                            skill_domain=comp_data['domain'],
                            difficulty_range=comp_data.get('difficulty_range', [1, 5]),
                            prerequisites=comp_data.get('prerequisites', [])
                        )
                        session.add(competency)
                        total_synced += 1

            return {
                'synced': total_synced,
                'updated': total_updated,
                'total': total_synced + total_updated,
                'message': f"✓ {total_synced} compétences ajoutées, {total_updated} mises à jour"
            }

    # ========================================================================
    # EXERCISE TO COMPETENCY MAPPING
    # ========================================================================

    def map_exercise_to_competencies(
        self,
        skill_domain: str,
        difficulty: int,
        grade_level: str,
        exercise_type: Optional[str] = None
    ) -> List[str]:
        """
        Map an exercise to relevant curriculum competencies

        Args:
            skill_domain: Domain (e.g., "addition", "multiplication")
            difficulty: Difficulty level (1-5)
            grade_level: Student grade level (CE1-CM2)
            exercise_type: Optional exercise type

        Returns:
            List of competency codes
        """
        with get_session() as session:
            query = session.query(CurriculumCompetency).filter(
                and_(
                    CurriculumCompetency.grade_level == grade_level,
                    CurriculumCompetency.skill_domain == skill_domain
                )
            )

            competencies = query.all()

            # Filter by difficulty range
            matching_codes = []
            for comp in competencies:
                diff_min, diff_max = comp.difficulty_range
                if diff_min <= difficulty <= diff_max:
                    matching_codes.append(comp.competency_code)

            return matching_codes

    def get_competency_details(self, competency_code: str) -> Optional[Dict]:
        """
        Get full details of a competency

        Args:
            competency_code: Competency code (e.g., "CE2.N.1.2")

        Returns:
            Dict with competency details or None
        """
        with get_session() as session:
            comp = session.query(CurriculumCompetency).filter(
                CurriculumCompetency.competency_code == competency_code
            ).first()

            if not comp:
                return None

            return {
                'code': comp.competency_code,
                'title': comp.title,
                'description': comp.description,
                'grade_level': comp.grade_level,
                'skill_domain': comp.skill_domain,
                'difficulty_range': comp.difficulty_range,
                'prerequisites': comp.prerequisites
            }

    # ========================================================================
    # STUDENT COMPETENCY PROGRESS TRACKING
    # ========================================================================

    def update_student_competency_progress(
        self,
        student_id: int,
        competency_code: str,
        is_correct: bool,
        exercise_difficulty: int
    ) -> Dict:
        """
        Update student progress on a competency after exercise completion

        Uses a simple mastery algorithm:
        - mastery_level increases with correct answers at appropriate difficulty
        - mastery_level decreases slightly with incorrect answers
        - mastery_level in [0.0, 1.0] where 0.8+ = mastered

        Args:
            student_id: Student ID
            competency_code: Competency code
            is_correct: Whether exercise was correct
            exercise_difficulty: Difficulty of completed exercise

        Returns:
            Dict with updated progress
        """
        with DatabaseSession() as session:
            # Get or create progress record
            progress = session.query(StudentCompetencyProgress).filter(
                and_(
                    StudentCompetencyProgress.student_id == student_id,
                    StudentCompetencyProgress.competency_code == competency_code
                )
            ).first()

            if not progress:
                # Create new progress record
                progress = StudentCompetencyProgress(
                    student_id=student_id,
                    competency_code=competency_code,
                    mastery_level=0.0,
                    exercises_completed=0,
                    exercises_correct=0
                )
                session.add(progress)

            # Update statistics
            progress.exercises_completed += 1
            if is_correct:
                progress.exercises_correct += 1

            # Update mastery level (weighted by difficulty)
            difficulty_weight = exercise_difficulty / 5.0  # Normalize to [0, 1]

            if is_correct:
                # Increase mastery (more for harder exercises)
                increment = 0.1 * difficulty_weight
                progress.mastery_level = min(1.0, progress.mastery_level + increment)

                # Update last practice date
                progress.last_practiced = datetime.now()

                # Check if mastered (80%+ and at least 5 exercises)
                if (progress.mastery_level >= 0.8 and
                    progress.exercises_completed >= 5 and
                    not progress.is_mastered):
                    progress.is_mastered = True
                    progress.mastered_at = datetime.now()
            else:
                # Decrease mastery slightly (less penalty for harder exercises)
                decrement = 0.05 * (1.0 - difficulty_weight)
                progress.mastery_level = max(0.0, progress.mastery_level - decrement)

                # Unmaster if mastery drops below threshold
                if progress.mastery_level < 0.7 and progress.is_mastered:
                    progress.is_mastered = False
                    progress.mastered_at = None

            # Calculate success rate
            progress.success_rate = (
                progress.exercises_correct / progress.exercises_completed
                if progress.exercises_completed > 0 else 0.0
            )

            session.flush()

            return {
                'student_id': student_id,
                'competency_code': competency_code,
                'mastery_level': progress.mastery_level,
                'is_mastered': progress.is_mastered,
                'success_rate': progress.success_rate,
                'exercises_completed': progress.exercises_completed
            }

    def bulk_update_from_exercise_history(
        self,
        student_id: int,
        grade_level: str,
        days_back: int = 30
    ) -> Dict:
        """
        Bulk update competency progress from recent exercise history

        Useful for backfilling progress or recalculating after curriculum changes

        Args:
            student_id: Student ID
            grade_level: Student grade level
            days_back: Number of days to look back

        Returns:
            Dict with update statistics
        """
        with get_session() as session:
            # Get recent exercise responses
            cutoff_date = datetime.now() - timedelta(days=days_back)

            exercises = session.query(ExerciseResponse).filter(
                and_(
                    ExerciseResponse.user_id == student_id,
                    ExerciseResponse.created_at >= cutoff_date
                )
            ).all()

            competencies_updated = set()

            for exercise in exercises:
                # Map exercise to competencies
                competency_codes = self.map_exercise_to_competencies(
                    skill_domain=exercise.skill_domain,
                    difficulty=exercise.difficulty,
                    grade_level=grade_level,
                    exercise_type=exercise.exercise_type
                )

                # Update each competency
                for code in competency_codes:
                    self.update_student_competency_progress(
                        student_id=student_id,
                        competency_code=code,
                        is_correct=exercise.is_correct,
                        exercise_difficulty=exercise.difficulty
                    )
                    competencies_updated.add(code)

            return {
                'exercises_processed': len(exercises),
                'competencies_updated': len(competencies_updated),
                'date_range': f"{days_back} derniers jours",
                'message': f"✓ {len(competencies_updated)} compétences mises à jour"
            }

    # ========================================================================
    # COMPETENCY REPORTS
    # ========================================================================

    def get_student_competency_report(
        self,
        student_id: int,
        grade_level: str,
        skill_domain: Optional[str] = None
    ) -> Dict:
        """
        Generate comprehensive competency report for a student

        Args:
            student_id: Student ID
            grade_level: Grade level (CE1-CM2)
            skill_domain: Optional filter by domain

        Returns:
            Dict with competency breakdown
        """
        with get_session() as session:
            # Get all competencies for grade level
            query = session.query(CurriculumCompetency).filter(
                CurriculumCompetency.grade_level == grade_level
            )

            if skill_domain:
                query = query.filter(CurriculumCompetency.skill_domain == skill_domain)

            all_competencies = query.all()

            # Get student progress
            progress_records = session.query(StudentCompetencyProgress).filter(
                StudentCompetencyProgress.student_id == student_id
            ).all()

            # Create progress lookup
            progress_map = {
                p.competency_code: p for p in progress_records
            }

            # Build report
            competencies = []
            mastered_count = 0
            in_progress_count = 0
            not_started_count = 0

            for comp in all_competencies:
                progress = progress_map.get(comp.competency_code)

                if progress:
                    status = 'mastered' if progress.is_mastered else 'in_progress'
                    mastery_level = progress.mastery_level
                    exercises_completed = progress.exercises_completed
                    success_rate = progress.success_rate
                    last_practiced = progress.last_practiced

                    if progress.is_mastered:
                        mastered_count += 1
                    else:
                        in_progress_count += 1
                else:
                    status = 'not_started'
                    mastery_level = 0.0
                    exercises_completed = 0
                    success_rate = 0.0
                    last_practiced = None
                    not_started_count += 1

                competencies.append({
                    'code': comp.competency_code,
                    'title': comp.title,
                    'domain': comp.skill_domain,
                    'difficulty_range': comp.difficulty_range,
                    'status': status,
                    'mastery_level': mastery_level,
                    'exercises_completed': exercises_completed,
                    'success_rate': success_rate,
                    'last_practiced': last_practiced.isoformat() if last_practiced else None
                })

            # Calculate overall stats
            total = len(all_competencies)
            completion_rate = mastered_count / total if total > 0 else 0.0

            return {
                'student_id': student_id,
                'grade_level': grade_level,
                'skill_domain': skill_domain,
                'summary': {
                    'total_competencies': total,
                    'mastered': mastered_count,
                    'in_progress': in_progress_count,
                    'not_started': not_started_count,
                    'completion_rate': completion_rate
                },
                'competencies': competencies
            }

    def get_class_competency_overview(
        self,
        student_ids: List[int],
        grade_level: str
    ) -> Dict:
        """
        Get competency overview for entire class

        Args:
            student_ids: List of student IDs
            grade_level: Grade level

        Returns:
            Dict with class-wide competency statistics
        """
        with get_session() as session:
            # Get all competencies for grade
            competencies = session.query(CurriculumCompetency).filter(
                CurriculumCompetency.grade_level == grade_level
            ).all()

            competency_stats = []

            for comp in competencies:
                # Get progress for all students on this competency
                progress_records = session.query(StudentCompetencyProgress).filter(
                    and_(
                        StudentCompetencyProgress.competency_code == comp.competency_code,
                        StudentCompetencyProgress.student_id.in_(student_ids)
                    )
                ).all()

                mastered_count = sum(1 for p in progress_records if p.is_mastered)
                avg_mastery = (
                    sum(p.mastery_level for p in progress_records) / len(progress_records)
                    if progress_records else 0.0
                )

                students_attempted = len(progress_records)

                competency_stats.append({
                    'code': comp.competency_code,
                    'title': comp.title,
                    'domain': comp.skill_domain,
                    'students_mastered': mastered_count,
                    'students_attempted': students_attempted,
                    'mastery_rate': mastered_count / len(student_ids) if student_ids else 0.0,
                    'avg_mastery_level': avg_mastery,
                    'difficulty_range': comp.difficulty_range
                })

            # Overall class stats
            total_comps = len(competencies)
            avg_class_mastery = (
                sum(c['avg_mastery_level'] for c in competency_stats) / total_comps
                if total_comps > 0 else 0.0
            )

            return {
                'grade_level': grade_level,
                'student_count': len(student_ids),
                'total_competencies': total_comps,
                'avg_class_mastery': avg_class_mastery,
                'competencies': competency_stats
            }

    # ========================================================================
    # RECOMMENDATIONS & GAP ANALYSIS
    # ========================================================================

    def identify_competency_gaps(
        self,
        student_id: int,
        grade_level: str
    ) -> List[Dict]:
        """
        Identify competency gaps requiring attention

        Args:
            student_id: Student ID
            grade_level: Grade level

        Returns:
            List of competencies needing work (sorted by priority)
        """
        report = self.get_student_competency_report(student_id, grade_level)

        gaps = []

        for comp in report['competencies']:
            # Gap if:
            # 1. Not started (highest priority)
            # 2. In progress but low mastery
            # 3. Not practiced recently (stale)

            priority_score = 0
            reason = ""

            if comp['status'] == 'not_started':
                priority_score = 10
                reason = "Non démarré"
            elif comp['status'] == 'in_progress':
                # Priority based on mastery level (lower = higher priority)
                priority_score = 5 + (1.0 - comp['mastery_level']) * 5

                if comp['mastery_level'] < 0.3:
                    reason = "Maîtrise faible"
                elif comp['mastery_level'] < 0.6:
                    reason = "En cours d'acquisition"
                else:
                    reason = "Presque maîtrisé"

                # Check if stale (not practiced in 14 days)
                if comp['last_practiced']:
                    last_date = datetime.fromisoformat(comp['last_practiced'])
                    if datetime.now() - last_date > timedelta(days=14):
                        priority_score += 2
                        reason += " (non pratiqué récemment)"

            if priority_score > 0:
                gaps.append({
                    'code': comp['code'],
                    'title': comp['title'],
                    'domain': comp['domain'],
                    'mastery_level': comp['mastery_level'],
                    'priority_score': priority_score,
                    'reason': reason,
                    'recommended_difficulty': comp['difficulty_range'][0]  # Start with easiest
                })

        # Sort by priority (highest first)
        gaps.sort(key=lambda x: x['priority_score'], reverse=True)

        return gaps

    def recommend_next_competencies(
        self,
        student_id: int,
        grade_level: str,
        count: int = 3
    ) -> List[Dict]:
        """
        Recommend next competencies to work on

        Args:
            student_id: Student ID
            grade_level: Grade level
            count: Number of recommendations

        Returns:
            List of recommended competencies
        """
        gaps = self.identify_competency_gaps(student_id, grade_level)

        # Take top N gaps
        recommendations = gaps[:count]

        # Add reasoning for each
        for rec in recommendations:
            if rec['priority_score'] >= 8:
                rec['recommendation'] = f"Commencer par {rec['title']} - compétence fondamentale"
            elif rec['priority_score'] >= 5:
                rec['recommendation'] = f"Renforcer {rec['title']} avec exercices ciblés"
            else:
                rec['recommendation'] = f"Réviser {rec['title']} pour consolider"

        return recommendations


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_competencies_by_domain(grade_level: str, skill_domain: str) -> List[Dict]:
    """
    Get all competencies for a specific domain and grade

    Args:
        grade_level: Grade level (CE1-CM2)
        skill_domain: Skill domain

    Returns:
        List of competency dicts
    """
    with get_session() as session:
        competencies = session.query(CurriculumCompetency).filter(
            and_(
                CurriculumCompetency.grade_level == grade_level,
                CurriculumCompetency.skill_domain == skill_domain
            )
        ).all()

        return [
            {
                'code': c.competency_code,
                'title': c.title,
                'description': c.description,
                'difficulty_range': c.difficulty_range
            }
            for c in competencies
        ]
