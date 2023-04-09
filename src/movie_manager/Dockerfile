FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /movie_manager

COPY . /movie_manager

RUN pip install -r requirements.txt

# Added the --reload flag to enable hot reloading, which is useful for development

WORKDIR /movie_manager/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
