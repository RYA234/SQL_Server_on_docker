FROM python:3.11-slim

WORKDIR /app

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --no-cache-dir -r requirements.txt

# Copy application code
COPY mcp_server.py .

EXPOSE 8000

CMD ["python", "mcp_server.py"]