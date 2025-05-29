# Base image
FROM python:3.12-slim

# Environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Collect static files (uncomment if needed)
# RUN python manage.py collectstatic --noinput

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
