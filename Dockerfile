FROM python:3.6

RUN mkdir -p /opt/pycard

COPY . /opt/pycard

RUN cd /opt/pycard &&\
    pip install -r requirements.txt

WORKDIR /opt/pycard

ENTRYPOINT [ "./docker-entrypoint.sh" ]
