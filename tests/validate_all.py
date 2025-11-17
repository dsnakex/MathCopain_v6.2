"""
Validation Script - Automated testing for MathCopain Phase 8

Runs:
1. Database setup
2. Seed data creation
3. API tests (pytest)
4. Manual API validation (curl-like)
5. Generate test report

Usage:
    python -m tests.validate_all
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import subprocess
import requests
from datetime import datetime
import json


class Colors:
    """Terminal colors"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.ENDC}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.ENDC} {text}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.ENDC} {text}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.ENDC} {text}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.ENDC} {text}")


class ValidationReport:
    """Test validation report"""
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.failures = []
        self.start_time = datetime.now()

    def add_test(self, name, passed, error=None):
        """Add test result"""
        self.tests_run += 1
        if passed:
            self.tests_passed += 1
            print_success(f"{name}")
        else:
            self.tests_failed += 1
            self.failures.append((name, error))
            print_error(f"{name}: {error}")

    def print_summary(self):
        """Print test summary"""
        duration = (datetime.now() - self.start_time).total_seconds()

        print_header("TEST SUMMARY")
        print(f"Total tests run: {self.tests_run}")
        print(f"{Colors.GREEN}Passed: {self.tests_passed}{Colors.ENDC}")
        print(f"{Colors.RED}Failed: {self.tests_failed}{Colors.ENDC}")
        print(f"Duration: {duration:.2f}s")

        if self.tests_failed > 0:
            print(f"\n{Colors.RED}FAILURES:{Colors.ENDC}")
            for name, error in self.failures:
                print(f"  - {name}: {error}")

        # Final status
        if self.tests_failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ALL TESTS PASSED{Colors.ENDC}")
            return True
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ SOME TESTS FAILED{Colors.ENDC}")
            return False


