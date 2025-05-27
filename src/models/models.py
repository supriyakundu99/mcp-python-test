from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Student(Base):
    __tablename__ = "students"
    __table_args__ = {"schema": "student_schema"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    roll_number = Column(String, unique=True, index=True)
    department = Column(String, index=True)
    class_year = Column(Integer)
    email = Column(String, unique=True, index=True)

    marks = relationship("StudentMarks", back_populates="student")

class StudentMarks(Base):
    __tablename__ = "student_marks"
    __table_args__ = {"schema": "student_schema"}

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_schema.students.id"))
    subject = Column(String)
    marks = Column(Float)
    semester = Column(Integer)

    student = relationship("Student", back_populates="marks") 