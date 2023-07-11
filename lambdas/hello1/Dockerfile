FROM public.ecr.aws/lambda/python:3.10

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY app.py .

CMD ["app.handler"]