def setup_database():
    """Setup database and seed data"""
    print_header("DATABASE SETUP")

    try:
        print_info("Running seed data script...")
        result = subprocess.run(
            [sys.executable, "-m", "tests.seed_data"],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print_success("Database setup complete")
            return True
        else:
            print_error(f"Seed data failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print_error("Seed data timeout (60s)")
        return False
    except Exception as e:
        print_error(f"Seed data error: {str(e)}")
        return False


def run_pytest():
    """Run pytest tests"""
    print_header("PYTEST TESTS")

    try:
        print_info("Running pytest...")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_api.py", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=120
        )

        # Parse pytest output
        output = result.stdout
        print(output)

        if result.returncode == 0:
            print_success("All pytest tests passed")
            return True
        else:
            print_error("Some pytest tests failed")
            return False
    except subprocess.TimeoutExpired:
        print_error("Pytest timeout (120s)")
        return False
    except Exception as e:
        print_error(f"Pytest error: {str(e)}")
        return False


def validate_api_endpoints(report: ValidationReport):
    """Validate key API endpoints manually"""
    print_header("API ENDPOINT VALIDATION")

    base_url = "http://localhost:5000/api"

    # Mock session for authenticated requests
    session = requests.Session()
    session.cookies.set('teacher_id', '1')

    # Test cases
    tests = [
        # Health check
        {
            "name": "Health Check",
            "method": "GET",
            "url": f"{base_url}/health",
            "auth": False,
            "validate": lambda r: r.status_code == 200 and r.json().get('status') == 'healthy'
        },

        # Classrooms
        {
            "name": "GET Classrooms",
            "method": "GET",
            "url": f"{base_url}/teacher/classrooms",
            "auth": True,
            "validate": lambda r: r.status_code == 200 and 'classrooms' in r.json()
        },
        {
            "name": "GET Classroom Details",
            "method": "GET",
            "url": f"{base_url}/teacher/classrooms/1",
            "auth": True,
            "validate": lambda r: r.status_code == 200 and r.json().get('classroom', {}).get('id') == 1
        },
        {
            "name": "GET Classroom Students",
            "method": "GET",
            "url": f"{base_url}/teacher/classrooms/1/students",
            "auth": True,
            "validate": lambda r: r.status_code == 200 and len(r.json().get('students', [])) > 0
        },
        {
            "name": "GET At-Risk Students",
            "method": "GET",
            "url": f"{base_url}/teacher/classrooms/1/at-risk?threshold=0.40",
            "auth": True,
            "validate": lambda r: r.status_code == 200 and 'at_risk_students' in r.json()
        },

        # Assignments
        {
            "name": "GET Assignments",
            "method": "GET",
            "url": f"{base_url}/teacher/assignments",
            "auth": True,
            "validate": lambda r: r.status_code == 200 and 'assignments' in r.json()
        },
        {
            "name": "GET Assignment Completion",
            "method": "GET",
            "url": f"{base_url}/teacher/assignments/1/completion",
            "auth": True,
            "validate": lambda r: r.status_code == 200 and 'completions' in r.json()
        },

        # Analytics
        {
            "name": "GET Leaderboard",
            "method": "GET",
            "url": f"{base_url}/teacher/analytics/leaderboard?classroom_id=1&days_back=30&top_n=10",
            "auth": True,
            "validate": lambda r: r.status_code == 200 and 'leaderboard' in r.json()
        },
        {
            "name": "GET Progress Trajectory",
            "method": "GET",
            "url": f"{base_url}/teacher/analytics/trajectory?student_id=1&days_back=30&granularity=daily",
            "auth": True,
            "validate": lambda r: r.status_code == 200 and 'trajectory' in r.json()
        },
        {
            "name": "GET Performance Heatmap",
            "method": "GET",
            "url": f"{base_url}/teacher/analytics/heatmap?student_id=1&days_back=30",
            "auth": True,
            "validate": lambda r: r.status_code == 200 and 'heatmap' in r.json()
        },

        # Curriculum
        {
            "name": "GET Competencies",
            "method": "GET",
            "url": f"{base_url}/teacher/curriculum/competencies?grade_level=CE2",
            "auth": True,
            "validate": lambda r: r.status_code == 200 and len(r.json().get('competencies', [])) > 0
        },
        {
            "name": "GET Student Competency Progress",
            "method": "GET",
            "url": f"{base_url}/teacher/curriculum/student-progress?student_id=1&grade_level=CE2",
            "auth": True,
            "validate": lambda r: r.status_code == 200 and 'progress' in r.json()
        },
        {
            "name": "GET Class Competency Overview",
            "method": "GET",
            "url": f"{base_url}/teacher/curriculum/class-overview?classroom_id=1&grade_level=CE2",
            "auth": True,
            "validate": lambda r: r.status_code == 200 and 'overview' in r.json()
        },

        # Reports
        {
            "name": "POST Class Overview Report",
            "method": "POST",
            "url": f"{base_url}/teacher/reports/class-overview",
            "auth": True,
            "json": {"classroom_id": 1, "days_back": 30},
            "validate": lambda r: r.status_code == 200 and 'report' in r.json()
        },
    ]

    # Run tests
    for test in tests:
        try:
            if test["method"] == "GET":
                if test.get("auth"):
                    response = session.get(test["url"], timeout=10)
                else:
                    response = requests.get(test["url"], timeout=10)
            elif test["method"] == "POST":
                if test.get("auth"):
                    response = session.post(test["url"], json=test.get("json"), timeout=10)
                else:
                    response = requests.post(test["url"], json=test.get("json"), timeout=10)

            # Validate
            if test["validate"](response):
                report.add_test(test["name"], True)
            else:
                report.add_test(test["name"], False, f"Validation failed (status {response.status_code})")

        except requests.exceptions.ConnectionError:
            report.add_test(test["name"], False, "Connection refused - Is API running?")
        except requests.exceptions.Timeout:
            report.add_test(test["name"], False, "Request timeout")
        except Exception as e:
            report.add_test(test["name"], False, str(e))


def check_api_running():
    """Check if API is running"""
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def main():
    """Main validation function"""
    print_header("MathCopain Phase 8 - Automated Validation")

    # Check API
    if not check_api_running():
        print_error("API not running at http://localhost:5000")
        print_info("Please start the API: python -m api.app")
        return False

    print_success("API is running")

    # Initialize report
    report = ValidationReport()

    # Step 1: Setup database
    if not setup_database():
        print_error("Database setup failed - aborting")
        return False

    # Step 2: Run pytest
    pytest_passed = run_pytest()
    report.add_test("Pytest Suite", pytest_passed, "See output above")

    # Step 3: Validate API endpoints
    validate_api_endpoints(report)

    # Print summary
    all_passed = report.print_summary()

    # Save report
    report_path = Path(__file__).parent / "validation_report.json"
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "tests_run": report.tests_run,
        "tests_passed": report.tests_passed,
        "tests_failed": report.tests_failed,
        "all_passed": all_passed,
        "failures": [{"test": name, "error": error} for name, error in report.failures]
    }

    with open(report_path, 'w') as f:
        json.dump(report_data, f, indent=2)

    print(f"\n{Colors.BLUE}Report saved to: {report_path}{Colors.ENDC}")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
