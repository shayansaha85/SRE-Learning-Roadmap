"""
Curriculum Builder - Part 3: Sections 12 to 16
AWS for SRE, Docker, Kubernetes Deep Dive (10 Labs), CI/CD (GitHub Actions), Terraform
"""

def get_part3_content() -> str:
    return r'''# 12. AWS for SRE

### 12.1 AWS as the Primary Enterprise Cloud

Amazon Web Services (AWS) is the dominant cloud platform in modern site reliability engineering. As an SRE, you must not simply know how to click the AWS Management Console; you must understand the failure modes, throttles, regional failure domains, and API limits of each managed service.

```
+-------------------------------------------------------------+
|               AWS SRE Core Infrastructure Stack             |
+-------------------------------------------------------------+
| Edge: Route 53 (DNS / Latency Routing) + CloudFront (CDN)   |
|                                |                            |
| Gateway: Application Load Balancer (ALB) / NLB (L4/L7)      |
|                                |                            |
| Compute: EKS / EC2 Auto Scaling / AWS Lambda                |
|                                |                            |
| Datastores: RDS Aurora Multi-AZ + DynamoDB + ElastiCache    |
|                                |                            |
| Storage & Queues: S3 + EBS + SQS + SNS                      |
|                                |                            |
| Telemetry: CloudWatch Metrics/Logs + CloudTrail             |
+-------------------------------------------------------------+
```

### 12.2 Compute Services

#### 1. EC2 (Elastic Compute Cloud)
- **What it does**: Provides resizable virtual compute instances across multiple availability zones.
- **Why SREs care**: Hosts Kubernetes worker nodes, legacy databases, and specialized workloads.
- **Instance Types**:
  - *Compute Optimized (c6i, c7g)*: High CPU-to-memory ratio. Best for API proxies, CPU-heavy microservices.
  - *Memory Optimized (r6i, r7g)*: High RAM-to-CPU ratio. Indispensable for Redis, Memcached, Elasticsearch.
  - *General Purpose (m6i, t4g)*: Balanced. *Danger*: Burstable `t`-series instances accumulate CPU credits. If exhausted, CPU performance is throttled to 20% baseline, creating severe production latency outages!
- **Common Failure Modes**: Instance hardware degradation (AWS retirement notice), EBS volume detachment, noisy neighbor contention.
- **Monitoring Metrics**: `CPUUtilization`, `StatusCheckFailed_System`, `StatusCheckFailed_Instance`, `EBSReadOps`.

#### 2. AWS Lambda (Serverless Compute)
- **What it does**: Event-driven execution of stateless functions with zero server management.
- **Why SREs care**: Powers automated remediation scripts, Slack chatops, event triggers, and API backends.
- **SRE Challenges**:
  - *Cold Starts*: Latency penalty when container initializes (can be $500\text{ ms} - 5\text{ s}$). Mitigated via Provisioned Concurrency.
  - *Concurrency Limits*: Account-level limit (default 1,000 concurrent executions). A runaway Lambda can starve all other serverless functions in the AWS account!
- **Monitoring Metrics**: `Invocations`, `Errors`, `Duration`, `Throttles`, `ConcurrentExecutions`.

#### 3. Auto Scaling Groups (ASG)
- **What it does**: Dynamically scales EC2 instance capacity up or down based on load metrics or health checks.
- **Scaling Policies**:
  - *Target Tracking*: Maintains metric at target (e.g., maintain average CPU at 60%).
  - *Step Scaling*: Increases capacity in discrete tiers based on CloudWatch alarm breaches.
  - *Cooldown Periods*: Prevents rapid over-provisioning ("flapping") by halting scaling actions for $N$ seconds post-scale.
- **Lifecycle Hooks**: Allows SREs to run draining scripts (e.g., `kubectl drain`) before AWS terminates an instance.

### 12.3 Networking Services

#### 1. VPC (Virtual Private Cloud) & Subnets
- Private, isolated virtual network defined by an IPv4/IPv6 CIDR block (e.g., `10.0.0.0/16`).
- **Public Subnet**: Route table points to an **Internet Gateway (IGW)**. Resources have public IPs.
- **Private Subnet**: Route table points to a **NAT Gateway** for outbound internet traffic. No direct inbound access from the public internet.

#### 2. NAT Gateway (Single vs Multi-AZ & Cost Optimization)
- *SRE Architecture Rule*: In production, deploy one NAT Gateway per Availability Zone! If you deploy a single NAT Gateway in `us-east-1a` and that AZ goes down, all private subnets across all AZs lose external internet access!
- *Cost Consideration*: NAT Gateway charges per GB processed. Terabytes of inter-service traffic routed through NAT gateways can generate surprise multi-thousand-dollar AWS bills. Use **VPC Endpoints (PrivateLink)** for S3, DynamoDB, and ECR to keep traffic internal and free!

#### 3. Security Groups vs NACLs
- **Security Groups**: Stateful virtual firewalls applied at the Elastic Network Interface (ENI) level. Return traffic is automatically allowed regardless of inbound rules.
- **Network ACLs (NACLs)**: Stateless packet filters applied at the subnet boundary. Must explicitly permit both inbound and outbound ports.

#### 4. Application Load Balancer (ALB)
- Layer 7 reverse proxy. Terminates TLS, supports path-based and host-based routing, gRPC, and HTTP/2.
- **Key SRE Settings**:
  - *Deregistration Delay (Connection Draining)*: Keeps in-flight requests alive for $N$ seconds (e.g., 30s) while removing unhealthy targets.
  - *Target Response Time*: Monitors upstream application latency.
  - *HTTP 5xx Alarms*: Alerts when ALB returns 502/504 vs when upstream target returns 500.

#### 5. Route 53 (Global DNS)
- High-availability DNS with 100% SLA.
- **Routing Policies**: Weighted (canary testing), Latency-Based (routes to lowest latency AWS region), Failover (active-passive disaster recovery), Geolocation.

### 12.4 Storage & Databases

#### 1. S3 (Simple Storage Service)
- Object storage offering 11 9s of durability ($99.999999999\%$).
- **Lifecycle Policies**: Automatically transition objects from Standard -> Infrequent Access (IA) -> Glacier -> Deep Archive to cut costs by up to 90%.
- **Versioning**: Protects against accidental deletion and ransomware.

#### 2. EBS (Elastic Block Store)
- Block storage volumes attached to EC2 instances.
- **gp3**: General Purpose SSD with baseline 3,000 IOPS and 125 MB/s throughput, independent of volume size.
- **io2 Block Express**: Mission-critical sub-millisecond databases requiring up to 256,000 IOPS.

#### 3. RDS (Relational Database Service) & Aurora
- **Multi-AZ Replication**: Synchronous physical block replication to an active-standby instance in an alternate AZ. Automatic failover takes 60–120 seconds.
- **Read Replicas**: Asynchronous replication for read-heavy scaling. *SRE Alert*: Monitor `ReplicaLag`! If replica lag spikes, users reading from replicas will receive stale data.

#### 4. DynamoDB (NoSQL Datastore)
- Fully managed key-value and document database.
- **Partition Keys**: Drives internal data sharding. *Anti-pattern*: Hot partition keys (e.g., routing all writes to `date=2026-09-04`) cause `ProvisionedThroughputExceededException`.
- **Capacity Modes**: On-Demand (pay-per-request for spiky traffic) vs Provisioned (predictable baseline workloads).

### 12.5 Messaging & Monitoring

#### 1. SQS (Simple Queue Service)
- Decouples microservices asynchronously.
- **Dead-Letter Queue (DLQ)**: Catches messages that fail processing after $N$ retry attempts (`maxReceiveCount`). SREs must alert on `ApproximateNumberOfMessagesVisible` on the DLQ!
- **Visibility Timeout**: The duration during which SQS prevents other consumers from receiving a message currently being processed. If processing takes longer than the timeout, duplicate processing occurs!

#### 2. CloudWatch & CloudTrail
- **CloudWatch Metrics & Alarms**: Ingests infrastructure telemetry; triggers SNS alerts and auto-scaling policies.
- **CloudTrail**: Complete immutable audit log of every AWS API call (who changed what, when, and from what IP). Indispensable for post-incident security forensics.

---

# 13. Docker & Containerization

### 13.1 Container Architecture & Kernel Isolation

A container is **not** a lightweight virtual machine. A container is simply a standard Linux process running with isolated kernel namespaces and metered resource limits via cgroups:

```
+-------------------------------------------------------------+
|                    Linux Container Isolation                |
+-------------------------------------------------------------+
| Namespaces (What can the process SEE?):                     |
| - PID: Private process tree (container PID 1 != host PID 1) |
| - NET: Private network stack (loopback, veth, IP, iptables) |
| - MNT: Private root filesystem mount (OverlayFS)             |
| - IPC: Private Inter-Process Communication & shared memory  |
| - UTS: Private Hostname and domain name                     |
| - USER: Maps container UID 0 (root) to unprivileged host UID|
+-------------------------------------------------------------+
| cgroups v2 (What can the process USE?):                     |
| - cpu.max: Limits CPU cycles per quota window (CFS)         |
| - memory.max: Hard memory ceiling (Triggers OOM Killer)     |
| - io.max: Disk read/write IOPS and byte limits              |
+-------------------------------------------------------------+
```

### 13.2 Docker Image Layers & Optimization

Docker images consist of a series of read-only layers stacked on top of each other using the **OverlayFS** union filesystem. When a container runs, Docker adds a thin read-write layer on top.

*SRE Optimization Rules*:
1. Order Dockerfile commands from **least frequently changing** to **most frequently changing** to maximize Docker layer cache hits.
2. Combine shell commands with `&&` to prevent intermediate layers from bloating the image size:
   ```dockerfile
   # Good SRE Practice
   RUN apt-get update && apt-get install -y --no-install-recommends \
       curl \
       && rm -rf /var/lib/apt/lists/*
   ```
3. Always use `.dockerignore` to exclude `.git`, `__pycache__`, `.env`, and local virtual environments.

### 13.3 Multi-Stage Builds

Multi-stage builds separate the build environment (compilers, build headers, git) from the production runtime image:
- Shrinks image size from 1.5GB to $< 80\text{ MB}$.
- Eliminates security attack surface by removing compilers (`gcc`), package managers, and shell utilities.

### 13.4 Essential 10 Docker Commands for SRE

```bash
# 1. Inspect real-time container resource consumption (CPU, Mem, Net I/O)
docker stats --no-stream
# 2. Inspect container metadata, cgroup limits, and IP address
docker inspect --format '{{json .NetworkSettings.Networks}}' <container_id>
# 3. Follow container logs with timestamps
docker logs -f --tail 100 -t <container_id>
# 4. Open interactive shell inside running container for debugging
docker exec -it <container_id> /bin/sh
# 5. List all running and stopped containers
docker ps -a --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}"
# 6. Build production image with build arguments
docker build -t api:v1.0.0 --build-arg APP_ENV=production .
# 7. Run container with strict resource limits and read-only rootfs
docker run -d --name payment-api -p 8080:8080 --memory="512m" --cpus="1.0" --read-only --tmpfs /tmp api:v1.0.0
# 8. Clean up unused container images, volumes, and networks
docker system prune -af --volumes
# 9. View layer history and sizes
docker history --human --format "{{.CreatedBy}}: {{.Size}}" api:v1.0.0
# 10. Graceful stop with 30-second timeout before SIGKILL
docker stop -t 30 <container_id>
```

---

# 14. Kubernetes — Deep Dive

### 14.1 Kubernetes Cluster Architecture

Kubernetes is a declarative, distributed container orchestrator designed to manage containerized workloads across a cluster of nodes.

```
+------------------------------------------------------------------------------------+
|                                CONTROL PLANE                                       |
|                                                                                    |
|   +-------------+       +-------------------------+       +--------------------+   |
|   |  etcd       |<----->| kube-apiserver          |<----->| kube-scheduler     |   |
|   | (Raft KV)   |       | (REST / Auth / State)   |       | (Node Placement)   |   |
|   +-------------+       +-------------------------+       +--------------------+   |
|                                     ^                                              |
|                                     |                     +--------------------+   |
|                                     +-------------------->| kube-controller-   |   |
|                                                           | manager            |   |
|                                                           +--------------------+   |
+------------------------------------------------------------------------------------+
                                      |
                     gRPC / mTLS TLS Communication
                                      |
+-------------------------------------+----------------------------------------------+
| WORKER NODE 1                                      | WORKER NODE 2                 |
|                                                    |                               |
| +------------------------------------------------+ | +---------------------------+ |
| | kubelet (Manages Pods via CRI)                 | | | kubelet                   | |
| +------------------------------------------------+ | +---------------------------+ |
| | kube-proxy (Manages iptables/IPVS service mesh)| | | kube-proxy                | |
| +------------------------------------------------+ | +---------------------------+ |
| | Container Runtime (containerd / CRI-O)         | | | Container Runtime         | |
| +------------------------------------------------+ | +---------------------------+ |
| | Pods / Containers                              | | | Pods / Containers         | |
| +------------------------------------------------+ | +---------------------------+ |
+----------------------------------------------------+-------------------------------+
```

1. **kube-apiserver**: The central brain. All components communicate exclusively with the API server via REST.
2. **etcd**: Consistent, highly-available key-value store (using Raft consensus) holding the entire cluster state.
3. **kube-scheduler**: Watches for unscheduled pods and selects the optimal worker node based on resource requests, affinities, and taints.
4. **kube-controller-manager**: Runs reconciliation loops (DeploymentController, ReplicaSetController, NodeController) that continuously compare **Current State** against **Desired State**.
5. **kubelet**: Agent running on each worker node. Communicates with the container runtime via the Container Runtime Interface (CRI) to launch pods, execute health probes, and report status.
6. **kube-proxy**: Programs host `iptables` or IPVS rules to load balance traffic destined for Kubernetes `Service` virtual IPs across backend Pod IPs.

### 14.2 Kubernetes Workloads & Primitives

- **Pod**: The smallest deployable computing unit. Encapsulates one or more containers sharing storage volumes, Linux network namespace, and IP address.
- **Deployment**: Declarative controller that manages declarative rollouts and rollbacks of ReplicaSets.
- **StatefulSet**: Manages stateful applications requiring unique network identities (`app-0`, `app-1`), ordered startup/shutdown, and dedicated PersistentVolumeClaims.
- **DaemonSet**: Ensures an exact single copy of a pod runs on every eligible worker node (used for New Relic Infrastructure agents, fluentd, node-exporter).
- **Service**: Abstraction defining a logical set of Pods and a policy to access them:
  - *ClusterIP*: Internal virtual IP accessible only within the cluster.
  - *NodePort*: Exposes service on a static high port (`30000-32767`) on every node's IP.
  - *LoadBalancer*: Provisions a cloud provider load balancer (AWS ALB/NLB).

### 14.3 Requests, Limits, and the Linux CFS Bandwidth Controller

```yaml
resources:
  requests:
    cpu: "250m"      # 0.25 core
    memory: "512Mi"  # 512 Megabytes
  limits:
    cpu: "1000m"     # 1 core
    memory: "1Gi"    # 1 Gigabyte
```

#### Why SREs Must Master Requests vs Limits:
1. **CPU Requests**: Used by `kube-scheduler` during node placement. In the kernel, translates to CPU shares (`cpu.weight`).
2. **CPU Limits**: Enforced by the kernel Completely Fair Scheduler (CFS) quota. If a pod exceeds its CPU limit, **the process is throttled, NOT killed**. Throttling causes sudden latency spikes!
3. **Memory Requests**: Reserves physical RAM on the node.
4. **Memory Limits**: Hard ceiling (`memory.max` in cgroups v2). If a pod allocates even 1 byte over its limit, the kernel **instantly terminates the container with OOMKilled (Exit Code 137)**!

### 14.4 Kubernetes Probes: Liveness, Readiness, Startup

```
Startup Probe: Has the application finished bootstrapping and warming caches?
     |
     v (Once succeeded, hand off to Liveness & Readiness)
Liveness Probe: Has the application deadlocked? (If failed -> KILL & RESTART container)
Readiness Probe: Is the application ready to accept traffic? (If failed -> CUT OFF traffic)
```

- **Production Mistake**: Placing database dependency checks inside the `livenessProbe`. If your PostgreSQL database has a temporary 10-second blip, all 50 application pods fail their liveness probes simultaneously, causing a cascading restart storm across the entire cluster!
- *Correct Rule*: Put database dependency checks in `readinessProbe` (stops sending traffic to pods). Keep `livenessProbe` strictly local to test if the web server thread loop is responsive.

### 14.5 Horizontal Pod Autoscaler (HPA)

The HPA controller runs periodically (every 15s) and adjusts deployment replicas based on observed CPU, memory, or custom metrics:
$$\text{Desired Replicas} = \lceil \text{Current Replicas} \times \frac{\text{Current Metric Value}}{\text{Target Metric Value}} \rceil$$

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: payment-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 14.6 Ten Production Kubernetes Troubleshooting Labs with Full Solutions

#### Lab 1: CrashLoopBackOff (Application Crash on Startup)
- **Problem**: Pod continuously restarts, transitioning to `CrashLoopBackOff`.
- **Symptoms**: `kubectl get pods` shows `RESTARTS: 8`, status `CrashLoopBackOff`.
- **Investigation**:
  ```bash
  # 1. View previous container termination logs
  kubectl logs <pod-name> --previous
  # 2. Inspect exit code and reason
  kubectl describe pod <pod-name>
  ```
- **Root Cause**: `kubectl logs --previous` reveals: `KeyError: 'DATABASE_PASSWORD'`. The application crashed immediately on startup because a required secret was missing from the ConfigMap/Secret.
- **Fix**: Add `DATABASE_PASSWORD` to the Kubernetes Secret.
- **Verification**: Pod transitions to `Running 1/1`.
- **Prevention**: Use Pydantic with fallback defaults; validate configs in CI/CD.

#### Lab 2: OOMKilled (Out Of Memory Termination - Exit Code 137)
- **Problem**: Pod terminates abruptly during traffic bursts.
- **Symptoms**: `Last State: Terminated`, `Reason: OOMKilled`, `Exit Code: 137`.
- **Investigation**:
  ```bash
  kubectl describe pod <pod-name> | grep -E "OOMKilled|Limits"
  kubectl top pod <pod-name>
  ```
- **Root Cause**: Memory limit was set to `256Mi`. Under peak load, in-flight JSON payload processing pushed memory to `260Mi`. Kernel cgroup triggered `OOMKilled`.
- **Fix**: Profile memory consumption using `tracemalloc`; increase memory limit to `512Mi`.
- **Verification**: Pod survives load tests without restart.
- **Prevention**: Set memory requests equal to memory limits (Guaranteed QoS class) for latency-critical stateful services; alert on container memory utilization $> 80\%$.

#### Lab 3: ImagePullBackOff / ErrImagePull
- **Problem**: New deployment fails to roll out pods.
- **Symptoms**: Status `ImagePullBackOff` or `ErrImagePull`.
- **Investigation**:
  ```bash
  kubectl describe pod <pod-name> | grep Events -A 10
  ```
- **Root Cause**: Events reveal: `Failed to pull image "ecr.aws/corp/api:v2.1.0": rpc error: code = Unknown desc = Error response from daemon: pull access denied, repository does not exist or may require 'docker login'`. The container repository was private, and the namespace lacked an `imagePullSecrets` reference.
- **Fix**: Create docker-registry secret and link to ServiceAccount:
  ```bash
  kubectl create secret docker-registry ecr-secret --docker-server=... --docker-username=... --docker-password=...
  kubectl patch serviceaccount default -p '{"imagePullSecrets": [{"name": "ecr-secret"}]}'
  ```
- **Verification**: Image pulls successfully; pod transitions to `Running`.

#### Lab 4: Pods Stuck in Pending State
- **Problem**: Pods created by HPA cannot be scheduled.
- **Symptoms**: `kubectl get pods` shows `Pending` for $> 15$ minutes.
- **Investigation**:
  ```bash
  kubectl describe pod <pod-name> | grep Events -A 5
  ```
- **Root Cause**: Events report: `0/6 nodes are available: 6 Insufficient cpu`. All cluster worker nodes have their CPU requests 100% allocated.
- **Fix**: Trigger cluster autoscaling (AWS Karpenter or Cluster Autoscaler) to provision new EC2 nodes, or reduce oversized CPU requests on non-critical workloads.
- **Verification**: New node joins cluster (`Ready`), and pending pods are scheduled immediately.

#### Lab 5: Failed Deployment & Stalled Rollout
- **Problem**: `kubectl rollout status deployment/api` hangs indefinitely.
- **Symptoms**: Old pods remain running; new ReplicaSet cannot reach ready state.
- **Investigation**:
  ```bash
  kubectl rollout status deployment/api
  kubectl get replicasets
  kubectl describe pod <new-replicaset-pod>
  ```
- **Root Cause**: The new version updated the readiness probe path to `/ready`, but the application code had implemented `/healthz`. Readiness probe failed continuously, preventing the Deployment controller from progressing the rolling update.
- **Fix**: Roll back immediately:
  ```bash
  kubectl rollout undo deployment/api
  ```
- **Verification**: Rollback completes; traffic continues without interruption.
- **Prevention**: End-to-end integration tests in ephemeral staging namespaces.

#### Lab 6: Service Unavailable (HTTP 503 / Endpoint Drop)
- **Problem**: Ingress returns HTTP 503; Service cannot route traffic.
- **Symptoms**: `curl http://api-service.prod.svc.cluster.local` returns Connection Refused.
- **Investigation**:
  ```bash
  # Check if Service has active Endpoints
  kubectl get endpoints api-service
  # Compare Service selector with Pod labels
  kubectl get svc api-service -o yaml | grep -A 3 selector
  kubectl get pods --show-labels
  ```
- **Root Cause**: The Service selector was `app: payment-api`, but the deployment label was typoed as `app: payments-api`. Zero endpoints were matched!
- **Fix**: Correct the selector in the Service YAML: `kubectl edit svc api-service`.
- **Verification**: `kubectl get endpoints api-service` now lists pod IP addresses.

#### Lab 7: Cluster DNS Resolution Failure
- **Problem**: Applications fail to resolve external or internal services: `EAI_AGAIN`.
- **Symptoms**: `nslookup kubernetes.default` times out.
- **Investigation**:
  ```bash
  # 1. Check CoreDNS pod status
  kubectl get pods -n kube-system -l k8s-app=kube-dns
  # 2. Check CoreDNS logs
  kubectl logs -n kube-system -l k8s-app=kube-dns
  ```
- **Root Cause**: CoreDNS pods were scheduled on a single worker node that crashed. Additionally, applications without `dnsConfig` were issuing 5 DNS queries per lookup due to `ndots:5`.
- **Fix**: Deploy CoreDNS across multiple nodes using `podAntiAffinity` and enable `NodeLocal DNSCache`.
- **Verification**: DNS lookup returns in $< 1\text{ ms}$.

#### Lab 8: Silent CPU Throttling
- **Problem**: API latency spikes under moderate load, but node CPU is only 30%.
- **Symptoms**: High p99 latency; zero errors.
- **Investigation**:
  ```bash
  # Query CFS throttling metrics from container cgroup
  kubectl exec -it <pod-name> -- cat /sys/fs/cgroup/cpu/cpu.stat
  # Look for nr_throttled and throttled_time
  ```
- **Root Cause**: Pod CPU limit was set to `500m`. In multi-threaded Python/Node runtimes, concurrent threads consumed the 500m quota in the first 20ms of the 100ms CFS quota period, leaving the process frozen for the remaining 80ms!
- **Fix**: Remove artificial CPU limits or increase CPU limits to `2000m`.
- **Verification**: `nr_throttled` stops incrementing; latency drops to baseline.

#### Lab 9: Node Eviction Due to Disk Pressure
- **Problem**: Multiple pods suddenly terminated across worker node `ip-10-0-1-50`.
- **Symptoms**: Pods in `Evicted` status; node reports `DiskPressure`.
- **Investigation**:
  ```bash
  kubectl describe node ip-10-0-1-50 | grep Conditions -A 8
  ```
- **Root Cause**: Unmanaged container log files in `/var/log/pods` consumed $88\%$ of root volume space, crossing the Kubelet eviction threshold (`imagefs.available < 15%`).
- **Fix**: Trigger logrotate, clean up unreferenced images (`crictl rmi --prune`), and increase EBS root volume size.
- **Verification**: `DiskPressure` condition clears (`False`); pods reschedule.

#### Lab 10: Worker Node NotReady Condition
- **Problem**: Worker node transitions to `NotReady`; pods on node stop responding.
- **Symptoms**: `kubectl get nodes` displays `ip-10-0-2-12 NotReady`.
- **Investigation**:
  ```bash
  # SSH into node or use AWS SSM Session Manager
  sudo systemctl status kubelet
  sudo journalctl -u kubelet -e --no-pager
  ```
- **Root Cause**: The container runtime daemon (`containerd`) crashed due to an unhandled kernel dead-lock on an NVMe storage driver. Kubelet could not communicate with CRI socket.
- **Fix**: Restart containerd and kubelet:
  ```bash
  sudo systemctl restart containerd kubelet
  ```
- **Verification**: Node transitions back to `Ready` within 30 seconds.

---

# 15. Continuous Integration & Continuous Deployment (CI/CD)

### 15.1 Production CI/CD Pipelines

Continuous Integration (CI) guarantees that every code commit is automatically built, linted, type-checked, security-scanned, and tested. Continuous Deployment (CD) automates the release of validated artifacts to production using progressive rollout strategies.

```
+-------------------------------------------------------------+
|               Enterprise SRE CI/CD Pipeline                 |
+-------------------------------------------------------------+
| Commit -> Lint (Ruff) -> Type Check (Mypy) -> Unit Test     |
|                                |                            |
| Build Docker Image -> Container Security Scan (Trivy)       |
|                                |                            |
| Push to Registry (ECR) -> Deploy to Staging (Helm/Argo CD)  |
|                                |                            |
| Run Integration Tests & Synthetics Validation               |
|                                |                            |
| Canary Deploy to Prod (10% Traffic) -> Check NRQL Error Rate|
|                                |                            |
| Full Production Promotion -> New Relic Deployment Marker    |
+-------------------------------------------------------------+
```

### 15.2 Complete GitHub Actions Pipeline with New Relic Deployment Marker

```yaml
name: Production SRE Delivery Pipeline

on:
  push:
    branches: [ main ]

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: production-payment-api
  NEW_RELIC_ACCOUNT_ID: ${{ secrets.NEW_RELIC_ACCOUNT_ID }}
  NEW_RELIC_API_KEY: ${{ secrets.NEW_RELIC_USER_KEY }}

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: |
          pip install ruff mypy pytest
          ruff check .
          mypy --strict src/
          pytest -v tests/

  build-and-scan:
    needs: quality-gate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker Image
        run: docker build -t ${{ env.ECR_REPOSITORY }}:${{ github.sha }} .

      - name: Security Scan with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.ECR_REPOSITORY }}:${{ github.sha }}
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'

  deploy-production:
    needs: build-and-scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Kubernetes
        run: |
          # Apply manifest updates
          kubectl set image deployment/payment-api payment-api=${{ env.ECR_REPOSITORY }}:${{ github.sha }} -n prod
          kubectl rollout status deployment/payment-api -n prod --timeout=180s

      - name: Record New Relic Deployment Marker
        run: |
          curl -X POST https://api.newrelic.com/graphql \
            -H "Content-Type: application/json" \
            -H "API-Key: ${{ secrets.NEW_RELIC_USER_KEY }}" \
            -d '{
              "query": "mutation { changeTrackingCreateDeployment(deployment: { entityGuid: \"${{ secrets.NR_ENTITY_GUID }}\", version: \"${{ github.sha }}\", user: \"GitHub Actions CI\", description: \"Automated Production Release\" }) { deploymentId } }"
            }'
```

---

# 16. Infrastructure as Code: Terraform

### 16.1 Terraform Fundamentals & State Architecture

Terraform is a declarative Infrastructure as Code (IaC) tool that manages cloud resources via state tracking.

```
+-------------------------------------------------------------+
|                 Terraform State Reconciliation              |
+-------------------------------------------------------------+
| Configuration Files (*.tf)  <-- Desired State               |
|            |                                                |
|            v                                                |
| terraform plan: Compares Desired State vs Current State     |
|            |                                                |
|            v                                                |
| AWS / Cloud APIs            <-- Actual Real-World State     |
|            |                                                |
|            v                                                |
| terraform.tfstate           <-- Recorded State              |
| (Stored in S3 with DynamoDB Locking to prevent race states) |
+-------------------------------------------------------------+
```

### 16.2 Complete Terraform Infrastructure Specification

```hcl
# main.tf - Production AWS VPC & New Relic Alert Policy
terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    newrelic = {
      source  = "newrelic/newrelic"
      version = "~> 3.30"
    }
  }
  backend "s3" {
    bucket         = "corp-sre-terraform-state-us-east-1"
    key            = "prod/vpc_and_observability.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock-table"
  }
}

provider "aws" {
  region = var.aws_region
}

provider "newrelic" {
  account_id = var.new_relic_account_id
  api_key    = var.new_relic_api_key
  region     = "US"
}

# AWS Production VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "prod-sre-vpc"
    Environment = "production"
  }
}

resource "aws_subnet" "public_1a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  tags = { Name = "prod-public-1a" }
}

# New Relic Alert Policy
resource "newrelic_alert_policy" "sre_policy" {
  name                = "Production SRE Core Policy"
  incident_preference = "PER_CONDITION"
}

# New Relic NRQL Alert Condition
resource "newrelic_nrql_alert_condition" "high_error_rate" {
  policy_id                    = newrelic_alert_policy.sre_policy.id
  name                         = "API High Error Rate (> 2%)"
  type                         = "static"
  value_function               = "single_value"
  enabled                      = true
  aggregation_window           = 60
  aggregation_method           = "event_flow"
  aggregation_delay            = 120

  nrql {
    query = "SELECT percentage(count(*), WHERE httpResponseCode >= 500) FROM Transaction WHERE appName = 'Payment-API'"
  }

  critical {
    operator              = "above"
    threshold             = 2.0
    threshold_duration    = 300
    threshold_occurrences = "ALL"
  }
}
```
'''
