# Set base image (host OS)
FROM python:3.8-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /CC_PORTAL_ALUNOS

# Copy everything
COPY . .

# Install GCC
RUN apk add build-base

# Install any dependencies
RUN pip install -r requirements.txt

# Specify the command to run on container start
CMD [ "python3", "-m" , "flask", "--app", "app", "run", "--host=0.0.0.0"]