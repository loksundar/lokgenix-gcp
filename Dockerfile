# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# 4. Copy the requirements file into the container at /app
COPY requirements.txt .

# 5. Install any needed packages specified in requirements.txt
# --no-cache-dir: Disables the cache, which can reduce image size.
# --trusted-host pypi.python.org: Can sometimes help with network issues in certain environments, optional.
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# 6. Copy the rest of the application code (app.py) into the container at /app
COPY app.py .

# 7. Make port 8080 available. Cloud Run will provide a PORT environment variable (often 8080)
#    and expects the application to listen on that $PORT.
EXPOSE 8080

# 8. Define environment variable for the Hugging Face API Token
# IMPORTANT: You will set the actual value of HF_API_TOKEN when you deploy
# on GCP (e.g., as an environment variable in Cloud Run or a Kubernetes secret).
# DO NOT hardcode your actual token here.
ENV HF_API_TOKEN=""

# 9. Run the Gradio app using the Gradio CLI.
# This command tells Gradio to listen on all network interfaces (0.0.0.0)
# and on the port specified by the PORT environment variable (provided by Cloud Run).
# If PORT is not set (e.g., during local testing without -e PORT=...), it defaults to 8080.
# The 'exec' command ensures that Gradio is the main process and handles signals correctly.
CMD ["sh", "-c", "exec gradio app.py --host 0.0.0.0 --port ${PORT:-8080}"]
