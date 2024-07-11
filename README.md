# DuckDB Concurrent Connections Benchmark

This repository contains a benchmark script to test the maximum number of concurrent connections to a DuckDB database. The script measures the performance and success rate of running concurrent queries as the number of connections increases.

## Contents

- `benchmark.py`: The main Python script that runs the benchmark.
- `Dockerfile`: Used to create a Docker image for running the benchmark.

## Requirements

- Docker

## How It Works

The benchmark script does the following:

1. Creates a sample DuckDB database with a simple table.
2. Attempts to run concurrent queries, increasing the number of connections in steps.
3. For each step, it measures:
   - Number of successful queries
   - Time taken to complete all queries
   - Any errors encountered
4. The benchmark stops when it fails to complete all concurrent queries successfully.

## Running the Benchmark

You can run the benchmark using Docker. Follow these steps:

1. Clone this repository
2. run this from the cli: `MAX_CONNECTIONS=10000 STEP=1000 docker-compose up --build`

You can replace the number of max connection and step increases to whatever you want