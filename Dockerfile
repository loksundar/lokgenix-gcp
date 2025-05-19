# Dockerfile for Lokgenix Gradio App

# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the requirements file into the container at /app
COPY requirements.txt .

# 4. Install any needed packages specified in requirements.txt
# --no-cache-dir: Disables the cache, which can reduce image size.
# --trusted-host pypi.python.org: Can sometimes help with network issues in certain environments, optional.
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# 5. Copy the rest of the application code (app.py) into the container at /app
COPY app.py .

# 6. Make port 7860 available to the world outside this container
# This is the default port Gradio runs on. If your app uses a different port, change this.
EXPOSE 7860

# 7. Define environment variable for the Hugging Face API Token
# IMPORTANT: You will set the actual value of HF_API_TOKEN when you deploy
# on GCP (e.g., as an environment variable in Cloud Run or a Kubernetes secret).
# DO NOT hardcode your actual token here.
ENV HF_API_TOKEN=""

# 8. Run app.py when the container launches
# The command `gradio app.py` is also an option if you prefer,
# but `python app.py` will execute your script which includes `launch()`.
# The `app.py` script uses `server_name="0.0.0.0"` which is good for Docker.
CMD ["python", "app.py"]