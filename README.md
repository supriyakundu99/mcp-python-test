# Student Management MCP Server

This is a Model Context Protocol (MCP) server implementation for student management. It provides various tools for managing student records, marks, and performing various queries.

## Features

- Student CRUD operations
- Student marks management
- Statistical analysis
- Search operations by various criteria
- Marks-based filtering and analysis

## Prerequisites

- Python 3.8+
- PostgreSQL database

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a PostgreSQL database and schema:
```sql
CREATE DATABASE student_db;
\c student_db
CREATE SCHEMA student_schema;
```

4. Create a `.env` file in the root directory with your database configuration:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/student_db
```

## Running the Server

To start the server:

```bash
cd src
python main.py
```

The server will start on `http://localhost:8000`.

## Available MCP Tools

1. Student Management:
   - `getStudentStatisticsWithCount`: Get statistical information about students
   - `createStudent`: Create a new student record
   - `getStudent`: Get student details by ID
   - `updateStudent`: Update student information
   - `deleteStudent`: Delete a student record

2. Marks Management:
   - `addMarks`: Add marks for a student
   - `updateMarks`: Update existing marks
   - `getStudentMarks`: Get marks for a specific student

3. Search Operations:
   - `searchStudentsByName`: Search students by name
   - `searchStudentsByDepartment`: Search students by department
   - `searchStudentsByClass`: Search students by class year
   - `searchStudentsByMarksRange`: Search students by marks range
   - `getStudentsAboveMarks`: Get students with marks above threshold
   - `getStudentsBelowMarks`: Get students with marks below threshold

## API Endpoint

The MCP server is accessible at:
```
POST http://localhost:8000/student-mcp
```

## Database Schema

The system uses two main tables:

1. `students` table:
   - id (Primary Key)
   - name
   - roll_number (Unique)
   - department
   - class_year
   - email (Unique)

2. `student_marks` table:
   - id (Primary Key)
   - student_id (Foreign Key)
   - subject
   - marks
   - semester 