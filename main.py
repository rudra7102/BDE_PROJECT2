import duckdb
import time

con = duckdb.connect()

# Experiment 1: Aggregation
start = time.time()
con.execute("SELECT SUM(i) FROM range(10000000) t(i)").fetchall()
print("Aggregation Time:", time.time() - start)

# Experiment 2: Join
start = time.time()
con.execute("""
SELECT *
FROM range(1000000) t1(i)
JOIN range(1000000) t2(j)
ON t1.i = t2.j
""").fetchall()
print("Join Time:", time.time() - start)

# Experiment 3: Parallelism
con.execute("PRAGMA threads=1")
start = time.time()
con.execute("SELECT SUM(i) FROM range(10000000) t(i)").fetchall()
print("1 Thread:", time.time() - start)

con.execute("PRAGMA threads=4")
start = time.time()
con.execute("SELECT SUM(i) FROM range(10000000) t(i)").fetchall()
print("4 Threads:", time.time() - start)