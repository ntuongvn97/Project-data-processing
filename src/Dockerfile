# this is an official Python runtime, used as the parent image
FROM python:3.6.5-slim

# set the working directory in the container to /app
WORKDIR /src

# add the current directory to the container as /app
ADD . /src

# execute everyone's favorite pip command, pip install -r
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

# execute the Flask app
CMD ["python", "app_mqtt.py"]