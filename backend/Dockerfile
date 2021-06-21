FROM python:3.9.5

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ставим русскую локаль
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y locales locales-all
ENV LANGUAGE ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
RUN locale-gen ru_RU.UTF-8 && dpkg-reconfigure locales

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy wait-for-it.sh
COPY ./entrypoint.py /usr/src/app/entrypoint.py
RUN chmod +x /usr/src/app/entrypoint.py

# copy project
COPY . /usr/src/app/

# run entrypoint.py
ENTRYPOINT ["python", "/usr/src/app/entrypoint.py"]
