from datetime import date
from sqlalchemy import Integer, String, Float, Date, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    students: Mapped[list["Student"]] = relationship("Student", back_populates="group")


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    subjects: Mapped[list["Subject"]] = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    teacher_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)

    teacher: Mapped["Teacher | None"] = relationship("Teacher", back_populates="subjects")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="subject")

    __table_args__ = (
        UniqueConstraint("name", "teacher_id", name="uq_subject_teacher"),
    )


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    group_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("groups.id", ondelete="SET NULL"), nullable=True)

    group: Mapped["Group | None"] = relationship("Group", back_populates="students")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="student")


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    
    grade: Mapped[float] = mapped_column(Float, nullable=False)
    date_received: Mapped[date] = mapped_column(Date, nullable=False)   

    student: Mapped["Student"] = relationship("Student", back_populates="grades")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="grades")

    __table_args__ = (
        CheckConstraint("grade >= 10.0 AND grade <= 20.0", name="check_grade_range"),
    )
