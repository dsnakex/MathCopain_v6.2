"""
Teacher API Routes - Endpoints for teacher dashboard and classroom management

Provides REST API endpoints for:
- Classroom management (CRUD)
- Student enrollment
- Assignment creation and tracking
- Analytics and reports
- Curriculum progress
"""

from flask import Blueprint, request, jsonify, session
from functools import wraps
from datetime import datetime, timedelta
from typing import Dict, Optional

from core.classroom import (
    ClassroomManager,
    AssignmentEngine,
    CurriculumMapper,
    AnalyticsEngine,
    ReportGenerator
)
from core.classroom.analytics_engine import get_class_leaderboard


# Create Blueprint
teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')


# ============================================================================
# AUTHENTICATION DECORATOR
# ============================================================================

def teacher_required(f):
    """Decorator to require teacher authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        teacher_id = session.get('teacher_id')
        if not teacher_id:
            return jsonify({'error': 'Authentication required'}), 401
        return f(teacher_id=teacher_id, *args, **kwargs)
    return decorated_function


# ============================================================================
# CLASSROOM ENDPOINTS
# ============================================================================

@teacher_bp.route('/classrooms', methods=['GET'])
@teacher_required
def get_classrooms(teacher_id: int):
    """Get all classrooms for authenticated teacher"""
    try:
        manager = ClassroomManager(teacher_id)
        classrooms = manager.list_classrooms()

        return jsonify({
            'success': True,
            'classrooms': classrooms
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/classrooms', methods=['POST'])
@teacher_required
def create_classroom(teacher_id: int):
    """Create a new classroom"""
    try:
        data = request.get_json()

        manager = ClassroomManager(teacher_id)
        classroom = manager.create_classroom(
            name=data['name'],
            grade_level=data['grade_level'],
            school_year=data.get('school_year'),
            max_students=data.get('max_students', 30),
            description=data.get('description')
        )

        return jsonify({
            'success': True,
            'classroom': classroom
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@teacher_bp.route('/classrooms/<int:classroom_id>', methods=['GET'])
@teacher_required
def get_classroom_details(teacher_id: int, classroom_id: int):
    """Get detailed classroom information"""
    try:
        manager = ClassroomManager(teacher_id)
        overview = manager.get_classroom_overview(classroom_id)

        return jsonify({
            'success': True,
            'classroom': overview
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@teacher_bp.route('/classrooms/<int:classroom_id>', methods=['PUT'])
@teacher_required
def update_classroom(teacher_id: int, classroom_id: int):
    """Update classroom information"""
    try:
        data = request.get_json()

        manager = ClassroomManager(teacher_id)
        classroom = manager.update_classroom(
            classroom_id=classroom_id,
            name=data.get('name'),
            description=data.get('description'),
            max_students=data.get('max_students')
        )

        return jsonify({
            'success': True,
            'classroom': classroom
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@teacher_bp.route('/classrooms/<int:classroom_id>', methods=['DELETE'])
@teacher_required
def delete_classroom(teacher_id: int, classroom_id: int):
    """Archive/delete a classroom"""
    try:
        manager = ClassroomManager(teacher_id)
        result = manager.delete_classroom(classroom_id)

        return jsonify({
            'success': True,
            'message': result['message']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ============================================================================
# STUDENT ENROLLMENT ENDPOINTS
# ============================================================================

@teacher_bp.route('/classrooms/<int:classroom_id>/students', methods=['POST'])
@teacher_required
def add_student_to_classroom(teacher_id: int, classroom_id: int):
    """Add a student to classroom"""
    try:
        data = request.get_json()

        manager = ClassroomManager(teacher_id)
        enrollment = manager.add_student(
            classroom_id=classroom_id,
            student_username=data['student_username']
        )

        return jsonify({
            'success': True,
            'enrollment': enrollment
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@teacher_bp.route('/classrooms/<int:classroom_id>/students/<int:student_id>', methods=['DELETE'])
@teacher_required
def remove_student_from_classroom(teacher_id: int, classroom_id: int, student_id: int):
    """Remove a student from classroom"""
    try:
        manager = ClassroomManager(teacher_id)
        result = manager.remove_student(
            classroom_id=classroom_id,
            student_id=student_id
        )

        return jsonify({
            'success': True,
            'message': result['message']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@teacher_bp.route('/classrooms/<int:classroom_id>/students', methods=['GET'])
@teacher_required
def get_classroom_students(teacher_id: int, classroom_id: int):
    """Get all students in classroom"""
    try:
        manager = ClassroomManager(teacher_id)
        students = manager.get_classroom_students(classroom_id)

        return jsonify({
            'success': True,
            'students': students
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@teacher_bp.route('/classrooms/<int:classroom_id>/at-risk', methods=['GET'])
@teacher_required
def get_at_risk_students(teacher_id: int, classroom_id: int):
    """Get at-risk students in classroom"""
    try:
        threshold = float(request.args.get('threshold', 0.40))

        manager = ClassroomManager(teacher_id)
        at_risk = manager.get_at_risk_students(
            classroom_id=classroom_id,
            threshold=threshold
        )

        return jsonify({
            'success': True,
            'at_risk_students': at_risk
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ASSIGNMENT ENDPOINTS
# ============================================================================

@teacher_bp.route('/assignments', methods=['GET'])
@teacher_required
def get_assignments(teacher_id: int):
    """Get all assignments for teacher"""
    try:
        classroom_id = request.args.get('classroom_id', type=int)
        status = request.args.get('status')

        engine = AssignmentEngine(teacher_id)
        assignments = engine.list_assignments(
            classroom_id=classroom_id,
            status=status
        )

        return jsonify({
            'success': True,
            'assignments': assignments
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/assignments', methods=['POST'])
@teacher_required
def create_assignment(teacher_id: int):
    """Create a new assignment"""
    try:
        data = request.get_json()

        # Parse due_date
        due_date = None
        if data.get('due_date'):
            due_date = datetime.fromisoformat(data['due_date'])

        engine = AssignmentEngine(teacher_id)
        assignment = engine.create_assignment(
            classroom_id=data['classroom_id'],
            title=data['title'],
            skill_domains=data['skill_domains'],
            difficulty_levels=data.get('difficulty_levels'),
            exercise_count=data.get('exercise_count', 10),
            due_date=due_date,
            description=data.get('description'),
            adaptive=data.get('adaptive', True)
        )

        return jsonify({
            'success': True,
            'assignment': assignment
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@teacher_bp.route('/assignments/<int:assignment_id>', methods=['GET'])
@teacher_required
def get_assignment_details(teacher_id: int, assignment_id: int):
    """Get assignment details"""
    try:
        engine = AssignmentEngine(teacher_id)

        # Get assignment info (from database)
        from database.connection import get_session
        from database.models import Assignment

        with get_session() as session:
            assignment = session.query(Assignment).filter(
                Assignment.id == assignment_id
            ).first()

            if not assignment:
                return jsonify({'error': 'Assignment not found'}), 404

            assignment_data = {
                'id': assignment.id,
                'classroom_id': assignment.classroom_id,
                'title': assignment.title,
                'description': assignment.description,
                'skill_domains': assignment.skill_domains,
                'difficulty_levels': assignment.difficulty_levels,
                'exercise_count': assignment.exercise_count,
                'due_date': assignment.due_date.isoformat() if assignment.due_date else None,
                'is_published': assignment.is_published,
                'is_adaptive': assignment.is_adaptive,
                'created_at': assignment.created_at.isoformat()
            }

        return jsonify({
            'success': True,
            'assignment': assignment_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@teacher_bp.route('/assignments/<int:assignment_id>/publish', methods=['POST'])
@teacher_required
def publish_assignment(teacher_id: int, assignment_id: int):
    """Publish an assignment"""
    try:
        engine = AssignmentEngine(teacher_id)
        result = engine.publish_assignment(assignment_id)

        return jsonify({
            'success': True,
            'assignment': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@teacher_bp.route('/assignments/<int:assignment_id>', methods=['PUT'])
@teacher_required
def update_assignment(teacher_id: int, assignment_id: int):
    """Update an assignment"""
    try:
        data = request.get_json()

        due_date = None
        if data.get('due_date'):
            due_date = datetime.fromisoformat(data['due_date'])

        engine = AssignmentEngine(teacher_id)
        assignment = engine.update_assignment(
            assignment_id=assignment_id,
            title=data.get('title'),
            description=data.get('description'),
            due_date=due_date
        )

        return jsonify({
            'success': True,
            'assignment': assignment
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@teacher_bp.route('/assignments/<int:assignment_id>', methods=['DELETE'])
@teacher_required
def delete_assignment(teacher_id: int, assignment_id: int):
    """Delete an assignment"""
    try:
        engine = AssignmentEngine(teacher_id)
        result = engine.delete_assignment(assignment_id)

        return jsonify({
            'success': True,
            'message': result['message']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@teacher_bp.route('/assignments/<int:assignment_id>/completion', methods=['GET'])
@teacher_required
def get_assignment_completion(teacher_id: int, assignment_id: int):
    """Get assignment completion status"""
    try:
        engine = AssignmentEngine(teacher_id)
        completions = engine.get_assignment_completion(assignment_id)

        return jsonify({
            'success': True,
            'completions': completions
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================

@teacher_bp.route('/analytics/trajectory', methods=['GET'])
@teacher_required
def get_progress_trajectory(teacher_id: int):
    """Get student or class progress trajectory"""
    try:
        student_id = request.args.get('student_id', type=int)
        skill_domain = request.args.get('skill_domain')
        days_back = request.args.get('days_back', 30, type=int)
        granularity = request.args.get('granularity', 'daily')

        analytics = AnalyticsEngine()

        if student_id:
            trajectory = analytics.get_student_progress_trajectory(
                student_id=student_id,
                skill_domain=skill_domain,
                days_back=days_back,
                granularity=granularity
            )
        else:
            # Class trajectory
            classroom_id = request.args.get('classroom_id', type=int)
            if not classroom_id:
                return jsonify({'error': 'classroom_id required for class trajectory'}), 400

            manager = ClassroomManager(teacher_id)
            students = manager.get_classroom_students(classroom_id)
            student_ids = [s['id'] for s in students]

            trajectory = analytics.get_class_progress_trajectory(
                student_ids=student_ids,
                skill_domain=skill_domain,
                days_back=days_back
            )

        return jsonify({
            'success': True,
            'trajectory': trajectory
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/analytics/heatmap', methods=['GET'])
@teacher_required
def get_performance_heatmap(teacher_id: int):
    """Get student performance heatmap"""
    try:
        student_id = request.args.get('student_id', type=int)
        days_back = request.args.get('days_back', 30, type=int)

        if not student_id:
            return jsonify({'error': 'student_id required'}), 400

        analytics = AnalyticsEngine()
        heatmap = analytics.generate_performance_heatmap(
            student_id=student_id,
            days_back=days_back
        )

        return jsonify({
            'success': True,
            'heatmap': heatmap
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/analytics/forecast', methods=['GET'])
@teacher_required
def get_performance_forecast(teacher_id: int):
    """Get ML performance forecast"""
    try:
        student_id = request.args.get('student_id', type=int)
        skill_domain = request.args.get('skill_domain')
        days_ahead = request.args.get('days_ahead', 7, type=int)

        if not student_id or not skill_domain:
            return jsonify({'error': 'student_id and skill_domain required'}), 400

        analytics = AnalyticsEngine()
        forecast = analytics.forecast_student_performance(
            student_id=student_id,
            skill_domain=skill_domain,
            days_ahead=days_ahead
        )

        return jsonify({
            'success': True,
            'forecast': forecast
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/analytics/engagement', methods=['GET'])
@teacher_required
def get_engagement_metrics(teacher_id: int):
    """Get student engagement metrics"""
    try:
        student_id = request.args.get('student_id', type=int)
        days_back = request.args.get('days_back', 30, type=int)

        if not student_id:
            return jsonify({'error': 'student_id required'}), 400

        analytics = AnalyticsEngine()
        engagement = analytics.get_student_engagement_metrics(
            student_id=student_id,
            days_back=days_back
        )

        return jsonify({
            'success': True,
            'engagement': engagement
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/analytics/compare', methods=['GET'])
@teacher_required
def compare_student_to_class(teacher_id: int):
    """Compare student to class average"""
    try:
        student_id = request.args.get('student_id', type=int)
        classroom_id = request.args.get('classroom_id', type=int)
        skill_domain = request.args.get('skill_domain')
        days_back = request.args.get('days_back', 30, type=int)

        if not student_id or not classroom_id:
            return jsonify({'error': 'student_id and classroom_id required'}), 400

        manager = ClassroomManager(teacher_id)
        students = manager.get_classroom_students(classroom_id)
        student_ids = [s['id'] for s in students]

        analytics = AnalyticsEngine()
        comparison = analytics.compare_student_to_class(
            student_id=student_id,
            classroom_student_ids=student_ids,
            skill_domain=skill_domain,
            days_back=days_back
        )

        return jsonify({
            'success': True,
            'comparison': comparison
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/analytics/leaderboard', methods=['GET'])
@teacher_required
def get_leaderboard(teacher_id: int):
    """Get class leaderboard"""
    try:
        classroom_id = request.args.get('classroom_id', type=int)
        skill_domain = request.args.get('skill_domain')
        days_back = request.args.get('days_back', 30, type=int)
        top_n = request.args.get('top_n', 10, type=int)

        if not classroom_id:
            return jsonify({'error': 'classroom_id required'}), 400

        manager = ClassroomManager(teacher_id)
        students = manager.get_classroom_students(classroom_id)
        student_ids = [s['id'] for s in students]

        leaderboard = get_class_leaderboard(
            classroom_student_ids=student_ids,
            skill_domain=skill_domain,
            days_back=days_back,
            top_n=top_n
        )

        return jsonify({
            'success': True,
            'leaderboard': leaderboard
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# CURRICULUM ENDPOINTS
# ============================================================================

@teacher_bp.route('/curriculum/competencies', methods=['GET'])
@teacher_required
def get_competencies(teacher_id: int):
    """Get curriculum competencies"""
    try:
        grade_level = request.args.get('grade_level')
        skill_domain = request.args.get('skill_domain')

        if not grade_level:
            return jsonify({'error': 'grade_level required'}), 400

        from core.classroom.curriculum_mapper import get_competencies_by_domain

        if skill_domain:
            competencies = get_competencies_by_domain(grade_level, skill_domain)
        else:
            # Get all competencies for grade level
            mapper = CurriculumMapper()
            competencies = []
            for domain in ['addition', 'soustraction', 'multiplication', 'division',
                          'fractions', 'decimaux', 'geometrie', 'mesures', 'proportionnalite']:
                comps = get_competencies_by_domain(grade_level, domain)
                competencies.extend(comps)

        return jsonify({
            'success': True,
            'competencies': competencies
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/curriculum/student-progress', methods=['GET'])
@teacher_required
def get_student_competency_progress(teacher_id: int):
    """Get student competency progress"""
    try:
        student_id = request.args.get('student_id', type=int)
        grade_level = request.args.get('grade_level')
        skill_domain = request.args.get('skill_domain')

        if not student_id or not grade_level:
            return jsonify({'error': 'student_id and grade_level required'}), 400

        mapper = CurriculumMapper()
        report = mapper.get_student_competency_report(
            student_id=student_id,
            grade_level=grade_level,
            skill_domain=skill_domain
        )

        return jsonify({
            'success': True,
            'progress': report
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/curriculum/class-overview', methods=['GET'])
@teacher_required
def get_class_competency_overview(teacher_id: int):
    """Get class competency overview"""
    try:
        classroom_id = request.args.get('classroom_id', type=int)
        grade_level = request.args.get('grade_level')

        if not classroom_id or not grade_level:
            return jsonify({'error': 'classroom_id and grade_level required'}), 400

        manager = ClassroomManager(teacher_id)
        students = manager.get_classroom_students(classroom_id)
        student_ids = [s['id'] for s in students]

        mapper = CurriculumMapper()
        overview = mapper.get_class_competency_overview(
            student_ids=student_ids,
            grade_level=grade_level
        )

        return jsonify({
            'success': True,
            'overview': overview
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/curriculum/gaps', methods=['GET'])
@teacher_required
def get_competency_gaps(teacher_id: int):
    """Get student competency gaps"""
    try:
        student_id = request.args.get('student_id', type=int)
        grade_level = request.args.get('grade_level')

        if not student_id or not grade_level:
            return jsonify({'error': 'student_id and grade_level required'}), 400

        mapper = CurriculumMapper()
        gaps = mapper.identify_competency_gaps(
            student_id=student_id,
            grade_level=grade_level
        )

        return jsonify({
            'success': True,
            'gaps': gaps
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/curriculum/recommendations', methods=['GET'])
@teacher_required
def get_competency_recommendations(teacher_id: int):
    """Get competency recommendations for student"""
    try:
        student_id = request.args.get('student_id', type=int)
        grade_level = request.args.get('grade_level')
        count = request.args.get('count', 3, type=int)

        if not student_id or not grade_level:
            return jsonify({'error': 'student_id and grade_level required'}), 400

        mapper = CurriculumMapper()
        recommendations = mapper.recommend_next_competencies(
            student_id=student_id,
            grade_level=grade_level,
            count=count
        )

        return jsonify({
            'success': True,
            'recommendations': recommendations
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# REPORT ENDPOINTS
# ============================================================================

@teacher_bp.route('/reports/student-progress', methods=['POST'])
@teacher_required
def generate_student_report(teacher_id: int):
    """Generate student progress report"""
    try:
        data = request.get_json()

        generator = ReportGenerator(teacher_id)
        report = generator.generate_student_progress_report(
            student_id=data['student_id'],
            classroom_id=data['classroom_id'],
            format=data.get('format', 'structured'),
            days_back=data.get('days_back', 30)
        )

        return jsonify({
            'success': True,
            'report': report
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/reports/class-overview', methods=['POST'])
@teacher_required
def generate_class_report(teacher_id: int):
    """Generate class overview report"""
    try:
        data = request.get_json()

        generator = ReportGenerator(teacher_id)
        report = generator.generate_class_overview_report(
            classroom_id=data['classroom_id'],
            days_back=data.get('days_back', 30)
        )

        return jsonify({
            'success': True,
            'report': report
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/reports/at-risk', methods=['POST'])
@teacher_required
def generate_at_risk_report(teacher_id: int):
    """Generate at-risk students report"""
    try:
        data = request.get_json()

        generator = ReportGenerator(teacher_id)
        report = generator.generate_at_risk_report(
            classroom_id=data['classroom_id'],
            threshold=data.get('threshold', 0.40)
        )

        return jsonify({
            'success': True,
            'report': report
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/reports/assignment', methods=['POST'])
@teacher_required
def generate_assignment_report(teacher_id: int):
    """Generate assignment completion report"""
    try:
        data = request.get_json()

        generator = ReportGenerator(teacher_id)
        report = generator.generate_assignment_completion_report(
            assignment_id=data['assignment_id']
        )

        return jsonify({
            'success': True,
            'report': report
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/reports/curriculum-coverage', methods=['POST'])
@teacher_required
def generate_curriculum_coverage_report(teacher_id: int):
    """Generate curriculum coverage report"""
    try:
        data = request.get_json()

        generator = ReportGenerator(teacher_id)
        report = generator.generate_curriculum_coverage_report(
            classroom_id=data['classroom_id'],
            grade_level=data['grade_level']
        )

        return jsonify({
            'success': True,
            'report': report
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@teacher_bp.route('/reports/export/csv', methods=['POST'])
@teacher_required
def export_csv_report(teacher_id: int):
    """Export report as CSV"""
    try:
        data = request.get_json()
        report_type = data['report_type']

        generator = ReportGenerator(teacher_id)

        if report_type == 'class_progress':
            csv_path = generator.export_class_progress_csv(
                classroom_id=data['classroom_id']
            )
        elif report_type == 'assignment_results':
            csv_path = generator.export_assignment_results_csv(
                assignment_id=data['assignment_id']
            )
        else:
            return jsonify({'error': 'Invalid report_type'}), 400

        return jsonify({
            'success': True,
            'csv_path': csv_path
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
