from sqlalchemy.orm import Session
from sqlalchemy import func
from models.models import Student, StudentMarks
from typing import Dict, List, Optional

class StudentService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_students(self) -> List[Student]:
        """Get all students from the database"""
        return self.db.query(Student).all()

    def get_student_statistics(self) -> Dict:
        by_dept_and_class = (
            self.db.query(
                Student.department,
                Student.class_year,
                func.count(Student.id).label("count")
            )
            .group_by(Student.department, Student.class_year)
            .all()
        )

        by_dept = (
            self.db.query(
                Student.department,
                func.count(Student.id).label("count")
            )
            .group_by(Student.department)
            .all()
        )

        by_class = (
            self.db.query(
                Student.class_year,
                func.count(Student.id).label("count")
            )
            .group_by(Student.class_year)
            .all()
        )

        total = self.db.query(func.count(Student.id)).scalar()

        return {
            "byDepartmentAndClass": [{"department": d, "class_year": c, "count": cnt} for d, c, cnt in by_dept_and_class],
            "byDepartment": [{"department": d, "count": cnt} for d, cnt in by_dept],
            "byClassYear": [{"class_year": c, "count": cnt} for c, cnt in by_class],
            "totalStudents": total
        }

    def create_student(self, student_data: Dict) -> Student:
        student = Student(**student_data)
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def get_student(self, student_id: int) -> Optional[Student]:
        return self.db.query(Student).filter(Student.id == student_id).first()

    def update_student(self, student_id: int, student_data: Dict) -> Optional[Student]:
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if student:
            for key, value in student_data.items():
                setattr(student, key, value)
            self.db.commit()
            self.db.refresh(student)
        return student

    def delete_student(self, student_id: int) -> Optional[Student]:
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if student:
            self.db.delete(student)
            self.db.commit()
        return student

    def add_marks(self, marks_data: Dict) -> StudentMarks:
        marks = StudentMarks(**marks_data)
        self.db.add(marks)
        self.db.commit()
        self.db.refresh(marks)
        return marks

    def update_marks(self, marks_id: int, marks_data: Dict) -> Optional[StudentMarks]:
        marks = self.db.query(StudentMarks).filter(StudentMarks.id == marks_id).first()
        if marks:
            for key, value in marks_data.items():
                setattr(marks, key, value)
            self.db.commit()
            self.db.refresh(marks)
        return marks

    def search_students_by_name(self, name: str) -> List[Student]:
        return self.db.query(Student).filter(Student.name.ilike(f"%{name}%")).all()

    def search_students_by_department(self, department: str) -> List[Student]:
        return self.db.query(Student).filter(Student.department == department).all()

    def search_students_by_class(self, class_year: int) -> List[Student]:
        return self.db.query(Student).filter(Student.class_year == class_year).all()

    def search_students_by_marks_range(self, min_marks: float, max_marks: float) -> List[Student]:
        return (
            self.db.query(Student)
            .join(StudentMarks)
            .filter(StudentMarks.marks.between(min_marks, max_marks))
            .distinct()
            .all()
        )

    def get_student_marks(self, student_id: int) -> List[StudentMarks]:
        return (
            self.db.query(StudentMarks)
            .filter(StudentMarks.student_id == student_id)
            .all()
        )

    def get_students_above_marks(self, marks: float) -> List[Student]:
        return (
            self.db.query(Student)
            .join(StudentMarks)
            .filter(StudentMarks.marks > marks)
            .distinct()
            .all()
        )

    def get_students_below_marks(self, marks: float) -> List[Student]:
        return (
            self.db.query(Student)
            .join(StudentMarks)
            .filter(StudentMarks.marks < marks)
            .distinct()
            .all()
        ) 