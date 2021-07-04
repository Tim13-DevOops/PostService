FROM python:3.8.6-slim

WORKDIR /work

RUN apt-get update && apt-get install -y netcat && apt-get install -y dos2unix

RUN pip install coverage

COPY entrypoint.sh setup.py setup.cfg /work/

RUN python /work/setup.py install

RUN dos2unix /work/entrypoint.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*

ADD /app /work/app/

ADD /test /work/test/

ENTRYPOINT ["sh", "/work/entrypoint.sh"]