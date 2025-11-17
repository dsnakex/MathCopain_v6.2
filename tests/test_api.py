"""
API Tests - Flask REST API for MathCopain Phase 8

Tests all major endpoints:
- Classrooms CRUD
- Student enrollment
- Assignments
- Analytics
- Curriculum
- Reports
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.app import create_app
from database.connection import create_tables, get_engine
from tests.seed_data import (
    create_teacher_account, create_classrooms_and_enroll,
    create_sample_assignments, sync_curriculum
)


@pytest.fixture(scope="module")
def app():
    """Create Flask app for testing"""
    app = create_app({'TESTING': True})

    # Setup database
    create_tables()

    # Create test data
    teacher_id = create_teacher_account()
    classroom_ids = create_classrooms_and_enroll(teacher_id)
    create_sample_assignments(teacher_id, classroom_ids)
    sync_curriculum()

    yield app


@pytest.fixture(scope="module")
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope="module")
def authenticated_client(client):
    """Create authenticated test client"""
    with client.session_transaction() as sess:
        sess['teacher_id'] = 1  # Mock teacher authentication
    return client


# ============================================================================
# HEALTH CHECK TESTS
# ============================================================================

def test_health_check(client):
    """Test API health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200

    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'MathCopain Teacher API'


# ============================================================================
# CLASSROOM TESTS
# ============================================================================

def test_get_classrooms(authenticated_client):
    """Test GET /api/teacher/classrooms"""
    response = authenticated_client.get('/api/teacher/classrooms')
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'classrooms' in data
    assert len(data['classrooms']) > 0

    # Check classroom structure
    classroom = data['classrooms'][0]
    assert 'id' in classroom
    assert 'name' in classroom
    assert 'grade_level' in classroom


def test_get_classroom_details(authenticated_client):
    """Test GET /api/teacher/classrooms/:id"""
    response = authenticated_client.get('/api/teacher/classrooms/1')
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'classroom' in data

    classroom = data['classroom']
    assert classroom['id'] == 1
    assert 'name' in classroom
    assert 'stats' in classroom


def test_create_classroom(authenticated_client):
    """Test POST /api/teacher/classrooms"""
    new_classroom = {
        'name': 'Test Classroom',
        'grade_level': 'CE2',
        'school_year': '2025-2026',
        'max_students': 25
    }

    response = authenticated_client.post(
        '/api/teacher/classrooms',
        json=new_classroom
    )
    assert response.status_code == 201

    data = response.get_json()
    assert data['success'] is True
    assert 'classroom' in data
    assert data['classroom']['name'] == 'Test Classroom'


def test_get_classroom_students(authenticated_client):
    """Test GET /api/teacher/classrooms/:id/students"""
    response = authenticated_client.get('/api/teacher/classrooms/1/students')
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'students' in data
    assert len(data['students']) > 0


def test_get_at_risk_students(authenticated_client):
    """Test GET /api/teacher/classrooms/:id/at-risk"""
    response = authenticated_client.get('/api/teacher/classrooms/1/at-risk?threshold=0.40')
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'at_risk_students' in data


# ============================================================================
# ASSIGNMENT TESTS
# ============================================================================

def test_get_assignments(authenticated_client):
    """Test GET /api/teacher/assignments"""
    response = authenticated_client.get('/api/teacher/assignments')
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'assignments' in data


def test_get_assignment_details(authenticated_client):
    """Test GET /api/teacher/assignments/:id"""
    response = authenticated_client.get('/api/teacher/assignments/1')
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'assignment' in data

    assignment = data['assignment']
    assert assignment['id'] == 1
    assert 'title' in assignment
    assert 'skill_domains' in assignment


def test_create_assignment(authenticated_client):
    """Test POST /api/teacher/assignments"""
    from datetime import datetime, timedelta

    new_assignment = {
        'classroom_id': 1,
        'title': 'Test Assignment',
        'skill_domains': ['addition', 'soustraction'],
        'exercise_count': 10,
        'due_date': (datetime.now() + timedelta(days=7)).isoformat(),
        'adaptive': True
    }

    response = authenticated_client.post(
        '/api/teacher/assignments',
        json=new_assignment
    )
    assert response.status_code == 201

    data = response.get_json()
    assert data['success'] is True
    assert 'assignment' in data


