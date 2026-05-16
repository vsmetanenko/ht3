from sqlalchemy import func, desc, cast, Numeric
from database import SessionLocal
from models import Student, Grade, Subject, Teacher, Group


def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    session = SessionLocal()
    try:
        result = (
            session.query(
                Student.first_name,
                Student.last_name,
                func.round(cast(func.avg(Grade.grade), Numeric), 2).label("avg_grade"),
            )
            .join(Grade, Grade.student_id == Student.id)
            .group_by(Student.id)
            .order_by(desc("avg_grade"))
            .limit(5)
            .all()
        )
        return result
    finally:
        session.close()


def select_2(subject_id: int):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    session = SessionLocal()
    try:
        result = (
            session.query(
                Student.first_name,
                Student.last_name,
                func.round(cast(func.avg(Grade.grade), Numeric), 2).label("avg_grade"),
            )
            .join(Grade, Grade.student_id == Student.id)
            .filter(Grade.subject_id == subject_id)
            .group_by(Student.id)
            .order_by(desc("avg_grade"))
            .first()
        )
        return result
    finally:
        session.close()


def select_3(subject_id: int):
    """Знайти середній бал у групах з певного предмета."""
    session = SessionLocal()
    try:
        result = (
            session.query(
                Group.name,
                func.round(cast(func.avg(Grade.grade), Numeric), 2).label("avg_grade"),
            )
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .filter(Grade.subject_id == subject_id)
            .group_by(Group.id)
            .all()
        )
        return result
    finally:
        session.close()


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    session = SessionLocal()
    try:
        result = session.query(
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("avg_grade")
        ).scalar()
        return result
    finally:
        session.close()


def select_5(teacher_id: int):
    """Знайти які курси читає певний викладач."""
    session = SessionLocal()
    try:
        result = (
            session.query(Subject.name)
            .filter(Subject.teacher_id == teacher_id)
            .all()
        )
        return result
    finally:
        session.close()


def select_6(group_id: int):
    """Знайти список студентів у певній групі."""
    session = SessionLocal()
    try:
        result = (
            session.query(Student.first_name, Student.last_name)
            .filter(Student.group_id == group_id)
            .order_by(Student.last_name)
            .all()
        )
        return result
    finally:
        session.close()


def select_7(group_id: int, subject_id: int):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    session = SessionLocal()
    try:
        result = (
            session.query(
                Student.first_name,
                Student.last_name,
                Grade.grade,
                Grade.date_received,
            )
            .join(Grade, Grade.student_id == Student.id)
            .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
            .order_by(Student.last_name)
            .all()
        )
        return result
    finally:
        session.close()


def select_8(teacher_id: int):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    session = SessionLocal()
    try:
        result = (
            session.query(
                func.round(cast(func.avg(Grade.grade), Numeric), 2).label("avg_grade")
            )
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Subject.teacher_id == teacher_id)
            .scalar()
        )
        return result
    finally:
        session.close()


def select_9(student_id: int):
    """Знайти список курсів, які відвідує певний студент."""
    session = SessionLocal()
    try:
        result = (
            session.query(Subject.name)
            .join(Grade, Grade.subject_id == Subject.id)
            .filter(Grade.student_id == student_id)
            .distinct()
            .all()
        )
        return result
    finally:
        session.close()


def select_10(student_id: int, teacher_id: int):
    """Список курсів, які певному студенту читає певний викладач."""
    session = SessionLocal()
    try:
        result = (
            session.query(Subject.name)
            .join(Grade, Grade.subject_id == Subject.id)
            .filter(
                Grade.student_id == student_id,
                Subject.teacher_id == teacher_id,
            )
            .distinct()
            .all()
        )
        return result
    finally:
        session.close()



def get_subject_name(subject_id: int) -> str:
    session = SessionLocal()
    try:
        subj = session.query(Subject).filter(Subject.id == subject_id).first()
        return subj.name if subj else f"id={subject_id}"
    finally:
        session.close()


def get_group_name(group_id: int) -> str:
    session = SessionLocal()
    try:
        grp = session.query(Group).filter(Group.id == group_id).first()
        return grp.name if grp else f"id={group_id}"
    finally:
        session.close()


def get_teacher_name(teacher_id: int) -> str:
    session = SessionLocal()
    try:
        t = session.query(Teacher).filter(Teacher.id == teacher_id).first()
        return f"{t.last_name} {t.first_name}" if t else f"id={teacher_id}"
    finally:
        session.close()


def get_student_name(student_id: int) -> str:
    session = SessionLocal()
    try:
        s = session.query(Student).filter(Student.id == student_id).first()
        return f"{s.last_name} {s.first_name}" if s else f"id={student_id}"
    finally:
        session.close()



if __name__ == "__main__":
    SUBJECT_ID = 1
    GROUP_ID = 1
    TEACHER_ID = 1
    STUDENT_ID = 1

    subject_name = get_subject_name(SUBJECT_ID)
    group_name = get_group_name(GROUP_ID)
    teacher_name = get_teacher_name(TEACHER_ID)
    student_name = get_student_name(STUDENT_ID)

    print("Топ-5 студентів за середнім балом з усіх предметів ")
    for row in select_1():
        print(f"  {row.last_name} {row.first_name}: {row.avg_grade}")

    print(f"\n \n Студент із найвищим середнім балом з предмета '{subject_name}'")
    row = select_2(SUBJECT_ID)
    if row:
        print(f"  {row.last_name} {row.first_name}: {row.avg_grade}")

    print(f"\n \n Середній бал у групах з предмета '{subject_name}'")
    for row in select_3(SUBJECT_ID):
        print(f"  Група {row.name}: {row.avg_grade}")

    print(f"\n \n Середній бал на потоці (всі предмети, всі студенти)")
    print(f"  {select_4()}")

    print(f"\n \n Курси викладача {teacher_name}")
    for row in select_5(TEACHER_ID):
        print(f"  {row.name}")

    print(f"\n \n Список студентів групи '{group_name}'")
    for row in select_6(GROUP_ID):
        print(f"  {row.last_name} {row.first_name}")

    print(f"\n \n Оцінки студентів групи '{group_name}' з предмета '{subject_name}'")
    for row in select_7(GROUP_ID, SUBJECT_ID):
        print(f"  {row.last_name} {row.first_name}: {row.grade} ({row.date_received})")

    print(f"\n \n Середній бал, який ставить викладач {teacher_name} зі своїх предметів")
    print(f"  {select_8(TEACHER_ID)}")

    print(f"\n \n Список курсів, які відвідує студент {student_name} ")
    for row in select_9(STUDENT_ID):
        print(f"  {row.name}")

    print(f"\n \n Курси студента {student_name} у викладача {teacher_name}")
    for row in select_10(STUDENT_ID, TEACHER_ID):
        print(f"  {row.name}")