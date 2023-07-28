# Use the official Python image as the base image
FROM python:3.10

# Set the working directory in the container



# Copy the current directory contents into the container at /app


COPY ./app /app
COPY ./db /db

COPY ./lancedb /lancedb
# Install system dependencies


RUN apt-get update && apt-get install -y g++
RUN pip install gradio langchain chromadb gradio_client openai fastapi unstructured lancedb


# Expose the port that Gradio uses (default is 7860)
WORKDIR /app
# Command to run your Gradio app
CMD ["uvicorn", "main:app","--host","0.0.0.0","--port","3200"]
