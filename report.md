# 🦆 DuckDB System Analysis

---

## 🎯 Problem Statement

DuckDB is designed to solve the problem of fast analytical query processing on large datasets.

Traditional databases are optimized for transactional workloads (OLTP), but analytical queries (SUM, JOIN, GROUP BY) are computationally expensive and slow.

DuckDB provides:
- Columnar storage for efficient data access
- Vectorized execution for high performance
- In-memory processing for fast query execution

It is mainly used for data analytics workloads where speed and efficiency are critical.

---

## 🧠 Execution Path (Detailed)

Query starts from Python:
con.execute("SELECT SUM(i) FROM range(1000000) t(i)")

### Step 1: API Layer
Connection::Query()
- Entry point from Python
- Sends query to ClientContext

### Step 2: Query Preparation
ClientContext::Query()
→ calls PendingQuery()

ClientContext::PendingQuery()
- Creates PendingQueryResult object
- Stores query before execution

### Step 3: Query Processing Pipeline

1. Parse
- SQL string → AST (tree structure)

2. Bind
- Resolves table/column names

3. Plan
- Creates Logical Plan

4. Optimize
- Improves query plan

5. Physical Plan
- Converts to executable operators

### Step 4: Execution Engine

PendingQueryResult::Execute()

- Creates pipelines
- Each pipeline = chain of operators

Example pipeline:
Scan → Aggregate → Output

### Step 5: Execution

Executor:
- Processes data in chunks (vectorized execution)
- Operators work on batches, not rows

Final result returned to Python

---

## 🔬 Deep Dive: Vectorized Execution

DuckDB uses vectorized execution.

### What it means
Instead of processing one row at a time,
DuckDB processes data in batches (DataChunks).

### How it works

- DataChunk → ~1024 rows  
- Each column → Vector  

Execution:
- Operators process entire chunk at once

Example:
Instead of:
for each row → SUM

DuckDB:
process 1024 rows together → SUM

### Why it is powerful
- Better CPU cache utilization
- Faster computation
- Uses SIMD instructions

### Tradeoff
- Complex execution engine

---

## 🧱 Design Decisions

### 1. Columnar Storage
- Implemented in: `src/storage/column`
- Data stored column-wise

Why:
- Efficient for analytical queries (SUM, AVG)

Tradeoff:
- Slower for row-based updates

---

### 2. Vectorized Execution
- Implemented in: `src/execution`, DataChunk, Vector

Why:
- High CPU efficiency
- Faster batch processing

Tradeoff:
- Complex execution design

---

### 3. In-Memory First Design
- Managed by: buffer manager (`src/storage`)

Why:
- Very fast query performance

Tradeoff:
- Limited by RAM size

---

## 🔗 Concept Mapping

### Columnar Storage
- Stores data column-wise
- Improves analytical query performance

### Vectorized Execution
- Batch-based processing
- Improves CPU efficiency

### Query Optimization
- Optimizes logical plans
- Reduces unnecessary computation

### Pipeline Execution
- Query split into stages
- Each stage executed sequentially

---

###  Experiments

### Experiment Setup
    -Used DuckDB Python API
    -Tested aggregation, join, parallel execution
    -Also tested behavior with increasing data size and join scaling

📊 Experiment 1: Basic Performance

Output
Aggregation Time: 0.0275 sec  
Join Time: 0.2867 sec  

1 Thread: 0.0288 sec  
4 Threads: 0.0277 sec  
Observation
Aggregation is very fast
Join is much slower compared to aggregation
Increasing threads shows very little improvement
Analysis
Aggregation is fast due to columnar storage and vectorized execution
Join is slower because it requires matching rows and building hash tables
Parallelism does not help much here because the dataset is small and overhead dominates

📊 Experiment 2: Data Size Scaling
Observation
As data size increases, execution time increases
Analysis
Query performance depends on amount of data scanned
More data → more computation → higher execution time
Shows DuckDB follows near-linear scaling for simple aggregation

### Output
Size 1000000: 0.0044  
Size 5000000: 0.0259  
Size 10000000: 0.0431  

📊 Experiment 3: Join Scaling
Observation
Join time increases much faster than aggregation
Analysis
Join operations require:
Building hash tables
Matching rows
This makes joins computationally expensive
Performance degrades faster with increasing data size

### Output
Join size 100000: 0.0364  
Join size 500000: 0.1964  
Join size 1000000: 0.3685  

📊 Experiment 4: Parallelism
Observation
Increasing threads gives limited improvement
Analysis
Small workloads do not fully utilize multiple threads
Thread management overhead reduces benefit
Parallelism is more effective for larger datasets

### Observation

- Aggregation is very fast due to columnar and vectorized execution
- Join is significantly slower due to row matching cost
- Parallel execution shows slight improvement (limited by workload size)

---

### Analysis

- Joins are expensive operations in analytical systems
- Parallelism helps but depends on workload size
- DuckDB is highly optimized for aggregation queries

---

### Execution Operators

DuckDB uses physical operators such as:
- PhysicalHashAggregate → used for aggregation
- PhysicalHashJoin → used for joins
- PhysicalRangeScan → used for scanning data

## ⚠️ Failure Analysis

### 1. Large Data Size
- Execution time increases as data grows
-When data exceeds RAM, DuckDB performs disk spilling.
 Disk access is slower than memory, causing performance degradation.

---

### 2. Data Skew
- Uneven data distribution
- Some operations become slower

---

### 3. Complex Queries
- Multiple joins increase computation cost
- Performance degrades

---

### System Assumption
- DuckDB assumes data fits in memory for optimal performance

---

## 📊 System Behavior Under Stress

### Large Data
- Performance degrades when exceeding RAM
- Disk spilling slows execution

### Heavy Joins
- Significant slowdown due to matching operations

### Parallel Load
- Performance improves with threads
- Limited by CPU cores and workload size

---

## ⚙️ Code Evidence

From `client_context.cpp`:

transaction.ResetActiveQuery();
transaction.Rollback(nullptr);

Meaning:
- DuckDB manages queries using transactions
- Ensures safe rollback on failure

---

From `pending_query_result.cpp`:

PendingQueryResult::Execute() {
    auto lock = LockContext();
    return ExecuteInternal(*lock);
}

Meaning:
- Execution is controlled and not direct
- Context locking ensures safe execution
- ExecuteInternal() performs actual query execution

---

## 🚀 Possible Improvements

### 1. Better Handling of Large Data
- Improve disk-based execution
- Reduce dependency on RAM

---

### 2. Adaptive Query Optimization
- Adjust execution plan dynamically
- Improve performance for complex queries

---

### 3. Handling Data Skew
- Balance workload dynamically
- Avoid bottlenecks

---

### 4. Improved Parallel Execution
- Smarter thread allocation
- Better CPU utilization

---

## 🔑 Key Insights

- DuckDB is optimized for analytical workloads
- Vectorized execution provides major performance gains
- Joins are the most expensive operations
- Parallelism improves performance but depends on workload
- Memory is the main limiting factor

---

## 🎯 Conclusion

DuckDB is a high-performance analytical database that uses columnar storage and vectorized execution to efficiently process queries.

Its design enables fast aggregation and analytical operations, but performance depends on memory and query complexity.

This project demonstrated how DuckDB processes queries internally, how design decisions impact performance, and how the system behaves under stress.