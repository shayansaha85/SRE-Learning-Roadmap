"""
Curriculum Builder - Part 6: Sections 39 & 40
Ten Progressive SRE Projects & Comprehensive Failure Injection / Chaos Engineering Labs
"""

def get_part6_content() -> str:
    return r'''# 39. Ten Progressive SRE Projects

This section outlines a complete 10-project path that transforms an engineer into a production-grade SRE with specialization in Python automation and New Relic observability.

---

### Project 1: Python Server Health Monitor
- **Objective**: Build a standalone Linux daemon that continuously samples system vital signs, detects resource exhaustion, and writes structured JSON logs.
- **Architecture**: A Python CLI application using `psutil`, running as a background `systemd` service with non-blocking intervals.
- **Requirements**: Python 3.10+, Linux host or VM, `psutil`.
- **Folder Structure**:
  ```text
  server-monitor/
  ├── monitor.py
  ├── config.yaml
  ├── systemd/
  │   └── server-monitor.service
  └── requirements.txt
  ```
- **Complete Code (`monitor.py`)**:
  ```python
  #!/usr/bin/env python3
  import psutil
  import time
  import json
  import logging
  from pathlib import Path

  logging.basicConfig(level=logging.INFO, format='%(message)s')

  def capture_metrics() -> dict:
      mem = psutil.virtual_memory()
      cpu_pct = psutil.cpu_percent(interval=1.0)
      disk = psutil.disk_usage('/')
      return {
          "timestamp": int(time.time()),
          "cpu_percent": cpu_pct,
          "memory_available_mb": mem.available // (1024**2),
          "memory_used_percent": mem.percent,
          "disk_used_percent": disk.percent
      }

  if __name__ == "__main__":
      while True:
          data = capture_metrics()
          logging.info(json.dumps(data))
          time.sleep(5)
  ```
- **Deployment**: Install systemd unit to `/etc/systemd/system/server-monitor.service`, enable and start via `systemctl enable --now server-monitor`.
- **Testing & Failure Injection**: Inject CPU load with `stress-ng --cpu 4 --timeout 30s`; verify CPU spike is logged in real time.
- **Expected Results**: Continuous JSON stream of telemetry without memory leaks.

---

### Project 2: High-Throughput Python API Synthetic Monitoring Tool
- **Objective**: Build a multi-threaded synthetic API prober that tests HTTP endpoints, checks assertions, measures latency percentiles, and alerts on SLO breaches.
- **Architecture**: `httpx` async client probing 50 endpoints concurrently, calculating p90/p99 response times.
- **Requirements**: `httpx`, `pytest`, Python 3.11+.
- **Folder Structure**:
  ```text
  api-prober/
  ├── prober.py
  ├── targets.json
  └── tests/
      └── test_prober.py
  ```
- **Code & Usage**: See Section 10 for complete async engine implementation.
- **Advanced Version**: Export results directly to New Relic Metric API via HTTP POST.

---

### Project 3: Microservice with PostgreSQL & New Relic APM
- **Objective**: Build a high-performance FastAPI service connected to PostgreSQL, instrumented with New Relic APM, custom transaction attributes, and health probes.
- **Architecture**:
  ```text
  Client -> FastAPI App (New Relic Agent) -> PostgreSQL Database
  ```
- **Folder Structure**:
  ```text
  payment-service/
  ├── app/
  │   ├── main.py
  │   ├── database.py
  │   └── models.py
  ├── newrelic.ini
  ├── Dockerfile
  └── requirements.txt
  ```
- **Complete Code (`app/main.py`)**:
  ```python
  from fastapi import FastAPI, HTTPException
  import newrelic.agent
  import asyncpg
  import os

  app = FastAPI()

  @app.get("/orders/{order_id}")
  async def get_order(order_id: int):
      newrelic.agent.add_custom_attribute("order_id", order_id)
      # Database query logic
      return {"order_id": order_id, "status": "CONFIRMED"}
  ```
- **Monitoring**: Verify transaction throughput, Apdex, and database query breakdown inside New Relic APM console.

---

### Project 4: Production Dockerized Python Microservice
- **Objective**: Containerize the Python service using multi-stage builds, non-root users, dumb-init/tini process reaping, and minimal attack surface.
- **Implementation**: Follow the Dockerfile specification provided in Section 11.3.
- **Testing**: Run vulnerability scans using `trivy image payment-api:latest`. Ensure zero HIGH or CRITICAL CVEs.

---

### Project 5: Kubernetes Production Deployment
- **Objective**: Deploy the containerized application onto a Kubernetes cluster with High Availability, Pod Anti-Affinity, RollingUpdates, and Resource Limits.
- **Folder Structure**:
  ```text
  k8s-manifests/
  ├── deployment.yaml
  ├── service.yaml
  ├── hpa.yaml
  └── ingress.yaml
  ```
- **Failure Injection**: Kill random pods with `kubectl delete pod` during high-volume curl tests; verify zero dropped requests due to preStop hooks and readiness probes.

---

### Project 6: Kubernetes Observability with New Relic
- **Objective**: Deploy New Relic Kubernetes integration to monitor Cluster, Node, Pod, and Container metrics, correlating Kubernetes events with APM transactions.
- **Implementation**: Deploy `nri-bundle` via Helm. Build NRQL dashboards querying `K8sContainerSample` and `K8sPodSample`.

---

### Project 7: Infrastructure as Code with Terraform & AWS
- **Objective**: Provision an enterprise AWS VPC across 3 Availability Zones, public/private subnets, NAT Gateways, EKS cluster, and New Relic alert conditions purely in Terraform.
- **Implementation**: Follow the Terraform specification in Section 16.2.

---

### Project 8: End-to-End Enterprise CI/CD Pipeline
- **Objective**: Build a GitHub Actions workflow that executes linting, type-checking, automated unit testing, container build, security scanning, Kubernetes deployment, and records a New Relic Deployment Marker.
- **Implementation**: Reference Section 15.2.

---

### Project 9: Python + New Relic Autonomous Remediation Daemon
- **Objective**: Build an autonomous webhook consumer that receives New Relic alert notifications, queries NerdGraph for root-cause telemetry, and executes controlled remediations.
- **Implementation**: Reference the complete script in Section 28.2.

---

### Project 10: Self-Healing Kubernetes SRE Platform
- **Objective**: Build an enterprise self-healing operator that detects CrashLoopBackOff and OOMKilled pods, isolates offending deployments, rolls back bad revisions, and sends a comprehensive postmortem summary to Slack.
- **Architecture**:
  ```text
  New Relic Alert -> Webhook Receiver -> Python SRE Engine -> K8s API Rollback -> Slack Bot
  ```

---

# 40. Chaos Engineering & Failure Injection Labs

### 40.1 Principles of Chaos Engineering
1. Build a hypothesis around steady-state behavior.
2. Simulate realistic real-world events (hardware failure, network latency, disk exhaustion).
3. Minimize blast radius (run tests in staging or off-peak production).
4. Automate experiments to run continuously.

### 40.2 Safe Local Failure Injection Labs

```bash
# Lab 1: CPU Exhaustion (Simulate Runaway Loop)
# Saturates 4 CPU cores at 100% for 60 seconds
stress-ng --cpu 4 --timeout 60s
# Diagnosis: top -b -n 1, New Relic SystemSample cpuPercent

# Lab 2: Physical Memory Exhaustion (Trigger Kernel OOM Killer)
# Allocates 4GB of RAM aggressively
stress-ng --vm 2 --vm-bytes 2G --timeout 30s
# Diagnosis: dmesg -T | grep -i oom, New Relic memoryAvailablePercent

# Lab 3: Disk Space Saturation
# Instantly fills 20GB of disk space
fallocate -l 20G /var/log/filler_test.img
# Diagnosis: df -h, New Relic StorageSample

# Lab 4: Artificial Network Latency & Packet Loss
# Injects 250ms of network delay and 10% packet drop on interface eth0
sudo tc qdisc add dev eth0 root netem delay 250ms loss 10%
# Diagnosis: ping, traceroute, New Relic NetworkSample
# Teardown: sudo tc qdisc del dev eth0 root

# Lab 5: DNS Failure Simulation
# Block outbound DNS lookups
sudo iptables -A OUTPUT -p udp --dport 53 -j DROP
# Diagnosis: dig api.example.com, Python gaierror
# Teardown: sudo iptables -D OUTPUT -p udp --dport 53 -j DROP

# Lab 6: Simulating HTTP 500 / 502 / 504 with Nginx / Python
# Configure Nginx return directive
# location /fail500 { return 500 "Internal Server Error Simulation"; }
# location /fail502 { return 502 "Bad Gateway Simulation"; }
# location /fail504 { return 504 "Gateway Timeout Simulation"; }
```
'''
