FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

COPY ./app .
COPY requirements.txt .

RUN pip install -r requirements.txt

# Added the --reload flag to enable hot reloading, which is useful for development

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
