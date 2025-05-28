# Student Management MCP Server

A FastAPI-based student management system with MCP (Model Context Protocol, also known as Method Call Protocol) integration for Cursor IDE.

## Prerequisites

- Docker and Docker Compose
- Python 3.12 or higher (for local development)
- [uv](https://github.com/astral-sh/uv) (for dependency management)
- Cursor IDE

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/supriyakundu99/mcp-python-test.git
cd mcp-python-test
```

## Cursor IDE Integration

1. Create or update your `sample-mcp.json` file in your Cursor IDE workspace:
```json
{
    "mcpServers": {
        "student-mcp-http-python": {
            "url": "http://127.0.0.1:3000/mcp"
        }
    }
}
```

2. Restart Cursor IDE to load the MCP configuration.

3. The Student Management System MCP tools will now be available in your Cursor IDE.

## Available MCP Tools

- `get_all_students`: Retrieve all student records
- `get_student_statistics`: Get statistical information about students
- `create_student`: Create a new student record
- `get_student`: Get student details by ID
- `update_student`: Update student information
- `delete_student`: Delete a student record
- `add_marks`: Add marks for a student
- `update_marks`: Update marks for a student
- `search_students_by_name`: Search students by name
- `search_students_by_department`: Search students by department
- `search_students_by_class`: Search students by class year
- `search_students_by_marks_range`: Search students by marks range
- `get_student_marks`: Get marks for a specific student
- `get_students_above_marks`: Get students with marks above threshold
- `get_students_below_marks`: Get students with marks below threshold

## Development

### Local Setup

1. Install dependencies and set up a virtual environment using uv and pyproject.toml:
```bash
uv sync
```

2. Start the PostgreSQL database using Docker Compose:
```bash
docker-compose up -d
```

3. Initialize the database schema and tables by running the provided SQL script:
```bash
docker exec -i <your_postgres_container_name> psql -U <your_db_user> -d <your_db_name> < init.sql
```
Replace `<your_postgres_container_name>`, `<your_db_user>`, and `<your_db_name>` with your actual container, user, and database names.

4. Run the application:
```bash
python src/main.py
```

## Database Schema

### Students Table
- id: Serial Primary Key
- name: VARCHAR(100)
- roll_number: VARCHAR(20) Unique
- department: VARCHAR(50)
- class_year: INTEGER
- email: VARCHAR(100) Unique

### Student Marks Table
- id: Serial Primary Key
- student_id: INTEGER (Foreign Key)
- subject: VARCHAR(100)
- marks: FLOAT
- semester: INTEGER