def test_get_assignment_completion(authenticated_client):
    """Test GET /api/teacher/assignments/:id/completion"""
    response = authenticated_client.get('/api/teacher/assignments/1/completion')
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'completions' in data


# ============================================================================
# ANALYTICS TESTS
# ============================================================================

def test_get_leaderboard(authenticated_client):
    """Test GET /api/teacher/analytics/leaderboard"""
    response = authenticated_client.get(
        '/api/teacher/analytics/leaderboard?classroom_id=1&days_back=30&top_n=10'
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'leaderboard' in data


def test_get_progress_trajectory(authenticated_client):
    """Test GET /api/teacher/analytics/trajectory"""
    response = authenticated_client.get(
        '/api/teacher/analytics/trajectory?student_id=1&days_back=30&granularity=daily'
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'trajectory' in data


def test_get_performance_heatmap(authenticated_client):
    """Test GET /api/teacher/analytics/heatmap"""
    response = authenticated_client.get(
        '/api/teacher/analytics/heatmap?student_id=1&days_back=30'
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'heatmap' in data


def test_get_engagement_metrics(authenticated_client):
    """Test GET /api/teacher/analytics/engagement"""
    response = authenticated_client.get(
        '/api/teacher/analytics/engagement?student_id=1&days_back=30'
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'engagement' in data


# ============================================================================
# CURRICULUM TESTS
# ============================================================================

def test_get_competencies(authenticated_client):
    """Test GET /api/teacher/curriculum/competencies"""
    response = authenticated_client.get(
        '/api/teacher/curriculum/competencies?grade_level=CE2'
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'competencies' in data
    assert len(data['competencies']) > 0


def test_get_student_competency_progress(authenticated_client):
    """Test GET /api/teacher/curriculum/student-progress"""
    response = authenticated_client.get(
        '/api/teacher/curriculum/student-progress?student_id=1&grade_level=CE2'
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'progress' in data


def test_get_class_competency_overview(authenticated_client):
    """Test GET /api/teacher/curriculum/class-overview"""
    response = authenticated_client.get(
        '/api/teacher/curriculum/class-overview?classroom_id=1&grade_level=CE2'
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'overview' in data


def test_get_competency_gaps(authenticated_client):
    """Test GET /api/teacher/curriculum/gaps"""
    response = authenticated_client.get(
        '/api/teacher/curriculum/gaps?student_id=1&grade_level=CE2'
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'gaps' in data


# ============================================================================
# REPORT TESTS
# ============================================================================

def test_generate_class_report(authenticated_client):
    """Test POST /api/teacher/reports/class-overview"""
    response = authenticated_client.post(
        '/api/teacher/reports/class-overview',
        json={'classroom_id': 1, 'days_back': 30}
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'report' in data


def test_generate_at_risk_report(authenticated_client):
    """Test POST /api/teacher/reports/at-risk"""
    response = authenticated_client.post(
        '/api/teacher/reports/at-risk',
        json={'classroom_id': 1, 'threshold': 0.40}
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data['success'] is True
    assert 'report' in data


# ============================================================================
# AUTHENTICATION TESTS
# ============================================================================

def test_unauthorized_access(client):
    """Test that endpoints require authentication"""
    response = client.get('/api/teacher/classrooms')
    assert response.status_code == 401

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Authentication required'


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

def test_classroom_not_found(authenticated_client):
    """Test 404 for non-existent classroom"""
    response = authenticated_client.get('/api/teacher/classrooms/9999')
    assert response.status_code == 404


def test_invalid_grade_level(authenticated_client):
    """Test validation for invalid grade level"""
    invalid_classroom = {
        'name': 'Invalid Classroom',
        'grade_level': 'INVALID',
        'school_year': '2025-2026'
    }

    response = authenticated_client.post(
        '/api/teacher/classrooms',
        json=invalid_classroom
    )
    assert response.status_code == 400


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
