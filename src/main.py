from db.database import engine, Base
from mcp_server.student_mcp import student_mcp

# Create database tables
Base.metadata.create_all(bind=engine)

# Run the FastMCP server using env-based configuration
if __name__ == "__main__":
    student_mcp.settings.host = "0.0.0.0"
    student_mcp.run("streamable-http")
