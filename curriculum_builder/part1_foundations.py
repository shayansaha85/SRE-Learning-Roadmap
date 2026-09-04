"""
Curriculum Builder - Part 1: Sections 1 to 5
Foundations, SLI/SLO/SLA/Error Budgets, Linux for SRE, Networking for SRE, Git & GitHub
"""

def get_part1_content() -> str:
    return r'''# Enterprise Site Reliability Engineering & Observability Curriculum
## The Production Master Guide: SRE, Python Automation & New Relic Observability

---

```
                    SRE
                     |
          +----------+----------+
          |                     |
       Python               New Relic
          |                     |
   Automation/APIs        Observability
          |                     |
   Self-healing          APM/Logs/Traces
          |                     |
          +----------+----------+
                     |
               Production SRE
```

---

## Master Table of Contents

- [1. SRE Fundamentals](#1-sre-fundamentals)
  - [1.1 What is Site Reliability Engineering?](#11-what-is-site-reliability-engineering)
  - [1.2 The History of SRE](#12-the-history-of-sre)
  - [1.3 SRE vs DevOps, SysAdmin, Platform & Production Engineering](#13-sre-vs-devops-sysadmin-platform--production-engineering)
  - [1.4 Core Responsibilities & Day-to-Day Activities](#14-core-responsibilities--day-to-day-activities)
  - [1.5 The Reliability Mindset & The War on Toil](#15-the-reliability-mindset--the-war-on-toil)
  - [1.6 System Characteristics: Availability, Scalability, Resilience, Fault Tolerance, Durability, Performance, Observability](#16-system-characteristics)
  - [1.7 Section 1 Knowledge Assessment & Questions](#17-section-1-knowledge-assessment--questions)
- [2. SLI, SLO, SLA and Error Budgets](#2-sli-slo-sla-and-error-budgets)
  - [2.1 The Core Triad: SLI, SLO, SLA](#21-the-core-triad-sli-slo-sla)
  - [2.2 Error Budgets & The Error Budget Policy](#22-error-budgets--the-error-budget-policy)
  - [2.3 The High-Availability Math: The Nines and Downtime Windows](#23-the-high-availability-math-the-nines-and-downtime-windows)
  - [2.4 Latency SLOs: Why Averages Lie and Percentiles Rule](#24-latency-slos-why-averages-lie-and-percentiles-rule)
  - [2.5 Burn Rate Mathematics & Multi-Window Multi-Burn-Rate Alerting](#25-burn-rate-mathematics--multi-window-multi-burn-rate-alerting)
  - [2.6 Practical Numerical Calculation Exercises with Full Solutions](#26-practical-numerical-calculation-exercises-with-full-solutions)
- [3. Linux for SRE](#3-linux-for-sre)
  - [3.1 Linux Architecture & The Kernel-Userspace Boundary](#31-linux-architecture--the-kernel-userspace-boundary)
  - [3.2 Processes, Threads, and Lifecycle](#32-processes-threads-and-lifecycle)
  - [3.3 Filesystem Hierarchy, VFS, Inodes, and File Descriptors](#33-filesystem-hierarchy-vfs-inodes-and-file-descriptors)
  - [3.4 Memory Management, Virtual Memory, and the OOM Killer](#34-memory-management-virtual-memory-and-the-oom-killer)
  - [3.5 CPU Utilization, Load Averages, and Scheduling](#35-cpu-utilization-load-averages-and-scheduling)
  - [3.6 The Virtual Filesystems: /proc, /sys, /dev](#36-the-virtual-filesystems-proc-sys-dev)
  - [3.7 systemd, cgroups v2, and journald](#37-systemd-cgroups-v2-and-journald)
  - [3.8 The Essential 30 SRE Linux Commands Reference](#38-the-essential-30-sre-linux-commands-reference)
  - [3.9 Ten Real-World Linux Troubleshooting Labs with Full Solutions](#39-ten-real-world-linux-troubleshooting-labs-with-full-solutions)
- [4. Networking for SRE](#4-networking-for-sre)
  - [4.1 OSI Model vs TCP/IP Stack in Production](#41-osi-model-vs-tcpip-stack-in-production)
  - [4.2 TCP Deep Dive: Handshake, Windowing, Teardown, and Socket States](#42-tcp-deep-dive-handshake-windowing-teardown-and-socket-states)
  - [4.3 DNS Architecture, Record Types, TTL, and Resolution Flow](#43-dns-architecture-record-types-ttl-and-resolution-flow)
  - [4.4 HTTP/1.1, HTTP/2, HTTP/3, and the TLS 1.3 Handshake](#44-http11-http2-http3-and-the-tls-13-handshake)
  - [4.5 Load Balancing, Reverse Proxies, and CDNs](#45-load-balancing-reverse-proxies-and-cdns)
  - [4.6 SRE Networking Diagnostics Toolkit](#46-sre-networking-diagnostics-toolkit)
  - [4.7 Eight Production Networking Incident Scenarios with Investigations](#47-eight-production-networking-incident-scenarios-with-investigations)
- [5. Git and GitHub for SRE](#5-git-and-github-for-sre)
  - [5.1 Git Internals: Objects, Trees, Commits, and References](#51-git-internals-objects-trees-commits-and-references)
  - [5.2 Branching Strategies: Trunk-Based Development vs GitFlow for SRE](#52-branching-strategies-trunk-based-development-vs-gitflow-for-sre)
  - [5.3 Rebasing, Merging, Cherry-Picking, Reset vs Revert](#53-rebasing-merging-cherry-picking-reset-vs-revert)
  - [5.4 Conflict Resolution, Pull Request Reviews, and Operability Standards](#54-conflict-resolution-pull-request-reviews-and-operability-standards)
  - [5.5 GitHub Actions Workflows for Infrastructure and Operations](#55-github-actions-workflows-for-infrastructure-and-operations)
  - [5.6 Practical Exercises and Solutions](#56-practical-exercises-and-solutions)
- [6. Python for SRE — Deep Dive](#6-python-for-sre--deep-dive)
- [7. Python System Automation](#7-python-system-automation)
- [8. Python APIs and Automation](#8-python-apis-and-automation)
- [9. Python Production Engineering](#9-python-production-engineering)
- [10. Python Concurrency](#10-python-concurrency)
- [11. Flask and FastAPI for SREs](#11-flask-and-fastapi-for-sres)
- [12. AWS for SRE](#12-aws-for-sre)
- [13. Docker & Containerization](#13-docker--containerization)
- [14. Kubernetes — Deep Dive](#14-kubernetes--deep-dive)
- [15. Continuous Integration & Continuous Deployment (CI/CD)](#15-continuous-integration--continuous-deployment-cicd)
- [16. Infrastructure as Code: Terraform](#16-infrastructure-as-code-terraform)
- [17. Observability Fundamentals](#17-observability-fundamentals)
- [18. New Relic — Architecture & Telemetry Data Platform](#18-new-relic--architecture--telemetry-data-platform)
- [19. New Relic APM](#19-new-relic-apm)
- [20. New Relic Infrastructure Monitoring](#20-new-relic-infrastructure-monitoring)
- [21. New Relic Logs & Log Management](#21-new-relic-logs--log-management)
- [22. NRQL — Deep Dive & 50 Production Queries](#22-nrql--deep-dive--50-production-queries)
- [23. New Relic Dashboards](#23-new-relic-dashboards)
- [24. New Relic Alerting & Incident Workflows](#24-new-relic-alerting--incident-workflows)
- [25. New Relic Synthetics](#25-new-relic-synthetics)
- [26. New Relic Kubernetes Monitoring](#26-new-relic-kubernetes-monitoring)
- [27. New Relic APIs & NerdGraph (GraphQL)](#27-new-relic-apis--nerdgraph-graphql)
- [28. Python + New Relic Autonomous Remediation Capstone](#28-python--new-relic-autonomous-remediation-capstone)
- [29. Prometheus and Grafana](#29-prometheus-and-grafana)
- [30. OpenTelemetry (OTel)](#30-opentelemetry-otel)
- [31. Production Incident Management](#31-production-incident-management)
- [32. Thirty Production SRE Troubleshooting Scenarios](#32-thirty-production-sre-troubleshooting-scenarios)
- [33. Performance Engineering & Load Testing](#33-performance-engineering--load-testing)
- [34. Capacity Planning & Traffic Forecasting](#34-capacity-planning--traffic-forecasting)
- [35. Distributed Systems Reliability](#35-distributed-systems-reliability)
- [36. Security Engineering for SRE](#36-security-engineering-for-sre)
- [37. GitOps with Argo CD](#37-gitops-with-argo-cd)
- [38. AIOps and Agentic SRE](#38-aiops-and-agentic-sre)
- [39. Ten Progressive SRE Projects](#39-ten-progressive-sre-projects)
- [40. Chaos Engineering & Failure Injection Labs](#40-chaos-engineering--failure-injection-labs)
- [41. Master SRE Interview Preparation Bank (470+ Questions & Answers)](#41-master-sre-interview-preparation-bank-470-questions--answers)
- [42. Scenario-Based Troubleshooting Interview Walkthroughs](#42-scenario-based-troubleshooting-interview-walkthroughs)
- [43. SRE System Design (10 Enterprise Architectures)](#43-sre-system-design-10-enterprise-architectures)
- [44. Production Verification Checklists](#44-production-verification-checklists)
- [45. Comprehensive Learning Exercises](#45-comprehensive-learning-exercises)
- [46. Knowledge Verification Checks](#46-knowledge-verification-checks)
- [47. Final Enterprise Capstone Project](#47-final-enterprise-capstone-project)
- [48. Recommended Production SRE Tool Matrix](#48-recommended-production-sre-tool-matrix)
- [49. SRE Competency Skill Assessment Framework](#49-sre-competency-skill-assessment-framework)
- [50. The Complete 14-Phase SRE Learning Roadmap](#50-the-complete-14-phase-sre-learning-roadmap)

---

# 1. SRE Fundamentals

### 1.1 What is Site Reliability Engineering?

Site Reliability Engineering (SRE) is what happens when you treat operations as if it were a software engineering problem. First coined by Ben Treynor Sloss at Google in 2003, SRE is an engineering discipline dedicated to creating scalable, highly reliable, and resilient software systems.

In classical enterprise IT, a fundamental conflict existed between **Development** (whose goal is to release features as fast as possible) and **Operations** (whose goal is to keep systems stable by preventing change). SRE removes this tension through shared ownership, quantified risk tolerance (Error Budgets), and treating infrastructure and operations as software engineering problems.

An SRE applies software engineering skills to fix operational bottlenecks, automates away manual toil, designs telemetry architectures, and balances velocity against reliability.

```
+-------------------------------------------------------------+
|                      SRE Core Axioms                        |
+-------------------------------------------------------------+
| 1. Reliability is the most important feature of any product.|
| 2. 100% uptime is virtually always the wrong target.        |
| 3. Systems fail; design for failure and rapid MTTR.         |
| 4. Automate repetitive work (Toil must remain < 50%).       |
| 5. Blameless culture: People don't fail; systems do.        |
+-------------------------------------------------------------+
```

### 1.2 The History of SRE

In 2003, Google was experiencing hypergrowth. Traditional IT operations teams were overwhelmed by the rate of server deployments and manual intervention. Ben Treynor Sloss, a software engineer by training, was tasked with running a team of seven engineers to keep Google's production systems running.

Instead of hiring system administrators who manually configured servers, Treynor hired software engineers who wrote code to automate administration, detect anomalies, heal services, and provision resources. Treynor defined the team's mandate:
1. **50% Cap on Toil**: At least 50% of an SRE’s time must be spent on engineering projects (coding, architecture, automation, reliability enhancements). No more than 50% may be spent on operational toil (tickets, manual interventions, on-call shifts).
2. **Error Budgets**: Product teams own their error budgets. If an application stays within its budget, new features can ship freely. If the budget is exhausted, releases are gated while developers and SREs work together on reliability.

### 1.3 SRE vs DevOps, SysAdmin, Platform & Production Engineering

| Dimension | Site Reliability Engineer (SRE) | DevOps Engineer | Systems Administrator (SysAdmin) | Platform Engineer | Production Engineer |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Goal** | Maximize reliability, minimize MTTR, automate operations via software | Bridge Dev and Ops collaboration, optimize CI/CD pipelines | Keep servers, hardware, and OS operating via manual/scripted tasks | Provide developer self-service internal developer platforms (IDPs) | Ensure high-scale production systems run reliably (Meta terminology) |
| **Code Competency** | High (Python, Go; writes microservices, controllers, CLI tools) | Medium to High (Bash, Python, declarative YAML/HCL) | Low to Medium (Bash, PowerShell) | High (Go, Python, Kubernetes CRDs, Backstage) | High (C++, Python, Go, kernel hacking) |
| **Metric Focus** | SLI, SLO, SLA, Error Budget, MTTR, MTBF, Burn Rate | Deployment Frequency, Lead Time for Changes, Change Failure Rate | Server uptime, CPU/Memory utilization, ticket throughput | Developer adoption, time-to-first-commit, platform reliability | Latency percentiles, throughput, saturation, capacity headroom |
| **Culture** | "class SRE implements interface DevOps" (Google view) | Cultural movement emphasizing shared responsibility and speed | Ticket-driven operational silo | Internal product management for engineering teams | High-scale engineering at infrastructure and service tiers |

### 1.4 Core Responsibilities & Day-to-Day Activities

A Senior SRE does not spend their days sitting in front of a console waiting for servers to break. A representative work breakdown:

```
+------------------------------------------------------------+
|             SRE Work Breakdown (Weekly Average)            |
+------------------------------------------------------------+
| [ Engineering & Automation ]       ████████████████  50-60% |
| [ Architecture & Production Prep ] ████████          20%    |
| [ Observability & Alert Hygiene ]  ████              10%    |
| [ Incident Response & Postmortems] ████              10%    |
+------------------------------------------------------------+
```

Day-to-day responsibilities:
1. **Observability Engineering**: Instrumenting applications with OpenTelemetry, configuring New Relic APM, building NRQL queries, establishing SLO-based alerts.
2. **Software Automation**: Writing Python microservices, CLI utilities, Kubernetes operators, and API integrations that eliminate operational drag.
3. **Incident Response & On-Call**: Acting as Incident Commander during Sev-1/Sev-2 incidents; driving mitigation, communication, and resolution.
4. **Blameless Postmortems**: Leading post-incident reviews to identify systemic vulnerabilities and track action items.
5. **Capacity Planning & Load Testing**: Modeling traffic growth, executing distributed load tests with Locust/k6, forecasting compute/database headroom.
6. **Chaos Engineering**: Injecting controlled faults into staging and production to test system resiliency.

### 1.5 The Reliability Mindset & The War on Toil

#### The Definition of Toil
Toil is operational work that exhibits the following properties:
- **Manual**: Performed by a human by clicking or typing commands.
- **Repetitive**: Performed over and over again.
- **Automatable**: Could easily be performed by a Python script, cron job, or operator.
- **Tactical**: Reactive rather than strategic.
- **Devoid of Enduring Value**: Once done, the system is in the exact same state as before; it does not permanently make the service more reliable.
- **Scales Linearly with Service Size**: If your traffic doubles, your toil doubles.

#### Why SREs Must Cap Toil at 50%
When an SRE team spends more than 50% of its time on toil, engineering output stops. Morale drops, burnout accelerates, systems become fragile, and operational debt compounds until the team is trapped in a permanent reactive fire-fighting cycle.

### 1.6 System Characteristics

1. **Reliability**: The probability that a system will perform its required functions under specified conditions for a specified period.
2. **Availability**: The percentage of time that a service is functioning properly and accessible to users:
   $$\text{Availability} = \frac{\text{Total Time} - \text{Downtime}}{\text{Total Time}} \times 100\%$$
3. **Scalability**: The capability of a system to handle a growing amount of work by adding resources.
   - *Vertical (Scaling Up)*: Adding CPU, RAM, or NVMe disks to a single server.
   - *Horizontal (Scaling Out)*: Adding identical stateless container replicas behind an Application Load Balancer.
4. **Resilience**: The capacity of a system to recover quickly from difficulties, absorb shocks, and maintain acceptable service levels during failures (e.g., graceful degradation).
5. **Fault Tolerance**: The property that enables a system to continue operating properly in the event of the failure of one or more components (e.g., Raft consensus tolerating $(N-1)/2$ node failures).
6. **Durability**: The guarantee that stored data will remain intact and uncorrupted over long periods (e.g., AWS S3 offering $99.999999999\%$ [11 9s] durability).
7. **Performance**: The speed and efficiency with which a system executes operations under a given workload (measured in latency percentiles and resource consumption).
8. **Observability**: The degree to which the internal state of a system can be inferred solely from knowledge of its external outputs (metrics, logs, traces).

### 1.7 Section 1 Knowledge Assessment & Questions

#### Question 1
**Question:** Why is 100% availability an anti-pattern in modern software engineering?
**Answer:** Setting a 100% availability target is economically irrational, technically impossible in distributed systems, and halts product innovation. The cost of going from 99.99% to 100% is exponential, requiring redundant active-active multi-region systems, private networks, and isolated power grids. Furthermore, users cannot perceive 100% availability because their local ISP, Wi-Fi, and cellular carrier typically operate between 99% and 99.9% availability. Any reliability beyond user perception is wasted money that prevents teams from shipping features.
**Why the answer is correct:** The SRE philosophy dictates that the gap between your SLO and 100% is your **Error Budget**, which is an asset to be spent on risky deployments, experimentation, and rapid feature releases.

#### Question 2
**Question:** A developer asks an SRE to manually restart an application pod every Tuesday morning because of an unresolved memory leak. How should the SRE respond under SRE principles?
**Answer:** The SRE must reject this manual request as operational toil. Under SRE principles, the SRE should:
1. Temporarily configure an automated Kubernetes `livenessProbe` with memory thresholds or a CronJob if an immediate workaround is strictly necessary.
2. File a high-priority bug with the development team to isolate the memory leak using Python profiling tools (`tracemalloc`, `py-spy`).
3. If the memory leak consumes significant error budget, block further feature deployments until the underlying bug is fixed.
**Why the answer is correct:** SREs do not perform manual repetitive maintenance. SREs automate temporary mitigation and hold the engineering team accountable for fixing the systemic root cause.

#### Question 3
**Question:** Explain the difference between Fault Tolerance and Resilience using a production payment system example.
**Answer:** Fault tolerance means the component failure is completely invisible to the user. For example, if a payment database uses a three-node CockroachDB cluster, the sudden crash of node 2 causes zero errors or dropped transactions because quorum is maintained. Resilience means the system absorbs a catastrophic failure and degrades gracefully. For example, if the primary third-party credit card gateway (e.g., Stripe) experiences a global outage, a resilient payment service catches the timeout, does not crash, queues the orders asynchronously in an SQS queue, and alerts the customer: "Your payment is being processed; we will email you within 10 minutes," thereby saving the order.
**Why the answer is correct:** Fault tolerance prevents any impact; resilience gracefully manages impact when prevention is impossible.

#### Question 4
**Question:** What makes work qualify as "Toil"? List all six characteristics.
**Answer:** Toil is manual, repetitive, automatable, tactical (lacking enduring architectural value), devoid of lasting improvements, and scales linearly as service load or server count grows.
**Why the answer is correct:** This definition directly derives from the Google SRE framework to differentiate operational drag from legitimate engineering.

#### Question 5
**Question:** How does an SRE distinguish between Availability and Reliability?
**Answer:** Availability is a simple temporal or count ratio: "Was the HTTP port returning 200 OK when pinged?" Reliability is the broader quality of user satisfaction: "Did the system perform the user's intended action correctly, securely, within acceptable latency bounds, and with complete data integrity?" A service can be 100% available (returning HTTP 200) while being 0% reliable (e.g., returning an empty JSON body or corrupt data).
**Why the answer is correct:** Reliability is user-centric; availability is often a naive infrastructure metric.

#### Question 6
**Question:** What is the fundamental difference between Horizontal Scaling and Vertical Scaling, and what is the SRE architectural preference?
**Answer:** Vertical scaling (Scale Up) increases CPU, memory, or disk bandwidth on an existing single virtual machine or server. Horizontal scaling (Scale Out) adds additional stateless application worker instances behind a load balancer. SREs strongly prefer horizontal scaling because it removes single points of failure (SPOFs), enables zero-downtime rolling updates, allows auto-scaling based on real-time traffic demand, and is bounded only by the capacity of the load balancer and backing datastore.
**Why the answer is correct:** Vertical scaling has physical hardware limits, requires downtime to resize, and leaves the service vulnerable to single-host hardware crashes.

#### Question 7
**Question:** What is the primary role of an Error Budget Policy?
**Answer:** An Error Budget Policy is a pre-agreed contract between Product Management, Software Engineering, and SRE that mandates specific actions when a service exhausts its error budget within a defined window. If the budget is spent, feature releases are automatically suspended, and engineering effort is redirected entirely toward reliability fixes, bug remediation, test coverage, and observability improvements.
**Why the answer is correct:** Without an enforceable policy, error budgets are ignored by product managers under pressure to deliver features.

#### Question 8
**Question:** What is Durability, and how does it differ from Availability?
**Answer:** Durability measures the permanence and survival of data over time without corruption or loss. Availability measures whether that data can be read right now. If an AWS S3 region has a temporary networking outage, its availability drops to 0% for those minutes, but its durability remains 99.999999999% because not a single byte of data was lost on disk.
**Why the answer is correct:** Durability relates to disk storage integrity; availability relates to real-time network and service access.

#### Question 9
**Question:** What is the concept of "Blameless Postmortems"?
**Answer:** A blameless postmortem operates on the foundational assumption that humans make mistakes because complex systems are poorly designed, ambiguous, or lacking guardrails. Instead of asking "Who broke production?", the postmortem investigates: "What systemic vulnerabilities, missing alerts, brittle configurations, or process gaps allowed a well-intentioned engineer to cause an outage?"
**Why the answer is correct:** Blaming individuals leads to fear, hiding of mistakes, delayed incident declaration, and failure to fix root causes.

#### Question 10
**Question:** What is MTTR and MTBF, and which metric does an SRE prioritize optimizing?
**Answer:** MTBF is Mean Time Between Failures; MTTR is Mean Time To Recovery. While high MTBF is desirable, modern distributed systems are so complex that failures are inevitable. Therefore, SRE prioritizes minimizing MTTR through robust observability, rapid automated rollbacks, self-healing systems, and clear runbooks.
**Why the answer is correct:** In microservices running across thousands of nodes, something is always broken. Resilience depends on fast detection and recovery, not the illusion that failures will never happen.

---

# 2. SLI, SLO, SLA and Error Budgets

### 2.1 The Core Triad: SLI, SLO, SLA

```
+-------------------------------------------------------------+
|               The Reliability Contract Flow                 |
+-------------------------------------------------------------+
|   SLI: What did we measure? (Real-time telemetry)           |
|        e.g., Successful HTTP requests / Total requests       |
|                            |                                |
|                            v                                |
|   SLO: What did we promise ourselves internally?            |
|        e.g., 99.9% of requests successful over 30 days      |
|                            |                                |
|                            v                                |
|   SLA: What did the business promise the customer?          |
|        e.g., 99.0% uptime or customers receive 15% credits |
+-------------------------------------------------------------+
```

1. **Service Level Indicator (SLI)**: A carefully defined quantitative measure of some aspect of the level of service that is being provided.
   $$\text{SLI} = \frac{\text{Good Events}}{\text{Total Events}} \times 100\%$$
   *Examples*:
   - Availability SLI: Count of HTTP status codes $< 500$ divided by total HTTP requests.
   - Latency SLI: Count of HTTP requests completed in $< 200\text{ ms}$ divided by total HTTP requests.
2. **Service Level Objective (SLO)**: A target value or range of values for a service level that is measured by an SLI. This is set internally by engineering and product teams.
   *Example*: $99.9\%$ of API requests over any rolling 30-day window must return HTTP status $< 500$ and complete in $< 250\text{ ms}$.
3. **Service Level Agreement (SLA)**: An explicit or implicit contract with your users that includes consequences (usually financial penalties, billing credits, or contract termination) if you fail to meet the agreement.
   *Rule of Thumb*: The SLA is always looser than the SLO ($\text{SLA} < \text{SLO}$). If your internal SLO is $99.9\%$, your legal SLA should be $99.0\%$. The $0.9\%$ safety margin allows you to detect, respond to, and fix incidents before facing contractual liabilities.

### 2.2 Error Budgets & The Error Budget Policy

The **Error Budget** is the allowable amount of unreliability a system can accumulate over a defined time window without violating its SLO:
$$\text{Error Budget} = 100\% - \text{SLO}$$

If your SLO is $99.9\%$ over a 30-day window:
$$\text{Error Budget} = 100\% - 99.9\% = 0.1\%$$

If your service processes $10,000,000$ requests in 30 days, your error budget is:
$$10,000,000 \times 0.001 = 10,000\text{ allowable failed requests}$$

#### The Error Budget Policy Matrix
When error budget consumption reaches critical thresholds, specific automated or organizational guardrails trigger:

| Budget Remaining | Production State | Permitted Actions | Engineering Mandate |
| :--- | :--- | :--- | :--- |
| **$100\% - 20\%$** | Green (Healthy) | Standard feature releases, A/B testing, refactoring | Normal business roadmap |
| **$20\% - 1\%$** | Yellow (At Risk) | Canary deployments required, releases must have SRE sign-off | Prioritize outstanding reliability tickets |
| **$\le 0\%$** | Red (Exhausted) | **Deployment Freeze** on all feature code | 100% of engineering bandwidth diverted to stability, testing, and bug fixes |

### 2.3 The High-Availability Math: The Nines and Downtime Windows

The following table displays allowable downtime for standard availability SLO targets:

| Target ("Nines") | Availability | Downtime per Year | Downtime per Quarter | Downtime per Month (30d) | Downtime per Week (7d) | Downtime per Day (24h) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1 Nine** | $90.0\%$ | 36.52 days | 9.13 days | 3.0 days | 16.8 hours | 2.4 hours |
| **2 Nines** | $99.0\%$ | 3.65 days | 21.9 hours | 7.2 hours | 1.68 hours | 14.4 minutes |
| **3 Nines** | $99.9\%$ | 8.76 hours | 2.19 hours | 43.8 minutes | 10.08 minutes | 1.44 minutes |
| **3.5 Nines**| $99.95\%$ | 4.38 hours | 1.09 hours | 21.6 minutes | 5.04 minutes | 43.2 seconds |
| **4 Nines** | $99.99\%$ | 52.56 minutes | 13.14 minutes | 4.32 minutes | 1.01 minutes | 8.64 seconds |
| **5 Nines** | $99.999\%$ | 5.26 minutes | 1.31 minutes | 25.92 seconds | 6.05 seconds | 0.86 seconds |

### 2.4 Latency SLOs: Why Averages Lie and Percentiles Rule

Never use the arithmetic mean (average) for latency SLIs.
Consider 100 requests: 99 requests take $10\text{ ms}$, but 1 request hangs for $10,000\text{ ms}$ (10 seconds).
$$\text{Average Latency} = \frac{99 \times 10 + 10,000}{100} = \frac{990 + 10,000}{100} = 109.9\text{ ms}$$
An average of $109.9\text{ ms}$ looks completely normal on a dashboard, masking the fact that a user suffered a 10-second freeze.

SREs measure **Percentiles**:
- **p50 (Median)**: 50% of requests were faster than this value. Measures typical user experience.
- **p90**: 90% of requests were faster than this value.
- **p99**: 99% of requests were faster than this value. Captures tail latency experienced by high-volume users.
- **p99.9**: The worst 1 in 1,000 requests. Vital for microservice architectures where a single user action triggers 50 downstream service calls.

### 2.5 Burn Rate Mathematics & Multi-Window Multi-Burn-Rate Alerting

#### The Burn Rate Equation
The **Burn Rate** is the rate at which a service consumes its error budget.
- A burn rate of **1.0** means the service will consume exactly 100% of its error budget over the designated measurement window (e.g., exactly 30 days).
- A burn rate of **2.0** will consume 100% of the budget in 15 days.
- A burn rate of **14.4** will consume 100% of the budget in 2 days (or $2\%$ of the budget in 1 hour).

$$\text{Burn Rate} = \frac{\text{Observed Error Rate}}{1 - \text{SLO Target}}$$

#### Google SRE Multi-Window Multi-Burn-Rate Alerting Matrix
Alerting on raw error rate causes alert fatigue during low traffic and fails to trigger during high traffic. Alerting on budget burn rate over multiple rolling windows solves both problems:

```
+----------------------------------------------------------------------------------------------------+
| SRE Multi-Window Multi-Burn-Rate Alerting Matrix (30-Day Budget Window, 99.9% SLO Target)          |
+-------------------+-----------+-----------------+------------------+------------------+------------+
| Alert Severity    | Burn Rate | % Budget Burned | Short Window     | Long Window      | Action     |
+-------------------+-----------+-----------------+------------------+------------------+------------+
| Critical (Page)   | 14.4      | 2% consumed     | 5 minutes (14.4) | 1 hour (14.4)    | Page SRE   |
| Critical (Page)   | 6.0       | 5% consumed     | 30 minutes (6.0) | 6 hours (6.0)    | Page SRE   |
| Warning (Ticket)  | 3.0       | 10% consumed    | 2 hours (3.0)    | 24 hours (3.0)   | File issue |
| Warning (Ticket)  | 1.0       | 10% consumed    | 6 hours (1.0)    | 3 days (1.0)     | File issue |
+-------------------+-----------+-----------------+------------------+------------------+------------+
```

*Why two windows?* Both the short window (e.g., 5 min) and the long window (e.g., 1 hour) must exceed the burn rate threshold simultaneously. This prevents pages from firing on transient spikes (short window resets quickly) while ensuring fast alerting when an outage starts.

### 2.6 Practical Numerical Calculation Exercises with Full Solutions

#### Exercise 1: Availability and Downtime Calculations
**Problem:** Your production service has an SLO of $99.95\%$ availability over a rolling 30-day window (assume 30 days = $2,592,000$ seconds).
1. Calculate the total allowable downtime in minutes and seconds.
2. During a catastrophic database migration, the API went completely offline for 18 minutes and 40 seconds. Did the service breach its SLO? What percentage of the error budget was consumed?

**Solution:**
1. Allowable downtime fraction:
   $$1 - 0.9995 = 0.0005$$
   $$\text{Allowable seconds} = 2,592,000 \times 0.0005 = 1,296\text{ seconds}$$
   $$\text{Minutes} = \frac{1,296}{60} = 21.6\text{ minutes} = 21\text{ minutes and } 36\text{ seconds}$$
2. Outage duration in seconds:
   $$18\text{ minutes} \times 60 + 40\text{ seconds} = 1,080 + 40 = 1,120\text{ seconds}$$
   Compare against allowable:
   $$1,120\text{ s} < 1,296\text{ s}$$
   **Result:** The service did *not* breach its SLO.
   Percentage of error budget consumed:
   $$\text{Budget Consumed} = \frac{1,120}{1,296} \times 100\% = 86.42\%$$
   **Production Consideration:** The team has only $13.58\%$ ($176\text{ seconds}$) of its error budget remaining for the next 29 days. An immediate feature freeze is warranted until the window rolls forward.

#### Exercise 2: Request-Based Availability SLI
**Problem:** An e-commerce API processed $45,000,000$ total HTTP requests over a 30-day period. Telemetry reveals that $32,150$ requests returned HTTP 5xx server errors, and $8,400$ requests timed out at the gateway (HTTP 504).
1. Calculate the actual availability SLI of the service to 4 decimal places.
2. If the team's internal SLO is $99.9\%$, did the service meet its objective?
3. What was the maximum number of additional failed requests the service could have tolerated?

**Solution:**
1. Total failed requests:
   $$\text{Total Errors} = 32,150 + 8,400 = 40,550$$
   Total successful requests:
   $$\text{Good Requests} = 45,000,000 - 40,550 = 44,959,450$$
   $$\text{SLI} = \frac{44,959,450}{45,000,000} \times 100\% = 99.909888\% \approx 99.9099\%$$
2. Since $99.9099\% \ge 99.9\%$, the service **met its internal SLO**.
3. Total allowable errors under $99.9\%$ SLO ($0.1\%$ failure rate):
   $$\text{Allowable Errors} = 45,000,000 \times 0.001 = 45,000$$
   Additional errors tolerated:
   $$45,000 - 40,550 = 4,450\text{ requests}$$

#### Exercise 3: Burn Rate and Multi-Window Calculation
**Problem:** A banking transaction engine has an SLO of $99.9\%$ over a 30-day period ($43,200\text{ minutes}$).
At 14:00, a faulty deployment causes $5\%$ of all incoming requests to fail.
1. What is the instantaneous burn rate?
2. At this error rate, how long will it take for the service to consume 100% of its monthly error budget?
3. Under the Google SRE matrix, will this trigger a Critical Page within 1 hour?

**Solution:**
1. Instantaneous Burn Rate:
   $$\text{SLO} = 0.999 \implies \text{Error Budget Fraction} = 1 - 0.999 = 0.001$$
   $$\text{Observed Error Rate} = 0.05$$
   $$\text{Burn Rate} = \frac{0.05}{0.001} = 50.0$$
2. Time to exhaust 100% of the 30-day budget:
   $$\text{Time} = \frac{30\text{ days}}{\text{Burn Rate}} = \frac{30}{50} = 0.6\text{ days} = 14.4\text{ hours} = 864\text{ minutes}$$
3. Under the Google matrix:
   A Critical Page is configured for a burn rate of $14.4$ over 1 hour ($2\%$ budget consumed in 1 hour).
   At a burn rate of $50.0$, the service consumes:
   $$\text{Consumption in 1 hour} = \frac{1\text{ hour}}{14.4\text{ hours}} \times 100\% = 6.94\%\text{ of total monthly budget}$$
   Since $50.0 \gg 14.4$ and $6.94\% > 2\%$, the 5-minute and 1-hour windows will both immediately breach within minutes, triggering a **Sev-1 Critical Page to the on-call SRE**.

---

# 3. Linux for SRE

### 3.1 Linux Architecture & The Kernel-Userspace Boundary

Modern Linux operates in a strict separation between **Kernel Space** and **User Space**, mediated by hardware CPU rings (Ring 0 for Kernel, Ring 3 for User Space on x86_64 architecture).

```
+-------------------------------------------------------------+
|                      Linux System Layers                    |
+-------------------------------------------------------------+
| User Space: Applications, Python, Nginx, Daemons, Shells    |
|             (Ring 3 - Restricted Memory Access)             |
+-------------------------------------------------------------+
| System Call Interface (glibc / syscalls: read, write, clone)|
+-------------------------------------------------------------+
| Kernel Space: Process Scheduler, VFS, Netfilter, Memory     |
|               (Ring 0 - Direct Hardware Access)             |
+-------------------------------------------------------------+
| Physical Hardware: CPU, RAM, NVMe Disks, Network Interfaces |
+-------------------------------------------------------------+
```

An SRE must understand that user-space applications (such as a Python web API) cannot directly touch the network card or hard drive. They execute a **System Call** (`syscall`), switching CPU context to the kernel. Common syscalls analyzed during debugging:
- `clone()` / `fork()`: Create new processes and threads.
- `epoll_wait()`: High-performance asynchronous I/O multiplexing.
- `openat()`, `read()`, `write()`, `close()`: File and socket operations.
- `mmap()` / `brk()`: Memory allocation requests.

### 3.2 Processes, Threads, and Lifecycle

In Linux, both processes and threads are represented internally by the kernel as `task_struct` objects. Threads are simply processes that share their virtual address space, file descriptor table, and signal handlers (created via `clone()` with flags `CLONE_VM`, `CLONE_FS`, `CLONE_FILES`).

#### Process States
- **R (Running / Runnable)**: The task is currently on the CPU or waiting in the run-queue.
- **S (Interruptible Sleep)**: Waiting for an event or resource (e.g., network packet or disk I/O). Can be woken by signals.
- **D (Uninterruptible Sleep)**: Waiting for disk I/O or NFS lock inside a kernel syscall. Cannot be killed, even with `kill -9`!
- **Z (Zombie / Defunct)**: The process has exited, but its parent process has not yet called `wait4()` to read its exit status code. Consumes a slot in the PID table.
- **T (Stopped / Traced)**: Stopped by job control (e.g., `Ctrl+Z`, `SIGSTOP`) or ptrace debugger.

### 3.3 Filesystem Hierarchy, VFS, Inodes, and File Descriptors

The **Virtual Filesystem (VFS)** is an abstraction layer inside the Linux kernel allowing diverse physical filesystems (ext4, XFS, Btrfs, NFS) to present a uniform POSIX API.

#### Inodes
An **inode** (index node) contains metadata about a file:
- File size, permissions, owner UID, group GID.
- Timestamps: `atime` (access), `mtime` (content modification), `ctime` (inode metadata change).
- Data block pointers on disk.
- *Crucially*: The inode does **not** store the file name! File names are stored in directory data blocks mapping names to inode numbers.

#### File Descriptors (FDs)
When a process opens a file or network socket, the kernel allocates a non-negative integer known as a File Descriptor.
- `0`: `stdin`
- `1`: `stdout`
- `2`: `stderr`
- `3+`: Opened files, network sockets, epoll instances, pipes.

The system-wide limit is configured in `/proc/sys/fs/file-max`, and per-process limits are controlled via `ulimit -n` and `/etc/security/limits.conf`.

### 3.4 Memory Management, Virtual Memory, and the OOM Killer

Every process sees a private, continuous **Virtual Address Space** (48-bit or 57-bit addressing in x86_64). The CPU's Memory Management Unit (MMU) translates virtual addresses to physical RAM pages using page tables.

#### The Virtual Memory Subsystems:
1. **Resident Set Size (RSS)**: Physical RAM currently allocated to the process.
2. **Virtual Memory Size (VIRT)**: Total memory mapped by the process, including shared libraries, allocated memory not yet touched, and swapped pages.
3. **Page Cache**: Kernel uses unused RAM to cache disk blocks. If a process needs memory, the kernel evicts clean page cache pages instantaneously.
4. **Swap Space**: Disk space used when physical RAM is exhausted. Swapping introduces severe latency spikes.

#### The Out-Of-Memory (OOM) Killer
Linux allows **Memory Overcommit**: processes can allocate more virtual memory than physical RAM exists. When physical memory and swap are 100% saturated, the kernel activates the OOM Killer:
1. Computes an `oom_score` for every running process based on memory usage percentage.
2. Multiplies by `/proc/[pid]/oom_score_adj` (ranging from -1000 to +1000).
3. Selects the process with the highest score and kills it with `SIGKILL` (signal 9) to protect the OS from freezing.

### 3.5 CPU Utilization, Load Averages, and Scheduling

#### Load Average Explained
The load average reported by `uptime` shows the average number of runnable tasks over 1, 5, and 15 minutes:
$$\text{Load} = \text{Tasks in R (Running/Runnable) state} + \text{Tasks in D (Uninterruptible Sleep) state}$$

*SRE Rule of Thumb*:
Divide the load average by the number of CPU cores:
- If Load / Cores $< 0.7$: System has headroom.
- If Load / Cores $= 1.0$: System is exactly at capacity.
- If Load / Cores $> 1.5$: Requests are queuing; latency will climb.
- *Warning*: If Load is high (e.g., 25.0) but CPU utilization is low (e.g., 5%), tasks are stuck in **D state** waiting on slow storage, hung NFS mounts, or locked hardware!

### 3.6 The Virtual Filesystems: /proc, /sys, /dev

Linux presents kernel data structures as virtual filesystems:
1. `/proc`: Process and kernel runtime data.
   - `/proc/cpuinfo`: Hardware CPU architecture, model, cache sizes, flags.
   - `/proc/meminfo`: Detailed RAM, buffers, cached, dirty pages, swap.
   - `/proc/net/dev`: Network interface packet counters and drops.
   - `/proc/sys/vm/overcommit_memory`: Controls overcommit handling (0=heuristic, 1=always overcommit, 2=strict no overcommit).
   - `/proc/[pid]/cmdline`: Exact invocation arguments.
   - `/proc/[pid]/fd/`: Directory containing symlinks to every open file descriptor.
   - `/proc/[pid]/status`: Memory breakdown (VmRSS, VmSize, Threads).
2. `/sys`: Sysfs exports device drivers, buses, and cgroups v2 resource accounting.
3. `/dev`: Device nodes (`/dev/null`, `/dev/zero`, `/dev/urandom`, NVMe block devices).

### 3.7 systemd, cgroups v2, and journald

Modern Linux distributions manage services via **systemd**.
- **Unit Types**: `.service` (daemons), `.timer` (cron replacement), `.socket` (socket activation), `.slice` (cgroup resource containers).
- **cgroups v2 (Control Groups)**: The kernel mechanism that isolates and meters resource usage (CPU, memory, I/O, network) for a collection of processes. This is the foundation of Docker and Kubernetes!
- **journald**: Unified binary logging system collecting kernel, systemd service, and stdout/stderr output.

### 3.8 The Essential 30 SRE Linux Commands Reference

Here are the 30 indispensable Linux commands with syntax, production SRE use cases, and debugging examples:

#### 1. `ps` (Process Status)
- **Syntax**: `ps aux` or `ps -efT`
- **SRE Use Case**: Inspect running processes, process trees, and thread groups.
- **Example**: Find top 5 memory-consuming processes:
  ```bash
  ps aux --sort=-%mem | head -n 6
  ```

#### 2. `top` / `htop` (Dynamic Process Monitor)
- **Syntax**: `htop`
- **SRE Use Case**: Real-time visualization of per-core CPU, memory, and thread states.
- **Troubleshooting**: Press `P` (sort by CPU), `M` (sort by Memory), `t` (tree view).

#### 3. `free` (Memory Utilization)
- **Syntax**: `free -h`
- **SRE Use Case**: Check total, used, free, shared, buff/cache, and available RAM.
- **Production Tip**: Always check the **available** column, not the **free** column. Linux uses free memory for disk caching.

#### 4. `vmstat` (Virtual Memory Statistics)
- **Syntax**: `vmstat 1 5`
- **SRE Use Case**: Inspect context switches (`cs`), interrupts (`in`), run queue (`r`), blocked tasks (`b`), and swap in/out (`si`/`so`).
- **Diagnosis**: High `si`/`so` indicates physical memory exhaustion and severe disk thrashing.

#### 5. `iostat` (I/O Statistics)
- **Syntax**: `iostat -xz 1 5`
- **SRE Use Case**: Measure disk saturation (`%util`), read/write throughput, and await time.
- **Diagnosis**: If `%util` approaches $100\%$ or `await` exceeds $20\text{ ms}$ on NVMe, disk I/O is your bottleneck.

#### 6. `df` (Disk Free)
- **Syntax**: `df -hT` and `df -i`
- **SRE Use Case**: Monitor filesystem capacity and inode utilization.
- **Troubleshooting**: If `df -h` shows space available but you get "No space left on device", check `df -i` to find inode exhaustion!

#### 7. `du` (Disk Usage)
- **Syntax**: `du -sh /var/log/* | sort -hr | head -n 10`
- **SRE Use Case**: Identify giant directories consuming disk capacity.

#### 8. `ss` (Socket Statistics)
- **Syntax**: `ss -tulpn`
- **SRE Use Case**: Replaces deprecated `netstat`. Inspect open TCP/UDP listening sockets, process bindings, and TCP socket queues.
- **Troubleshooting**:
  ```bash
  ss -tan state time-wait | wc -l
  ```

#### 9. `lsof` (List Open Files)
- **Syntax**: `lsof -p <PID>` or `lsof -i :8080`
- **SRE Use Case**: Discover which process is listening on a port or holding open deleted files.
- **Deleted File Hunter**:
  ```bash
  lsof +L1 | grep deleted
  ```

#### 10. `uptime` (System Load & Uptime)
- **Syntax**: `uptime`
- **SRE Use Case**: Quick assessment of system uptime, logged-in users, and 1-, 5-, and 15-minute load averages.

#### 11. `systemctl` (systemd Management)
- **Syntax**: `systemctl status <service>`, `systemctl restart <service>`
- **SRE Use Case**: Managing service lifecycles, enabling boot persistence, viewing unit status.

#### 12. `journalctl` (systemd Log Inspection)
- **Syntax**: `journalctl -u <service> -n 100 --no-pager -f`
- **SRE Use Case**: Real-time tailing and filtering of daemon logs, including stdout/stderr.
- **Kernel Logs**:
  ```bash
  journalctl -k -b 0
  ```

#### 13. `grep` (Global Regular Expression Print)
- **Syntax**: `grep -rnEI "ERROR|CRITICAL" /var/log/app/`
- **SRE Use Case**: Fast searching across thousands of log files for errors or correlation IDs.

#### 14. `awk` (Pattern Scanning & Processing)
- **Syntax**: `awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -n 10`
- **SRE Use Case**: Parsing structured server logs to extract top IP addresses or status codes.

#### 15. `sed` (Stream Editor)
- **Syntax**: `sed -i 's/DEBUG/INFO/g' /etc/app/config.yaml`
- **SRE Use Case**: Automated configuration updates in deployment pipelines.

#### 16. `cut`, `sort`, `uniq`
- **Syntax**: `cut -d' ' -f9 access.log | sort | uniq -c`
- **SRE Use Case**: Extract HTTP status code distribution from access logs.

#### 17. `xargs` (Build and Execute Commands)
- **Syntax**: `find /tmp -name "*.tmp" -mtime +7 -print0 | xargs -0 rm -f`
- **SRE Use Case**: Execute operations on large batches of files without exceeding `ARG_MAX`.

#### 18. `find` (File Search)
- **Syntax**: `find /var/log -type f -size +500M -exec ls -lh {} \;`
- **SRE Use Case**: Locating rogue log files or core dumps filling disks.

#### 19. `kill` / `pkill` (Signal Transmission)
- **Syntax**: `kill -15 <PID>` (SIGTERM) or `kill -9 <PID>` (SIGKILL)
- **SRE Principle**: Always attempt `SIGTERM` first to allow graceful shutdown, connection draining, and flushing buffers. Only escalate to `SIGKILL` if the process is completely unresponsive.

#### 20. `curl` (Client URL Transfer)
- **Syntax**: `curl -ivs -o /dev/null -w "%{http_code} time: %{time_total}s\n" https://api.internal/health`
- **SRE Use Case**: Testing API response codes, measuring DNS/TLS/TTFB connection timings.

#### 21. `wget` (Non-Interactive File Downloader)
- **Syntax**: `wget --timeout=10 --tries=3 https://repo.internal/package.tar.gz`
- **SRE Use Case**: Reliable automated asset fetching in CI/CD pipelines.

#### 22. `tar` (Archive Utility)
- **Syntax**: `tar -czvf logs_backup.tar.gz /var/log/app`
- **SRE Use Case**: Archiving logs or extracting deployment packages.

#### 23. `chmod` (Change File Mode)
- **Syntax**: `chmod 600 ~/.ssh/id_rsa`, `chmod 755 /usr/local/bin/monitor.py`
- **SRE Security**: Enforcing least privilege on configuration files and private keys.

#### 24. `chown` (Change File Owner)
- **Syntax**: `chown -R appuser:appgroup /opt/app`
- **SRE Security**: Preventing services from running as `root`.

#### 25. `strace` (Trace System Calls)
- **Syntax**: `strace -p <PID> -f -T -e trace=network,file`
- **SRE Use Case**: When an application hangs with no logs, `strace` reveals the exact syscall where it is blocked.

#### 26. `tcpdump` (Packet Analyzer)
- **Syntax**: `tcpdump -i eth0 -nn -s0 -vv 'port 443 and host 10.0.1.5'`
- **SRE Use Case**: Analyzing dropped packets, TLS resets, and handshake latency.

#### 27. `dmesg` (Driver Message Buffer)
- **Syntax**: `dmesg -T | grep -iE "oom|segfault|error"`
- **SRE Use Case**: Investigating kernel-level panics, hardware driver errors, and OOM kills.

#### 28. `nc` (Netcat)
- **Syntax**: `nc -zv 10.0.2.15 5432`
- **SRE Use Case**: Verifying raw TCP port connectivity through firewalls.

#### 29. `ip` (Network Device & Route Management)
- **Syntax**: `ip addr show`, `ip route show`
- **SRE Use Case**: Inspecting interface IP bindings, MTU configurations, and routing tables.

#### 30. `tar` / `gzip` / `zcat`
- **Syntax**: `zcat /var/log/nginx/access.log.2.gz | grep " 500 "`
- **SRE Use Case**: Searching historical compressed log archives without unpacking them to disk.

### 3.9 Ten Real-World Linux Troubleshooting Labs with Full Solutions

#### Lab 1: High CPU Utilization Investigation
- **Problem**: Host alerting CPU utilization $> 98\%$.
- **Symptoms**: High latency on web requests; SSH connection sluggish.
- **Investigation**:
  ```bash
  # 1. Identify which processes are consuming CPU
  top -b -n 1 | head -n 20
  # 2. Check if CPU is in user space (us) or system space (sy)
  # High 'us' means application calculation/infinite loop
  # High 'sy' means kernel context switching, memory allocation, or syscall storms
  mpstat -P ALL 1 3
  # 3. If a specific PID is spinning, inspect its running threads
  top -H -p <PID>
  # 4. Profile the process to find the exact function
  perf top -p <PID>
  ```
- **Root Cause**: A worker thread encountered an unhandled exception in an infinite `while True:` loop without a backoff/sleep condition.
- **Fix**: Kill process gracefully (`kill -15 <PID>`), deploy patch adding proper loop termination and circuit breaking.
- **Prevention**: Enforce CPU quotas via cgroups/Kubernetes `resources.limits.cpu`.

#### Lab 2: Out of Memory (OOM) Killed Process
- **Problem**: Python API process vanishes spontaneously without writing an error log.
- **Symptoms**: HTTP 502 Bad Gateway from reverse proxy; container restarts.
- **Investigation**:
  ```bash
  # 1. Check kernel ring buffer for OOM events
  dmesg -T | grep -i "killed process"
  # 2. Check journald system logs
  journalctl -xb | grep -i oom
  # 3. Verify process memory limits vs system memory
  free -h
  cat /proc/meminfo
  ```
- **Root Cause**: Python process loaded a 4GB CSV export into memory simultaneously across 10 concurrent requests, exhausting the 8GB host limit. Kernel OOM killer terminated the process.
- **Fix**: Stream large file processing using Python chunking/generators; configure pagination.
- **Prevention**: Set `resources.limits.memory` in Kubernetes and implement New Relic Infrastructure alerts on memory usage $> 85\%$.

#### Lab 3: Disk Full (No Space Left on Device) with Open Deleted Files
- **Problem**: Service fails with `IOError: [Errno 28] No space left on device`, but `du -sh /*` accounts for only 40% of the disk.
- **Symptoms**: `df -h` shows `/var/log` at $100\%$ capacity.
- **Investigation**:
  ```bash
  # Check for unlinked files that are still held open by running processes
  lsof +L1 | grep deleted
  ```
- **Root Cause**: A junior engineer ran `rm /var/log/app.log` while the application was actively logging to it. In Linux, deleting a file removes its directory entry, but the disk blocks are *not* freed until all processes holding open file descriptors close them!
- **Fix**: Truncate the file via its open file descriptor without restarting the process:
  ```bash
  # Find the PID and FD from lsof (e.g., PID 1420, FD 3)
  : > /proc/1420/fd/3
  ```
- **Prevention**: Use logrotate with `copytruncate` directive.

#### Lab 4: Zombie Process Accumulation
- **Problem**: System cannot spawn new processes (`fork: retry: Resource temporarily unavailable`).
- **Symptoms**: Process table is saturated with `[app] <defunct>` entries.
- **Investigation**:
  ```bash
  ps aux | grep 'Z'
  # Find the parent process responsible for creating and abandoning zombies
  ps -o ppid,pid,stat,cmd -C defunct
  ```
- **Root Cause**: A custom Python multiprocessing supervisor spawned worker children but failed to register a `SIGCHLD` signal handler or call `os.wait()` / `os.waitpid()` to reap terminated children.
- **Fix**: Send `SIGHUP` or restart the parent process so orphaned zombies are inherited and reaped by PID 1 (`systemd` or `tini`).
- **Prevention**: In Docker containers, always use an init daemon such as `tini` (`ENTRYPOINT ["/usr/bin/tini", "--"]`).

#### Lab 5: Service Fails to Start (systemd Debugging)
- **Problem**: `systemctl start api.service` fails with `Job for api.service failed because the control process exited with error code`.
- **Symptoms**: Service in `failed` state.
- **Investigation**:
  ```bash
  # 1. Check exit code and systemd status
  systemctl status api.service -l
  # 2. View exact failure logs from journald
  journalctl -u api.service -e --no-pager
  # 3. Test execution manually as the configured service user
  sudo -u appuser /opt/app/venv/bin/python /opt/app/server.py
  ```
- **Root Cause**: The service environment file `/etc/app.env` was owned by `root:root` with permissions `0600`, preventing the `appuser` from reading database secrets.
- **Fix**: `chown appuser:appgroup /etc/app.env && chmod 600 /etc/app.env`
- **Prevention**: Automated configuration validation in CI/CD pipeline.

#### Lab 6: Port Already in Use (Address Already in Use: EADDRINUSE)
- **Problem**: Application server crashes on startup: `OSError: [Errno 98] Address already in use`.
- **Symptoms**: Deployment rollback fails.
- **Investigation**:
  ```bash
  # Identify which process is holding port 8000
  ss -tulpn | grep :8000
  # Alternatively with lsof
  lsof -i :8000
  ```
- **Root Cause**: A previous instance of the Python Gunicorn server hung during shutdown and was still bound to `0.0.0.0:8000`.
- **Fix**:
  ```bash
  kill -15 <PID>
  # If still stuck after 10 seconds:
  kill -9 <PID>
  ```
- **Prevention**: Configure `SO_REUSEADDR` in socket configuration and configure graceful termination timeouts in systemd (`TimeoutStopSec=30`).

#### Lab 7: Permission Denied Despite Correct Permissions (SELinux / ACL Issue)
- **Problem**: Web server returns HTTP 403 Forbidden reading `/var/www/data.json` despite file permissions being `777`.
- **Symptoms**: User `nginx` has read permissions, but `open()` syscall returns `EACCES`.
- **Investigation**:
  ```bash
  # 1. Check Access Control Lists (ACLs)
  getfacl /var/www/data.json
  # 2. Check SELinux security context
  ls -lZ /var/www/data.json
  # 3. Check audit log for SELinux denials
  ausearch -m avc -ts recent
  ```
- **Root Cause**: SELinux was enforcing policy, and the file context was `default_t` instead of `httpd_sys_content_t`.
- **Fix**:
  ```bash
  restorecon -v /var/www/data.json
  ```
- **Prevention**: Manage infrastructure via Terraform and Ansible with predefined SELinux context tasks.

#### Lab 8: Network Connectivity Failure (Routing & Firewalls)
- **Problem**: Application cannot connect to RDS database at `10.0.5.20:5432`.
- **Symptoms**: `Connection timed out` after 30 seconds.
- **Investigation**:
  ```bash
  # 1. Verify routing table
  ip route get 10.0.5.20
  # 2. Test TCP handshake
  nc -zv -w 3 10.0.5.20 5432
  # 3. Check local iptables/nftables firewall rules
  sudo iptables -L -n -v
  # 4. Trace the network path
  traceroute -n -T -p 5432 10.0.5.20
  ```
- **Root Cause**: The AWS Security Group attached to the RDS instance did not permit ingress on port 5432 from the application subnet CIDR.
- **Fix**: Update AWS Security Group ingress rule to allow `10.0.1.0/24` on port `5432`.
- **Prevention**: Define security group rules declaratively in Terraform with module tests.

#### Lab 9: High Load Average with Low CPU Utilization (Uninterruptible Sleep)
- **Problem**: Load average spikes to 45 on an 8-core machine, but CPU usage is only 4%.
- **Symptoms**: Commands like `ls` freeze indefinitely; users cannot write files.
- **Investigation**:
  ```bash
  # Check for processes in 'D' state
  ps aux | awk '$8 ~ /D/'
  # Inspect stack trace of the blocked process
  cat /proc/<PID>/stack
  ```
- **Root Cause**: An NFS storage server lost network connectivity. Processes writing to the mount point entered uninterruptible kernel sleep (`nfs_wait_bit_uninterruptible`).
- **Fix**: Remount NFS with `soft` and `intr` flags, or restore network connectivity to the NFS filer.
- **Prevention**: Mount external storage with timeouts (`timeo=30`) and monitor NFS export latency in New Relic.

#### Lab 10: Process Consuming Excessive File Descriptors (EMFILE)
- **Problem**: API starts throwing `OSError: [Errno 24] Too many open files`.
- **Symptoms**: Web server rejects new incoming HTTP connections.
- **Investigation**:
  ```bash
  # 1. Count open file descriptors for the process
  ls -1 /proc/<PID>/fd | wc -l
  # 2. Check process limits
  cat /proc/<PID>/limits | grep "open files"
  # 3. Inspect what the descriptors are pointing to
  lsof -p <PID> | awk '{print $5}' | sort | uniq -c | sort -nr
  ```
- **Root Cause**: Python application was opening outbound HTTP connections without a connection pool or `with` context manager, leaking sockets in `ESTABLISHED` or `CLOSE_WAIT` states until hitting the 1024 limit.
- **Fix**: Increase limit immediately:
  ```bash
  prlimit --pid=<PID> --nofile=65536:65536
  ```
- **Prevention**: Refactor Python code to use `urllib3.PoolManager` or `httpx.Client()` as a singleton session.

---

# 4. Networking for SRE

### 4.1 OSI Model vs TCP/IP Stack in Production

```
+------------------------------------+------------------------------------+
|            OSI 7-Layer             |           TCP/IP 4-Layer           |
+------------------------------------+------------------------------------+
| 7. Application (HTTP, DNS, gRPC)   |                                    |
| 6. Presentation (TLS, JSON)        | Application Layer                  |
| 5. Session (Sockets, RPC sessions) |                                    |
+------------------------------------+------------------------------------+
| 4. Transport (TCP, UDP)            | Transport Layer (TCP, UDP)         |
+------------------------------------+------------------------------------+
| 3. Network (IP, ICMP, BGP, ARP)    | Internet Layer (IPv4, IPv6, ICMP)  |
+------------------------------------+------------------------------------+
| 2. Data Link (Ethernet, MAC, VLAN) | Network Access / Link Layer        |
| 1. Physical (Fiber, Copper, Wi-Fi) |                                    |
+------------------------------------+------------------------------------+
```

*SRE Mental Model*:
When debugging an outage, troubleshoot **bottom-up**:
1. *Link/Physical*: Is the network interface up? (`ip link show`)
2. *Network*: Can we route to the IP? (`ping`, `traceroute`, `ip route`)
3. *Transport*: Is the port listening? Is the TCP handshake completing? (`ss -tulpn`, `nc -zv`)
4. *Application*: Is TLS valid? Is the HTTP status code 200? (`curl -Iv`)

### 4.2 TCP Deep Dive: Handshake, Windowing, Teardown, and Socket States

TCP is a connection-oriented, reliable, byte-stream transport protocol.

#### 1. The Three-Way Handshake
```
Client                                     Server
  |                                          |
  | -------- SYN (seq=X) ------------------> | [Listen Queue]
  |                                          |
  | <------- SYN-ACK (seq=Y, ack=X+1) ------ |
  |                                          |
  | -------- ACK (seq=X+1, ack=Y+1) -------> | [Accept Queue]
  |                                          |
  | [Connection Established]                 | [Connection Established]
```
- **SYN Flood**: An attacker sends thousands of `SYN` packets from spoofed IPs without returning the final `ACK`. The server's `syn_backlog` fills up, rejecting legitimate traffic.
- **Defense**: Enable SYN cookies (`net.ipv4.tcp_syncookies = 1`).

#### 2. Flow Control & Congestion Control
- **TCP Windowing**: The receiver advertises its available buffer space (`rwnd`). The sender cannot send more bytes than the receiver can buffer.
- **Congestion Control**: Algorithms (Cubic, BBR) dynamically measure network round-trip time (RTT) and packet drops to scale the congestion window (`cwnd`).

#### 3. Connection Teardown & TIME_WAIT State
```
Client (Initiates Close)                    Server
  |                                          |
  | -------- FIN (seq=A) ------------------> |
  | <------- ACK (ack=A+1) ----------------- |
  |                                          |
  | <------- FIN (seq=B) ------------------- |
  | -------- ACK (ack=B+1) ----------------> |
  |                                          |
[TIME_WAIT: 2 * MSL = 60s]                   [CLOSED]
```
- **Why TIME_WAIT exists**: To ensure delayed packets from the old connection do not corrupt a new connection reusing the same 4-tuple (Source IP, Source Port, Dest IP, Dest Port).
- **SRE Danger**: In high-throughput microservices opening and closing millions of short-lived connections, ephemeral ports ($32768 - 60999 \approx 28,000$ ports) get exhausted in `TIME_WAIT`.
- **Solution**: Use HTTP Keep-Alive connection pools!

### 4.3 DNS Architecture, Record Types, TTL, and Resolution Flow

DNS (Domain Name System) is a globally distributed hierarchical database.

```
                  . (Root Servers)
                         |
                .com / .io / .org (TLD)
                         |
           example.com (Authoritative Servers)
```

#### Core DNS Record Types
- **A**: Maps a hostname to an IPv4 address (`api.example.com -> 93.184.216.34`).
- **AAAA**: Maps a hostname to an IPv6 address.
- **CNAME (Canonical Name)**: Alias pointing one name to another (`www.example.com -> example.com`). *Note*: CNAME cannot coexist with other records at the apex/zone root.
- **MX**: Mail exchange routing.
- **TXT**: Text data used for domain ownership validation, SPF, and DKIM.
- **NS**: Identifies the authoritative nameservers for the domain.
- **PTR**: Reverse DNS lookup (IP to hostname).
- **SOA (Start of Authority)**: Zone metadata, administrator email, serial number, and refresh timers.

#### TTL (Time To Live) Strategy for SRE
- **High TTL (e.g., 86400s / 24h)**: Reduces DNS query traffic, speeds up user lookups via ISP cache. *Problem*: If you need to failover to a disaster recovery IP, users are stuck for 24 hours!
- **Low TTL (e.g., 60s - 300s)**: Essential for production APIs using DNS-based failover (AWS Route 53 latency/failover routing).

### 4.4 HTTP/1.1, HTTP/2, HTTP/3, and the TLS 1.3 Handshake

1. **HTTP/1.1**: Persistent connections, chunked transfer. Suffers from **Head-of-Line (HoL) Blocking** at the application layer (only 1 request per TCP socket at a time).
2. **HTTP/2**: Binary framing, multiplexing (multiple requests/responses concurrently over a single TCP connection), header compression (HPACK).
3. **HTTP/3**: Uses **QUIC** over UDP instead of TCP. Eliminates TCP Head-of-Line blocking (packet drop on stream 1 does not freeze stream 2) and supports instantaneous connection migration across IP changes (e.g., mobile Wi-Fi to 5G).

#### The TLS 1.3 Handshake
TLS 1.3 reduced handshake latency from 2 Round Trips (2-RTT in TLS 1.2) to **1-RTT**:
```
Client                                     Server
  |                                          |
  | --- ClientHello (Key Share, Ciphers) --> |
  |                                          |
  | <-- ServerHello (Key Share, Cert, Enc) - | [Derives Session Keys]
  |                                          |
  | === Encrypted Application Data (HTTP) == |
```

### 4.5 Load Balancing, Reverse Proxies, and CDNs

- **Layer 4 Load Balancer (Transport Layer)**: Routes traffic based on IP and Port (TCP/UDP) without terminating TLS or inspecting HTTP headers. Ultra-high throughput, minimal latency (e.g., AWS NLB, IPVS).
- **Layer 7 Load Balancer (Application Layer)**: Terminates TLS, inspects HTTP paths, headers, cookies, and routes traffic intelligently (e.g., AWS ALB, Nginx, Envoy, HAProxy).
- **Content Delivery Network (CDN)**: Geographically distributed edge cache network (Cloudflare, Fastly, AWS CloudFront). Serves static assets and caches API responses at edge points of presence (PoPs) close to users, offloading origin servers.

### 4.6 SRE Networking Diagnostics Toolkit

```bash
# 1. Query DNS records and inspect query time
dig +trace +nocmd api.example.com A
# 2. Test TLS certificate expiration and cipher suite
openssl s_client -connect api.example.com:443 -servername api.example.com < /dev/null 2>/dev/null | openssl x509 -noout -dates -issuer -subject
# 3. High-precision HTTP timing
curl -w "\nLookup time:\t%{time_namelookup}\nConnect time:\t%{time_connect}\nAppCon time:\t%{time_appconnect}\nPreTransfer:\t%{time_pretransfer}\nStartTransfer:\t%{time_starttransfer}\nTotal time:\t%{time_total}\n" -o /dev/null -s https://api.example.com/health
# 4. Capture TCP packets on specific port
sudo tcpdump -i any -nn -c 10 'tcp[tcpflags] & (tcp-syn|tcp-fin|tcp-rst) != 0 and port 443'
```

### 4.7 Eight Production Networking Incident Scenarios with Investigations

#### Scenario 1: DNS Resolution Failing (NXDOMAIN vs SERVFAIL)
- **Symptoms**: Applications log `gaierror: [Errno -2] Name or service not known`.
- **Investigation**:
  ```bash
  # Test with local resolver
  dig api.internal.corp
  # Test directly against authoritative server
  dig @10.0.0.2 api.internal.corp
  # Check system resolver configuration
  cat /etc/resolv.conf
  ```
- **Root Cause**: `resolv.conf` contained an obsolete nameserver IP following a VPC subnet migration, and `ndots:5` in Kubernetes configuration caused excessive recursive lookup storms hitting rate limits.
- **Fix**: Update DHCP option set / CoreDNS config; set `ndots:2`.

#### Scenario 2: API Returning HTTP 502 Bad Gateway
- **Symptoms**: Reverse proxy (Nginx) returns 502 to clients.
- **Investigation**:
  ```bash
  # Check reverse proxy error log
  grep "502" /var/log/nginx/error.log
  # Test upstream application socket directly
  curl -Iv http://127.0.0.1:8080/health
  ```
- **Root Cause**: Nginx error log shows: `connect() failed (111: Connection refused) while connecting to upstream`. The backing Python process crashed due to an unhandled exception and was not restarted.
- **Fix**: Restart upstream daemon; implement systemd `Restart=always`.

#### Scenario 3: API Returning HTTP 504 Gateway Timeout
- **Symptoms**: Client requests hang for exactly 60 seconds, then return 504.
- **Investigation**:
  ```bash
  # Inspect upstream processing latency
  journalctl -u backend.service --since "10 minutes ago"
  # Check slow query log on database
  tail -n 50 /var/log/postgresql/postgresql.log
  ```
- **Root Cause**: An upstream PostgreSQL database had a table lock on `orders` during an unindexed query. The backend request exceeded Nginx's `proxy_read_timeout 60s`.
- **Fix**: Kill blocking SQL query; optimize database index; adjust timeout.

#### Scenario 4: Server Reachable via Ping but Port Unavailable
- **Symptoms**: `ping 10.0.1.50` succeeds ($< 1\text{ ms}$), but `curl http://10.0.1.50:8080` times out.
- **Investigation**:
  ```bash
  # 1. Check if application is listening on 0.0.0.0 vs 127.0.0.1
  ss -tulpn | grep 8080
  # 2. Check host iptables
  iptables -L -n -v | grep 8080
  ```
- **Root Cause**: The Python web application was started with `app.run(host="127.0.0.1")` instead of `host="0.0.0.0"`. It was only accepting connections originating from the local loopback interface.
- **Fix**: Bind to `0.0.0.0` or `::`.

#### Scenario 5: TLS Certificate Validation Error
- **Symptoms**: Microservices fail to communicate: `SSL: CERTIFICATE_VERIFY_FAILED`.
- **Investigation**:
  ```bash
  openssl s_client -connect auth.service:443 -showcerts
  ```
- **Root Cause**: The TLS certificate was renewed, but the intermediate CA certificate was omitted from the bundle. The browser had it cached, but backend Python clients (`requests`) failed strict verification.
- **Fix**: Concatenate the server certificate with the full intermediate certificate chain (`fullchain.pem`).

#### Scenario 6: High Network Latency & TCP Retransmissions
- **Symptoms**: API latency jumps from 15ms to 450ms intermittently.
- **Investigation**:
  ```bash
  # Check interface packet drops and errors
  netstat -s | grep -i retrans
  # Measure MTU path
  tracepath -n 10.0.2.100
  ```
- **Root Cause**: Path MTU Discovery (PMTUD) black hole. A router along the path had an MTU of 1420 bytes, but ICMP Type 3 Code 4 ("Fragmentation Needed") was blocked by an overly aggressive firewall.
- **Fix**: Allow ICMP fragmentation needed packets; set clamp-mss on routers.

#### Scenario 7: Connection Timeout (Silent Drop)
- **Symptoms**: `curl -v http://192.168.10.5` hangs indefinitely until client timeout.
- **Investigation**:
  ```bash
  tcpdump -i any host 192.168.10.5 -nn
  ```
- **Root Cause**: `tcpdump` shows outgoing `SYN` packets, but zero incoming response packets (`SYN-ACK` or `RST`). This proves traffic is being silently dropped by a stateful packet filter (AWS Security Group or iptables `DROP`).
- **Fix**: Add ingress rule in AWS Security Group.

#### Scenario 8: Connection Refused (TCP RST)
- **Symptoms**: `curl http://10.0.1.50:9000` immediately returns `curl: (7) Failed to connect to 10.0.1.50 port 9000: Connection refused`.
- **Investigation**:
  ```bash
  tcpdump -i any port 9000 -nn
  ```
- **Root Cause**: `tcpdump` shows an immediate `RST` (Reset) packet returned from the destination host. This confirms the network and host are reachable, but no process is bound to port 9000.
- **Fix**: Start the target service daemon.

---

# 5. Git and GitHub for SRE

### 5.1 Git Internals: Objects, Trees, Commits, and References

Git is a content-addressable cryptographic filesystem stored inside the `.git` directory:
1. **Blob**: Stores pure file data, identified by the SHA-1/SHA-256 hash of its contents:
   $$\text{Hash} = \text{SHA1}(\text{"blob "} + \text{size} + \backslash 0 + \text{content})$$
2. **Tree**: Represents a directory. Contains a list of mode permissions, object types, hashes, and filenames.
3. **Commit**: Points to a root tree object, parent commit hashes, author/committer metadata, and the commit message.
4. **Refs**: Text files in `.git/refs/heads/` containing commit hashes pointing to branch tips. `HEAD` is a reference pointing to the currently checked-out branch or commit.

### 5.2 Branching Strategies: Trunk-Based Development vs GitFlow for SRE

- **GitFlow**: Involves long-lived branches (`develop`, `release`, `hotfix`, `main`).
  *SRE Critique*: Leads to massive merge conflicts, delayed releases, and batching of changes. Large batch sizes are the primary cause of production outages!
- **Trunk-Based Development (TBD)**: All engineers commit small, frequent changes directly to a single branch (`main`) or via short-lived feature branches ($< 24\text{ hours}$) gated by automated CI tests and **Feature Flags**.
  *SRE Endorsement*: TBD minimizes change batch size, accelerates MTTR, and makes rollbacks trivial.

### 5.3 Rebasing, Merging, Cherry-Picking, Reset vs Revert

#### Rebase vs Merge
- `git merge feature`: Creates a non-linear history with a merge commit. Preserves exact history.
- `git rebase main`: Replays feature commits on top of the latest `main`, creating a completely linear history. *SRE Rule*: Never rebase commits that have already been pushed to a shared public branch!

#### Reset vs Revert
- `git reset --hard HEAD~1`: Destructively rewrites local commit history. Dangerous in production!
- `git revert <commit_hash>`: Creates a **new commit** that applies the exact inverse diff of the target commit. *SRE Rule*: Always use `git revert` to roll back changes in production repositories to preserve audit logs and prevent desynchronizing other engineers' clones.

#### Cherry-Pick
- `git cherry-pick <commit_hash>`: Applies a specific single commit from another branch onto your current branch. Essential for backporting critical production security fixes to a release branch.

### 5.4 Conflict Resolution, Pull Request Reviews, and Operability Standards

When reviewing Infrastructure as Code (Terraform) or SRE automation (Python) pull requests, enforce an **Operability Checklist**:
1. *Observability*: Does this change add metrics, logs, and trace context?
2. *Rollback Plan*: Can this change be reverted via git or feature flag without data corruption?
3. *Idempotency*: Can this script or Terraform module be applied multiple times safely?
4. *Secret Safety*: Are there any hardcoded tokens, passwords, or private keys?
5. *Failure Modes*: What happens if the database, network, or external API is down when this runs?

### 5.5 GitHub Actions Workflows for Infrastructure and Operations

GitHub Actions allows declarative, event-driven CI/CD automation stored in `.github/workflows/`.

```yaml
# .github/workflows/sre_python_ci.yml
name: SRE Automation CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff mypy pytest -r requirements.txt

      - name: Lint with Ruff
        run: ruff check .

      - name: Static Type Check with Mypy
        run: mypy --strict .

      - name: Run Test Suite with Pytest
        run: pytest -v --cov=src tests/
```

### 5.6 Practical Exercises and Solutions

#### Exercise 1: Emergency Git Rollback in Production
**Scenario:** A broken Terraform commit (`a3f89b1`) was pushed to `main` and broke the staging environment.
**Task:** Roll back the change cleanly without rewriting public history.
**Solution:**
```bash
git checkout main
git pull origin main
# Create revert commit
git revert --no-edit a3f89b1
# Push immediately to trigger automated CI/CD pipeline
git push origin main
```

#### Exercise 2: Resolving a Merge Conflict
**Scenario:** Two SREs modified the same line in `deploy.sh`.
**Task:** Resolve the conflict cleanly and verify changes.
**Solution:**
```bash
git checkout feature/fix-healthcheck
git fetch origin
git rebase origin/main
# Git halts with: CONFLICT (content): Merge conflict in deploy.sh
# Open deploy.sh, resolve <<<<<<< HEAD vs >>>>>>> markers
# Stage resolved file
git add deploy.sh
# Continue rebase
git rebase --continue
# Push to feature branch with lease
git push --force-with-lease origin feature/fix-healthcheck
```
'''
