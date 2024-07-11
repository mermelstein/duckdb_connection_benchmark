import os
import duckdb
import time
import concurrent.futures
from typing import Tuple, List

def create_sample_database(db_path: str) -> None:
    """Create a sample DuckDB database with some data."""
    with duckdb.connect(db_path) as conn:
        conn.execute("DROP TABLE IF EXISTS test")
        conn.execute("CREATE TABLE test (id INTEGER, value VARCHAR)")
        conn.execute("INSERT INTO test VALUES (1, 'a'), (2, 'b'), (3, 'c')")

def run_query(db_path: str) -> Tuple[bool, str]:
    """Run a simple query on the database."""
    try:
        with duckdb.connect(db_path, read_only=True) as conn:
            conn.execute("SELECT * FROM test").fetchall()
        return True, ""
    except Exception as e:
        return False, str(e)

def benchmark_concurrent_connections(db_path: str, num_connections: int) -> Tuple[int, float, List[str]]:
    """
    Attempt to run concurrent queries with a specified number of connections.
    
    Returns:
    - Number of successful queries
    - Time taken
    - List of error messages (if any)
    """
    start_time = time.time()
    successful_connections = 0
    errors = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_connections) as executor:
        future_to_connection = {executor.submit(run_query, db_path): i for i in range(num_connections)}
        for future in concurrent.futures.as_completed(future_to_connection):
            success, error = future.result()
            if success:
                successful_connections += 1
            else:
                errors.append(error)

    elapsed_time = time.time() - start_time
    return successful_connections, elapsed_time, errors

def run_benchmark(db_path: str, max_connections: int, step: int = 10) -> None:
    """Run the benchmark with increasing number of concurrent connections."""
    for num_connections in range(step, max_connections + 1, step):
        successful, time_taken, errors = benchmark_concurrent_connections(db_path, num_connections)
        print(f"Attempted concurrent connections: {num_connections}")
        print(f"Successful queries: {successful}")
        print(f"Time taken: {time_taken:.2f} seconds")
        if errors:
            print(f"Errors encountered: {len(errors)}")
            print(f"First error: {errors[0]}")
        print("---")

        if successful < num_connections:
            print("Failed to complete all concurrent queries. Stopping benchmark.")
            break

if __name__ == "__main__":
    db_path = "benchmark.db"
    max_connections = int(os.getenv('MAX_CONNECTIONS', 1000))
    step = int(os.getenv('STEP', 50))
    create_sample_database(db_path)
    run_benchmark(db_path, max_connections=max_connections, step=step)