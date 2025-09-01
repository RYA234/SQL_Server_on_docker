-- Initialize PostgreSQL for MCP Server
CREATE DATABASE mcp_db;
CREATE USER mcp_user WITH PASSWORD 'mcp_pass';
GRANT ALL PRIVILEGES ON DATABASE mcp_db TO mcp_user;

-- Connect to mcp_db and create a sample table for demonstration
\c mcp_db;

-- Create a sample table to demonstrate PostgreSQL functionality
CREATE TABLE IF NOT EXISTS mcp_connections (
    id SERIAL PRIMARY KEY,
    connection_name VARCHAR(100),
    target_server VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert a sample record
INSERT INTO mcp_connections (connection_name, target_server) 
VALUES ('SQL Server Connection', 'sql_server_db');

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mcp_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mcp_user;