FROM arm32v7/python:3.10

RUN pip install pymysql \
    pandas \
    pandas_ta \
    numpy \
    peewee \
    plotly \
    yfinance

WORKDIR /opt/trading/src
COPY . .

CMD ["python3", "./main.py"]

