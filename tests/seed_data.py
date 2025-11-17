"""
Seed Data Script - Create test data for MathCopain Phase 8

Creates:
- Teacher accounts
- Test classrooms
- Test students with exercise history
- Sample assignments
- Curriculum competencies

Usage:
    python -m tests.seed_data
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
import random
from database.connection import DatabaseSession, create_tables
from database.models import (
    User, TeacherAccount, Classroom, ClassroomEnrollment,
    ExerciseResponse, SkillProfile, Assignment, AssignmentCompletion
)
from core.classroom import CurriculumMapper


# Test data configuration
TEACHER_EMAIL = "prof.dupont@mathcopain.fr"
TEACHER_PASSWORD = "password123"

CLASSROOMS = [
    {"name": "CE2 - Classe A", "grade_level": "CE2", "school_year": "2025-2026"},
    {"name": "CM1 - Classe B", "grade_level": "CM1", "school_year": "2025-2026"},
]

STUDENTS_CE2 = [
    "alice_ce2", "bob_ce2", "charlie_ce2", "diane_ce2", "emma_ce2",
    "felix_ce2", "gabrielle_ce2", "hugo_ce2", "iris_ce2", "jules_ce2",
    "lea_ce2", "martin_ce2", "nina_ce2", "oscar_ce2", "pauline_ce2"
]

STUDENTS_CM1 = [
    "alice_cm1", "bob_cm1", "charlie_cm1", "diane_cm1", "emma_cm1",
    "felix_cm1", "gabrielle_cm1", "hugo_cm1", "iris_cm1", "jules_cm1"
]

SKILL_DOMAINS = ["addition", "soustraction", "multiplication", "division", "fractions"]


def create_teacher_account():
    """Create test teacher account"""
    with DatabaseSession() as session:
        # Check if teacher exists
        teacher = session.query(TeacherAccount).filter(
            TeacherAccount.email == TEACHER_EMAIL
        ).first()

        if teacher:
            print(f"✓ Teacher already exists: {TEACHER_EMAIL}")
            return teacher.id

        teacher = TeacherAccount(
            email=TEACHER_EMAIL,
            password_hash="$2b$12$dummy_hash_for_testing",  # Dummy hash
            first_name="Jean",
            last_name="Dupont",
            school_name="École Primaire Victor Hugo"
        )
        session.add(teacher)
        session.flush()

        print(f"✓ Created teacher: {TEACHER_EMAIL} (ID: {teacher.id})")
        return teacher.id


def create_students(grade_level: str, usernames: list):
    """Create test students"""
    created_students = []

    with DatabaseSession() as session:
        for username in usernames:
            # Check if student exists
            student = session.query(User).filter(User.username == username).first()

            if student:
                print(f"  - Student already exists: {username}")
                created_students.append(student.id)
                continue

            student = User(
                username=username,
                password_hash="$2b$12$dummy_hash_for_testing",
                grade_level=grade_level,
                learning_style=random.choice(["visual", "auditif", "kinesthésique"])
            )
            session.add(student)
            session.flush()

            print(f"  ✓ Created student: {username} ({grade_level})")
            created_students.append(student.id)

    return created_students


def create_exercise_history(student_id: int, days_back: int = 30):
    """Create realistic exercise history for a student"""
    with DatabaseSession() as session:
        # Check if history exists
        existing = session.query(ExerciseResponse).filter(
            ExerciseResponse.user_id == student_id
        ).count()

        if existing > 0:
            print(f"    - Exercise history exists for student {student_id}")
            return

        # Generate exercise responses
        base_success_rate = random.uniform(0.5, 0.95)  # Student's base skill level
        exercises_per_day = random.randint(3, 15)

        for day in range(days_back):
            date = datetime.now() - timedelta(days=day)

            for _ in range(random.randint(1, exercises_per_day)):
                domain = random.choice(SKILL_DOMAINS)
                difficulty = random.randint(1, 5)

                # Success rate varies by difficulty
                difficulty_factor = 1.0 - (difficulty - 1) * 0.1
                success_prob = base_success_rate * difficulty_factor
                is_correct = random.random() < success_prob

                response = ExerciseResponse(
                    user_id=student_id,
                    skill_domain=domain,
                    difficulty=difficulty,
                    exercise_type="calculation",
                    is_correct=is_correct,
                    time_taken_seconds=random.randint(20, 180),
                    hint_used=random.random() < 0.2,
                    error_type="calcul" if not is_correct else None,
                    created_at=date
                )
                session.add(response)

        print(f"    ✓ Created {days_back * exercises_per_day // 2} exercise responses")


def create_skill_profile(student_id: int):
    """Create skill profile for student"""
    with DatabaseSession() as session:
        # Check if profile exists
        existing = session.query(SkillProfile).filter(
            SkillProfile.user_id == student_id
        ).count()

        if existing > 0:
            return

        for domain in SKILL_DOMAINS:
            proficiency = random.uniform(0.3, 0.95)

            profile = SkillProfile(
                user_id=student_id,
                skill_domain=domain,
                proficiency_level=proficiency,
                exercises_completed=random.randint(50, 200),
                last_practiced=datetime.now() - timedelta(days=random.randint(0, 7))
            )
            session.add(profile)


def create_classrooms_and_enroll(teacher_id: int):
    """Create classrooms and enroll students"""
    classroom_ids = []

    with DatabaseSession() as session:
        for i, classroom_data in enumerate(CLASSROOMS):
            # Check if classroom exists
            classroom = session.query(Classroom).filter(
                Classroom.name == classroom_data["name"]
            ).first()

            if classroom:
                print(f"✓ Classroom already exists: {classroom_data['name']}")
                classroom_ids.append(classroom.id)
                continue

            classroom = Classroom(
                teacher_id=teacher_id,
                name=classroom_data["name"],
                grade_level=classroom_data["grade_level"],
                school_year=classroom_data["school_year"],
                max_students=30
            )
            session.add(classroom)
            session.flush()

            print(f"✓ Created classroom: {classroom_data['name']} (ID: {classroom.id})")
            classroom_ids.append(classroom.id)

            # Enroll students
            students = STUDENTS_CE2 if i == 0 else STUDENTS_CM1
            student_ids = create_students(classroom_data["grade_level"], students)

            for student_id in student_ids:
                enrollment = ClassroomEnrollment(
                    classroom_id=classroom.id,
                    student_id=student_id,
                    enrolled_at=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                session.add(enrollment)

                # Create exercise history and skill profiles
                create_exercise_history(student_id, days_back=30)
                create_skill_profile(student_id)

            print(f"  ✓ Enrolled {len(student_ids)} students")

    return classroom_ids


def create_sample_assignments(teacher_id: int, classroom_ids: list):
    """Create sample assignments"""
    with DatabaseSession() as session:
        # Check if assignments exist
        existing = session.query(Assignment).filter(
            Assignment.classroom_id.in_(classroom_ids)
        ).count()

        if existing > 0:
            print("✓ Assignments already exist")
            return

        assignments_data = [
            {
                "title": "Révision multiplication - Tables 2 à 5",
                "skill_domains": ["multiplication"],
                "classroom_idx": 0,
                "is_published": True,
                "is_adaptive": True
            },
            {
                "title": "Addition et soustraction",
                "skill_domains": ["addition", "soustraction"],
                "classroom_idx": 0,
                "is_published": True,
                "is_adaptive": False,
                "difficulty_levels": [2, 3]
            },
            {
                "title": "Fractions simples",
                "skill_domains": ["fractions"],
                "classroom_idx": 0,
                "is_published": False,
                "is_adaptive": True
            },
            {
                "title": "Division euclidienne",
                "skill_domains": ["division"],
                "classroom_idx": 1,
                "is_published": True,
                "is_adaptive": True
            }
        ]

        for assign_data in assignments_data:
            classroom_id = classroom_ids[assign_data["classroom_idx"]]

            assignment = Assignment(
                classroom_id=classroom_id,
                title=assign_data["title"],
                description=f"Devoir de test : {assign_data['title']}",
                skill_domains=assign_data["skill_domains"],
                difficulty_levels=assign_data.get("difficulty_levels"),
                exercise_count=10,
                due_date=datetime.now() + timedelta(days=7),
                is_published=assign_data["is_published"],
                is_adaptive=assign_data["is_adaptive"]
            )
            session.add(assignment)
            session.flush()

            print(f"✓ Created assignment: {assign_data['title']}")

            # Create assignment completions if published
            if assign_data["is_published"]:
                # Get students in classroom
                enrollments = session.query(ClassroomEnrollment).filter(
                    ClassroomEnrollment.classroom_id == classroom_id
                ).all()

                for enrollment in enrollments:
                    exercises_total = 10
                    exercises_completed = random.randint(0, exercises_total)
                    exercises_correct = int(exercises_completed * random.uniform(0.5, 0.95))

                    completion = AssignmentCompletion(
                        assignment_id=assignment.id,
                        student_id=enrollment.student_id,
                        exercises_completed=exercises_completed,
                        exercises_total=exercises_total,
                        exercises_correct=exercises_correct,
                        started_at=datetime.now() - timedelta(days=random.randint(1, 5)),
                        completed_at=datetime.now() - timedelta(days=random.randint(0, 3)) if exercises_completed == exercises_total else None
                    )
                    session.add(completion)

                print(f"  ✓ Created {len(enrollments)} assignment completions")


def sync_curriculum():
    """Sync curriculum competencies to database"""
    print("\n📚 Syncing curriculum competencies...")
    mapper = CurriculumMapper()
    result = mapper.sync_competencies_to_database()
    print(f"✓ {result['message']}")


def main():
    """Main seed data function"""
    print("=" * 60)
    print("MathCopain Phase 8 - Seed Data Script")
    print("=" * 60)

    # Ensure tables exist
    print("\n🗄️  Creating database tables...")
    create_tables()
    print("✓ Tables created")

    # Create teacher
    print("\n👨‍🏫 Creating teacher account...")
    teacher_id = create_teacher_account()

    # Create classrooms and students
    print("\n🏫 Creating classrooms and students...")
    classroom_ids = create_classrooms_and_enroll(teacher_id)

    # Create assignments
    print("\n📝 Creating sample assignments...")
    create_sample_assignments(teacher_id, classroom_ids)

    # Sync curriculum
    sync_curriculum()

    print("\n" + "=" * 60)
    print("✅ SEED DATA COMPLETE")
    print("=" * 60)
    print("\n📋 Summary:")
    print(f"  - Teacher: {TEACHER_EMAIL}")
    print(f"  - Password: {TEACHER_PASSWORD} (for testing)")
    print(f"  - Classrooms: {len(CLASSROOMS)}")
    print(f"  - Students: {len(STUDENTS_CE2) + len(STUDENTS_CM1)}")
    print(f"  - Curriculum: 108 competencies")
    print("\n🚀 You can now test the API and frontend!")
    print(f"  - API: http://localhost:5000/api")
    print(f"  - Frontend: http://localhost:8080")
    print()


if __name__ == "__main__":
    main()
