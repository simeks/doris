# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app


# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m doris
RUN chown -R doris:doris /app
USER doris

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]