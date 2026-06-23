FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY . .

RUN uv sync

CMD ["uv", "run", "--directory", "apps/api", "python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]