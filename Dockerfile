# Dockerfile
FROM python:3.10-slim

# Prevents Python buffering logs
ENV PYTHONUNBUFFERED=1 

# Set working dir
WORKDIR /app

# Install runtime deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy app code
COPY . .

# Ensure the data folder exists
RUN mkdir -p /app/data

# Expose Flask port
EXPOSE 5001

# Launch with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
