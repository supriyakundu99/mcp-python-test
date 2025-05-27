from sqlalchemy.orm import Session
from sqlalchemy import func
from models.models import Student, StudentMarks
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StudentService:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def get_all_students(self) -> List[Student]:
        """Get all students from the database"""
        self.logger.info("Fetching all students")
        students = self.db.query(Student).all()
        self.logger.info(f"Retrieved {len(students)} students")
        return students

    def get_student_statistics(self) -> Dict:
        self.logger.info("Calculating student statistics")
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
        
        self.logger.info(f"Statistics calculated. Total students: {total}")
        return {
            "byDepartmentAndClass": [{"department": d, "class_year": c, "count": cnt} for d, c, cnt in by_dept_and_class],
            "byDepartment": [{"department": d, "count": cnt} for d, cnt in by_dept],
            "byClassYear": [{"class_year": c, "count": cnt} for c, cnt in by_class],
            "totalStudents": total
        }

    def create_student(self, student_data: Dict) -> Student:
        self.logger.info(f"Creating new student with data: {student_data}")
        try:
            student = Student(**student_data)
            self.db.add(student)
            self.db.commit()
            self.db.refresh(student)
            self.logger.info(f"Successfully created student with ID: {student.id}")
            return student
        except Exception as e:
            self.logger.error(f"Error creating student: {str(e)}")
            self.db.rollback()
            raise

    def get_student(self, student_id: int) -> Optional[Student]:
        self.logger.info(f"Fetching student with ID: {student_id}")
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if student:
            self.logger.info(f"Found student: {student.name}")
        else:
            self.logger.warning(f"Student with ID {student_id} not found")
        return student

    def update_student(self, student_id: int, student_data: Dict) -> Optional[Student]:
        self.logger.info(f"Updating student {student_id} with data: {student_data}")
        try:
            student = self.db.query(Student).filter(Student.id == student_id).first()
            if student:
                for key, value in student_data.items():
                    setattr(student, key, value)
                self.db.commit()
                self.db.refresh(student)
                self.logger.info(f"Successfully updated student {student_id}")
            else:
                self.logger.warning(f"Student {student_id} not found for update")
            return student
        except Exception as e:
            self.logger.error(f"Error updating student {student_id}: {str(e)}")
            self.db.rollback()
            raise

    def delete_student(self, student_id: int) -> Optional[Student]:
        self.logger.info(f"Attempting to delete student {student_id}")
        try:
            student = self.db.query(Student).filter(Student.id == student_id).first()
            if student:
                self.db.delete(student)
                self.db.commit()
                self.logger.info(f"Successfully deleted student {student_id}")
            else:
                self.logger.warning(f"Student {student_id} not found for deletion")
            return student
        except Exception as e:
            self.logger.error(f"Error deleting student {student_id}: {str(e)}")
            self.db.rollback()
            raise

    def add_marks(self, marks_data: Dict) -> StudentMarks:
        self.logger.info(f"Adding marks for student {marks_data.get('student_id')}: {marks_data}")
        try:
            marks = StudentMarks(**marks_data)
            self.db.add(marks)
            self.db.commit()
            self.db.refresh(marks)
            self.logger.info(f"Successfully added marks with ID: {marks.id}")
            return marks
        except Exception as e:
            self.logger.error(f"Error adding marks: {str(e)}")
            self.db.rollback()
            raise

    def update_marks(self, marks_id: int, marks_data: Dict) -> Optional[StudentMarks]:
        self.logger.info(f"Updating marks {marks_id} with data: {marks_data}")
        try:
            marks = self.db.query(StudentMarks).filter(StudentMarks.id == marks_id).first()
            if marks:
                for key, value in marks_data.items():
                    setattr(marks, key, value)
                self.db.commit()
                self.db.refresh(marks)
                self.logger.info(f"Successfully updated marks {marks_id}")
            else:
                self.logger.warning(f"Marks {marks_id} not found for update")
            return marks
        except Exception as e:
            self.logger.error(f"Error updating marks {marks_id}: {str(e)}")
            self.db.rollback()
            raise

    def search_students_by_name(self, name: str) -> List[Student]:
        self.logger.info(f"Searching students by name: {name}")
        students = self.db.query(Student).filter(Student.name.ilike(f"%{name}%")).all()
        self.logger.info(f"Found {len(students)} students matching name: {name}")
        return students

    def search_students_by_department(self, department: str) -> List[Student]:
        self.logger.info(f"Searching students by department: {department}")
        students = self.db.query(Student).filter(Student.department == department).all()
        self.logger.info(f"Found {len(students)} students in department: {department}")
        return students

    def search_students_by_class(self, class_year: int) -> List[Student]:
        self.logger.info(f"Searching students by class year: {class_year}")
        students = self.db.query(Student).filter(Student.class_year == class_year).all()
        self.logger.info(f"Found {len(students)} students in class year: {class_year}")
        return students

    def search_students_by_marks_range(self, min_marks: float, max_marks: float) -> List[Student]:
        self.logger.info(f"Searching students with marks between {min_marks} and {max_marks}")
        students = (
            self.db.query(Student)
            .join(StudentMarks)
            .filter(StudentMarks.marks.between(min_marks, max_marks))
            .distinct()
            .all()
        )
        self.logger.info(f"Found {len(students)} students in marks range")
        return students

    def get_student_marks(self, student_id: int) -> List[StudentMarks]:
        self.logger.info(f"Fetching marks for student: {student_id}")
        marks = (
            self.db.query(StudentMarks)
            .filter(StudentMarks.student_id == student_id)
            .all()
        )
        self.logger.info(f"Retrieved {len(marks)} marks entries for student {student_id}")
        return marks

    def get_students_above_marks(self, marks: float) -> List[Student]:
        self.logger.info(f"Searching students with marks above {marks}")
        students = (
            self.db.query(Student)
            .join(StudentMarks)
            .filter(StudentMarks.marks > marks)
            .distinct()
            .all()
        )
        self.logger.info(f"Found {len(students)} students with marks above {marks}")
        return students

    def get_students_below_marks(self, marks: float) -> List[Student]:
        self.logger.info(f"Searching students with marks below {marks}")
        students = (
            self.db.query(Student)
            .join(StudentMarks)
            .filter(StudentMarks.marks < marks)
            .distinct()
            .all()
        )
        self.logger.info(f"Found {len(students)} students with marks below {marks}")
        return students 