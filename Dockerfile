# Base image
FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Set the environment variable for Django
ENV DJANGO_SETTINGS_MODULE=orion.settings.production

# Expose the port used by Django
EXPOSE 8000

# Start the Django development server
CMD ["dotenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
