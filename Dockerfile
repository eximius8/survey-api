FROM python:3

# set work directory
WORKDIR /code

# set environment variables
ENV SECRET_KEY 4lv5*mmca23wyeics&^%j71h!qy@43&c(wsd@fj+_0mp#x-8y-


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . /code