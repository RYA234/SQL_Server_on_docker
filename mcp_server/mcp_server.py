#!/usr/bin/env python3
"""
MCP Server for bridging PostgreSQL and SQL Server
Acts as a Model Context Protocol server that can query SQL Server data
"""

import asyncio
import psycopg2
import pymssql
import json
from fastapi import FastAPI, HTTPException
from typing import Dict, Any, List
import os

app = FastAPI(title="SQL Server MCP", version="1.0.0")

# SQL Server connection configuration
SQL_SERVER_CONFIG = {
    "server": "sql_server_db",  # Container name
    "port": "1433",
    "database": "master",
    "username": "sa", 
    "password": "user@12345"
}

class MCPServer:
    def __init__(self):
        self.sql_server_conn = None
        
    def get_sql_server_connection(self):
        """Get SQL Server connection"""
        try:
            conn = pymssql.connect(
                server=SQL_SERVER_CONFIG['server'],
                port=SQL_SERVER_CONFIG['port'],
                user=SQL_SERVER_CONFIG['username'],
                password=SQL_SERVER_CONFIG['password'],
                database=SQL_SERVER_CONFIG['database']
            )
            return conn
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"SQL Server connection error: {str(e)}")
        
    def query_sql_server(self, query: str) -> List[Dict[str, Any]]:
        """Execute query on SQL Server and return results"""
        try:
            conn = self.get_sql_server_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            
            # Get column names
            columns = [column[0] for column in cursor.description]
            
            # Fetch results
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
                
            conn.close()
            return results
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"SQL Server query error: {str(e)}")

mcp_server = MCPServer()

@app.get("/")
async def root():
    return {"message": "SQL Server MCP is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test SQL Server connection
        result = mcp_server.query_sql_server("SELECT @@VERSION as version")
        return {"status": "healthy", "sql_server_version": result[0]["version"]}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

@app.post("/query")
async def execute_query(request: Dict[str, str]):
    """Execute SQL query on SQL Server"""
    if "query" not in request:
        raise HTTPException(status_code=400, detail="Missing 'query' parameter")
    
    query = request["query"]
    results = mcp_server.query_sql_server(query)
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }

@app.get("/tables")
async def get_tables():
    """Get list of tables from SQL Server"""
    query = """
    SELECT 
        TABLE_SCHEMA,
        TABLE_NAME,
        TABLE_TYPE
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE = 'BASE TABLE'
    ORDER BY TABLE_SCHEMA, TABLE_NAME
    """
    results = mcp_server.query_sql_server(query)
    return {"tables": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)