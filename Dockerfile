FROM python:3.8-buster as builder
WORKDIR /opt/app
COPY requirements.lock /opt/app
RUN pip3 install -r requirements.lock

FROM python:3.8-slim-buster as runner
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY fetch_ohlcv.py /scripts/fetch_ohlcv.py

# RUN apt update \
#   && apt install -y libpq5 libxml2 \
#   && apt-get clean \
#   && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python3", "/scripts/fetch_ohlcv.py"]