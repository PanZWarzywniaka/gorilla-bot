FROM python:latest

RUN pip install pymysql \
    pandas \
    pandas_ta \
    numpy \
    peewee \
    plotly \
    yfinance \
    cryptography

WORKDIR /opt/trading/src
COPY . .

CMD ["python3", "./main.py"]

