FROM python:3
RUN pip install duckdb
COPY benchmark.py /app/benchmark.py
WORKDIR /app
CMD ["python", "benchmark.py"]