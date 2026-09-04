"""
Curriculum Builder - Part 4: Sections 17 to 28
Observability Fundamentals, New Relic Architecture, APM, Infrastructure, Logs,
NRQL Deep Dive (50 Production Queries), Dashboards, Alerting, Synthetics, Kubernetes,
NerdGraph GraphQL APIs, and Python + New Relic Autonomous Remediation Capstone
"""

def get_part4_content() -> str:
    return r'''# 17. Observability Fundamentals

### 17.1 The Three Pillars of Observability and Beyond

Observability is the degree to which you can understand the internal state of a system based purely on its external outputs. In distributed systems, observability is what distinguishes an SRE from someone guessing in the dark.

```
                    +--------------------------------+
                    |       Observability Core       |
                    +--------------------------------+
                                    |
          +-------------------------+-------------------------+
          |                         |                         |
          v                         v                         v
     [ METRICS ]                [ LOGS ]                 [ TRACES ]
 "What is happening?"      "What happened?"         "Where did it happen?"
Aggregated, numerical      Discrete, contextual     Causal path of a request
time-series data           timestamped events       across microservices
```

### 17.2 Metrics: Types and Mathematics
1. **Counter**: A cumulative metric that represents a single monotonically increasing value. It can only increase or be reset to zero on restart (e.g., total requests served, error counts).
   - *Rate Calculation*: SREs calculate the per-second rate of increase:
     $$\text{rate} = \frac{\Delta \text{Counter}}{\Delta \text{Time}}$$
2. **Gauge**: A metric that represents a single numerical value that can arbitrarily go up and down (e.g., current memory usage, CPU temperature, active worker threads).
3. **Histogram**: Samples observations (usually request durations or response sizes) and counts them in configurable bucket intervals. Used to calculate mathematical percentiles ($p50, p95, p99$).
4. **Summary**: Similar to histograms, calculates streaming quantiles directly over a sliding time window.

#### The High-Cardinality Trap
**Cardinality** refers to the number of unique values in a dataset.
- *Low Cardinality*: `http_status` (200, 400, 500 $\approx 10$ values), `environment` (`production`, `staging` $\approx 2$ values).
- *High Cardinality*: `user_id`, `email`, `order_id` (millions of unique values).
- *Production Warning*: In traditional metrics engines (Prometheus), putting high-cardinality values into metric labels will cause memory explosion and crash your metrics server. In New Relic's Telemetry Data Platform (NRDB), high cardinality is natively indexed and queried efficiently without explosion.

### 17.3 Logs: Unstructured vs Structured vs Correlated
- **Unstructured Log**: `2026-09-04 12:00:00 Failed to process order for user 10293`
  - Requires slow, expensive regex scanning.
- **Structured JSON Log**:
  ```json
  {"timestamp": "2026-09-04T12:00:00Z", "level": "ERROR", "user_id": 10293, "order_id": "ORD-991", "error": "InsufficientFundsException", "trace.id": "4bf92f3577b34da6a3ce929d0e0e4736"}
  ```
  - Instant indexing and filtering on `user_id` and `error`.

### 17.4 Traces: Distributed Context Propagation

In a microservices architecture, a single user click may traverse 20 independent services. **Distributed Tracing** tracks the complete execution path:
- **Trace**: The end-to-end journey of a request through a distributed system.
- **Span**: A single named, timed operation representing a contiguous unit of work within a trace (e.g., an HTTP call, an SQL query).
- **Trace Context Propagation**: Carried via W3C standard HTTP headers:
  - `traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`
    - `00`: Version
    - `4bf92f3577b34da6a3ce929d0e0e4736`: Trace ID (shared across all services)
    - `00f067aa0ba902b7`: Parent Span ID
    - `01`: Trace Flags (sampled)

---

# 18. New Relic — Architecture & Telemetry Data Platform

### 18.1 The New Relic Telemetry Engine (NRDB)

New Relic is built upon the **Telemetry Data Platform (TDP)** powered by **NRDB (New Relic Database)**, an ultra-fast, petabyte-scale, column-oriented database optimized for real-time aggregation across metrics, events, logs, and traces (MELT).

```
+------------------------------------------------------------------------------------+
|                         NEW RELIC TELEMETRY ARCHITECTURE                           |
+------------------------------------------------------------------------------------+
| DATA SOURCES:                                                                      |
| Python APM Agent  | Infra Agent | Kubernetes Daemon | OpenTelemetry | CloudWatch   |
+------------------------------------------------------------------------------------+
                                      |
                       HTTPS (TLS 1.3) / OTLP (gRPC)
                                      |
                                      v
+------------------------------------------------------------------------------------+
| NEW RELIC INGESTION PIPELINE:                                                      |
| Authentication -> Validation -> Parsing & Attribute Enrichment -> Stream Routing   |
+------------------------------------------------------------------------------------+
                                      |
                                      v
+------------------------------------------------------------------------------------+
| NRDB (Telemetry Data Platform):                                                    |
| Column-Oriented Storage | Distributed Query Engine | Global Entity Registry        |
+------------------------------------------------------------------------------------+
            |                         |                          |
            v                         v                          v
     [ NRQL Engine ]        [ Alerting & Workflows ]    [ NerdGraph (GraphQL) ]
  Dashboards & Analytics     SLO & Anomaly Triggers      Automation & Python SDK
```

### 18.2 Entities, Tags, and Entity Relationships

In New Relic, an **Entity** is any uniquely identifiable component that produces telemetry:
- An APM Application (`Payment-API`)
- A Host Virtual Machine (`ip-10-0-1-50`)
- A Kubernetes Pod (`order-processor-7c89b-x92f`)
- An AWS RDS Database (`aurora-prod-cluster`)

Every entity has a globally unique identifier: **Entity GUID** (e.g., `MjUyMDUyfEFQTXxBRVBMSUNBVElPTnwxMDQ4NTky`). Entities are automatically linked via **Relationship Mapping**:
$$\text{Host} \longrightarrow \text{Kubernetes Pod} \longrightarrow \text{APM Application} \longrightarrow \text{Database Service}$$

---

# 19. New Relic APM

### 19.1 Key APM Concepts
- **Transaction**: A logical unit of work in an application (e.g., processing an HTTP `POST /checkout` request or consuming an AMQP queue message).
- **Throughput**: Measured in Requests Per Minute (RPM) or Transactions Per Minute (TPM).
- **Response Time**: Total wall-clock duration of a transaction, broken down into execution tiers: Python interpreter time, database queries, and external HTTP calls.
- **Error Rate**: Percentage of transactions that resulted in an unhandled exception or HTTP status code $\ge 500$.
- **Apdex (Application Performance Index)**: An open industry standard measuring user satisfaction based on response time:
  $$\text{Apdex} = \frac{\text{Satisfied Count} + \frac{\text{Tolerating Count}}{2}}{\text{Total Count}}$$
  Where $T$ is the target response time threshold:
  - *Satisfied*: Response time $\le T$
  - *Tolerating*: $T < \text{Response Time} \le 4T$
  - *Frustrated*: Response time $> 4T$ or returns an unhandled error.

### 19.2 Instrumenting Python Applications

#### Instrumenting FastAPI with New Relic Python Agent
1. Install package: `pip install newrelic`
2. Generate configuration: `newrelic-admin generate-config <YOUR_LICENSE_KEY> newrelic.ini`
3. Launch with agent injection:
   ```bash
   NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program uvicorn main:app --host 0.0.0.0 --port 8000
   ```

#### Programmatic Custom Instrumentation in Python
```python
import newrelic.agent

# Initialize agent manually in code
newrelic.agent.initialize("newrelic.ini")

# Record custom application metrics
newrelic.agent.record_custom_metric("Custom/Order/HighValueCheckout", 1)

# Record custom attributes attached to the current active transaction
@app.post("/api/checkout")
async def checkout(order: dict):
    # Enriches transaction telemetry in New Relic
    newrelic.agent.add_custom_attribute("order_id", order["id"])
    newrelic.agent.add_custom_attribute("customer_tier", order.get("tier", "standard"))
    newrelic.agent.add_custom_attribute("cart_total", float(order["amount"]))
    return {"status": "processed"}
```

---

# 20. New Relic Infrastructure

### 20.1 Host-Level Telemetry Collection

The **New Relic Infrastructure Agent (`newrelic-infra`)** is a lightweight daemon written in Go that runs on Linux hosts, Kubernetes nodes, or Windows servers.
- Gathers hardware and OS metrics from `/proc`, `/sys`, and system APIs.
- Captures system inventory: package versions, kernel version, network interfaces, AWS instance metadata.
- Samples host metrics every 5–20 seconds into the `SystemSample`, `ProcessSample`, `NetworkSample`, and `StorageSample` events.

```yaml
# /etc/newrelic-infra.yml
license_key: <NEW_RELIC_LICENSE_KEY>
display_name: prod-k8s-worker-node-1
custom_attributes:
  environment: production
  availability_zone: us-east-1a
  role: kubernetes-worker
log_file: /var/log/newrelic-infra/newrelic-infra.log
```

---

# 21. New Relic Logs & Log Management

### 21.1 Connecting Logs with APM Traces (Logs in Context)

The ultimate superpower of an SRE during an outage is **Logs in Context**. When inspecting an error in New Relic APM or Distributed Tracing, you can click directly on a slow database query or HTTP 500 error and view the exact matching log lines printed by that specific container thread, linked by `trace.id` and `span.id`.

```python
# Enabling New Relic Log Decorating in Python
import logging
from newrelic.agent import NewRelicContextFormatter

logger = logging.getLogger()
handler = logging.StreamHandler()
# Formatter automatically injects trace.id, span.id, and entity.guid into every JSON log line
handler.setFormatter(NewRelicContextFormatter())
logger.addHandler(handler)
```

---

# 22. NRQL — Deep Dive & 50 Production Queries

NRQL (New Relic Query Language) is the SQL-flavored declarative query language used to extract telemetry from NRDB.

### Syntax Fundamentals
```sql
SELECT function(attribute) 
FROM EventType 
WHERE condition 
FACET grouping_attribute 
TIMESERIES 1 minute 
SINCE 1 day ago 
UNTIL now 
LIMIT 100 
COMPARE WITH 1 week ago
```

---

### Fifty Production NRQL Queries for SREs

#### Query 1: Top 10 APIs by p99 Latency
```sql
SELECT percentile(duration, 99) FROM Transaction WHERE appName = 'Payment-API' FACET name SINCE 3 hours ago LIMIT 10
```
- **Explanation**: Calculates 99th percentile execution time for each web transaction endpoint.
- **Expected Result**: Table listing the 10 slowest API routes and their p99 latency in seconds.
- **SRE Use Case**: Identifying worst-case tail latencies impacting high-value users.

#### Query 2: Endpoints Generating the Most 5xx Server Errors
```sql
SELECT count(*) FROM Transaction WHERE appName = 'Payment-API' AND httpResponseCode >= 500 FACET name, httpResponseCode SINCE 1 hour ago
```
- **Explanation**: Counts server errors grouped by transaction name and exact HTTP status.
- **Expected Result**: Table listing failing endpoints (e.g., `/api/v1/checkout -> 500`).
- **SRE Use Case**: Immediate triage during Sev-1 incidents to isolate failing backend handlers.

#### Query 3: Host CPU Saturation (Top Hosts Over 90%)
```sql
SELECT average(cpuPercent) FROM SystemSample FACET hostname SINCE 10 minutes ago WHERE cpuPercent > 90 ORDER BY average(cpuPercent) DESC LIMIT 20
```
- **Explanation**: Averages CPU utilization per host and filters for saturated nodes.
- **Expected Result**: List of EC2 hostnames experiencing sustained high CPU.
- **SRE Use Case**: Investigating host degradation and unbalanced load balancer traffic.

#### Query 4: Deployment Latency Impact (Compare with Yesterday)
```sql
SELECT average(duration) FROM Transaction WHERE appName = 'Order-Service' TIMESERIES 5 minutes SINCE 1 day ago COMPARE WITH 1 day ago
```
- **Explanation**: Plots response time today against the exact same time yesterday.
- **Expected Result**: Chart with two time-series lines showing divergence post-deployment.
- **SRE Use Case**: Instant post-deployment verification to detect performance regressions.

#### Query 5: Percentage of Overall Traffic Failing (Global Error Rate)
```sql
SELECT percentage(count(*), WHERE error IS true OR httpResponseCode >= 500) AS 'Failure Rate %' FROM Transaction WHERE appName = 'Frontend-Gateway' TIMESERIES 1 minute SINCE 30 minutes ago
```
- **Explanation**: Calculates the percentage of total requests that failed.
- **Expected Result**: Time-series chart of error rate percentage.
- **SRE Use Case**: Core SLI for availability monitoring and error budget consumption.

#### Query 6: Slowest External Third-Party API Calls
```sql
SELECT average(duration), percentile(duration, 95), count(*) FROM Span WHERE category = 'http' AND span.kind = 'client' FACET http.url SINCE 2 hours ago LIMIT 10
```
- **Explanation**: Analyzes outbound HTTP calls made by microservices to external APIs.
- **Expected Result**: Table showing latency and call volume for external SaaS providers (e.g., Stripe, Twilio).
- **SRE Use Case**: Determining whether an outage is caused by internal code or third-party vendor downtime.

#### Query 7: Slowest Database Queries by Total Wall-Clock Time
```sql
SELECT sum(duration), average(duration), count(*) FROM Span WHERE category = 'datastore' FACET db.statement SINCE 1 hour ago LIMIT 10
```
- **Explanation**: Calculates total time consumed across all executions of each SQL query.
- **Expected Result**: The top 10 SQL statements consuming database capacity.
- **SRE Use Case**: Isolating unindexed queries causing database CPU spikes.

#### Query 8: Out of Memory (OOMKilled) Containers in Kubernetes
```sql
SELECT count(*) FROM K8sContainerSample WHERE reason = 'OOMKilled' FACET containerName, podName, namespaceName SINCE 6 hours ago
```
- **Explanation**: Counts container terminations caused by memory limit breaches.
- **Expected Result**: List of OOMKilled containers with their pods and namespaces.
- **SRE Use Case**: Sizing Kubernetes memory requests and limits.

#### Query 9: High Apdex Dissatisfaction (Top Frustrated Endpoints)
```sql
SELECT apdex(duration, t: 0.25) FROM Transaction WHERE appName = 'Web-Store' FACET name SINCE 12 hours ago ORDER BY apdex(duration, t: 0.25) ASC LIMIT 10
```
- **Explanation**: Calculates Apdex score per endpoint with a 250ms satisfaction target.
- **Expected Result**: Endpoints with the lowest Apdex scores ($< 0.70$).
- **SRE Use Case**: Prioritizing software engineering optimization tickets.

#### Query 10: Real-Time Request Throughput (RPM) per Microservice
```sql
SELECT rate(count(*), 1 minute) AS 'RPM' FROM Transaction FACET appName TIMESERIES 1 minute SINCE 2 hours ago
```
- **Explanation**: Normalizes transaction volume to requests per minute across microservices.
- **Expected Result**: Stacked area chart showing service traffic distribution.
- **SRE Use Case**: Spotting sudden drops (upstream failure) or spikes (DDoS attack).

#### Query 11: Top Client IP Addresses Causing 4xx Rate Limits
```sql
SELECT count(*) FROM Transaction WHERE httpResponseCode = 429 FACET request.headers.xForwardedFor SINCE 1 hour ago LIMIT 15
```
- **Explanation**: Tracks client IPs encountering HTTP 429 Too Many Requests.
- **Expected Result**: List of offending IP addresses.
- **SRE Use Case**: Detecting rogue API consumers, scraping bots, or misconfigured clients.

#### Query 12: Host Memory Available Percentage
```sql
SELECT average(memoryAvailablePercent) FROM SystemSample FACET hostname TIMESERIES 5 minutes SINCE 6 hours ago
```
- **Explanation**: Monitors available physical RAM percentage over time.
- **Expected Result**: Line graph showing memory trajectory.
- **SRE Use Case**: Early detection of operating system memory leaks before OOM kicks in.

#### Query 13: Disk Inode Utilization Alert Query
```sql
SELECT latest(diskUsedPercent), latest(inodesUsedPercent) FROM StorageSample FACET hostname, mountPoint WHERE inodesUsedPercent > 80 SINCE 15 minutes ago
```
- **Explanation**: Reports disk mount points exceeding 80% inode capacity.
- **Expected Result**: Table of saturated filesystems.
- **SRE Use Case**: Catching inode exhaustion before servers freeze.

#### Query 14: Kubernetes Pod Restart Storms
```sql
SELECT diff(restartCount) FROM K8sPodSample FACET podName, namespaceName WHERE restartCount > 0 TIMESERIES 5 minutes SINCE 1 hour ago
```
- **Explanation**: Measures rapid changes in restart count across pods.
- **Expected Result**: Spike graph showing crashing workloads.
- **SRE Use Case**: Detecting cascading failure loops in Kubernetes.

#### Query 15: Error Traces Grouped by Exception Class
```sql
SELECT count(*) FROM TransactionError WHERE appName = 'Order-Service' FACET `error.class`, `error.message` SINCE 4 hours ago LIMIT 20
```
- **Explanation**: Aggregates stack traces by root Python exception type.
- **Expected Result**: Table showing breakdown of `ConnectionResetError`, `KeyError`, etc.
- **SRE Use Case**: Rapid triage of bugs introduced in new code deployments.

#### Query 16: Synthetics Monitor Availability Percentage (SLI)
```sql
SELECT percentage(count(*), WHERE result = 'SUCCESS') AS 'Synthetics SLI %' FROM SyntheticCheck FACET monitorName SINCE 30 days ago
```
- **Explanation**: Calculates monthly availability SLI based on external synthetic probes.
- **Expected Result**: Gauge showing 99.9x% compliance.
- **SRE Use Case**: Contractual SLA and SLO reporting to business leadership.

#### Query 17: Multi-Window Burn Rate Calculation (1-Hour Window)
```sql
SELECT (percentage(count(*), WHERE httpResponseCode >= 500) / 0.1) AS '1h Burn Rate' FROM Transaction WHERE appName = 'Payment-API' SINCE 1 hour ago
```
- **Explanation**: Calculates the current burn rate against a 99.9% SLO (error budget fraction = 0.1%).
- **Expected Result**: Single numerical burn rate value (e.g., 14.4).
- **SRE Use Case**: Multi-window multi-burn-rate alerting engine.

#### Query 18: Unhandled HTTP 504 Gateway Timeouts by ALB
```sql
SELECT count(*) FROM LoadBalancerSample WHERE targetResponseTime > 30.0 OR elbStatus = 504 FACET loadBalancerName TIMESERIES 1 minute SINCE 30 minutes ago
```
- **Explanation**: Tracks AWS ALB timeouts where upstream targets failed to respond.
- **Expected Result**: Spike chart during upstream server deadlocks.
- **SRE Use Case**: Correlating network reverse-proxy errors with application thread hangs.

#### Query 19: Database Connection Pool Saturation
```sql
SELECT average(custom.db.pool.active_connections), max(custom.db.pool.active_connections) FROM Metric WHERE appName = 'Billing-API' TIMESERIES 1 minute SINCE 1 hour ago
```
- **Explanation**: Monitors active database pool connections against pool capacity.
- **Expected Result**: Trend line reaching ceiling limit (e.g., 50 connections).
- **SRE Use Case**: Detecting database connection leaks and preventing pool exhaustion.

#### Query 20: Slowest Python Functions Profiled via Custom Spans
```sql
SELECT average(duration) FROM Span WHERE appName = 'Payment-API' AND name LIKE 'Custom/%' FACET name SINCE 2 hours ago LIMIT 10
```
- **Explanation**: Evaluates execution latency of manually instrumented Python helper methods.
- **Expected Result**: Top internal code bottlenecks.
- **SRE Use Case**: Code optimization and algorithmic performance tuning.

#### Query 21: Distribution of HTTP Status Codes
```sql
SELECT count(*) FROM Transaction WHERE appName = 'Payment-API' FACET httpResponseCode TIMESERIES 5 minutes SINCE 6 hours ago
```
- **Explanation**: Plots request distribution broken down by HTTP response code (200, 201, 400, 404, 500).
- **Expected Result**: Stacked bar or area chart.
- **SRE Use Case**: Baseline health monitoring.

#### Query 22: Network Dropped Packets on Host Interfaces
```sql
SELECT sum(receiveDroppedPerSecond), sum(transmitDroppedPerSecond) FROM NetworkSample FACET interfaceName, hostname SINCE 30 minutes ago
```
- **Explanation**: Detects network packet drops at the physical/virtual NIC layer.
- **Expected Result**: Alert table if dropped packets $> 0$.
- **SRE Use Case**: Troubleshooting intermittent network latency and packet loss.

#### Query 23: Top Customers Affected by Errors (High-Value User Triage)
```sql
SELECT count(*) FROM TransactionError WHERE customer_tier = 'enterprise' FACET customer_id, `error.message` SINCE 1 hour ago LIMIT 10
```
- **Explanation**: Filters errors impacting VIP enterprise customers using custom attributes.
- **Expected Result**: Table showing specific customer IDs affected by failures.
- **SRE Use Case**: Customer support escalation and incident severity boosting.

#### Query 24: Correlating High CPU with Specific API Endpoints
```sql
SELECT average(cpuPercent) FROM ProcessSample WHERE processDisplayName = 'python' FACET hostname TIMESERIES 1 minute SINCE 1 hour ago
```
- **Explanation**: Tracks Python runtime CPU usage across all EC2 nodes.
- **Expected Result**: Node-by-node CPU trajectory.
- **SRE Use Case**: Identifying single-node compute hotspots.

#### Query 25: SSL/TLS Handshake Duration Breakdown
```sql
SELECT percentile(durationBlocked, 95), percentile(durationConnect, 95), percentile(durationHandshake, 95) FROM SyntheticRequest SINCE 24 hours ago
```
- **Explanation**: Measures DNS lookup, TCP connect, and TLS handshake latency from external synthetics.
- **Expected Result**: Breakdown of connection phase overhead.
- **SRE Use Case**: Detecting CDN and TLS certificate performance degradation.

#### Query 26: AWS Lambda Cold Starts vs Warm Invocations
```sql
SELECT count(*) FROM ServerlessSample FACET coldStart SINCE 3 hours ago
```
- **Explanation**: Compares execution counts where `coldStart = true` vs `coldStart = false`.
- **Expected Result**: Pie chart of cold starts.
- **SRE Use Case**: Sizing provisioned concurrency for serverless APIs.

#### Query 27: Average Garbage Collection (GC) Pause Duration in Python/JVM
```sql
SELECT average(gcTime) FROM JvmGarbageCollectionSample TIMESERIES 5 minutes SINCE 6 hours ago
```
- **Explanation**: Tracks stop-the-world garbage collection pauses.
- **Expected Result**: Latency spikes corresponding to full GC sweeps.
- **SRE Use Case**: Eliminating tail latency spikes caused by memory churn.

#### Query 28: Kubernetes Pods Pending Scheduling
```sql
SELECT count(*) FROM K8sPodSample WHERE status = 'Pending' FACET namespaceName, podName SINCE 15 minutes ago
```
- **Explanation**: Alerts on unscheduled pods stuck in the pending state.
- **Expected Result**: List of starved pods.
- **SRE Use Case**: Capacity scaling and node pool exhaustion alerting.

#### Query 29: Slowest HTTP Methods (GET vs POST vs PUT)
```sql
SELECT average(duration), percentile(duration, 95) FROM Transaction WHERE appName = 'Order-API' FACET request.method SINCE 4 hours ago
```
- **Explanation**: Evaluates latency differences across HTTP verbs.
- **Expected Result**: Table comparing GET vs POST latency.
- **SRE Use Case**: Architectural performance auditing.

#### Query 30: Cache Hit vs Cache Miss Ratio (Redis/Memcached)
```sql
SELECT percentage(count(*), WHERE custom.cache.status = 'HIT') AS 'Cache Hit Rate %' FROM Transaction WHERE appName = 'Catalog-API' TIMESERIES 1 minute SINCE 2 hours ago
```
- **Explanation**: Tracks Redis caching efficiency.
- **Expected Result**: Line graph showing cache hit rate (target $> 95\%$).
- **SRE Use Case**: Catching cache evictions or cache stampedes before they hit the database.

#### Query 31: Endpoints with Highest Request Variance (Traffic Volatility)
```sql
SELECT stddev(duration), average(duration) FROM Transaction WHERE appName = 'Auth-Service' FACET name SINCE 6 hours ago LIMIT 10
```
- **Explanation**: Uses standard deviation to find endpoints with erratic, unstable response times.
- **Expected Result**: Endpoints with high performance instability.
- **SRE Use Case**: Stabilizing tail latency.

#### Query 32: Kubernetes Node Memory Working Set
```sql
SELECT latest(workingSetBytes) / latest(allocatableWorkingSetBytes) * 100 AS 'Memory Usage %' FROM K8sNodeSample FACET nodeName SINCE 10 minutes ago
```
- **Explanation**: Measures active working memory on Kubernetes nodes against allocatable capacity.
- **Expected Result**: Node memory utilization ranking.
- **SRE Use Case**: Node autoscaling and eviction prevention.

#### Query 33: Total Network Ingress/Egress Bandwidth (AWS Cost Driver)
```sql
SELECT sum(bytesReceivedPerSecond) / 1024 / 1024 AS 'Ingress MB/s', sum(bytesSentPerSecond) / 1024 / 1024 AS 'Egress MB/s' FROM NetworkSample TIMESERIES 5 minutes SINCE 1 day ago
```
- **Explanation**: Tracks aggregate network bandwidth across all nodes.
- **Expected Result**: Dual area graph showing network throughput.
- **SRE Use Case**: Network interface saturation detection and AWS egress cost tracking.

#### Query 34: Change Tracking: Deployments Recorded in the Past 7 Days
```sql
SELECT count(*) FROM Deployment FACET entity.name, description, user SINCE 7 days ago
```
- **Explanation**: Lists all deployment markers recorded across microservices.
- **Expected Result**: Audit log of code changes.
- **SRE Use Case**: Correlating newly surfaced errors with specific Git commit deployments.

#### Query 35: Top Slow SQL Transactions Grouped by Database Table
```sql
SELECT average(duration) FROM Span WHERE category = 'datastore' FACET db.collection SINCE 1 hour ago LIMIT 10
```
- **Explanation**: Analyzes which database tables account for the highest query latency.
- **Expected Result**: Table listing database tables (e.g., `audit_events`, `order_items`).
- **SRE Use Case**: Database schema optimization and partition planning.

#### Query 36: Ingested Log Volume by Microservice (Log Cost Optimization)
```sql
SELECT count(*) FROM Log FACET service.name TIMESERIES 1 hour SINCE 24 hours ago
```
- **Explanation**: Measures log line ingestion volume per service.
- **Expected Result**: Bar chart showing services generating excessive debug log spam.
- **SRE Use Case**: Controlling observability ingestion billing and enforcing log level standards.

#### Query 37: Correlating Error Rate with Host CPU
```sql
SELECT percentage(count(*), WHERE httpResponseCode >= 500) FROM Transaction TIMESERIES 1 minute SINCE 1 hour ago
```
- **SRE Use Case**: Placed directly adjacent to Host CPU widget on dashboards to verify compute-induced failures.

#### Query 38: HTTP 503 Service Unavailable Spikes (Under-Provisioning)
```sql
SELECT count(*) FROM Transaction WHERE httpResponseCode = 503 FACET appName TIMESERIES 1 minute SINCE 30 minutes ago
```
- **Explanation**: Tracks upstream microservices rejecting connections due to thread pool saturation.
- **Expected Result**: Spikes indicating insufficient worker replicas.
- **SRE Use Case**: Tuning HPA min-replicas.

#### Query 39: Average Payload Size (Bytes) of API Requests
```sql
SELECT average(request.headers.contentLength) / 1024 AS 'Avg Request KB', max(request.headers.contentLength) / 1024 AS 'Max Request KB' FROM Transaction WHERE appName = 'Upload-API' SINCE 2 hours ago
```
- **Explanation**: Monitors incoming HTTP payload sizes.
- **Expected Result**: Request size metrics.
- **SRE Use Case**: Detecting oversized payload attacks or bulk upload abuse.

#### Query 40: Distributed Traces with Highest Span Count (Architectural Complexity)
```sql
SELECT max(trace.spanCount), average(trace.spanCount) FROM Span FACET appName SINCE 6 hours ago
```
- **Explanation**: Evaluates microservice dependency graph depth.
- **Expected Result**: Services making dozens of synchronous RPC hops per transaction.
- **SRE Use Case**: Identifying distributed monolith anti-patterns.

#### Query 41: Top Errors During a Sev-1 Incident Window
```sql
SELECT count(*) FROM TransactionError WHERE appName = 'Payment-API' FACET `error.message` SINCE '2026-09-04 14:00:00' UNTIL '2026-09-04 14:45:00' LIMIT 10
```
- **Explanation**: Scopes error aggregation to the exact timeline of a production incident.
- **Expected Result**: Primary error messages responsible for the outage.
- **SRE Use Case**: Incident postmortem root cause analysis.

#### Query 42: Top Slowest Microservice RPC Calls (gRPC/HTTP)
```sql
SELECT percentile(duration, 95) FROM Span WHERE category = 'http' AND span.kind = 'client' FACET http.url SINCE 1 hour ago LIMIT 15
```
- **Explanation**: Uncovers internal microservice communication latency.
- **Expected Result**: Identification of the specific downstream internal service slowing the gateway.
- **SRE Use Case**: Eliminating cascading microservice slowdowns.

#### Query 43: Slowest Transactions by Operating System / Browser
```sql
SELECT percentile(duration, 95) FROM PageView FACET userAgentOS, userAgentName SINCE 1 day ago
```
- **Explanation**: Front-end real user monitoring (RUM) latency breakdown.
- **Expected Result**: Browser/OS compatibility bottlenecks.
- **SRE Use Case**: User experience optimization.

#### Query 44: Host Swap Space Usage Trend
```sql
SELECT latest(swapUsedBytes) / latest(swapTotalBytes) * 100 AS 'Swap Used %' FROM SystemSample FACET hostname WHERE swapTotalBytes > 0 SINCE 1 hour ago
```
- **Explanation**: Tracks systems actively consuming swap memory.
- **Expected Result**: Hosts with swap thrashing.
- **SRE Use Case**: Preventing performance degradation caused by disk swapping.

#### Query 45: Rate of Process Context Switches
```sql
SELECT average(contextSwitchesPerSecond) FROM SystemSample FACET hostname TIMESERIES 5 minutes SINCE 2 hours ago
```
- **Explanation**: Evaluates CPU context switching overhead.
- **Expected Result**: High context switches indicate excessive thread contention or syscall storms.
- **SRE Use Case**: Kernel and thread pool tuning.

#### Query 46: Kubernetes Workload CPU Limit vs Usage
```sql
SELECT latest(cpuUsedCores), latest(cpuLimitCores) FROM K8sContainerSample FACET containerName, podName SINCE 10 minutes ago
```
- **Explanation**: Compares actual core consumption against configured cgroup limits.
- **Expected Result**: Containers running perilously close to CPU limits.
- **SRE Use Case**: Preventing CPU throttling before latency degrades.

#### Query 47: Log Errors Grouped by Container Name
```sql
SELECT count(*) FROM Log WHERE level IN ('ERROR', 'FATAL', 'CRITICAL') FACET container_name, message SINCE 1 hour ago LIMIT 15
```
- **Explanation**: Centralized log search isolating high-severity log events by container.
- **Expected Result**: Actionable error summaries without logging into individual nodes.
- **SRE Use Case**: Rapid triage across thousands of ephemeral pods.

#### Query 48: HTTP 401 Unauthorized Spike (Authentication Outage)
```sql
SELECT count(*) FROM Transaction WHERE httpResponseCode = 401 FACET appName TIMESERIES 1 minute SINCE 30 minutes ago
```
- **Explanation**: Monitors unexpected spikes in authentication rejections.
- **Expected Result**: Identifies expired JWT signing keys or third-party OAuth provider outages.
- **SRE Use Case**: Catching authentication outages early.

#### Query 49: Database Transaction Rollback Rate
```sql
SELECT count(*) FROM DatastoreSample WHERE statementType = 'ROLLBACK' FACET databaseName SINCE 1 hour ago
```
- **Explanation**: Measures database transaction rollbacks.
- **Expected Result**: Rollback frequency graph.
- **SRE Use Case**: Detecting database deadlocks, unique constraint violations, and serialization failures.

#### Query 50: Golden Signals Summary Dashboard Query
```sql
SELECT rate(count(*), 1 minute) AS 'Throughput (RPM)', average(duration) * 1000 AS 'Latency (ms)', percentage(count(*), WHERE httpResponseCode >= 500) AS 'Error Rate %' FROM Transaction WHERE appName = 'Core-API' TIMESERIES 1 minute SINCE 1 hour ago
```
- **Explanation**: Computes three of the four Golden Signals (Traffic, Latency, Errors) in a single unified time-series query.
- **Expected Result**: Multi-line visualization giving an instantaneous health pulse of the entire microservice.
- **SRE Use Case**: The primary widget on every production executive and on-call dashboard.

---

# 23. New Relic Dashboards

### 23.1 The Golden Signals Dashboard Architecture
A production dashboard must never be a random dumping ground of 50 graphs. Follow Google’s **Four Golden Signals**:
1. **Latency**: The time it takes to service a request (p50, p95, p99).
2. **Traffic**: A measure of demand on your system (RPM, active users, I/O operations).
3. **Errors**: The rate of requests that fail (HTTP 5xx, unhandled exceptions, synthetic check failures).
4. **Saturation**: How full your service is (CPU, RAM, Disk I/O, DB connection pool headroom).

---

# 24. New Relic Alerting & Incident Workflows

### 24.1 The Alert Pipeline: Signal to Notification

```
[ Telemetry Signal ] (e.g., NRQL: Transaction Error Rate)
         |
         v
[ Alert Condition ] (Static: > 2% for 5m | Baseline Anomaly: 3 StdDev)
         |
         v (Condition Breached)
[ Incident Created ] (Correlates related violations to prevent alert storms)
         |
         v
[ Alert Policy ] (Defines incident roll-up: Per Condition vs Per Policy)
         |
         v
[ Workflow Engine ] (Applies filters, mutates payload, routes destinations)
         |
         v
[ Notification Destination ] (PagerDuty, Slack, SRE Remediation Webhook)
```

### 24.2 Baseline Anomaly Alerts vs Static Thresholds
- **Static Thresholds**: Excellent for deterministic failure conditions (e.g., Disk Space $> 90\%$, HTTP Status 500 $> 5\%$).
- **Baseline (Anomaly) Conditions**: Uses dynamic machine learning models that learn normal diurnal traffic patterns (e.g., Tuesday at 2:00 PM usually has 5,000 RPM; if today has 200 RPM, trigger alert even though error rate is zero!).

---

# 25. New Relic Synthetics

### 25.1 Scripted API Monitoring

Synthetics simulate real user journeys from global edge locations, validating availability before real customers are impacted:

```javascript
// New Relic Synthetics Scripted API Monitor (Node.js runtime)
const assert = require('assert');

// 1. Validate /health endpoint
$http.get('https://api.example.com/health', function (err, response, body) {
  assert.equal(response.statusCode, 200, 'Expected HTTP 200 OK from /health');
  const data = JSON.parse(body);
  assert.equal(data.status, 'alive', 'Expected status: alive');
});

// 2. Validate Authenticated POST /api/login
const options = {
  url: 'https://api.example.com/api/v1/login',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: $secure.SYNTHETIC_USER, password: $secure.SYNTHETIC_PASSWORD })
};

$http.post(options, function (err, response, body) {
  assert.equal(response.statusCode, 200, 'Login failed');
  const payload = JSON.parse(body);
  assert.ok(payload.token, 'Response missing JWT token');
});
```

---

# 26. New Relic Kubernetes Monitoring

### 26.1 End-to-End Cluster Observability

New Relic monitors the entire Kubernetes hierarchy seamlessly:
$$\text{Cluster} \longrightarrow \text{Worker Nodes} \longrightarrow \text{Namespaces} \longrightarrow \text{Deployments} \longrightarrow \text{Pods} \longrightarrow \text{Containers} \longrightarrow \text{APM Instrumented Apps}$$

Deployed via Helm:
```bash
helm repo add newrelic-helm https://helm-charts.newrelic.com
helm upgrade --install newrelic-bundle newrelic-helm/nri-bundle \
  --set global.licenseKey=<NEW_RELIC_LICENSE_KEY> \
  --set global.cluster=production-eks-cluster \
  --set infrastructure.enabled=true \
  --set k8s-agents.metrics.enabled=true \
  --set kubeEvents.enabled=true \
  --set logging.enabled=true \
  --namespace newrelic --create-namespace
```

---

# 27. New Relic APIs & NerdGraph (GraphQL)

### 27.1 NerdGraph Architecture
NerdGraph is New Relic's unified GraphQL API. It replaces fragmented REST endpoints with a single entry point (`https://api.newrelic.com/graphql`) supporting strongly-typed queries and mutations.

### 27.2 Python NerdGraph Client

```python
#!/usr/bin/env python3
"""
Python NerdGraph Client
Executes GraphQL queries against New Relic to fetch real-time telemetry.
"""
import httpx
import os
import json
from typing import Dict, Any

class NerdGraphClient:
    NERDGRAPH_URL = "https://api.newrelic.com/graphql"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "API-Key": self.api_key
        }

    def execute_query(self, query: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
        payload = {"query": query, "variables": variables or {}}
        with httpx.Client(timeout=15.0) as client:
            response = client.post(self.NERDGRAPH_URL, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            if "errors" in data:
                raise RuntimeError(f"GraphQL Query Failed: {data['errors']}")
            return data["data"]

    def query_nrql(self, account_id: int, nrql_statement: str) -> list:
        gql_query = """
        query($accountId: Int!, $nrql: Nrql!) {
          actor {
            account(id: $accountId) {
              nrql(query: $nrql) {
                results
              }
            }
          }
        }
        """
        variables = {"accountId": account_id, "nrql": nrql_statement}
        result = self.execute_query(gql_query, variables)
        return result["actor"]["account"]["nrql"]["results"]

if __name__ == "__main__":
    # Test client
    API_KEY = os.getenv("NEW_RELIC_API_KEY", "NRAK-MOCK-KEY")
    ACCOUNT_ID = int(os.getenv("NEW_RELIC_ACCOUNT_ID", "1234567"))
    client = NerdGraphClient(API_KEY)
    print("NerdGraph client initialized.")
```

---

# 28. Python + New Relic Autonomous Remediation Capstone

### 28.1 The Autonomous Self-Healing Architecture

```
+-------------------------------------------------------------+
|        Autonomous SRE Self-Healing Engine Architecture      |
+-------------------------------------------------------------+
| 1. New Relic Alert Condition Breached (Error Rate > 5%)     |
|                             |                               |
|                             v                               |
| 2. Webhook triggers Python Remediation Service              |
|                             |                               |
|                             v                               |
| 3. Python queries NerdGraph (NRQL: Error class, logs, spans)|
|                             |                               |
|                             v                               |
| 4. Correlates with Kubernetes pod memory & restarts         |
|                             |                               |
|                             v                               |
| 5. Evaluates Runbook Logic (Is Pod OOMing? Database locked?)|
|                             |                               |
|                             v                               |
| 6. Executes Guarded Action (Restart deployment / scale pod) |
|                             |                               |
|                             v                               |
| 7. Polls New Relic for 3 minutes to verify recovery         |
|                             |                               |
|                             v                               |
| 8. Publishes Post-Remediation Incident Report to Slack/Jira |
+-------------------------------------------------------------+
```

### 28.2 Complete Production Autonomous Remediation Script

```python
#!/usr/bin/env python3
"""
Production SRE Autonomous Remediation Daemon
Integrates with New Relic NerdGraph API to diagnose alerts,
trigger controlled Kubernetes remediation, verify recovery, and publish audit logs.
"""
import os
import sys
import time
import json
import logging
import httpx
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='{"time": "%(asctime)s", "level": "%(levelname)s", "msg": "%(message)s"}')
logger = logging.getLogger("sre_remediation")

class AutonomousRemediationEngine:
    def __init__(self, nr_api_key: str, nr_account_id: int, dry_run: bool = False):
        self.api_key = nr_api_key
        self.account_id = nr_account_id
        self.dry_run = dry_run
        self.nerdgraph_url = "https://api.newrelic.com/graphql"
        self.headers = {"Content-Type": "application/json", "API-Key": self.api_key}

    def query_nrql(self, statement: str) -> list:
        gql = """
        query($accountId: Int!, $nrql: Nrql!) {
          actor {
            account(id: $accountId) {
              nrql(query: $nrql) { results }
            }
          }
        }
        """
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(self.nerdgraph_url, headers=self.headers, json={"query": gql, "variables": {"accountId": self.account_id, "nrql": statement}})
            resp.raise_for_status()
            data = resp.json()
            return data.get("data", {}).get("actor", {}).get("account", {}).get("nrql", {}).get("results", [])

    def diagnose_alert(self, entity_name: str) -> Dict[str, Any]:
        logger.info(f"Diagnosing alert for entity: {entity_name}")
        
        # 1. Query error classes
        error_query = f"SELECT count(*) FROM TransactionError WHERE appName = '{entity_name}' FACET `error.class`, `error.message` SINCE 10 minutes ago LIMIT 3"
        errors = self.query_nrql(error_query)

        # 2. Query pod restarts and memory
        infra_query = f"SELECT latest(restartCount), latest(memoryWorkingSetBytes) / 1024 / 1024 AS 'MemoryMB' FROM K8sPodSample WHERE deploymentName = '{entity_name}' FACET podName SINCE 10 minutes ago LIMIT 5"
        infra_stats = self.query_nrql(infra_query)

        diagnosis = {
            "entity": entity_name,
            "root_cause_hypothesis": "UNKNOWN",
            "recommended_action": "NOOP",
            "evidence": {"errors": errors, "infra": infra_stats}
        }

        # Analyze errors
        for err in errors:
            err_class = err.get("error.class", "")
            if "MemoryError" in err_class or "OOM" in err_class:
                diagnosis["root_cause_hypothesis"] = "CONTAINER_OOM_EXHAUSTION"
                diagnosis["recommended_action"] = "SCALE_DEPLOYMENT_REPLICAS"
                return diagnosis
            elif "Deadlock" in err_class or "PoolTimeout" in err_class:
                diagnosis["root_cause_hypothesis"] = "DB_CONNECTION_EXHAUSTION"
                diagnosis["recommended_action"] = "ROLLING_RESTART"
                return diagnosis

        diagnosis["root_cause_hypothesis"] = "APPLICATION_CRASH_LOOP"
        diagnosis["recommended_action"] = "ROLLING_RESTART"
        return diagnosis

    def execute_remediation(self, diagnosis: Dict[str, Any]) -> bool:
        action = diagnosis["recommended_action"]
        entity = diagnosis["entity"]
        logger.info(f"Executing remediation: {action} for {entity} (Dry Run: {self.dry_run})")

        if self.dry_run:
            logger.info(f"[DRY RUN] Would execute: kubectl rollout restart deployment/{entity}")
            return True

        if action == "ROLLING_RESTART":
            import subprocess
            cmd = ["kubectl", "rollout", "restart", f"deployment/{entity}", "-n", "prod"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                logger.info(f"Successfully triggered rollout restart for {entity}")
                return True
            else:
                logger.error(f"Failed to restart deployment: {res.stderr}")
                return False
        return False

    def verify_recovery(self, entity_name: str, wait_seconds: int = 120) -> bool:
        logger.info(f"Waiting {wait_seconds}s before verifying recovery...")
        time.sleep(wait_seconds)
        
        # Verify error rate dropped below 1%
        verify_query = f"SELECT percentage(count(*), WHERE httpResponseCode >= 500) AS 'ErrorRate' FROM Transaction WHERE appName = '{entity_name}' SINCE 3 minutes ago"
        results = self.query_nrql(verify_query)
        
        if results and results[0].get("ErrorRate", 100.0) < 1.0:
            logger.info(f"RECOVERY VERIFIED: Error rate for {entity_name} is now < 1%. Incident resolved.")
            return True
        else:
            logger.critical(f"RECOVERY FAILED: {entity_name} error rate still elevated. Escalating to human SRE on-call!")
            return False

if __name__ == "__main__":
    API_KEY = os.getenv("NEW_RELIC_API_KEY", "NRAK-MOCK")
    ACCOUNT_ID = int(os.getenv("NEW_RELIC_ACCOUNT_ID", "1234567"))
    
    engine = AutonomousRemediationEngine(API_KEY, ACCOUNT_ID, dry_run=True)
    diag = engine.diagnose_alert("Payment-API")
    print(json.dumps(diag, indent=2))
    if engine.execute_remediation(diag):
        print("Remediation execution confirmed.")
```
'''
