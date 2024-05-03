FROM python:3.8-buster as builder
WORKDIR /opt/app
COPY requirements.txt /opt/app
RUN pip3 install -r requirements.txt

FROM python:3.8-slim-buster as runner
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY fetch_ohlcv.py /scripts/fetch_ohlcv.py

ENTRYPOINT ["python3", "/scripts/fetch_ohlcv.py"]