FROM python:3.11

WORKDIR etl/src

COPY requirements.txt /etl/requirements.txt

RUN pip install --no-cache-dir -r /etl/requirements.txt

COPY src /etl/src

CMD ["python", "main.py"]
