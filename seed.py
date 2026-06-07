import random
from datetime import date
from faker import Faker
from database import SessionLocal
from models import Group, Teacher, Subject, Student, Grade

fake = Faker("en_US")

GROUPS = 3
TEACHERS = fake.random_int(min=3, max=5)
SUBJECTS = fake.random_int(min=5, max=8)
STUDENTS = fake.random_int(min=30, max=50)
MIN_GRADES = 10
MAX_GRADES = 20

SUBJECT_NAMES = [
    "Databases",
    "javascript",
    "Python",
    "Operating systems",
    "Algorithms and data structures",
    "Java",
    "C++",
    "Web development",
]



def seed():
    session = SessionLocal()
    try:
        groups = []
        for i in range(1, GROUPS + 1):
           group = Group(name=f"{fake.bothify(text='####')}")
           session.add(group)
           groups.append(group)
        session.flush()

        teachers = []
        for _ in range(TEACHERS):
            teacher = Teacher(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            session.add(teacher)
            teachers.append(teacher)
        session.flush()

        subjects = []
        chosen_names = random.sample(SUBJECT_NAMES, SUBJECTS)
        for name in chosen_names:
            subject = Subject(
                name=name,
                teacher_id=random.choice(teachers).id,
            )
            session.add(subject)
            subjects.append(subject)
        session.flush()

        students = []
        for _ in range(STUDENTS):
            student = Student(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                group_id=random.choice(groups).id,
            )
            session.add(student)
            students.append(student)
        session.flush()

        # Grades
        for student in students:
            num_grades = fake.random_int(min=MIN_GRADES, max=MAX_GRADES)
            for _ in range(num_grades):
                subject = random.choice(subjects)
                grade_value = fake.random_int(min=10, max=20)
                received = fake.date_between(start_date=date(2025, 10, 1), end_date='today')
                grade = Grade(
                    student_id=student.id,
                    subject_id=subject.id,
                    grade=grade_value,
                    date_received=received,
                )
                session.add(grade)

        session.commit()
        print("==========Заповнено!==========")
        print(f"Групи: {GROUPS}")
        print(f"Викладачі: {TEACHERS}")
        print(f"Предмети: {SUBJECTS}")
        print(f"Студенти: {STUDENTS}")
    except Exception as e:
        session.rollback()
        print(f"Помилка: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
