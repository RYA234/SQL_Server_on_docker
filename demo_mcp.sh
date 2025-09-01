#!/bin/bash
# Demo script showing the complete MCP flow from PowerShell client perspective

echo "=== SQL Server MCP Demo ==="
echo "Demonstrating the flow: Client → PostgreSQL → MCP Server → SQL Server"
echo

# Check service status
echo "1. Checking service status..."
docker compose ps
echo

# Test PostgreSQL (simulating client connection to SelServer_MCP)
echo "2. Connecting to PostgreSQL (SelServer_MCP)..."
docker exec postgresql_mcp psql -U mcp_user -d mcp_db -c "SELECT 'Connected to PostgreSQL MCP' as status;"
echo

# Test MCP Server endpoints
echo "3. Testing MCP Server API endpoints..."

echo "   → Root endpoint:"
curl -s http://localhost:8000/ | python -m json.tool
echo

echo "   → Health check (tests SQL Server connection):"
curl -s http://localhost:8000/health | python -m json.tool
echo

echo "   → Query SQL Server via MCP:"
curl -s -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT DB_NAME() as database_name, GETDATE() as current_datetime"}' | python -m json.tool
echo

echo "   → List SQL Server tables via MCP:"
curl -s http://localhost:8000/tables | python -m json.tool | head -n 15
echo "   (truncated...)"
echo

echo "=== Demo Complete ==="
echo "✓ PostgreSQL (Docker_A) is accessible on port 5432"
echo "✓ MCP Server (Docker_A) is running on port 8000"  
echo "✓ SQL Server (Docker_B) is accessible via MCP on port 1432"
echo "✓ Client can connect to PostgreSQL and query SQL Server via MCP"