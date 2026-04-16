FROM python:3.11-slim
WORKDIR /code

COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir .

CMD ["uvicorn", "the_oracle.main:app", "--host", "0.0.0.0", "--port", "8080"]
