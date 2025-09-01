# SQL Server on Docker Development Environment

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Prerequisites
- Docker and Docker Compose v2 must be installed
- Minimum 8GB RAM available for SQL Server container
- Port 1432 must be available on host machine

### Build and Run the Environment
- **Build the container**: `docker compose build` -- takes 30 seconds. NEVER CANCEL. Set timeout to 90+ seconds.
- **Start the services**: `docker compose up -d` -- takes 60 seconds total (container start + SQL Server initialization + tSQLt setup). NEVER CANCEL. Set timeout to 120+ seconds.
- **Check startup logs**: `docker compose logs sql_server_db` -- monitor for "running set up script" completion
- **Stop the services**: `docker compose down` -- takes 10 seconds. Set timeout to 60+ seconds.

### SQL Server Access
- **Connection inside container**: `docker compose exec sql_server_db /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C`
- **Run SQL query**: `docker compose exec sql_server_db /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "SELECT @@VERSION"`
- **Execute SQL file**: `docker compose exec sql_server_db /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/[filepath].sql`
- **Host**: sql1 (container name)
- **Port**: 1432 (host) -> 1433 (container)
- **SA Password**: user@12345
- **Databases**: `main` (production), `tSQLt_Example` (testing framework)

## Validation

### Mandatory Post-Change Validation
After making any code changes, always run these validation steps:

1. **Build and start environment**:
   ```bash
   docker compose build    # 30 seconds
   docker compose up -d    # 60 seconds total
   ```

2. **Verify SQL Server connectivity**:
   ```bash
   docker compose exec sql_server_db /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "SELECT @@VERSION"
   ```

3. **Verify databases exist**:
   ```bash
   docker compose exec sql_server_db /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "SELECT name FROM sys.databases"
   ```
   Expected: master, tempdb, model, msdb, tSQLt_Example, main

4. **Test stored procedure execution**:
   ```bash
   docker compose exec sql_server_db /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "USE [main]; DECLARE @output int; EXEC dbo.input_pass_output @inputValue = 42, @outputValue = @output OUTPUT; SELECT @output AS result;"
   ```
   Expected: Result should be 42

5. **Run tSQLt test suite**:
   ```bash
   docker compose exec sql_server_db /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "USE [tSQLt_Example]; EXEC tSQLt.Run 'AcceleratorTests'"
   ```
   Expected: 10+ tests should pass (some may fail, which is expected for demonstration purposes)

6. **Clean shutdown**:
   ```bash
   docker compose down     # 10 seconds
   ```

### Critical Timing Expectations
- **NEVER CANCEL** Docker build or startup commands. SQL Server initialization requires time.
- Container build: 30 seconds (set timeout to 90+ seconds)
- Container startup: 60 seconds total (set timeout to 120+ seconds)
- SQL Server ready: Wait for "running set up script" completion in logs
- Container shutdown: 10 seconds (set timeout to 60+ seconds)

## Common Tasks

### Working with SQL Code
- **Main code location**: `src/main/sample/` - Production stored procedures and functions
- **Test code location**: `src/test/sample/` - tSQLt unit tests  
- **tSQLt setup files**: `src/tSQLt_setting/` - Testing framework installation scripts

### Running Tests
- **Run all tSQLt tests**: `docker compose exec sql_server_db /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "USE [tSQLt_Example]; EXEC tSQLt.RunAll"`
- **Run specific test class**: `docker compose exec sql_server_db /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "USE [tSQLt_Example]; EXEC tSQLt.Run 'AcceleratorTests'"`
- **Run single test**: `docker compose exec sql_server_db /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "USE [tSQLt_Example]; EXEC tSQLt.Run 'AcceleratorTests.[test name]'"`

### Development Workflow
1. Make changes to SQL files in `src/main/` or `src/test/`
2. Apply main code changes: `docker compose exec sql_server_db /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/main/sample/input_output.sql`
3. Apply test changes: `docker compose exec sql_server_db /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/test/sample/test_input_output.sql`
4. Run validation tests (see Mandatory Post-Change Validation above)
5. For persistent changes, rebuild container: `docker compose down && docker compose build && docker compose up -d`

## Project Structure

### Repository Root
```
.
├── Dockerfile              # SQL Server container definition
├── docker-compose.yml      # Service orchestration
├── entrypoint.sh           # Container startup script
├── db-init.sh             # Database initialization script
├── readme.md              # Japanese documentation
└── src/                   # SQL source code
    ├── main/              # Production code
    │   └── sample/        # Sample stored procedures
    ├── test/              # Test code  
    │   └── sample/        # Sample test procedures
    └── tSQLt_setting/     # tSQLt framework files
```

### Key Configuration Details
- **Base Image**: mcr.microsoft.com/mssql/server:2022-latest
- **SQL Server Version**: 2022 Developer Edition  
- **tSQLt Version**: 1.0.8083.3529
- **Environment**: ACCEPT_EULA=Y, SA_PASSWORD=user@12345, MSSQL_AGENT_ENABLED=true
- **Volume Mount**: `./src:/usr/src/docker/src` (for live code editing)
- **Data Persistence**: `sqlserver-data` volume for database files

## Troubleshooting

### Common Issues
- **Port 1432 in use**: Change port mapping in docker-compose.yml or stop conflicting service
- **Insufficient memory**: SQL Server requires minimum 8GB RAM, increase Docker memory allocation
- **Connection refused**: Wait for full SQL Server startup (check logs for "running set up script" completion)
- **tSQLt tests failing**: Some sample tests are designed to fail for demonstration purposes
- **Database not found**: Ensure container fully initialized by checking `docker compose logs sql_server_db`

### Recovery Commands
- **Full reset**: `docker compose down -v && docker compose build && docker compose up -d`
- **View container logs**: `docker compose logs sql_server_db`  
- **Access container shell**: `docker compose exec sql_server_db bash`
- **Force container rebuild**: `docker compose build --no-cache`

### Known Limitations
- Some test procedures reference incorrect database schemas (productg vs main) - this is in the original sample code
- Japanese documentation in readme.md - SQL code itself is in English
- The docker-compose.yml version attribute warning can be safely ignored

## Important Notes
- Always wait for complete startup before connecting (monitor logs for initialization completion)
- Use `-C` flag with sqlcmd to ignore certificate warnings
- tSQLt framework is pre-installed and ready to use
- Database changes made via sqlcmd are temporary unless applied to source files and container rebuilt
- Volume mounts allow live editing of SQL files in `src/` directory