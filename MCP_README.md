# SQL Server MCP Setup

This setup implements the architecture shown in the PlantUML diagram with two Docker containers:

## Architecture

- **Docker_B (sql_server_db)**: SQL Server 2022 with login `sa/user@12345` on port `1432`
- **Docker_A**: Contains:
  - **PostgreSQL**: Database server acting as "SelServer_MCP" on port `5432`
  - **Python MCP Server**: FastAPI server that bridges PostgreSQL and SQL Server on port `8000`

## Services

### SQL Server (Docker_B)
- **Container**: `sql1`
- **Port**: `1432` (external) → `1433` (internal)
- **Credentials**: 
  - User: `sa`
  - Password: `user@12345`
  - IP: `127.0.0.1`

### PostgreSQL (Docker_A)
- **Container**: `postgresql_mcp`
- **Port**: `5432`
- **Credentials**:
  - User: `mcp_user`
  - Password: `mcp_pass`
  - Database: `mcp_db`

### MCP Server (Docker_A)
- **Container**: `python_mcp`
- **Port**: `8000`
- **API Endpoints**:
  - `GET /`: Server info
  - `GET /health`: Health check and SQL Server connection test
  - `POST /query`: Execute SQL queries on SQL Server
  - `GET /tables`: List SQL Server tables

## Usage

1. **Start the services**:
```bash
docker compose up -d
```

2. **Test the setup**:
```bash
python test_mcp.py
```

3. **Connect from PowerShell** (or any client):
   - Connect to PostgreSQL: `localhost:5432`
   - Use MCP API to query SQL Server: `http://localhost:8000`

## Example API Usage

```bash
# Health check
curl http://localhost:8000/health

# Execute SQL Server query via MCP
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT @@VERSION"}'

# List SQL Server tables
curl http://localhost:8000/tables
```

## Client Connection Flow

```
PowerShell/Client → PostgreSQL (port 5432) → MCP Server (port 8000) → SQL Server (port 1432)
```

This matches the PlantUML diagram requirements where the client connects to PostgreSQL, which then connects to SQL Server via the MCP protocol to retrieve information.