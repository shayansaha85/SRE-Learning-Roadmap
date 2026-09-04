"""
Curriculum Builder - Part 8: Sections 43 to 50
SRE System Design (10 Architectures with Mermaid), Production Checklists,
Learning Exercises with Solutions, Knowledge Checks, Final Enterprise Capstone,
Tool Matrix, Skill Assessment Framework, and 14-Phase Final Roadmap
"""

def get_part8_content() -> str:
    return r'''# 43. SRE System Design (10 Enterprise Architectures)

This section details 10 enterprise system designs tailored for high-scale reliability, with complete architecture flows, failure domain analysis, and trade-offs.

---

### System Design 1: Enterprise Monitoring Platform

```mermaid
graph TD
    A[Worker Nodes / Containers] -->|Push Metrics / Telemetry| B[OpenTelemetry Collector DaemonSet]
    B -->|Batch / Filter / OTLP| C[New Relic Telemetry Data Platform]
    B -->|Fallback / Edge| D[Prometheus Server]
    C -->|NRQL Aggregations| E[SRE Executive Dashboards]
    C -->|Continuous Evaluation| F[New Relic Alerting Engine]
    F -->|Webhook Trigger| G[SRE Python Automation Engine]
    F -->|Escalation| H[PagerDuty / Slack]
```

- **Architecture Walkthrough**: Every Kubernetes node runs an OpenTelemetry Collector as a DaemonSet. The collector batches and scrubs high-cardinality telemetry before exporting over encrypted OTLP to New Relic's Telemetry Data Platform.
- **Resilience Design**: If the external SaaS network partition occurs, the OTel collector buffers metrics locally in memory up to 500MB, preventing telemetry loss.

---

### System Design 2: High-Throughput Centralized Logging Platform

```mermaid
graph LR
    Apps[Microservice Pods] -->|JSON stdout/stderr| DockerLog[/var/log/pods/*.log]
    DockerLog -->|Tail & Parse| Fluentbit[Fluent Bit DaemonSet]
    Fluentbit -->|Enrich with K8s Metadata| Fluentbit
    Fluentbit -->|HTTPS Chunked Transfer| NRLogs[New Relic Logs Engine]
    NRLogs -->|Logs in Context Link| APMTraces[New Relic APM Traces]
```

- **SRE Key Consideration**: Multi-stage parsing via Fluent Bit strips sensitive PII (passwords, credit card numbers) at the node layer before transmission, ensuring PCI-DSS compliance.

---

### System Design 3: Global Distributed Tracing Platform

```mermaid
graph TD
    Client[Web / Mobile Client] -->|W3C traceparent| Gateway[Envoy API Gateway]
    Gateway -->|Inject Span| ServiceA[Order Microservice]
    ServiceA -->|Propagate Context| ServiceB[Payment Microservice]
    ServiceB -->|Async Message + Trace ID| SQS[AWS SQS Queue]
    SQS -->|Consume Context| Worker[Async Fulfillment Worker]
    ServiceA -.->|Export Spans| OTel[OTel Collector]
    ServiceB -.->|Export Spans| OTel
    Worker -.->|Export Spans| OTel
    OTel -->|OTLP| NewRelic[New Relic Distributed Tracing]
```

---

### System Design 4: Global Synthetic Health-Check System
- Multi-location synthetic probes (Dublin, Virginia, Tokyo, Sydney) issue real HTTP requests every 60 seconds.
- Probes evaluate SSL validity, DNS resolution latency, HTTP status, and assert on JSON response schema.

---

### System Design 5: Multi-Tier Alerting & Notification System
- Signal deduplication, correlation of downstream dependency failures into parent incidents, and notification routing to Slack, PagerDuty, and remediation webhooks.

---

### System Design 6: Incident Management System
- Automated declaration flow: New Relic alert -> Slack incident channel creation -> PagerDuty rotation page -> Zoom bridge provisioning -> Jira postmortem ticket creation.

---

### System Design 7: Autonomous Self-Healing System
- Closed-loop control: Alert webhook -> Python diagnosis engine -> NerdGraph root-cause analysis -> safe remediation execution -> 3-minute recovery verification.

---

### System Design 8: Large-Scale API Platform (100,000 RPS)
- Edge Route 53 latency routing -> CloudFront CDN -> AWS Application Load Balancers -> EKS Pods with HPA -> PgBouncer connection pooling -> Amazon Aurora Multi-AZ.

---

### System Design 9: Metrics Ingestion Pipeline (Petabyte Scale)
- High-throughput Kafka ingestion buffer -> stream processing workers -> columnar storage engine with automated rollup aggregation.

---

### System Design 10: Python-Based SRE Automation Platform
- Asynchronous Celery / FastAPI task engine executing audited, declarative operational runbooks across cloud infrastructure.

---

# 44. Production Verification Checklists

### Checklist 1: Before Deployment
- [ ] Code passed all unit tests and static type checking (`ruff check`, `mypy --strict`, `pytest`).
- [ ] Container image scanned for CVEs via Trivy; zero CRITICAL or HIGH vulnerabilities.
- [ ] Database migration is backward-compatible (expand-and-contract pattern applied).
- [ ] Application contains liveness and readiness probes.
- [ ] Resource requests and limits configured for CPU and Memory.
- [ ] Secret credentials managed via HashiCorp Vault or AWS Secrets Manager (zero plaintext tokens in Git).
- [ ] Rollback strategy verified and documented in runbook.

### Checklist 2: During Deployment
- [ ] Canary deployment initialized (10% traffic routed to new revision).
- [ ] Monitor real-time error rate in New Relic APM via NRQL.
- [ ] Monitor p99 latency in New Relic: verify no degradation $> 10\%$.
- [ ] Record New Relic Deployment Marker via NerdGraph GraphQL API.
- [ ] Inspect pod rollout status: `kubectl rollout status deployment/<app>`.

### Checklist 3: After Deployment
- [ ] Verify error budget consumption has not accelerated (Burn Rate $< 1.0$).
- [ ] Synthetic monitors confirm all critical business journeys are passing globally.
- [ ] Host and pod memory utilization stable; no monotonic memory leak trend.
- [ ] Old ReplicaSets scaled down cleanly with zero orphaned pods.

### Checklist 4: Incident Response Checklist
- [ ] Acknowledge PagerDuty page within 5 minutes.
- [ ] Join Incident War Room and establish Incident Commander (IC).
- [ ] Post initial internal communication: "Investigating Sev-1 incident on Payment API."
- [ ] Focus strictly on **mitigating impact** (rollback, traffic rerouting) before debugging root cause.
- [ ] Post public status update on Statuspage within 15 minutes.
- [ ] Confirm service recovery: all SLIs normal for at least 15 consecutive minutes.

### Checklist 5: Postmortem Checklist
- [ ] Schedule blameless postmortem meeting within 48 hours.
- [ ] Construct comprehensive chronological timeline with timestamps.
- [ ] Identify root causes using Five Whys methodology.
- [ ] Assign action items with designated owners and due dates.
- [ ] Publish postmortem document to engineering organization.

### Checklist 6: Kubernetes Troubleshooting Checklist
- [ ] Inspect pod status and restart count: `kubectl get pods -n <ns>`.
- [ ] Describe failing pod: `kubectl describe pod <pod> -n <ns>`.
- [ ] Inspect prior crash logs: `kubectl logs <pod> -n <ns> --previous`.
- [ ] Check node capacity and conditions: `kubectl describe node <node>`.
- [ ] Verify Service Endpoints: `kubectl get endpoints <service>`.

### Checklist 7: New Relic Setup Checklist
- [ ] Install New Relic APM Python agent in virtual environment / container.
- [ ] Configure `newrelic.ini` with correct license key and meaningful `app_name`.
- [ ] Deploy New Relic Infrastructure agent on all worker nodes.
- [ ] Deploy New Relic Kubernetes integration via Helm (`nri-bundle`).
- [ ] Configure Logs in Context with `NewRelicContextFormatter`.

### Checklist 8: New Relic Alert Review Checklist
- [ ] Alerts configured for SLO error budget burn rate over short and long windows.
- [ ] Apdex dissatisfaction alerts configured with realistic threshold $T$.
- [ ] Synthetics monitors configured for all Tier-1 customer journeys.
- [ ] Notification workflows routed to on-call PagerDuty schedules.

### Checklist 9: Application Onboarding Checklist
- [ ] Centralized structured JSON logging configured.
- [ ] Distributed tracing W3C headers propagated across all outbound calls.
- [ ] Service Level Objectives (SLOs) defined and published.
- [ ] Runbook link documented in New Relic alert condition metadata.

### Checklist 10: Production Readiness Checklist
- [ ] Architecture has zero single points of failure (multi-AZ compute, storage, and networking).
- [ ] Auto-scaling configured (HPA for pods, ASG for nodes).
- [ ] Backups automated, encrypted, and test-restored successfully.
- [ ] Disaster recovery RTO (Recovery Time Objective) and RPO (Recovery Point Objective) tested.

---

# 45. Comprehensive Learning Exercises

### Beginner Exercises
1. **Exercise**: Write a Python script using `os` and `pathlib` that lists all files in `/var/log` larger than 100MB.
   - *Solution*:
     ```python
     from pathlib import Path
     for p in Path("/var/log").glob("**/*"):
         if p.is_file() and p.stat().st_size > 100 * 1024 * 1024:
             print(f"{p}: {p.stat().st_size / (1024**2):.2f} MB")
     ```
2. **Exercise**: Write a Linux one-liner to count the top 5 most frequent client IP addresses in Nginx `access.log`.
   - *Solution*: `awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -n 5`

### Intermediate Exercises
1. **Exercise**: Construct an NRQL query that calculates the 95th percentile latency of transactions grouped by HTTP status code for the last 6 hours.
   - *Solution*: `SELECT percentile(duration, 95) FROM Transaction FACET httpResponseCode TIMESERIES 5 minutes SINCE 6 hours ago`
2. **Exercise**: Write a Python decorator that catches `ConnectionResetError` and retries up to 3 times with a 1-second pause.
   - *Solution*: Reference Section 6.7.

### Advanced Exercises
1. **Exercise**: Calculate the allowable downtime in a 30-day window for a 99.99% availability SLO, and determine whether an outage of 5 minutes breaches the SLO.
   - *Solution*: Total seconds in 30 days = $2,592,000$. Allowable fraction = $1 - 0.9999 = 0.0001$. Allowable downtime = $2,592,000 \times 0.0001 = 259.2\text{ seconds} = 4.32\text{ minutes}$. An outage of 5 minutes ($300\text{ seconds}$) **exceeds the 4.32-minute allowance and breaches the SLO**.

---

# 46. Knowledge Verification Checks

### Multiple Choice Questions (10 MCQs)
1. **What is the maximum allowable percentage of time an SRE should spend on operational toil?**
   - A) 10%
   - B) 30%
   - C) 50%
   - D) 80%
   - *Answer: C (50%). SRE principles dictate at least 50% of time must be dedicated to engineering.*
2. **Which Linux signal is sent by the kernel during an OOM kill event?**
   - A) SIGTERM (15)
   - B) SIGINT (2)
   - C) SIGHUP (1)
   - D) SIGKILL (9)
   - *Answer: D (SIGKILL - 9).*
3. **What is the allowable downtime per 30-day month for a 99.9% availability SLO?**
   - A) 4.32 minutes
   - B) 43.8 minutes
   - C) 7.2 hours
   - D) 21.6 hours
   - *Answer: B (43.8 minutes).*
4. **Which HTTP status code is returned by an ALB when upstream servers take too long to respond?**
   - A) 500
   - B) 502
   - C) 503
   - D) 504
   - *Answer: D (504 Gateway Timeout).*
5. **In Kubernetes, what happens when a container exceeds its CPU limit?**
   - A) The container is killed with exit code 137.
   - B) The container is throttled by the CFS quota.
   - C) The pod is evicted to another node.
   - D) The pod status changes to CrashLoopBackOff.
   - *Answer: B (It is throttled, not killed).*
6. **In New Relic, which query keyword groups results into time-series intervals?**
   - A) GROUP BY TIME
   - B) INTERVAL
   - C) TIMESERIES
   - D) TIME_BUCKET
   - *Answer: C (TIMESERIES).*
7. **Which standard HTTP header is used by OpenTelemetry for distributed trace propagation?**
   - A) X-Trace-ID
   - B) traceparent
   - C) X-Correlation-ID
   - D) Uber-Trace-Id
   - *Answer: B (traceparent).*
8. **What does an Apdex score of 0.85 represent?**
   - A) Poor performance
   - B) Acceptable user satisfaction
   - C) Critical failure
   - D) 85% packet loss
   - *Answer: B (Good/Acceptable performance).*
9. **In Python, which module is best suited for bypassing the GIL for CPU-bound computation?**
   - A) threading
   - B) asyncio
   - C) multiprocessing
   - D) socket
   - *Answer: C (multiprocessing).*
10. **Which AWS service provides private, free internal network connectivity to S3?**
    - A) Internet Gateway
    - B) NAT Gateway
    - C) S3 VPC Gateway Endpoint
    - D) Direct Connect
    - *Answer: C (S3 VPC Gateway Endpoint).*

---

# 47. Final Enterprise Capstone Project

### The Master Architecture
The capstone combines all competencies into a unified, resilient enterprise platform:

```
                       GitHub
                          |
                          ↓
                    CI/CD Pipeline (GitHub Actions)
                          |
                          ↓
                    Docker Multi-Stage Build
                          |
                          ↓
               Kubernetes Cluster (EKS / Multi-AZ)
                          |
              +-----------+-----------+
              |                       |
              ↓                       ↓
        FastAPI App              PostgreSQL Aurora
       (Instrumented)            (Multi-AZ)
              |
              ↓
       OpenTelemetry SDK
              |
              ↓
          New Relic
       (APM / Infra / Logs / Traces)
              |
       +------+------+
       |             |
       ↓             ↓
   Dashboards      Alerts
                       |
                       ↓
                 Python SRE Autonomous Daemon
                       |
             +---------+---------+
             |                   |
             ↓                   ↓
        NerdGraph           K8s Rollout
        Telemetry           Remediation
             |                   |
             +---------+---------+
                       ↓
                  Postmortem Log
```

### Complete Implementation Blueprint
1. **Terraform**: Provision AWS VPC, EKS Cluster, and New Relic alert conditions.
2. **FastAPI Application**: High-throughput microservice with `/health`, `/ready`, and New Relic instrumentation.
3. **Docker**: Secure multi-stage Dockerfile running as non-root user.
4. **Kubernetes**: Deployment with HPA, Pod Anti-Affinity, PDB, and Prometheus annotations.
5. **CI/CD**: GitHub Actions automating testing, image building, Trivy security scanning, and New Relic deployment marking.
6. **Automation**: Python self-healing daemon diagnosing alerts via NerdGraph and executing automated recovery.

---

# 48. Recommended Production SRE Tool Matrix

| Area | Primary Tool | Secondary Tool | SRE Production Rationale |
| :--- | :--- | :--- | :--- |
| **OS** | Linux (Ubuntu / RHEL) | Bash | Linux is the substrate of modern cloud compute and container runtimes. |
| **Programming** | Python | Go | Python leads automation, telemetry analysis, and AIOps; Go excels at low-level systems. |
| **Cloud** | AWS | GCP / Azure | AWS holds the largest enterprise market share; provides mature APIs and regional resilience. |
| **Containers** | Docker | Podman | Docker provides standard image building and developer ergonomics; Podman offers daemonless rootless containers. |
| **Orchestration**| Kubernetes | — | The undisputed standard for containerized distributed workload management. |
| **IaC** | Terraform | OpenTofu / Ansible | Terraform delivers declarative, multi-cloud stateful infrastructure provisioning. |
| **CI/CD** | GitHub Actions | GitLab CI / Jenkins | GitHub Actions integrates seamlessly with source control, PR reviews, and secrets. |
| **Observability**| New Relic | Prometheus + Grafana | New Relic provides unified petabyte-scale MELT data with zero maintenance overhead. |
| **Telemetry** | OpenTelemetry | — | CNCF vendor-neutral standard for instrumentation and context propagation. |
| **Load Testing** | Locust | k6 | Locust enables Python-based distributed load testing simulating complex user flows. |
| **Security** | Trivy | Snyk | Trivy provides fast, comprehensive vulnerability and misconfiguration scanning in CI. |
| **GitOps** | Argo CD | Flux | Argo CD provides visual drift detection and automated declarative synchronization. |
| **Secrets** | HashiCorp Vault | AWS Secrets Manager| Centralized, audited, dynamic secret leasing with zero plaintext storage. |

---

# 49. SRE Competency Skill Assessment Framework

Use this rubric to rate your capabilities from **0 (Never Used)** to **5 (Production Expert)** across the 16 core SRE disciplines:

```
0 = Never Used: No conceptual or hands-on experience.
1 = Beginner: Understands basic theory; needs guidance to run commands.
2 = Basic: Can complete routine tasks using documentation; follows runbooks.
3 = Intermediate: Independently designs, deploys, and debugs systems in staging.
4 = Strong: Deep production experience; troubleshoots Sev-1 outages; automates complex workflows.
5 = Production Expert: Architectural authority; authors complex automation; mentors teams.
```

- [ ] **1. Linux Systems Engineering**: Kernel tuning, `/proc`, memory allocation, process lifecycle, troubleshooting tools (`strace`, `perf`, `iostat`).
- [ ] **2. Networking**: TCP/IP mechanics, DNS architecture, TLS 1.3 handshake, HTTP/2/3, packet analysis with `tcpdump`.
- [ ] **3. Python Automation**: Advanced data structures, decorators, context managers, generators, concurrency (`asyncio`), robust error handling.
- [ ] **4. AWS Cloud Infrastructure**: Multi-AZ VPC design, compute sizing, RDS Aurora failover, IAM least privilege, cost optimization.
- [ ] **5. Docker Containerization**: Multi-stage builds, non-root security, layer caching, Linux namespaces, and cgroups isolation.
- [ ] **6. Kubernetes Orchestration**: Control plane internals, probes, HPA, scheduling rules, rolling deployments, pod disruption budgets.
- [ ] **7. Infrastructure as Code**: Terraform state management, remote backends, modules, state drift reconciliation.
- [ ] **8. CI/CD Engineering**: Declarative GitHub Actions pipelines, quality gates, automated security scanning, deployment markers.
- [ ] **9. Observability Fundamentals**: Golden signals, percentiles ($p99$), metric types, structured logging, distributed tracing.
- [ ] **10. New Relic Platform**: APM instrumentation, Infrastructure agent, Kubernetes integration, distributed tracing.
- [ ] **11. NRQL Mastery**: Writing advanced analytical queries, baseline alerts, error budget burn rates, custom dashboards.
- [ ] **12. OpenTelemetry**: Vendor-neutral SDK instrumentation, OTel Collector pipelines, OTLP exporter configuration.
- [ ] **13. Incident Management**: Incident Commander role, blameless postmortems, Five Whys, communication protocols.
- [ ] **14. SRE Principles**: Defining SLIs/SLOs/SLAs, managing error budgets, eliminating toil, capacity planning.
- [ ] **15. Distributed Systems**: CAP theorem, circuit breakers, idempotency, distributed locks, retry backoff algorithms.
- [ ] **16. Autonomous & Agentic SRE**: LLM tool calling, automated remediation runbooks, guardrails, human-in-the-loop validation.

---

# 50. The Complete 14-Phase SRE Learning Roadmap

This structured, phased roadmap guides your study journey from fundamental foundations to senior-level production mastery.

---

### Phase 1: Foundations & The SRE Mindset
- **Topics**: History of SRE, Toil reduction, Reliability vs Availability, Error Budgets, SLI/SLO/SLA math.
- **Hands-On**: Calculate availability, downtime, and burn rate scenarios using Python.
- **Completion Criteria**: Can construct an Error Budget Policy and calculate downtime windows for any SLA.

### Phase 2: Linux & Production Networking Mastery
- **Topics**: Kernel-userspace separation, `/proc`, process states, memory management, TCP handshakes, DNS, TLS 1.3.
- **Hands-On**: Complete the 10 Linux troubleshooting labs (High CPU, OOM, Inode exhaustion, Zombie processes).
- **Completion Criteria**: Comfortable using `strace`, `lsof`, `ss`, and `tcpdump` to isolate system failures.

### Phase 3: Python for SRE & Automation
- **Topics**: OOP, generators, decorators, context managers, exception hierarchies, `psutil`, `httpx`, `asyncio`.
- **Hands-On**: Build all 15 system automation tools and the async fleet health checker.
- **Completion Criteria**: Can write typed, tested, structured-logging Python automation scripts with zero external guidance.

### Phase 4: Cloud Engineering with AWS
- **Topics**: Multi-AZ VPC networking, EC2 Auto Scaling, RDS Aurora, S3 lifecycle, SQS/SNS, CloudWatch.
- **Hands-On**: Build an enterprise VPC with public/private subnets and multi-AZ NAT Gateways.
- **Completion Criteria**: Can explain failure domains and compute/network bottlenecks across core AWS services.

### Phase 5: Containerization with Docker
- **Topics**: Linux namespaces, cgroups v2, multi-stage builds, rootless container security, layer caching.
- **Hands-On**: Containerize a Python FastAPI microservice with Trivy vulnerability scanning.
- **Completion Criteria**: Production Docker images $< 80\text{ MB}$ with non-root security contexts.

### Phase 6: Kubernetes Deep Dive
- **Topics**: Cluster architecture, etcd, kube-scheduler, deployments, services, ingress, probes, HPA.
- **Hands-On**: Complete the 10 Kubernetes troubleshooting labs (CrashLoopBackOff, OOMKilled, Pending pods).
- **Completion Criteria**: Able to debug and repair complex scheduling, probe, and resource issues in Kubernetes.

### Phase 7: Observability Fundamentals & OpenTelemetry
- **Topics**: Metrics, structured logs, distributed tracing, W3C trace context, OpenTelemetry Collector.
- **Hands-On**: Instrument a Python application with OpenTelemetry SDK and export telemetry over OTLP.
- **Completion Criteria**: Can trace a transaction across 3 independent microservices with correlated logs.

### Phase 8: New Relic Mastery & NRQL Deep Dive
- **Topics**: New Relic APM, Infrastructure, Kubernetes integration, Logs in Context, 50 NRQL production queries, Synthetics.
- **Hands-On**: Build Golden Signals dashboards and multi-window burn rate alert policies.
- **Completion Criteria**: Can answer any production operational question instantly using NRQL.

### Phase 9: Infrastructure as Code & CI/CD
- **Topics**: Terraform state, modules, drift detection, GitHub Actions workflows, deployment markers.
- **Hands-On**: Provision AWS infrastructure and New Relic alert conditions declaratively via Terraform.
- **Completion Criteria**: Zero manual changes in cloud console; all infrastructure and alerts versioned in Git.

### Phase 10: Production Incident Management
- **Topics**: Incident command system, triage, mitigation, communication, blameless postmortems, Five Whys.
- **Hands-On**: Simulate production outages; lead post-incident reviews; author blameless postmortem documents.
- **Completion Criteria**: Able to act as Incident Commander during Sev-1 outages with calm, structured leadership.

### Phase 11: Advanced Python Automation & NerdGraph APIs
- **Topics**: NerdGraph GraphQL queries and mutations, webhook ingestion, programmatic alert management.
- **Hands-On**: Build the Python + New Relic Autonomous Remediation Daemon.
- **Completion Criteria**: Automation engine safely remediates production alerts and verifies recovery via telemetry.

### Phase 12: Distributed Systems Reliability
- **Topics**: CAP theorem, circuit breakers, idempotency, distributed locks, retry backoff with jitter.
- **Hands-On**: Implement Python circuit breakers and load test microservices using Locust.
- **Completion Criteria**: Systems degrade gracefully under network partitions and third-party vendor downtime.

### Phase 13: Self-Healing Systems & Chaos Engineering
- **Topics**: Chaos engineering principles, failure injection labs, Kubernetes operators, automated rollbacks.
- **Hands-On**: Execute chaos experiments (CPU, memory, disk, network latency) and verify automated recovery.
- **Completion Criteria**: Systems automatically detect failure, isolate faulty components, and restore health without human intervention.

### Phase 14: Agentic SRE & AIOps
- **Topics**: LLM tool calling, automated runbook execution, AI incident summarization, safety guardrails.
- **Hands-On**: Build an Agentic SRE prototype that triages alerts and assists the on-call engineer.
- **Completion Criteria**: Future-proof engineer capable of building and overseeing autonomous AI operations.
'''
