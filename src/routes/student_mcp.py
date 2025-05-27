from mcp.server.fastmcp import FastMCP
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from services.student_service import StudentService
from typing import Dict, List, Any

# Initialize FastMCP
student_mcp = FastMCP("Student Management System")

# Create a service instance for each request
def get_service(db: Session = Depends(get_db)) -> StudentService:
    return StudentService(db)

@student_mcp.tool()
def get_all_students() -> List[Dict]:
    """Get all student records"""
    db = next(get_db())
    service = StudentService(db)
    students = service.get_all_students()
    return [student.__dict__ for student in students]

@student_mcp.tool()
def get_student_statistics() -> Dict:
    """Get statistical information about students"""
    db = next(get_db())
    service = StudentService(db)
    return service.get_student_statistics()

# Student CRUD operations
@student_mcp.tool()
def create_student(
    name: str,
    roll_number: str,
    department: str,
    class_year: int,
    email: str
) -> Dict:
    """Create a new student record"""
    db = next(get_db())
    service = StudentService(db)
    return service.create_student({
        "name": name,
        "roll_number": roll_number,
        "department": department,
        "class_year": class_year,
        "email": email
    })

@student_mcp.tool()
def get_student(id: int) -> Dict:
    """Get student details by ID"""
    db = next(get_db())
    service = StudentService(db)
    return service.get_student(id)

@student_mcp.tool()
def update_student(id: int, data: Dict[str, Any]) -> Dict:
    """Update student information"""
    db = next(get_db())
    service = StudentService(db)
    return service.update_student(id, data)

@student_mcp.tool()
def delete_student(id: int) -> Dict:
    """Delete a student record"""
    db = next(get_db())
    service = StudentService(db)
    return service.delete_student(id)

# Marks operations
@student_mcp.tool()
def add_marks(
    student_id: int,
    subject: str,
    marks: float,
    semester: int
) -> Dict:
    """Add marks for a student"""
    db = next(get_db())
    service = StudentService(db)
    return service.add_marks({
        "student_id": student_id,
        "subject": subject,
        "marks": marks,
        "semester": semester
    })

@student_mcp.tool()
def update_marks(id: int, data: Dict[str, Any]) -> Dict:
    """Update marks for a student"""
    db = next(get_db())
    service = StudentService(db)
    return service.update_marks(id, data)

# Search operations
@student_mcp.tool()
def search_students_by_name(name: str) -> List[Dict]:
    """Search students by name"""
    db = next(get_db())
    service = StudentService(db)
    return service.search_students_by_name(name)

@student_mcp.tool()
def search_students_by_department(department: str) -> List[Dict]:
    """Search students by department"""
    db = next(get_db())
    service = StudentService(db)
    return service.search_students_by_department(department)

@student_mcp.tool()
def search_students_by_class(class_year: int) -> List[Dict]:
    """Search students by class year"""
    db = next(get_db())
    service = StudentService(db)
    return service.search_students_by_class(class_year)

@student_mcp.tool()
def search_students_by_marks_range(
    min_marks: float,
    max_marks: float
) -> List[Dict]:
    """Search students by marks range"""
    db = next(get_db())
    service = StudentService(db)
    return service.search_students_by_marks_range(min_marks, max_marks)

@student_mcp.tool()
def get_student_marks(student_id: int) -> List[Dict]:
    """Get marks for a specific student"""
    db = next(get_db())
    service = StudentService(db)
    return service.get_student_marks(student_id)

@student_mcp.tool()
def get_students_above_marks(marks: float) -> List[Dict]:
    """Get students with marks above threshold"""
    db = next(get_db())
    service = StudentService(db)
    return service.get_students_above_marks(marks)

@student_mcp.tool()
def get_students_below_marks(marks: float) -> List[Dict]:
    """Get students with marks below threshold"""
    db = next(get_db())
    service = StudentService(db)
    return service.get_students_below_marks(marks) 