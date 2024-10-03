FROM python:3.11

WORKDIR ugc_api/src

COPY requirements.txt /ugc_api/requirements.txt

RUN pip install --no-cache-dir -r /ugc_api/requirements.txt

COPY src /ugc_api/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
