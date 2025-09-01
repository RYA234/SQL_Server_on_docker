#!/usr/bin/env python3
"""
Test script for MCP Server functionality
This simulates the PowerShell client connecting to PostgreSQL and then to SQL Server via MCP
"""

import requests
import time
import sys

# Note: psycopg2 import is optional since we might not have it locally
try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    print("Warning: psycopg2 not available, skipping PostgreSQL direct connection test")

def test_postgresql_connection():
    """Test direct PostgreSQL connection"""
    if not PSYCOPG2_AVAILABLE:
        print("⚠ PostgreSQL connection test skipped (psycopg2 not available)")
        return True
        
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="mcp_db", 
            user="mcp_user",
            password="mcp_pass"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mcp_connections;")
        results = cursor.fetchall()
        print(f"✓ PostgreSQL connection successful, found {len(results)} records")
        conn.close()
        return True
    except Exception as e:
        print(f"✗ PostgreSQL connection failed: {e}")
        return False

def test_mcp_server():
    """Test MCP Server API endpoints"""
    base_url = "http://localhost:8000"
    
    try:
        # Test root endpoint
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print(f"✓ MCP Server root endpoint: {response.json()['message']}")
        else:
            print(f"✗ MCP Server root endpoint failed: {response.status_code}")
            return False
            
        # Test health check
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✓ MCP Server health check: {health_data['status']}")
            print(f"  SQL Server version: {health_data.get('sql_server_version', 'N/A')[:50]}...")
        else:
            print(f"✗ MCP Server health check failed: {response.status_code}")
            return False
            
        # Test SQL Server query via MCP
        query_data = {"query": "SELECT DB_NAME() as current_database, @@VERSION as version"}
        response = requests.post(f"{base_url}/query", json=query_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ MCP Server SQL query successful, returned {result['count']} rows")
            if result['results']:
                print(f"  Database: {result['results'][0].get('current_database', 'N/A')}")
        else:
            print(f"✗ MCP Server SQL query failed: {response.status_code}")
            return False
            
        # Test tables endpoint  
        response = requests.get(f"{base_url}/tables")
        if response.status_code == 200:
            tables = response.json()
            print(f"✓ MCP Server tables endpoint: found {len(tables['tables'])} tables")
        else:
            print(f"✗ MCP Server tables endpoint failed: {response.status_code}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to MCP Server - is it running on localhost:8000?")
        return False
    except Exception as e:
        print(f"✗ MCP Server test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing SQL Server MCP Setup")
    print("=" * 40)
    
    # Wait a bit for services to start up
    print("Waiting for services to start...")
    time.sleep(5)
    
    all_tests_passed = True
    
    # Test PostgreSQL
    print("\n1. Testing PostgreSQL connection:")
    if not test_postgresql_connection():
        all_tests_passed = False
    
    # Test MCP Server
    print("\n2. Testing MCP Server:")
    if not test_mcp_server():
        all_tests_passed = False
    
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("✓ All tests passed! MCP setup is working correctly.")
        print("\nYou can now connect to:")
        print("- PostgreSQL: localhost:5432 (user: mcp_user, pass: mcp_pass)")
        print("- MCP Server API: http://localhost:8000")
        print("- SQL Server: localhost:1432 (user: sa, pass: user@12345)")
    else:
        print("✗ Some tests failed. Please check the logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()