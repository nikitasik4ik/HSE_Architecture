FROM python:3.12

EXPOSE 8080/tcp

COPY ./requirements.txt /backend/requirements.txt
COPY . /backend/
WORKDIR ./backend

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /backend/requirements.txt \
    && rm -rf /root/.cache/pip

#CMD ["python", "app.py"] \
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "8080"]