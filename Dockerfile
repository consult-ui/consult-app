FROM python:3.12.4

WORKDIR /workdir

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update &&  \
    apt-get install libpq-dev -y

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /workdir/

CMD alembic upgrade head && \
    uvicorn app.main:app --port $PORT --forwarded-allow-ips='*' --proxy-headers --host=0.0.0.0 --log-level warning