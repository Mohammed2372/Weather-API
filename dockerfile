# base image to start with
FROM python:3.11-alpine

# run commands
RUN apk update && apk add nano redis supervisor

# prevent pyc files write to disk
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Requirements
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project files
COPY . /app/

# expose ports
EXPOSE 8000 6379

# copy supervisor config into the image
COPY ./supervisord.conf /etc/supervisord.conf

# set redis host/port for Django inside container
ENV REDIS_HOST=127.0.0.1
ENV REDIS_PORT=6379

# run supervisor
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
