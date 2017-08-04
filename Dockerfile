FROM python:latest
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip3 install -r requirements.txt
CMD python3 run.py
