"""
Curriculum Builder - Part 5: Sections 29 to 38
Prometheus/Grafana, OpenTelemetry, Incident Management,
30 Production SRE Troubleshooting Scenarios, Performance Engineering,
Capacity Planning, Distributed Systems, Security, GitOps, and AIOps/Agentic SRE
"""

def get_part5_content() -> str:
    return r'''# 29. Prometheus and Grafana

### 29.1 The Prometheus Architecture
Prometheus is an open-source, metrics-based monitoring and alerting system developed at SoundCloud. Unlike New Relic's push-based agent model, Prometheus primarily uses a **Pull-Based (Scraping)** architecture:

```
+-------------------------------------------------------------+
|                  Prometheus Architecture                    |
+-------------------------------------------------------------+
| Targets (Node Exporter, Apps, Blackbox) <-- /metrics HTTP   |
|                             ^                               |
|                             | (HTTP Scraping every 15s)     |
| [ Prometheus Server (Retrieval -> TSDB -> PromQL Engine) ]  |
|                             |                               |
|          +------------------+------------------+            |
|          |                                     |            |
|          v                                     v            |
|    [ Alertmanager ]                      [ Grafana ]        |
|  (Deduplicates & Pages)             (Visual Dashboards)     |
+-------------------------------------------------------------+
```

### 29.2 PromQL Deep Dive
```promql
# 1. Per-second rate of HTTP requests over 5-minute window
rate(http_requests_total{job="api", status="500"}[5m])

# 2. 99th Percentile Latency across API endpoints
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, handler))

# 3. Memory Usage Percentage on Linux Nodes
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

### 29.3 New Relic vs Prometheus + Grafana Comparison

| Dimension | New Relic (Telemetry Data Platform) | Prometheus + Grafana (Self-Hosted) |
| :--- | :--- | :--- |
| **Model** | Managed SaaS (Zero server management) | Self-Hosted Open Source (Requires operational upkeep) |
| **Telemetry** | Unified MELT (Metrics, Events, Logs, Traces) | Metrics only (Logs require Loki, Traces require Tempo) |
| **Cardinality** | High Cardinality natively supported in NRDB | High Cardinality causes memory exhaustion and crashes |
| **Retention** | Long-term retention out-of-the-box (Months/Years) | Requires Thanos, Cortex, or M3DB for long-term storage |
| **Cost** | Consumption-based pricing (per GB ingested) | Infrastructure compute/storage costs + SRE maintenance toil |
| **Best For** | Enterprise visibility, distributed tracing, speed | Edge environments, strict air-gapped data sovereignty |

---

# 30. OpenTelemetry (OTel)

### 30.1 Why OpenTelemetry is the Industry Standard
OpenTelemetry is an open-source observability framework hosted by the Cloud Native Computing Foundation (CNCF). It merges OpenTracing and OpenMetrics into a single unified specification, providing vendor-neutral APIs, SDKs, and tooling.

**The Golden Rule of SRE Telemetry**: *Instrument once with OpenTelemetry; export anywhere (New Relic, Prometheus, Datadog) by simply changing configuration, with zero code rewrites.*

```
+-------------------------------------------------------------+
|              OpenTelemetry Data Collection Flow             |
+-------------------------------------------------------------+
| Python App (FastAPI) Instrumented with OpenTelemetry SDK    |
|                             |                               |
|                             v (OTLP / gRPC on port 4317)    |
| [ OpenTelemetry Collector (Receiver -> Processors -> Exporters) ]
|                             |                               |
|                             v (OTLP over HTTPS)             |
| [ New Relic Telemetry Ingestion Endpoint ]                  |
+-------------------------------------------------------------+
```

### 30.2 Instrumenting a Python Application with OpenTelemetry

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# 1. Configure Resource Attributes
resource = Resource.create({"service.name": "payment-api", "environment": "production"})

# 2. Initialize Tracer Provider
provider = TracerProvider(resource=resource)

# 3. Export directly to OTel Collector or New Relic OTLP endpoint
otlp_exporter = OTLPSpanExporter(
    endpoint="otlp.nr-data.net:4317",
    headers=(("api-key", "<NEW_RELIC_LICENSE_KEY>"),)
)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("payment-api.core")

# 4. Instrumenting work
with tracer.start_as_current_span("process_payment") as span:
    span.set_attribute("payment.amount", 149.99)
    span.set_attribute("payment.currency", "USD")
    # Execute database and external calls
```

---

# 31. Production Incident Management

### 31.1 The Incident Lifecycle

```
[ DETECT ] -> [ TRIAGE & DECLARE ] -> [ MITIGATE ] -> [ RECOVER ] -> [ POSTMORTEM ] -> [ PREVENT ]
```

1. **Detect**: Alert fires from New Relic or customer reports an anomaly.
2. **Triage & Declare**: Assess business impact. If SLO is breaching, declare a Sev-1 incident immediately. Designate an **Incident Commander (IC)**.
3. **Mitigate**: Stop the bleeding! Roll back the deployment, route traffic to a secondary region, fail over the database, or shed non-essential load. *Never debug the root cause during an active outage if an immediate rollback is available!*
4. **Recover**: Confirm SLIs have returned to healthy baselines for at least 15 minutes.
5. **Postmortem**: Conduct a blameless post-incident review within 48 hours.
6. **Prevent**: Track corrective action items in Jira with high priority.

### 31.2 Incident Command System (ICS) Roles
- **Incident Commander (IC)**: Has sole decision-making authority. Manages the incident, assigns tasks, prevents chaos, and shields engineers from management inquiries.
- **Operations Lead**: Hands-on SRE executing diagnostics, rollbacks, and infrastructure fixes.
- **Communications Lead**: Updates internal stakeholders and posts customer-facing status updates (Statuspage) every 15–30 minutes.

---

# 32. Thirty Production SRE Troubleshooting Scenarios

Here are **30 detailed real-world production incident scenarios**, complete with symptoms, hypotheses, investigations, root causes, mitigations, fixes, prevention, and postmortems.

---

### Scenario 1: API Latency Increased Exponentially
- **Symptoms**: Customer checkout requests jump from $80\text{ ms}$ to $4,500\text{ ms}$.
- **Initial Hypothesis**: Database connection saturation or downstream microservice failure.
- **Investigation**:
  - *New Relic*: Distributed Tracing shows $90\%$ of the trace time spent in `auth-service.verify_token`.
  - *Linux*: Check auth host context switches and network drops: `vmstat 1 5`.
  - *Kubernetes*: `kubectl top pods -n auth` reveals auth pods pinned at 100% CPU.
  - *Python Tools*: Inspect request timeout settings in client wrapper.
- **Root Cause**: An upstream change bypassed Redis token caching, forcing every API call to execute expensive Argon2 password hashing on the database.
- **Mitigation**: Re-enable token caching in Redis and scale auth-service replicas from 5 to 25.
- **Permanent Fix**: Implement local in-memory LRU cache fallback in Python auth client.
- **Prevention**: Contractual latency SLI alert on internal auth microservice.

---

### Scenario 2: HTTP 500 Internal Server Errors Spike
- **Symptoms**: Error rate jumps from 0.01% to 18% immediately following deployment.
- **Investigation**:
  - *New Relic*: NRQL: `SELECT count(*) FROM TransactionError FACET error.message`. Shows `AttributeError: 'NoneType' object has no attribute 'get'`.
  - *Kubernetes*: Identify newly rolled out pod revision.
- **Root Cause**: A newly deployed frontend payload omitted the optional `billing_zip` field, causing an unhandled exception in the Python serializer.
- **Mitigation**: Immediate rollback: `kubectl rollout undo deployment/api`.
- **Permanent Fix**: Add schema validation using Pydantic with safe default values.
- **Prevention**: Automated end-to-end integration test suite in CI.

---

### Scenario 3: HTTP 502 Bad Gateway
- **Symptoms**: Nginx reverse proxy returns 502; users see "Bad Gateway".
- **Investigation**:
  - *Linux*: Nginx error log shows: `connect() failed (111: Connection refused) while connecting to upstream 127.0.0.1:8000`.
  - *Kubernetes*: `kubectl get pods` shows application container restarting with exit code 137.
- **Root Cause**: Gunicorn worker processes exceeded cgroup memory limits and were killed by the Linux OOM killer.
- **Mitigation**: Scale pod memory limit from 512Mi to 1Gi.
- **Permanent Fix**: Stream large database queries using Python cursor generators.

---

### Scenario 4: HTTP 503 Service Unavailable
- **Symptoms**: AWS ALB returns HTTP 503; error spikes on high traffic.
- **Investigation**:
  - *New Relic*: CloudWatch metric `HTTPCode_ELB_503_Count` increasing; healthy host count in Target Group dropping to zero.
  - *Kubernetes*: Pods fail readiness probe during peak traffic.
- **Root Cause**: Gunicorn had only 2 sync worker threads configured. Under 500 concurrent connections, all worker threads blocked, causing the `/ready` probe to time out.
- **Mitigation**: Switch Gunicorn worker class to `uvicorn.workers.UvicornWorker` and increase workers.
- **Prevention**: Load testing with Locust up to $3\times$ peak traffic.

---

### Scenario 5: HTTP 504 Gateway Timeout
- **Symptoms**: Client requests hang for 60 seconds, then fail with 504.
- **Investigation**:
  - *New Relic*: Transaction traces show requests stuck waiting for an external logistics partner API (`shipping.vendor.corp`).
- **Root Cause**: Python code used `requests.post()` without specifying a `timeout` argument. When the vendor hung, all Python threads hung.
- **Mitigation**: Set an immediate timeout in Nginx and restart backend workers.
- **Permanent Fix**: Wrap outbound HTTP calls in Python with `timeout=3.0` and a Circuit Breaker.

---

### Scenario 6: Database Latency Spikes to 10 Seconds
- **Symptoms**: All read operations experience extreme delays.
- **Investigation**:
  - *New Relic*: NRQL datastore query reveals full table scan on `orders` table.
  - *Linux*: Database server disk IOPS at 100% saturation: `iostat -xz 1`.
- **Root Cause**: A developer added a filter on `created_at` without creating a database B-Tree index.
- **Mitigation**: Cancel runaway long-running queries via `pg_terminate_backend()`.
- **Permanent Fix**: Apply database migration: `CREATE INDEX CONCURRENTLY idx_orders_created_at`.

---

### Scenario 7: Kubernetes Pods Continuously Restarting
- **Symptoms**: Pods cycle through `Running -> Error -> CrashLoopBackOff`.
- **Investigation**:
  - *Kubernetes*: `kubectl logs <pod> --previous` reveals `FileNotFoundError: /etc/secrets/jwt.key`.
- **Root Cause**: A Kubernetes Secret was accidentally deleted during a Helm release upgrade.
- **Mitigation**: Restore the Secret from HashiCorp Vault.
- **Prevention**: Use GitOps with Argo CD to prevent manual in-cluster deletions.

---

### Scenario 8: Slow Memory Leak Over Several Days
- **Symptoms**: Memory usage climbs monotonically from 20% to 95% over 72 hours until host freezes.
- **Investigation**:
  - *Python Profiling*: Run `tracemalloc` snapshots comparing memory allocations between day 1 and day 3.
- **Root Cause**: A global Python list was appending user telemetry objects on every request without an eviction policy.
- **Mitigation**: Perform a graceful rolling restart of the pods.
- **Permanent Fix**: Replace unbounded global list with `collections.deque(maxlen=1000)`.

---

### Scenario 9: Sudden CPU Spike to 100%
- **Symptoms**: Node CPU hits 100%; SSH sessions hang.
- **Investigation**:
  - *Linux*: `top -H` and `perf top` reveal 95% CPU time spent in Python regex evaluation `re.match()`.
- **Root Cause**: Catastrophic Regular Expression Backtracking (ReDoS) triggered by a malicious payload sent to an unanchored regex pattern.
- **Mitigation**: Block malicious request payload at the Cloudflare WAF.
- **Permanent Fix**: Replace complex regex with Google's `re2` library (guaranteed linear time).

---

### Scenario 10: Disk Full (No Space Left on Device)
- **Symptoms**: Database writes fail; services crash.
- **Investigation**:
  - *Linux*: `df -h` shows `/var/log` at 100%. `du -sh /var/log/*` shows `nginx/access.log` is 90GB.
- **Root Cause**: Logrotate daemon failed due to a syntax error in `/etc/logrotate.d/nginx`.
- **Mitigation**: Truncate log file safely: `: > /var/log/nginx/access.log`.
- **Permanent Fix**: Repair logrotate syntax and set up New Relic Storage alerts at 80% capacity.

---

### Scenario 11: Internal DNS Resolution Failure
- **Symptoms**: All microservices log `getaddrinfo failed`.
- **Investigation**:
  - *Kubernetes*: `kubectl get pods -n kube-system -l k8s-app=kube-dns` shows CoreDNS pods in `CrashLoopBackOff`.
- **Root Cause**: CoreDNS ran out of memory after a cluster expansion increased DNS query volume.
- **Mitigation**: Increase CoreDNS memory limit from 170Mi to 500Mi.
- **Permanent Fix**: Deploy NodeLocal DNSCache DaemonSet on all worker nodes.

---

### Scenario 12: TLS Certificate Validation Failure
- **Symptoms**: API clients fail with `SSL: CERTIFICATE_VERIFY_FAILED`.
- **Investigation**:
  - *Networking*: `openssl s_client -connect api.corp.com:443` shows certificate expired 10 minutes ago.
- **Root Cause**: The automated `cert-manager` Let's Encrypt renewal CronJob failed because DNS-01 challenge credentials had expired.
- **Mitigation**: Manually issue emergency certificate via AWS Certificate Manager (ACM).
- **Prevention**: Alert on certificate expiration 30 days, 14 days, and 7 days prior.

---

### Scenario 13: Faulty Deployment Causes Outage
- **Symptoms**: Error rate increases from 0% to 100% on specific payment route immediately after CI/CD push.
- **Mitigation**: Immediate rollback via `kubectl rollout undo deployment/payments`.
- **Postmortem**: The PR lacked unit tests for legacy payment methods. Enforce test coverage $> 85\%$ in CI gate.

---

### Scenario 14: Third-Party External API Outage
- **Symptoms**: Payment processing fails for all credit cards.
- **Investigation**:
  - *New Relic*: External service dashboard shows Stripe API returning HTTP 500.
- **Mitigation**: Enable graceful degradation: route users to alternative payment processor (PayPal) via dynamic feature flag.
- **Prevention**: Multi-vendor payment routing architecture.

---

### Scenario 15: SQS Queue Backlog Accumulation
- **Symptoms**: `ApproximateNumberOfMessagesVisible` climbs from 100 to 500,000.
- **Investigation**:
  - *New Relic*: Worker service throughput dropped to zero. Worker logs reveal: `Deadlock detected on database update`.
- **Root Cause**: Multiple workers attempted to lock identical customer rows concurrently.
- **Mitigation**: Scale worker pods down to 1 temporarily to eliminate concurrency deadlock while draining queue.
- **Permanent Fix**: Implement optimistic locking with retries and random jitter.

---

### Scenario 16: Message Processing Delayed
- **Symptoms**: Customers report order confirmation emails arriving 4 hours late.
- **Investigation**:
  - *AWS SQS*: Message age metric `ApproximateAgeOfOldestMessage` reached 14,400 seconds.
- **Root Cause**: A batch of malformed poison-pill messages caused worker crashes, consuming the visibility timeout repeatedly.
- **Fix**: Configure a Dead-Letter Queue (DLQ) with `maxReceiveCount = 3`.

---

### Scenario 17: Worker Node Hardware Failure
- **Symptoms**: AWS emits `StatusCheckFailed_System` alert on EC2 instance.
- **Investigation**:
  - *Kubernetes*: Node transitions to `NotReady`. Pods stuck in `Terminating`.
- **Mitigation**: Force delete stuck pods (`kubectl delete pod <name> --force --grace-period=0`) so they reschedule on healthy nodes.
- **Permanent Fix**: Enable AWS Auto Scaling Group automatic instance replacement.

---

### Scenario 18: Intermittent Network Packet Loss
- **Symptoms**: Intermittent 5-second latency spikes between VPC subnets.
- **Investigation**:
  - *Linux*: `netstat -s | grep retransmitted` shows massive TCP retransmissions.
- **Root Cause**: AWS NAT Gateway bandwidth reached the maximum 45 Gbps limit.
- **Fix**: Provision secondary NAT Gateway and balance subnets across AZs.

---

### Scenario 19: Load Balancer Health Check Flapping
- **Symptoms**: Pods continuously cycle in and out of ALB Target Group.
- **Root Cause**: Health check path `/health` executed an expensive deep check (database + redis + s3). Under load, health check took $> 5\text{ s}$, exceeding the ALB timeout.
- **Fix**: Separate deep checks into `/ready` and keep `/health` as a shallow, lightweight in-memory probe.

---

### Scenario 20: Sudden Traffic Spike (10x Flash Sale)
- **Symptoms**: Incoming traffic jumps from 2,000 RPM to 25,000 RPM in 30 seconds.
- **Mitigation**: Trigger manual emergency HPA scale-up: `kubectl scale deployment/api --replicas=50`.
- **Permanent Fix**: Implement predictive auto-scaling and pre-warming of load balancers before scheduled events.

---

### Scenario 21: Sudden Traffic Drop (Upstream Partition)
- **Symptoms**: Traffic unexpectedly drops to near zero without internal errors.
- **Investigation**:
  - *DNS*: Query Route 53 status; check CDN edge status.
- **Root Cause**: Cloudflare CDN edge rule was accidentally misconfigured to block all user traffic with a CAPTCHA.
- **Mitigation**: Revert Cloudflare WAF rule immediately.

---

### Scenario 22: Authentication Failure Storm
- **Symptoms**: HTTP 401 Unauthorized errors surge to 40% of all requests.
- **Root Cause**: The public key used to verify RS256 JWT tokens rotated, but the API cache did not invalidate the stale key.
- **Fix**: Flush JWT public key cache in API memory.

---

### Scenario 23: Slow Database Query Saturation
- **Symptoms**: Database CPU hits 100%; all queries back up.
- **Investigation**:
  - *PostgreSQL*: `SELECT pid, query, now() - query_start AS duration FROM pg_stat_activity WHERE state = 'active' ORDER BY duration DESC;`
- **Mitigation**: Terminate offending query PID via `SELECT pg_cancel_backend(<PID>);`.

---

### Scenario 24: Database Connection Pool Exhaustion
- **Symptoms**: Python logs `psycopg2.OperationalError: FATAL: remaining connection slots are reserved for non-replication superuser connections`.
- **Root Cause**: Pods autoscaled from 10 to 100, each opening 20 direct connections ($100 \times 20 = 2,000$ connections), exceeding Postgres `max_connections = 500`.
- **Fix**: Deploy **PgBouncer** connection pooler in transaction pooling mode between Kubernetes and Postgres.

---

### Scenario 25: Container OOM Killed in Kubernetes
- **Symptoms**: Container exits with code 137.
- **Fix**: Profile memory allocations; adjust Kubernetes container memory limits based on p99 utilization metrics in New Relic.

---

### Scenario 26: Application Deadlock
- **Symptoms**: Service stops accepting requests; CPU drops to 0%; all worker threads in `D` or `S` state.
- **Investigation**:
  - *Python*: Generate thread stack dump using `py-spy dump --pid <PID>`.
- **Root Cause**: Thread 1 acquired Lock A and waited for Lock B; Thread 2 acquired Lock B and waited for Lock A.
- **Fix**: Enforce strict lock acquisition ordering and lock timeouts (`lock.acquire(timeout=5.0)`).

---

### Scenario 27: Certificate Expiration Outage
- **Symptoms**: Mobile app users completely locked out due to expired SSL cert.
- **Fix**: Issue emergency renewal via automated Let's Encrypt / ACM pipeline; add automated monitoring alerting 30 days prior.

---

### Scenario 28: Alert Storm Overwhelming On-Call SRE
- **Symptoms**: On-call engineer receives 450 PagerDuty pages in 10 minutes.
- **Root Cause**: Alerts were configured per-server rather than per-service; downstream services alerted when the single shared database went down.
- **Fix**: Configure New Relic Incident Intelligence to group correlated alerts into a single incident; configure alert dependencies.

---

### Scenario 29: Monitoring Blind Spot (Silent Failure)
- **Symptoms**: Customer support reports checkout has been broken for 6 hours, but zero SRE alerts fired.
- **Root Cause**: The API returned HTTP 200 OK with JSON payload `{"status": "error", "message": "Failed"}`. Synthetic check only verified HTTP 200!
- **Fix**: Update New Relic Synthetics to assert on JSON response body: `assert.equal(data.status, "success")`.

---

### Scenario 30: Partial Cloud Regional Outage
- **Symptoms**: AWS `us-east-1` Availability Zone `us-east-1a` suffers power loss.
- **Investigation**:
  - *AWS Health Dashboard*: Confirms impaired EC2/EBS infrastructure in AZ `use1-az1`.
- **Mitigation**: Update Route 53 or ALB target groups to remove `us-east-1a` subnets; scale worker nodes in `us-east-1b` and `us-east-1c`.
- **Postmortem**: Ensure all Kubernetes Deployments enforce `podTopologySpreadConstraints` across AZs.

---

# 33. Performance Engineering & Load Testing

### 33.1 Profiling Python Services in Production with `py-spy`
Traditional profilers (`cProfile`) inject severe overhead, slowing execution by $300\%$. **`py-spy`** is a sampling profiler written in Rust that inspects the Python call stack from outside the process with zero performance degradation:

```bash
# Generate real-time interactive flamegraph of a running Python process
py-spy record -o profile_flamegraph.svg --pid <PID> --duration 60

# Live top-like view of Python functions
py-spy top --pid <PID>
```

### 33.2 High-Scale Distributed Load Testing with Locust

```python
# locustfile.py
from locust import HttpUser, task, between
import random

class HighScaleAPIUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(10)
    def browse_catalog(self):
        self.client.get("/api/v1/products", name="/api/v1/products")

    @task(2)
    def checkout_flow(self):
        order_payload = {"item_id": random.randint(1, 5000), "quantity": 1}
        headers = {"X-Correlation-ID": "load-test-sim"}
        with self.client.post("/api/v1/checkout", json=order_payload, headers=headers, catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Failed checkout: {resp.text}")
```
- **Execution**: `locust -f locustfile.py --headless -u 1000 -r 50 --run-time 10m --host https://staging.api.example.com`

---

# 34. Capacity Planning & Traffic Forecasting

### 34.1 The Mathematics of Capacity & Redundancy

#### $N+1$ and $N+2$ Redundancy
- **$N$**: Minimum number of compute units required to handle peak traffic.
- **$N+1$**: Cluster can survive the simultaneous loss of 1 node without degrading performance or dropping traffic.
- **$N+2$**: Cluster can survive the loss of 1 node during an active rolling deployment (which takes down a second node).

#### Numerical Capacity Planning Exercise
**Problem:**
Your payment API experiences peak traffic of $12,000$ requests per second (RPS).
A single pod instance running on Kubernetes can comfortably process $400$ RPS at $65\%$ CPU utilization (our SLO headroom ceiling).
1. Calculate the minimum baseline pods ($N$) required for peak load.
2. Calculate the pods required for $N+2$ availability.
3. If each worker node in EKS can host a maximum of 8 payment pods, how many EC2 worker nodes are required for $N+1$ node resilience?

**Solution:**
1. Baseline pod requirement ($N$):
   $$N = \frac{12,000\text{ RPS}}{400\text{ RPS/pod}} = 30\text{ pods}$$
2. $N+2$ pod requirement:
   $$N_{\text{pods}} = 30 + 2 = 32\text{ pods}$$
3. Node calculation:
   Each node hosts 8 pods.
   $$\text{Nodes needed} = \lceil \frac{32}{8} \rceil = 4\text{ nodes}$$
   For $N+1$ node resilience, if 1 entire physical node crashes, the remaining nodes must host all 32 pods:
   $$\text{Total Resilient Nodes} = 4 + 1 = 5\text{ nodes}$$

---

# 35. Distributed Systems Reliability

### 35.1 The CAP & PACELC Theorems
- **CAP Theorem**: In any asynchronous network subject to partitions ($P$), a distributed datastore can guarantee at most Consistency ($C$) or Availability ($A$), but not both.
- **PACELC Theorem**: If there is a Partition ($P$), trade off Availability ($A$) versus Consistency ($C$); Else ($E$), trade off Latency ($L$) versus Consistency ($C$).

### 35.2 The Core Four Resiliency Patterns
Whenever a distributed system makes a remote call across a network, it must combine:
$$\text{Timeout} + \text{Exponential Backoff with Jitter} + \text{Circuit Breaker} + \text{Idempotency}$$

```python
# Production Circuit Breaker Implementation in Python
import time
import logging

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout_sec: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout_sec
        self.failure_count = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
        self.last_state_change = time.monotonic()

    def call(self, func, *args, **kwargs):
        now = time.monotonic()
        
        # Check if circuit should transition from OPEN to HALF-OPEN
        if self.state == "OPEN":
            if now - self.last_state_change > self.recovery_timeout:
                logging.info("[CIRCUIT BREAKER] Transitioning from OPEN to HALF-OPEN trial")
                self.state = "HALF-OPEN"
            else:
                raise CircuitBreakerOpenException("Circuit is OPEN. Fast-failing request.")

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF-OPEN":
                logging.info("[CIRCUIT BREAKER] Trial succeeded. Closing circuit.")
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as exc:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.last_state_change = time.monotonic()
                logging.error(f"[CIRCUIT BREAKER] Breached threshold ({self.failure_count}). Circuit is now OPEN.")
            raise exc
```

---

# 36. Security Engineering for SRE

### 36.1 Security Best Practices in Infrastructure
1. **Principle of Least Privilege (PoLP)**: IAM roles and Kubernetes ServiceAccounts must have permissions restricted strictly to required actions and resources.
2. **Container Security**:
   - Run containers as non-root user (`USER 10001:10001`).
   - Use read-only root filesystems (`readOnlyRootFilesystem: true`).
   - Drop all Linux capabilities: `capabilities: { drop: ["ALL"] }`.
3. **Vulnerability Scanning**: Automated container image scanning in CI with **Trivy** to block images containing critical CVEs.

---

# 37. GitOps with Argo CD

### 37.1 Declarative Operations
GitOps treats a Git repository as the single source of truth for infrastructure and application state.
- **Argo CD** runs inside the Kubernetes cluster as an autonomous controller.
- Continuously compares the **Desired State** in Git against the **Live State** in the cluster.
- If an engineer manually tampers with production via `kubectl edit`, Argo CD detects the configuration drift and immediately reconciles it back to the Git definition!

```yaml
# Argo CD Application Manifest
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-api-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/corp/sre-gitops-manifests.git'
    targetRevision: main
    path: apps/payment-api/production
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

# 38. AIOps and Agentic SRE

### 38.1 The Rise of Autonomous and Agentic Operations

Agentic SRE utilizes Large Language Models (LLMs) paired with strongly-typed API tool-calling (New Relic NerdGraph, Kubernetes API, AWS SDK) to execute automated incident triage, root cause analysis, and guided remediation.

```
                 New Relic
                     |
                     ↓
                  Alert
                     |
                     ↓
               Python Agent
                     |
          +----------+----------+
          |                     |
          ↓                     ↓
       Analyze              Runbooks
          |                     |
          +----------+----------+
                     ↓
              Recommended Action
                     ↓
               Human Approval
                     ↓
                Remediation
                     ↓
              Recovery Check
```

### 38.2 Autonomous Agent Guardrails & Principles
Autonomous remediation must adhere to strict production safety guardrails:
1. **Never allow destructive unconstrained execution**: The agent must choose from a strictly audited whitelist of deterministic actions (`RESTART_POD`, `SCALE_REPLICAS`, `FLUSH_REDIS_KEY`).
2. **Rate Limits & Cooldowns**: Maximum 1 remediation attempt per service per hour.
3. **Human-in-the-Loop (HITL)**: For destructive operations (e.g., database failovers or traffic routing changes), require explicit Slack interactive approval button click before execution.
4. **Post-Action Verification**: The agent must verify telemetry recovery; if error rates do not drop within 3 minutes, roll back immediately and page human on-call!
'''
