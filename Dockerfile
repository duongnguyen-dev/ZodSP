FROM python:3.10-slim

LABEL maintainer="duongng2911"
LABEL organization="nrl"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app
COPY ./main.py /app
COPY ./services /app/services
COPY ./basemodel /app/basemodel
COPY ./utils /app/utils
COPY ./scripts /app/scripts
COPY ./model /app/model
COPY ./models /app/models

# Declaring which port the container might listen on runtime 
EXPOSE 3000

RUN pip install -r requirements.txt --no-cache-dir
RUN chmod +x ./scripts/download_model.sh
RUN ./scripts/download_model.sh 
RUN ls -l /app/models

# FastAPI port = Container port
# The best way to write docker file is to use an Entrypoint like this
ENTRYPOINT [ "uvicorn"]
CMD [ "main:app" , "--host", "0.0.0.0", "--port", "3000", "--reload"]
