FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies first for faster rebuilds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project code
COPY . .

# Expose FastAPI port and start Uvicorn
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]