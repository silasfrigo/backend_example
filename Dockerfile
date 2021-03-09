FROM public.ecr.aws/lambda/python:3.8

RUN python3.8 -m pip install --upgrade pip

COPY ./src/layers/requirements/requirements.txt /tmp/requirements.txt
RUN python3.8 -m pip install -r /tmp/requirements.txt

COPY ./requirements-dev.txt /tmp/requirements-dev.txt
RUN python3.8 -m pip install -r /tmp/requirements-dev.txt

# to wait mysql
RUN yum -y install nmap
COPY ./wait-for /