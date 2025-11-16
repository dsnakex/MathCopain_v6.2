"""
ReportGenerator - Export reports for teachers in multiple formats

Supports:
- PDF reports (individual students, class overview, competency reports)
- CSV exports (progress data, assignment results, analytics)
- Structured data for PowerPoint/presentation generation
- Email-ready summary reports
"""

from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import csv
import json

from database.models import User
from database.connection import get_session
from core.classroom.classroom_manager import ClassroomManager
from core.classroom.assignment_engine import AssignmentEngine
from core.classroom.curriculum_mapper import CurriculumMapper
from core.classroom.analytics_engine import AnalyticsEngine


class ReportGenerator:
    """
    Generates comprehensive reports for teachers

    Integrates data from all classroom modules
    """

    def __init__(self, teacher_id: int):
        """
        Initialize ReportGenerator

        Args:
            teacher_id: Teacher ID
        """
        self.teacher_id = teacher_id
        self.classroom_manager = ClassroomManager(teacher_id)
        self.assignment_engine = AssignmentEngine(teacher_id)
        self.curriculum_mapper = CurriculumMapper()
        self.analytics_engine = AnalyticsEngine()

    # ========================================================================
    # STUDENT REPORTS
    # ========================================================================

    def generate_student_progress_report(
        self,
        student_id: int,
        classroom_id: int,
        format: str = 'structured',
        days_back: int = 30
    ) -> Dict:
        """
        Generate comprehensive student progress report

        Args:
            student_id: Student ID
            classroom_id: Classroom ID
            format: 'structured', 'pdf', or 'csv'
            days_back: Number of days to include

        Returns:
            Dict with report data (or file path if PDF)
        """
        with get_session() as session:
            # Get student info
            student = session.query(User).filter(User.id == student_id).first()

            if not student:
                raise ValueError(f"Student {student_id} not found")

            # Gather all data
            # 1. Engagement metrics
            engagement = self.analytics_engine.get_student_engagement_metrics(
                student_id=student_id,
                days_back=days_back
            )

            # 2. Progress trajectory
            trajectory = self.analytics_engine.get_student_progress_trajectory(
                student_id=student_id,
                days_back=days_back
            )

            # 3. Performance heatmap
            heatmap = self.analytics_engine.generate_performance_heatmap(
                student_id=student_id,
                days_back=days_back
            )

            # 4. Competency report
            competency_report = self.curriculum_mapper.get_student_competency_report(
                student_id=student_id,
                grade_level=student.grade_level
            )

            # 5. Recommendations
            recommendations = self.curriculum_mapper.recommend_next_competencies(
                student_id=student_id,
                grade_level=student.grade_level,
                count=5
            )

            # 6. Forecasts for all domains
            forecasts = {}
            for domain_row in heatmap['heatmap']:
                domain = domain_row['domain']
                try:
                    forecast = self.analytics_engine.forecast_student_performance(
                        student_id=student_id,
                        skill_domain=domain,
                        days_ahead=7
                    )
                    forecasts[domain] = forecast
                except:
                    pass

            report_data = {
                'generated_at': datetime.now().isoformat(),
                'report_type': 'student_progress',
                'period_days': days_back,
                'student': {
                    'id': student.id,
                    'username': student.username,
                    'grade_level': student.grade_level,
                    'learning_style': student.learning_style
                },
                'engagement': engagement,
                'trajectory': trajectory,
                'performance_heatmap': heatmap,
                'competencies': competency_report,
                'recommendations': recommendations,
                'forecasts': forecasts
            }

            if format == 'structured':
                return report_data
            elif format == 'csv':
                return self._export_student_report_csv(report_data, student.username)
            elif format == 'pdf':
                return self._export_student_report_pdf(report_data)
            else:
                raise ValueError(f"Unsupported format: {format}")

    def generate_at_risk_report(
        self,
        classroom_id: int,
        threshold: float = 0.40
    ) -> Dict:
        """
        Generate report of at-risk students in classroom

        Args:
            classroom_id: Classroom ID
            threshold: Risk threshold

        Returns:
            Dict with at-risk student data
        """
        # Get at-risk students
        at_risk = self.classroom_manager.get_at_risk_students(
            classroom_id=classroom_id,
            threshold=threshold
        )

        # Get detailed info for each
        detailed_students = []
        for student in at_risk:
            # Get competency gaps
            gaps = self.curriculum_mapper.identify_competency_gaps(
                student_id=student['id'],
                grade_level=student.get('grade_level', 'CE2')  # Default
            )

            # Get engagement
            engagement = self.analytics_engine.get_student_engagement_metrics(
                student_id=student['id'],
                days_back=30
            )

            detailed_students.append({
                **student,
                'competency_gaps': gaps[:3],  # Top 3 gaps
                'engagement_level': engagement.get('engagement_level', 'unknown'),
                'engagement_score': engagement.get('engagement_score', 0)
            })

        return {
            'generated_at': datetime.now().isoformat(),
            'report_type': 'at_risk_students',
            'classroom_id': classroom_id,
            'threshold': threshold,
            'total_at_risk': len(at_risk),
            'students': detailed_students,
            'summary': self._generate_at_risk_summary(detailed_students)
        }

    # ========================================================================
    # CLASS REPORTS
    # ========================================================================

    def generate_class_overview_report(
        self,
        classroom_id: int,
        days_back: int = 30
    ) -> Dict:
        """
        Generate comprehensive class overview report

        Args:
            classroom_id: Classroom ID
            days_back: Number of days

        Returns:
            Dict with class-wide analytics
        """
        # Get classroom overview
        overview = self.classroom_manager.get_classroom_overview(classroom_id)

        student_ids = [s['id'] for s in overview['students']]

        # Class trajectory
        class_trajectory = self.analytics_engine.get_class_progress_trajectory(
            student_ids=student_ids,
            days_back=days_back
        )

        # Competency overview
        competency_overview = self.curriculum_mapper.get_class_competency_overview(
            student_ids=student_ids,
            grade_level=overview['grade_level']
        )

        # Leaderboard
        from core.classroom.analytics_engine import get_class_leaderboard
        leaderboard = get_class_leaderboard(
            classroom_student_ids=student_ids,
            days_back=days_back,
            top_n=10
        )

        # At-risk students
        at_risk = self.classroom_manager.get_at_risk_students(classroom_id)

        return {
            'generated_at': datetime.now().isoformat(),
            'report_type': 'class_overview',
            'classroom': {
                'id': overview['id'],
                'name': overview['name'],
                'grade_level': overview['grade_level'],
                'student_count': overview['student_count']
            },
            'period_days': days_back,
            'statistics': overview['stats'],
            'trajectory': class_trajectory,
            'competencies': competency_overview,
            'leaderboard': leaderboard,
            'at_risk_students': {
                'count': len(at_risk),
                'students': at_risk[:5]  # Top 5 most at risk
            }
        }

    def generate_assignment_completion_report(
        self,
        assignment_id: int
    ) -> Dict:
        """
        Generate assignment completion report

        Args:
            assignment_id: Assignment ID

        Returns:
            Dict with completion data
        """
        # Get completion data
        completions = self.assignment_engine.get_assignment_completion(assignment_id)

        # Calculate statistics
        total_students = len(completions)
        completed_count = sum(1 for c in completions if c['status'] == 'completed')
        avg_progress = (
            sum(c['progress_percentage'] for c in completions) / total_students
            if total_students > 0 else 0
        )
        avg_success = (
            sum(c['success_rate'] for c in completions if c['success_rate']) / total_students
            if total_students > 0 else 0
        )

        # Identify struggling students
        struggling = [
            c for c in completions
            if c['success_rate'] and c['success_rate'] < 0.5
        ]

        # Top performers
        top_performers = sorted(
            [c for c in completions if c['status'] == 'completed'],
            key=lambda x: x['success_rate'],
            reverse=True
        )[:5]

        return {
            'generated_at': datetime.now().isoformat(),
            'report_type': 'assignment_completion',
            'assignment_id': assignment_id,
            'summary': {
                'total_students': total_students,
                'completed_count': completed_count,
                'completion_rate': completed_count / total_students if total_students > 0 else 0,
                'avg_progress': avg_progress,
                'avg_success_rate': avg_success
            },
            'completions': completions,
            'struggling_students': struggling,
            'top_performers': top_performers
        }

    # ========================================================================
    # CURRICULUM REPORTS
    # ========================================================================

    def generate_curriculum_coverage_report(
        self,
        classroom_id: int,
        grade_level: str
    ) -> Dict:
        """
        Generate curriculum coverage report for class

        Shows which competencies are well-covered vs neglected

        Args:
            classroom_id: Classroom ID
            grade_level: Grade level

        Returns:
            Dict with coverage analysis
        """
        # Get students
        students = self.classroom_manager.get_classroom_students(classroom_id)
        student_ids = [s['id'] for s in students]

        # Get competency overview
        overview = self.curriculum_mapper.get_class_competency_overview(
            student_ids=student_ids,
            grade_level=grade_level
        )

        competencies = overview['competencies']

        # Classify coverage
        well_covered = []    # >70% mastery
        partially_covered = []  # 30-70% mastery
        neglected = []       # <30% mastery or not attempted

        for comp in competencies:
            if comp['mastery_rate'] >= 0.7:
                well_covered.append(comp)
            elif comp['mastery_rate'] >= 0.3:
                partially_covered.append(comp)
            else:
                neglected.append(comp)

        # Domain breakdown
        domain_coverage = {}
        for comp in competencies:
            domain = comp['domain']
            if domain not in domain_coverage:
                domain_coverage[domain] = {
                    'total': 0,
                    'well_covered': 0,
                    'partially_covered': 0,
                    'neglected': 0
                }

            domain_coverage[domain]['total'] += 1

            if comp['mastery_rate'] >= 0.7:
                domain_coverage[domain]['well_covered'] += 1
            elif comp['mastery_rate'] >= 0.3:
                domain_coverage[domain]['partially_covered'] += 1
            else:
                domain_coverage[domain]['neglected'] += 1

        return {
            'generated_at': datetime.now().isoformat(),
            'report_type': 'curriculum_coverage',
            'classroom_id': classroom_id,
            'grade_level': grade_level,
            'student_count': len(student_ids),
            'summary': {
                'total_competencies': len(competencies),
                'well_covered_count': len(well_covered),
                'partially_covered_count': len(partially_covered),
                'neglected_count': len(neglected),
                'overall_coverage': len(well_covered) / len(competencies) if competencies else 0
            },
            'domain_breakdown': domain_coverage,
            'well_covered': well_covered,
            'partially_covered': partially_covered,
            'neglected': neglected,
            'recommendations': self._generate_coverage_recommendations(
                neglected, partially_covered
            )
        }

    # ========================================================================
    # CSV EXPORTS
    # ========================================================================

    def export_class_progress_csv(
        self,
        classroom_id: int,
        output_path: Optional[str] = None
    ) -> str:
        """
        Export class progress data to CSV

        Args:
            classroom_id: Classroom ID
            output_path: Optional output file path

        Returns:
            Path to generated CSV file
        """
        # Get students
        students = self.classroom_manager.get_classroom_students(classroom_id)

        # Prepare CSV data
        rows = []
        for student in students:
            rows.append({
                'Student ID': student['id'],
                'Username': student['username'],
                'Grade Level': student['grade_level'],
                'Exercises Completed': student['exercises_completed'],
                'Success Rate': f"{student['success_rate']:.2%}",
                'Last Activity': student['last_activity'] or 'N/A',
                'At Risk': 'Yes' if student['at_risk'] else 'No',
                'Risk Score': f"{student['risk_score']:.2f}"
            })

        # Generate file path
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"reports/class_{classroom_id}_progress_{timestamp}.csv"

        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Write CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

        return output_path

    def export_assignment_results_csv(
        self,
        assignment_id: int,
        output_path: Optional[str] = None
    ) -> str:
        """
        Export assignment results to CSV

        Args:
            assignment_id: Assignment ID
            output_path: Optional output path

        Returns:
            Path to generated CSV file
        """
        completions = self.assignment_engine.get_assignment_completion(assignment_id)

        rows = []
        for completion in completions:
            rows.append({
                'Student ID': completion['student_id'],
                'Student Name': completion['student_name'],
                'Progress': completion['progress'],
                'Exercises Completed': completion['exercises_completed'],
                'Exercises Total': completion['exercises_total'],
                'Success Rate': f"{completion['success_rate']:.2%}" if completion['success_rate'] else 'N/A',
                'Time Spent (minutes)': completion['time_spent_minutes'],
                'Status': completion['status'],
                'Completed At': completion['completed_at'] or 'In Progress'
            })

        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"reports/assignment_{assignment_id}_results_{timestamp}.csv"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

        return output_path

    # ========================================================================
    # PRESENTATION DATA (for PowerPoint/Slides)
    # ========================================================================

    def generate_presentation_data(
        self,
        classroom_id: int,
        days_back: int = 30
    ) -> Dict:
        """
        Generate structured data for presentation (PowerPoint/Google Slides)

        Returns data optimized for chart/graph rendering

        Args:
            classroom_id: Classroom ID
            days_back: Number of days

        Returns:
            Dict with presentation-ready data
        """
        overview = self.generate_class_overview_report(classroom_id, days_back)

        # Extract data for charts
        presentation_data = {
            'title_slide': {
                'classroom_name': overview['classroom']['name'],
                'grade_level': overview['classroom']['grade_level'],
                'student_count': overview['classroom']['student_count'],
                'reporting_period': f"{days_back} derniers jours",
                'generated_date': datetime.now().strftime('%d/%m/%Y')
            },
            'statistics_slide': {
                'total_students': overview['statistics']['total_students'],
                'active_students_7d': overview['statistics']['active_students_7d'],
                'avg_success_rate': overview['statistics']['avg_success_rate'],
                'at_risk_count': overview['statistics']['at_risk_count']
            },
            'trajectory_chart': {
                'dates': [p['date'] for p in overview['trajectory']['data_points']],
                'success_rates': [p['class_avg_success_rate'] for p in overview['trajectory']['data_points']],
                'exercises_counts': [p['exercises_completed'] for p in overview['trajectory']['data_points']]
            },
            'leaderboard_slide': overview['leaderboard'],
            'at_risk_slide': overview['at_risk_students'],
            'competency_chart': {
                'domains': list(set(c['domain'] for c in overview['competencies']['competencies'])),
                'mastery_by_domain': self._aggregate_mastery_by_domain(
                    overview['competencies']['competencies']
                )
            }
        }

        return presentation_data

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    def _export_student_report_csv(self, report_data: Dict, student_username: str) -> str:
        """Export student report as CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"reports/student_{student_username}_{timestamp}.csv"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Flatten report data into CSV rows
        rows = []

        # Engagement row
        eng = report_data['engagement']
        rows.append({
            'Category': 'Engagement',
            'Metric': 'Total Exercises',
            'Value': eng.get('total_exercises', 0)
        })
        rows.append({
            'Category': 'Engagement',
            'Metric': 'Engagement Score',
            'Value': f"{eng.get('engagement_score', 0):.1f}/100"
        })

        # Competency rows
        comp_summary = report_data['competencies']['summary']
        rows.append({
            'Category': 'Competencies',
            'Metric': 'Mastered',
            'Value': comp_summary['mastered']
        })
        rows.append({
            'Category': 'Competencies',
            'Metric': 'In Progress',
            'Value': comp_summary['in_progress']
        })

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Category', 'Metric', 'Value'])
            writer.writeheader()
            writer.writerows(rows)

        return output_path

    def _export_student_report_pdf(self, report_data: Dict) -> str:
        """Export student report as PDF (placeholder for future PDF library integration)"""
        # TODO: Implement with reportlab or weasyprint
        # For now, export as JSON
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"reports/student_report_{timestamp}.json"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        return output_path

    def _generate_at_risk_summary(self, students: List[Dict]) -> Dict:
        """Generate summary for at-risk report"""
        if not students:
            return {
                'message': 'Aucun élève à risque détecté',
                'action_required': False
            }

        critical_count = sum(1 for s in students if s.get('risk_level') == 'CRITICAL')
        high_count = sum(1 for s in students if s.get('risk_level') == 'HIGH')

        return {
            'total_at_risk': len(students),
            'critical_count': critical_count,
            'high_count': high_count,
            'action_required': critical_count > 0 or high_count > 0,
            'recommendation': (
                f"Intervention immédiate requise pour {critical_count} élèves"
                if critical_count > 0
                else f"Suivi rapproché recommandé pour {high_count} élèves"
            )
        }

    def _generate_coverage_recommendations(
        self,
        neglected: List[Dict],
        partially_covered: List[Dict]
    ) -> List[str]:
        """Generate recommendations for curriculum coverage"""
        recommendations = []

        if neglected:
            top_neglected = sorted(neglected, key=lambda x: x['difficulty_range'][0])[:3]
            recommendations.append(
                f"Priorité: Travailler sur {', '.join(c['title'] for c in top_neglected)}"
            )

        if len(neglected) > 5:
            recommendations.append(
                f"⚠️ {len(neglected)} compétences non abordées - planifier des séances de révision"
            )

        if partially_covered:
            recommendations.append(
                f"Renforcer {len(partially_covered)} compétences en cours d'acquisition"
            )

        if not recommendations:
            recommendations.append("✓ Excellente couverture du programme")

        return recommendations

    def _aggregate_mastery_by_domain(self, competencies: List[Dict]) -> Dict[str, float]:
        """Aggregate mastery levels by domain"""
        domain_stats = {}

        for comp in competencies:
            domain = comp['domain']
            if domain not in domain_stats:
                domain_stats[domain] = {'total': 0, 'sum_mastery': 0}

            domain_stats[domain]['total'] += 1
            domain_stats[domain]['sum_mastery'] += comp['avg_mastery_level']

        return {
            domain: stats['sum_mastery'] / stats['total']
            for domain, stats in domain_stats.items()
        }
