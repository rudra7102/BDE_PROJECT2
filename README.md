# 🦆 DuckDB System Analysis (Big Data Engineering Project)

## 📌 Overview
This project analyzes the internal working of DuckDB, a high-performance analytical database system.

The goal is to understand how DuckDB processes queries, what design decisions it uses, and how it behaves under different workloads.

---

## 🎯 Objectives
- Understand DuckDB system architecture
- Trace query execution from API to execution engine
- Analyze key design decisions and tradeoffs
- Map system components to big data concepts
- Perform experiments to evaluate performance
- Study system behavior under stress

---

## 🏗️ System Studied
- **DuckDB**
- Analytical (OLAP) database
- Columnar storage engine
- Vectorized execution model

---

## 🔍 Key Concepts Covered
- Columnar Storage
- Vectorized Execution
- Query Optimization
- Pipeline Execution
- Parallel Processing

---

## ⚙️ Execution Flow (Simplified)
1. Query issued from Python (`con.execute()`)
2. Parsed into AST
3. Bound and validated
4. Converted into logical plan
5. Optimized
6. Converted into physical plan
7. Executed using operators:
   - `PhysicalRangeScan`
   - `PhysicalHashAggregate`
   - `PhysicalHashJoin`

---

## 🧪 Experiments Performed

### 1. Aggregation Performance
- Measured time for `SUM` operation
- Result: Very fast due to vectorized execution

### 2. Join Performance
- Measured time for join queries
- Result: Slower due to row matching and hash table construction

### 3. Parallelism
- Compared 1 thread vs multiple threads
- Result: Limited improvement for small workloads

### 4. Data Size Scaling
- Increased dataset size
- Result: Execution time increases with data size

### 5. Join Scaling
- Increased join size
- Result: Join cost grows faster than aggregation
  
Aggregation Time: ~0.03 sec
Join Time: ~0.39 sec

Size 1000000: ~0.004 sec
Size 10000000: ~0.043 sec

Join size 100000: ~0.036 sec
Join size 1000000: ~0.368 sec


---

## ⚠️ Observations & Insights
- Aggregation is highly optimized
- Joins are computationally expensive
- Performance depends on data size
- Parallelism benefits depend on workload size
- Memory is a key limiting factor

---

## 🚨 Failure Analysis
- Large data → memory bottleneck → disk spilling
- Data skew → uneven workload → slower execution
- Complex queries → higher computation cost

---

## 📂 Project Structure
BDE_PROJECT2/
│── main.py # Experiment code
│── report.md # Detailed system analysis
│── .gitignore


---

## ▶️ How to Run

### 1. Install DuckDB
pip install duckdb

### 2. Run the Script
python main.py


📈 Key Takeaways
DuckDB is optimized for analytical workloads
Vectorized execution improves performance significantly
Joins are the most expensive operations
System performance is limited by memory and workload size

---

## 📊 Sample Results
