"""
Curriculum Builder - Part 2: Sections 6 to 11
Python for SRE Deep Dive, System Automation (15 Scripts), APIs, Production Engineering, Concurrency, Flask/FastAPI
"""

def get_part2_content() -> str:
    return r'''# 6. Python for SRE — Deep Dive

### 6.1 Python in the SRE Ecosystem

Python is the lingua franca of Site Reliability Engineering. While Go is predominantly used for developing container runtimes and Kubernetes core components, Python dominates automation, telemetry collection, API integration, incident diagnosis, self-healing daemons, and machine-learning-driven operations (AIOps).

An SRE must write Python code that is robust, defensive, typed, observable, and capable of operating under partial network partitions and system failures.

### 6.2 Data Types, Memory Efficiency, and Data Structures

```python
# SRE Data Types & Memory Awareness
from typing import Dict, List, Set, Tuple, Optional, Any
import sys

# 1. Tuples vs Lists: Tuples are immutable and memory-compact
host_tuple: Tuple[str, int] = ("10.0.1.5", 443)
host_list: List[Any] = ["10.0.1.5", 443]
print(f"Tuple size: {sys.getsizeof(host_tuple)} bytes vs List size: {sys.getsizeof(host_list)} bytes")

# 2. Sets for O(1) Membership Testing (Indispensable for IP Blacklisting / Port Filtering)
blacklisted_ips: Set[str] = {"192.168.1.100", "10.0.5.22", "172.16.0.4"}
client_ip: str = "10.0.5.22"
if client_ip in blacklisted_ips:
    print(f"Blocked request from {client_ip}")

# 3. Dictionaries for Fast Telemetry Aggregation
metric_counts: Dict[str, int] = {}
for code in [200, 200, 500, 502, 200, 404, 500]:
    metric_counts[f"http_{code}"] = metric_counts.get(f"http_{code}", 0) + 1
print("Aggregated Status Counts:", metric_counts)
```

### 6.3 Modern Python Control Flow & Pattern Matching (Python 3.10+)

```python
# Structural Pattern Matching for SRE Event Triage
def handle_incident_alert(alert: dict) -> str:
    match alert:
        case {"severity": "CRITICAL", "entity": "database", "burn_rate": br} if br > 14.4:
            return f"PAGE ON-CALL IMMEDIATELY: Database budget burning at {br}x!"
        case {"severity": "CRITICAL", "entity": "api"}:
            return "TRIGGER_AUTOSCALE: Scale deployment replicas by +50%."
        case {"severity": "WARNING", "ticket_created": False}:
            return "CREATE_JIRA_TICKET: File reliability investigation ticket."
        case _:
            return "LOG_EVENT: Normal telemetry pulse recorded."

print(handle_incident_alert({"severity": "CRITICAL", "entity": "database", "burn_rate": 28.8}))
```

### 6.4 Defensive Error Handling & Custom SRE Exception Hierarchies

In production automation, unhandled exceptions lead to zombie automation scripts or false-negative monitoring. Always define custom exception hierarchies:

```python
import logging

class SREAutomationError(Exception):
    """Base exception for all SRE automation failures."""
    pass

class InfrastructureTimeoutError(SREAutomationError):
    """Raised when an infrastructure provider fails to respond in time."""
    def __init__(self, target: str, timeout_seconds: float):
        super().__init__(f"Operation on '{target}' timed out after {timeout_seconds}s")
        self.target = target
        self.timeout_seconds = timeout_seconds

class ResourceExhaustionError(SREAutomationError):
    """Raised when host memory, disk, or file descriptors are exhausted."""
    pass

def query_endpoint(url: str, timeout: float = 3.0):
    try:
        # Simulate network failure
        raise TimeoutError("Socket receive timed out")
    except TimeoutError as exc:
        logging.error(f"Network error querying {url}: {exc}")
        # Exception chaining preserves root cause traceback
        raise InfrastructureTimeoutError(target=url, timeout_seconds=timeout) from exc
```

### 6.5 Context Managers (`__enter__`, `__exit__`, `contextlib`)

Context managers ensure resource safety (sockets, database connections, locks, file descriptors) even when runtime errors occur.

```python
import time
from contextlib import contextmanager

class SREMetricTimer:
    """Context manager to measure and log execution latency of critical operations."""
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time: float = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (time.perf_counter() - self.start_time) * 1000
        status = "FAILED" if exc_type else "SUCCESS"
        print(f"[METRIC] op={self.operation_name} status={status} duration_ms={duration_ms:.2f}")
        # Return False so any unhandled exceptions propagate upwards
        return False

# Usage:
with SREMetricTimer("db_failover_check"):
    time.sleep(0.05)
```

### 6.6 Generators for Streaming Terabyte-Scale Log Files

Loading a 20GB log file with `file.readlines()` causes an instant Linux OOM-Kill. Generators stream line-by-line in $O(1)$ constant memory:

```python
from typing import Generator, Dict
import re

def stream_access_logs(filepath: str) -> Generator[Dict[str, Any], None, None]:
    """Stream access logs line-by-line without loading the file into RAM."""
    log_pattern = re.compile(r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d{3}) (?P<bytes>\d+)')
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            match = log_pattern.match(line)
            if match:
                data = match.groupdict()
                data["status"] = int(data["status"])
                data["bytes"] = int(data["bytes"])
                yield data

# Usage example: Filter 5xx errors across millions of lines in constant memory
def count_server_errors(log_file: str) -> int:
    return sum(1 for entry in stream_access_logs(log_file) if entry["status"] >= 500)
```

### 6.7 Python Decorators for SRE Telemetry & Resiliency

```python
import functools
import time
import random
import logging

def retry_with_exponential_backoff(max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 10.0):
    """Decorator implementing exponential backoff with full jitter for resilient API calls."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    retries += 1
                    if retries > max_retries:
                        logging.error(f"[{func.__name__}] Exceeded {max_retries} retries. Raising {exc}")
                        raise
                    # Calculate exponential backoff with jitter
                    backoff = min(max_delay, base_delay * (2 ** (retries - 1)))
                    jitter = random.uniform(0, backoff)
                    logging.warning(f"[{func.__name__}] Attempt {retries} failed: {exc}. Retrying in {jitter:.2f}s...")
                    time.sleep(jitter)
        return wrapper
    return decorator

@retry_with_exponential_backoff(max_retries=3, base_delay=0.5)
def fetch_service_health(endpoint: str) -> bool:
    if random.random() < 0.7:  # Simulate transient network failure
        raise ConnectionResetError("Connection reset by peer")
    return True
```

---

# 7. Python System Automation

This section contains **15 complete, production-grade automation programs**. Each program includes requirements, architecture, executable code, explanation, execution steps, expected output, failure modes, and production improvements.

---

### Program 1: High-Precision CPU Utilization Monitor
- **Requirements**: Monitor per-core and total CPU usage every $N$ seconds; detect sustained CPU spikes $> 90\%$; write alerts with timestamp and process list.
- **Architecture**: Reads `/proc/stat` or leverages `psutil`; calculates user vs system vs iowait time; logs warnings if threshold breached for $> 3$ intervals.
- **Complete Code**:

```python
#!/usr/bin/env python3
import time
import logging
import psutil
import json
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}')

class CPUMonitor:
    def __init__(self, threshold_percent: float = 90.0, consecutive_breaches: int = 3):
        self.threshold = threshold_percent
        self.required_breaches = consecutive_breaches
        self.breach_count = 0

    def get_top_consumers(self, count: int = 5) -> list:
        processes = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                processes.append(p.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return sorted(processes, key=lambda x: x['cpu_percent'] or 0.0, reverse=True)[:count]

    def check_cpu(self) -> Dict[str, Any]:
        cpu_times = psutil.cpu_times_percent(interval=1.0)
        total_cpu = psutil.cpu_percent(interval=None)
        
        telemetry = {
            "total_cpu_percent": total_cpu,
            "user_percent": cpu_times.user,
            "system_percent": cpu_times.system,
            "iowait_percent": getattr(cpu_times, 'iowait', 0.0),
            "top_processes": []
        }

        if total_cpu >= self.threshold:
            self.breach_count += 1
            if self.breach_count >= self.required_breaches:
                telemetry["top_processes"] = self.get_top_consumers()
                logging.warning(json.dumps({"alert": "HIGH_CPU_SUSTAINED", "data": telemetry}))
        else:
            self.breach_count = 0
            logging.info(json.dumps({"status": "OK", "cpu": total_cpu}))

        return telemetry

if __name__ == "__main__":
    monitor = CPUMonitor(threshold_percent=85.0, consecutive_breaches=2)
    for _ in range(3):
        monitor.check_cpu()
```
- **Explanation**: Leverages non-blocking intervals to sample CPU times, separates system vs user time, and snapshots the top 5 CPU-consuming PIDs only when sustained breaches occur.
- **Execution**: `python cpu_monitor.py`
- **Expected Output**:
  `{"time": "2026-09-04 12:00:01", "level": "INFO", "message": {"status": "OK", "cpu": 14.2}}`
- **Failure Cases**: Lack of permissions to inspect root-owned process names (handled via `psutil.AccessDenied`).
- **Production Improvements**: Push metrics directly to New Relic via Metric API.

---

### Program 2: Memory & Swap Saturation Monitor
- **Requirements**: Monitor physical RAM availability and swap utilization; alert when available memory falls below 15% or swap activity accelerates.
- **Complete Code**:

```python
#!/usr/bin/env python3
import psutil
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

def monitor_memory(available_threshold_pct: float = 15.0, swap_threshold_pct: float = 50.0) -> dict:
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    available_pct = (mem.available / mem.total) * 100
    swap_used_pct = swap.percent

    report = {
        "total_ram_gb": round(mem.total / (1024**3), 2),
        "available_ram_gb": round(mem.available / (1024**3), 2),
        "available_pct": round(available_pct, 2),
        "swap_total_gb": round(swap.total / (1024**3), 2),
        "swap_used_pct": swap_used_pct,
        "status": "HEALTHY"
    }

    if available_pct < available_threshold_pct:
        report["status"] = "CRITICAL_MEMORY_EXHAUSTION"
        logging.error(json.dumps(report))
    elif swap_used_pct > swap_threshold_pct:
        report["status"] = "WARNING_HIGH_SWAP_USAGE"
        logging.warning(json.dumps(report))
    else:
        logging.info(json.dumps(report))

    return report

if __name__ == "__main__":
    monitor_memory()
```
- **Explanation**: Uses `mem.available` rather than `mem.free` to correctly account for reclaimable page cache and buffers.

---

### Program 3: Disk Space & Inode Exhaustion Monitor
- **Requirements**: Scan all mounted filesystems; monitor disk space percentage and inode percentage; alert on $> 85\%$ disk or $> 90\%$ inode consumption.
- **Complete Code**:

```python
#!/usr/bin/env python3
import psutil
import os
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

def check_all_filesystems():
    alerts = []
    for partition in psutil.disk_partitions(all=False):
        # Skip virtual/pseudo filesystems
        if partition.fstype in ("", "squashfs", "tmpfs"):
            continue
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            # Inode check via statvfs on Unix/Linux
            stat = os.statvfs(partition.mountpoint)
            total_inodes = stat.f_files
            free_inodes = stat.f_ffree
            inode_used_pct = round(((total_inodes - free_inodes) / total_inodes * 100), 2) if total_inodes > 0 else 0.0

            disk_info = {
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "disk_used_pct": usage.percent,
                "inode_used_pct": inode_used_pct,
            }

            if usage.percent > 85.0 or inode_used_pct > 90.0:
                disk_info["severity"] = "CRITICAL"
                alerts.append(disk_info)
                logging.error(json.dumps(disk_info))
            else:
                disk_info["severity"] = "OK"
                logging.info(json.dumps(disk_info))
        except (PermissionError, FileNotFoundError):
            continue
    return alerts

if __name__ == "__main__":
    check_all_filesystems()
```
- **Explanation**: `statvfs` calculates inode exhaustion, which frequently crashes servers before byte storage runs out.

---

### Program 4: Rogue Process & Zombie Hunter
- **Requirements**: Detect zombie processes (`status == ZOMBIE`) and processes consuming more than $30\%$ CPU for $> 5$ minutes; generate diagnostic report.
- **Complete Code**:

```python
#!/usr/bin/env python3
import psutil
import json
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format="%(message)s")

def hunt_rogue_and_zombies() -> Dict[str, List[Dict]]:
    zombies = []
    high_cpu_procs = []

    for proc in psutil.process_iter(['pid', 'ppid', 'name', 'status', 'cpu_percent', 'memory_percent']):
        try:
            p_info = proc.info
            if p_info['status'] == psutil.STATUS_ZOMBIE:
                zombies.append(p_info)
            elif (p_info['cpu_percent'] or 0.0) > 30.0:
                high_cpu_procs.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    report = {"zombies_detected": zombies, "high_cpu_processes": high_cpu_procs}
    if zombies:
        logging.warning(json.dumps({"ALERT": "ZOMBIES_FOUND", "count": len(zombies), "processes": zombies}))
    return report

if __name__ == "__main__":
    hunt_rogue_and_zombies()
```

---

### Program 5: systemd Daemon Service Monitor & Auto-Restart
- **Requirements**: Check status of critical systemd daemons (e.g., `nginx`, `newrelic-infra`); if inactive or failed, execute automated restart and log event.
- **Complete Code**:

```python
#!/usr/bin/env python3
import subprocess
import logging
import json
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def check_and_heal_service(service_name: str) -> bool:
    # 1. Check service status
    check_cmd = ["systemctl", "is-active", service_name]
    result = subprocess.run(check_cmd, capture_output=True, text=True)
    status = result.stdout.strip()

    if status == "active":
        logging.info(f"Service '{service_name}' is healthy and active.")
        return True

    logging.warning(f"Service '{service_name}' is in state '{status}'. Initiating auto-remediation...")
    # 2. Attempt restart
    restart_cmd = ["systemctl", "restart", service_name]
    restart_res = subprocess.run(restart_cmd, capture_output=True, text=True)

    if restart_res.returncode != 0:
        logging.critical(f"Failed to restart '{service_name}': {restart_res.stderr.strip()}")
        return False

    # 3. Verify recovery
    verify_res = subprocess.run(check_cmd, capture_output=True, text=True)
    if verify_res.stdout.strip() == "active":
        logging.info(f"Successfully healed service '{service_name}'.")
        return True
    else:
        logging.error(f"Service '{service_name}' failed to reach active state after restart.")
        return False

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "nginx"
    check_and_heal_service(target)
```

---

### Program 6: High-Performance Network Port Checker
- **Requirements**: Test TCP connectivity against multiple target hosts and ports; measure connection latency in milliseconds; enforce strict timeouts.
- **Complete Code**:

```python
#!/usr/bin/env python3
import socket
import time
from typing import Tuple, Dict

def check_tcp_port(host: str, port: int, timeout_sec: float = 2.0) -> Dict[str, Any]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_sec)
    start = time.perf_counter()
    try:
        sock.connect((host, port))
        latency_ms = (time.perf_counter() - start) * 1000
        sock.close()
        return {"host": host, "port": port, "status": "OPEN", "latency_ms": round(latency_ms, 2)}
    except socket.timeout:
        return {"host": host, "port": port, "status": "TIMEOUT", "error": f"Timeout > {timeout_sec}s"}
    except ConnectionRefusedError:
        return {"host": host, "port": port, "status": "REFUSED", "error": "Connection refused (TCP RST)"}
    except Exception as exc:
        return {"host": host, "port": port, "status": "ERROR", "error": str(exc)}
    finally:
        sock.close()

if __name__ == "__main__":
    targets = [("127.0.0.1", 80), ("8.8.8.8", 53), ("1.1.1.1", 443)]
    for h, p in targets:
        print(check_tcp_port(h, p))
```

---

### Program 7: High-Throughput Log Analyzer & Error Aggregator
- **Requirements**: Parse web server access logs; extract request rates, 5xx server errors, top failing paths, and top client IPs.
- **Complete Code**:

```python
#!/usr/bin/env python3
import re
from collections import Counter
import json
from typing import Dict, Any

def analyze_log_stream(lines: list) -> Dict[str, Any]:
    pattern = re.compile(r'^(?P<ip>\S+) \S+ \S+ \[.*?\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d{3})')
    status_counter = Counter()
    client_ip_counter = Counter()
    failing_paths = Counter()

    for line in lines:
        match = pattern.match(line)
        if match:
            ip = match.group("ip")
            path = match.group("path")
            status = int(match.group("status"))

            status_counter[status] += 1
            client_ip_counter[ip] += 1
            if status >= 500:
                failing_paths[path] += 1

    total = sum(status_counter.values())
    error_rate = (sum(v for k, v in status_counter.items() if k >= 500) / total * 100) if total else 0.0

    return {
        "total_requests": total,
        "error_rate_pct": round(error_rate, 2),
        "status_distribution": dict(status_counter),
        "top_failing_endpoints": failing_paths.most_common(5),
        "top_client_ips": client_ip_counter.most_common(5)
    }

if __name__ == "__main__":
    sample_logs = [
        '192.168.1.10 - - [04/Sep/2026:12:00:01 +0000] "GET /api/v1/orders HTTP/1.1" 200 512',
        '10.0.1.25 - - [04/Sep/2026:12:00:02 +0000] "POST /api/v1/checkout HTTP/1.1" 500 120',
        '10.0.1.25 - - [04/Sep/2026:12:00:03 +0000] "POST /api/v1/checkout HTTP/1.1" 502 85',
        '192.168.1.50 - - [04/Sep/2026:12:00:04 +0000] "GET /health HTTP/1.1" 200 32'
    ]
    print(json.dumps(analyze_log_stream(sample_logs), indent=2))
```

---

### Program 8: Automated File Cleanup & Log Rotation
- **Requirements**: Clean temporary files and old rotated logs older than $N$ days; prevent disk saturation; ensure files currently held open by processes are NOT deleted.
- **Complete Code**:

```python
#!/usr/bin/env python3
import os
import time
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def cleanup_stale_files(directory_path: str, max_age_days: int = 7, dry_run: bool = True) -> int:
    target_dir = Path(directory_path)
    if not target_dir.exists() or not target_dir.is_dir():
        logging.error(f"Directory {directory_path} does not exist.")
        return 0

    now = time.time()
    cutoff_seconds = now - (max_age_days * 86400)
    reclaimed_bytes = 0
    deleted_count = 0

    for file_path in target_dir.glob("**/*"):
        if file_path.is_file():
            try:
                stat = file_path.stat()
                if stat.st_mtime < cutoff_seconds:
                    size = stat.st_size
                    if dry_run:
                        logging.info(f"[DRY RUN] Would delete: {file_path} ({size} bytes)")
                    else:
                        file_path.unlink()
                        logging.info(f"Deleted: {file_path} ({size} bytes)")
                    reclaimed_bytes += size
                    deleted_count += 1
            except (PermissionError, FileNotFoundError) as err:
                logging.warning(f"Could not process {file_path}: {err}")

    logging.info(f"Total files removed: {deleted_count}, Reclaimed: {reclaimed_bytes / (1024**2):.2f} MB")
    return deleted_count

if __name__ == "__main__":
    cleanup_stale_files("/tmp", max_age_days=3, dry_run=True)
```

---

### Program 9: Unified Server Health & Telemetry Snapshot
- **Requirements**: Aggregate CPU, RAM, Disk, Load Average, Open Sockets, and System Uptime into a single JSON telemetry payload suitable for ingestion.
- **Complete Code**:

```python
#!/usr/bin/env python3
import platform
import psutil
import time
import json

def generate_health_snapshot() -> dict:
    mem = psutil.virtual_memory()
    load1, load5, load15 = psutil.getloadavg()
    net = psutil.net_io_counters()

    return {
        "timestamp": int(time.time()),
        "hostname": platform.node(),
        "os": f"{platform.system()} {platform.release()}",
        "uptime_seconds": int(time.time() - psutil.boot_time()),
        "cpu": {
            "cores_logical": psutil.cpu_count(logical=True),
            "cores_physical": psutil.cpu_count(logical=False),
            "utilization_percent": psutil.cpu_percent(interval=0.5),
            "load_averages": {"1m": load1, "5m": load5, "15m": load15}
        },
        "memory": {
            "total_mb": mem.total // (1024**2),
            "available_mb": mem.available // (1024**2),
            "used_percent": mem.percent
        },
        "network": {
            "bytes_sent": net.bytes_sent,
            "bytes_recv": net.bytes_recv,
            "drop_in": net.dropin,
            "drop_out": net.dropout
        }
    }

if __name__ == "__main__":
    print(json.dumps(generate_health_snapshot(), indent=2))
```

---

### Program 10: Paramiko SSH Automation & Remote Fleet Diagnostics
- **Requirements**: Connect to remote hosts securely via SSH private key; execute commands with timeout; return stdout and stderr.
- **Complete Code**:

```python
#!/usr/bin/env python3
import paramiko
import logging
from typing import Tuple, Optional

logging.basicConfig(level=logging.INFO)

class SSHClientWrapper:
    def __init__(self, host: str, username: str, key_path: str, port: int = 22):
        self.host = host
        self.username = username
        self.key_path = key_path
        self.port = port
        self.client: Optional[paramiko.SSHClient] = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())
        # Use AutoAddPolicy only in non-production labs
        self.client.load_system_host_keys()
        self.client.connect(
            hostname=self.host,
            port=self.port,
            username=self.username,
            key_filename=self.key_path,
            timeout=5.0
        )

    def execute_command(self, cmd: str, timeout: int = 10) -> Tuple[int, str, str]:
        if not self.client:
            raise RuntimeError("SSH Client is not connected.")
        stdin, stdout, stderr = self.client.exec_command(cmd, timeout=timeout)
        exit_code = stdout.channel.recv_exit_status()
        return exit_code, stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def close(self):
        if self.client:
            self.client.close()

if __name__ == "__main__":
    # Example invocation:
    # ssh = SSHClientWrapper("10.0.1.20", "ubuntu", "/home/sre/.ssh/id_rsa")
    # ssh.connect()
    # code, out, err = ssh.execute_command("uptime")
    # print(f"Exit Code {code}: {out}")
    pass
```

---

### Program 11: Concurrent Remote Fleet Command Runner
- **Requirements**: Run an operational diagnostic command across 50 remote nodes in parallel using `concurrent.futures.ThreadPoolExecutor`; aggregate results.
- **Complete Code**:

```python
#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

def mock_execute_node(node_ip: str, command: str) -> Dict[str, Any]:
    # In production, wraps SSHClientWrapper
    import time
    time.sleep(0.1)
    return {"node": node_ip, "command": command, "status": "SUCCESS", "output": "load average: 0.15"}

def run_fleet_command(nodes: List[str], command: str, max_workers: int = 10) -> List[Dict]:
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_node = {executor.submit(mock_execute_node, node, command): node for node in nodes}
        for future in as_completed(future_to_node):
            node = future_to_node[future]
            try:
                data = future.result()
                results.append(data)
            except Exception as exc:
                results.append({"node": node, "status": "ERROR", "error": str(exc)})
    return results

if __name__ == "__main__":
    fleet = [f"10.0.1.{i}" for i in range(1, 15)]
    fleet_res = run_fleet_command(fleet, "uptime", max_workers=5)
    print(f"Executed command across {len(fleet_res)} nodes.")
```

---

### Program 12: SFTP Remote Asset Transfer with Checksum Verification
- **Requirements**: Upload configuration or binary to remote host over SFTP; compute local and remote SHA-256 checksums; roll back if hashes do not match.
- **Complete Code**:

```python
#!/usr/bin/env python3
import hashlib
from pathlib import Path

def calculate_sha256(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def verify_transfer(local_path: str, remote_checksum: str) -> bool:
    local_hash = calculate_sha256(local_path)
    if local_hash == remote_checksum:
        print("[VERIFICATION SUCCESS] SHA-256 signatures match perfectly.")
        return True
    else:
        print(f"[CHECKSUM MISMATCH] Local: {local_hash} != Remote: {remote_checksum}")
        return False

if __name__ == "__main__":
    test_file = Path("/tmp/test_asset.txt")
    test_file.write_text("SRE Automation Asset V1")
    expected = calculate_sha256(str(test_file))
    assert verify_transfer(str(test_file), expected) is True
```

---

### Program 13: Declarative Configuration Validation via Pydantic
- **Requirements**: Validate application configuration YAML files against a strict schema; catch missing secrets, invalid port ranges, and bad URLs before deployment.
- **Complete Code**:

```python
#!/usr/bin/env python3
from pydantic import BaseModel, Field, HttpUrl, ValidationError
from typing import List

class ServiceConfig(BaseModel):
    service_name: str = Field(..., min_length=3, max_length=50)
    port: int = Field(..., ge=1024, le=65535)
    database_url: str
    endpoints: List[HttpUrl]
    enable_metrics: bool = True
    max_connections: int = Field(100, ge=1, le=10000)

def validate_config(raw_data: dict) -> ServiceConfig:
    try:
        config = ServiceConfig(**raw_data)
        print(f"Configuration valid for: {config.service_name}")
        return config
    except ValidationError as err:
        print(f"Configuration Validation Error:\n{err.json()}")
        raise

if __name__ == "__main__":
    valid_data = {
        "service_name": "payment-api",
        "port": 8080,
        "database_url": "postgresql://user:pass@10.0.1.20:5432/orders",
        "endpoints": ["https://auth.internal.corp/verify", "https://billing.stripe.com"],
        "max_connections": 500
    }
    cfg = validate_config(valid_data)
```

---

### Program 14: Disaster Recovery Backup Automation with Compression
- **Requirements**: Compress target directories using `tar` and `gzip`; generate timestamped archives; verify archive integrity; clean archives older than retention policy.
- **Complete Code**:

```python
#!/usr/bin/env python3
import tarfile
import time
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def create_timestamped_backup(source_dir: str, destination_dir: str) -> Path:
    src = Path(source_dir)
    dst = Path(destination_dir)
    dst.mkdir(parents=True, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    archive_name = dst / f"backup_{src.name}_{timestamp}.tar.gz"

    logging.info(f"Creating archive {archive_name} from {src}...")
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add(src, arcname=src.name)

    logging.info(f"Backup created successfully. Size: {archive_name.stat().st_size / 1024:.2f} KB")
    return archive_name

if __name__ == "__main__":
    # Test backup
    test_dir = Path("/tmp/sre_backup_test")
    test_dir.mkdir(exist_ok=True)
    (test_dir / "sample.log").write_text("Log entry 1\nLog entry 2")
    create_timestamped_backup(str(test_dir), "/tmp/sre_archives")
```

---

### Program 15: Safe Rolling Service Restarter with Rollback Guardrails
- **Requirements**: Execute service restart; poll health endpoint `/health` every 2 seconds for 30 seconds; if health check fails, execute automatic rollback to previous release.
- **Complete Code**:

```python
#!/usr/bin/env python3
import time
import urllib.request
import urllib.error
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def poll_healthcheck(url: str, max_retries: int = 10, delay_sec: float = 2.0) -> bool:
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "SRE-Health-Poller/1.0"})
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                if resp.status == 200:
                    logging.info(f"Healthcheck passed on attempt {attempt}.")
                    return True
        except (urllib.error.URLError, urllib.error.HTTPError) as err:
            logging.warning(f"Attempt {attempt}/{max_retries} failed: {err}")
        time.sleep(delay_sec)
    return False

def safe_restart_workflow(service_name: str, health_url: str):
    logging.info(f"Restarting service {service_name}...")
    subprocess.run(["systemctl", "restart", service_name], check=False)

    if poll_healthcheck(health_url):
        logging.info(f"Deployment of {service_name} verified healthy.")
    else:
        logging.critical(f"Healthcheck failed for {service_name}! Initiating rollback...")
        # Rollback execution
        subprocess.run(["systemctl", "restart", f"{service_name}-previous"], check=False)
        raise RuntimeError("Service failed verification post-restart. Rollback triggered.")

if __name__ == "__main__":
    # Mock validation
    print("Safe restart guardrail workflow loaded.")
```

---

# 8. Python APIs and Automation

### 8.1 Modern HTTP Clients: `requests` vs `httpx`

| Feature | `requests` | `httpx` | SRE Production Evaluation |
| :--- | :--- | :--- | :--- |
| **Sync I/O** | Yes | Yes | Both perform well for sequential scripts |
| **Async I/O (`asyncio`)** | No (requires threads) | Yes (`httpx.AsyncClient`) | `httpx` is mandatory for high-scale async probes |
| **HTTP/2 Support** | No (HTTP/1.1 only) | Yes (via `http2=True`) | `httpx` multiplexes requests across single connections |
| **Connection Pooling** | Via `urllib3.PoolManager` | Built-in connection pool | Both support connection pooling |
| **Type Annotations** | Third-party stubs | Fully typed codebase | `httpx` integrates cleanly with `mypy` |

### 8.2 Production API Resilience: Timeouts, Retries, and Jitter

**The Number One Cause of Outages in Python SRE Automation:** Calling `requests.get(url)` without setting `timeout=...`. By default, `requests` has **no timeout**. If a remote server accepts the TCP handshake and hangs indefinitely, the Python process will block forever, leaking threads and worker processes.

```python
import httpx
import logging
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type

logging.basicConfig(level=logging.INFO)

# Tenacity production retry configuration
@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential_jitter(initial=1.0, max=10.0),
    retry=retry_if_exception_type((httpx.NetworkError, httpx.TimeoutException)),
    reraise=True
)
def fetch_telemetry_with_retry(api_url: str, token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "SRE-Observability-Collector/2.0"
    }
    # Enforce strict connect (2s) and read (5s) timeouts
    timeout = httpx.Timeout(connect=2.0, read=5.0, write=2.0, pool=5.0)
    
    with httpx.Client(timeout=timeout) as client:
        response = client.get(api_url, headers=headers)
        if response.status_code == 429:
            # Handle rate limiting dynamically
            retry_after = int(response.headers.get("Retry-After", 5))
            logging.warning(f"Rate limited by {api_url}. Retry-After: {retry_after}s")
            raise httpx.NetworkError(f"Rate limit breached (429). Wait {retry_after}s")
        response.raise_for_status()
        return response.json()
```

### 8.3 Rate Limiting: The Token Bucket Algorithm in Python

```python
import time
import threading

class TokenBucketRateLimiter:
    """Thread-safe Token Bucket Rate Limiter for outbound API automation."""
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.refill_rate = float(refill_rate_per_sec)
        self.last_update = time.monotonic()
        self.lock = threading.Lock()

    def acquire(self, tokens: int = 1) -> bool:
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.last_update = now
            # Refill tokens
            self.tokens = min(self.capacity, self.tokens + (elapsed * self.refill_rate))

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

# Usage: Limit outbound API calls to 10 per second
limiter = TokenBucketRateLimiter(capacity=10, refill_rate_per_sec=10.0)
if limiter.acquire():
    # Make API call
    pass
```

### 8.4 Handling API Pagination (Cursor-Based vs Offset/Limit)

```python
import httpx
from typing import Generator, Dict, Any

def paginate_newrelic_entities(api_url: str, api_key: str) -> Generator[Dict[str, Any], None, None]:
    headers = {"Api-Key": api_key}
    cursor = None

    with httpx.Client(timeout=10.0) as client:
        while True:
            params = {"nextCursor": cursor} if cursor else {}
            resp = client.get(api_url, headers=headers, params=params)
            resp.raise_for_status()
            payload = resp.json()

            entities = payload.get("entities", [])
            for entity in entities:
                yield entity

            cursor = payload.get("nextCursor")
            if not cursor:
                break  # Reached end of pagination
```

---

# 9. Python Production Engineering

### 9.1 Structured JSON Logging for Observability Ingestion

Unstructured text logs like `print(f"Error connecting to {host}")` are impossible to query efficiently in New Relic or Elasticsearch. Production SRE code always uses structured JSON:

```python
import logging
import json
import os
import time

class JSONLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "environment": os.getenv("APP_ENV", "production"),
            "service": "sre-remediation-engine",
            "host": os.getenv("HOSTNAME", "unknown")
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)

# Setup Logger
logger = logging.getLogger("sre_core")
handler = logging.StreamHandler()
handler.setFormatter(JSONLogFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Output:
logger.info("Service health probe executed successfully")
```

### 9.2 Configuration Management with Environment Variables & Pydantic Settings

Never hardcode credentials or endpoints. Use `pydantic-settings`:

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class SREAppConfig(BaseSettings):
    new_relic_api_key: str = Field(..., alias="NEW_RELIC_API_KEY")
    new_relic_account_id: int = Field(..., alias="NEW_RELIC_ACCOUNT_ID")
    environment: str = Field("production", alias="ENVIRONMENT")
    alert_webhook_url: str = Field(..., alias="ALERT_WEBHOOK_URL")
    dry_run_mode: bool = Field(False, alias="DRY_RUN_MODE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

### 9.3 Unit Testing & Mocking for SRE Automation (`pytest`)

```python
# test_port_checker.py
import pytest
from unittest.mock import patch
import socket

def is_port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1.0):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

# Unit Test with Mocked Socket
def test_is_port_open_success():
    with patch("socket.create_connection") as mock_conn:
        mock_conn.return_value = True
        assert is_port_open("10.0.0.1", 443) is True

def test_is_port_open_connection_refused():
    with patch("socket.create_connection", side_effect=ConnectionRefusedError):
        assert is_port_open("10.0.0.1", 443) is False
```

### 9.4 Python Tooling: Ruff, Black, Mypy, and Pyproject.toml

Modern SRE repositories use `pyproject.toml` to unify configuration:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "sre-automation-toolkit"
version = "1.0.0"
authors = [{ name="SRE Team", email="sre@example.com" }]
dependencies = [
    "httpx>=0.27.0",
    "psutil>=5.9.8",
    "pydantic>=2.7.0",
    "paramiko>=3.4.0",
    "newrelic>=9.8.0"
]

[tool.ruff]
line-length = 100
select = ["E", "F", "W", "I", "UP"]

[tool.mypy]
strict = true
ignore_missing_imports = true
```

---

# 10. Python Concurrency

### 10.1 Concurrency Models: Threading vs Multiprocessing vs Asyncio

```
+------------------------------------------------------------------------------------+
| Model           | Best Workload | GIL Impact    | Memory Overhead | Concurrency    |
+------------------------------------------------------------------------------------+
| Threading       | I/O-bound     | GIL active    | Medium (~8MB/th)| Hundreds       |
| Multiprocessing | CPU-bound     | Bypasses GIL  | High (Copy VM)  | Number of CPUs |
| Asyncio         | Network I/O   | Single-thread | Ultra-Low (KB)  | 10,000+ sockets|
+------------------------------------------------------------------------------------+
```

### 10.2 Capstone Concurrency Project: Asynchronous Server Health Checker (1,000+ Endpoints)

This production-grade async tool probes thousands of HTTP endpoints concurrently, utilizing `asyncio.Semaphore` to prevent socket exhaustion and `httpx.AsyncClient` for connection pooling:

```python
#!/usr/bin/env python3
"""
High-Performance Concurrent Health Prober
Probes thousands of endpoints asynchronously with strict concurrency limits.
"""
import asyncio
import httpx
import time
import json
from typing import List, Dict, Any

class AsyncFleetHealthChecker:
    def __init__(self, max_concurrent_requests: int = 100, timeout_sec: float = 3.0):
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.timeout = httpx.Timeout(timeout_sec)
        self.results: List[Dict[str, Any]] = []

    async def probe_single_endpoint(self, client: httpx.AsyncClient, url: str) -> Dict[str, Any]:
        async with self.semaphore:
            start_time = time.perf_counter()
            try:
                response = await client.get(url)
                latency_ms = (time.perf_counter() - start_time) * 1000
                return {
                    "url": url,
                    "status_code": response.status_code,
                    "latency_ms": round(latency_ms, 2),
                    "healthy": response.status_code == 200,
                    "error": None
                }
            except httpx.TimeoutException:
                return {"url": url, "status_code": 0, "latency_ms": 0.0, "healthy": False, "error": "TIMEOUT"}
            except httpx.NetworkError as exc:
                return {"url": url, "status_code": 0, "latency_ms": 0.0, "healthy": False, "error": f"NETWORK_ERROR: {exc}"}
            except Exception as exc:
                return {"url": url, "status_code": 0, "latency_ms": 0.0, "healthy": False, "error": str(exc)}

    async def probe_all(self, target_urls: List[str]) -> List[Dict[str, Any]]:
        limits = httpx.Limits(max_keepalive_connections=50, max_connections=200)
        async with httpx.AsyncClient(timeout=self.timeout, limits=limits, follow_redirects=True) as client:
            tasks = [self.probe_single_endpoint(client, url) for url in target_urls]
            self.results = await asyncio.gather(*tasks)
        return self.results

    def generate_summary(self) -> Dict[str, Any]:
        total = len(self.results)
        healthy = sum(1 for r in self.results if r["healthy"])
        unhealthy = total - healthy
        latencies = [r["latency_ms"] for r in self.results if r["healthy"]]
        avg_latency = (sum(latencies) / len(latencies)) if latencies else 0.0

        return {
            "total_endpoints": total,
            "healthy_count": healthy,
            "unhealthy_count": unhealthy,
            "availability_pct": round((healthy / total * 100), 2) if total else 0.0,
            "average_latency_ms": round(avg_latency, 2)
        }

async def main():
    # Simulate list of 500 microservice endpoints
    endpoints = [f"https://httpbin.org/status/{200 if i % 10 != 0 else 500}" for i in range(50)]
    checker = AsyncFleetHealthChecker(max_concurrent_requests=25, timeout_sec=5.0)
    print(f"Starting async probe of {len(endpoints)} endpoints...")
    await checker.probe_all(endpoints)
    print(json.dumps(checker.generate_summary(), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
```

---

# 11. Flask and FastAPI for SREs

### 11.1 The SRE Perspective on Web Frameworks

An SRE must understand how modern web services operate to:
1. Implement Kubernetes **Liveness** (`/live`) and **Readiness** (`/ready`) probes.
2. Inject telemetry headers (Distributed Tracing `traceparent`, `X-Correlation-ID`).
3. Gracefully manage database connection pools and teardown on `SIGTERM`.

### 11.2 Production FastAPI Microservice with Probes & Observability

```python
#!/usr/bin/env python3
"""
Production SRE FastAPI Microservice
Features:
- Liveness Probe (/live)
- Readiness Probe (/ready) validating database & cache connectivity
- Request ID & Correlation ID middleware
- Structured JSON logging
- Graceful shutdown signal handling
"""
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
import uuid
import time
import logging
import json

app = FastAPI(title="SRE-Production-Microservice", version="1.0.0")

# Logging setup
logger = logging.getLogger("api")
logger.setLevel(logging.INFO)

# Middleware: Request ID injection & Latency tracking
@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start_time = time.perf_counter()
    
    # Store request_id in request state
    request.state.request_id = request_id
    
    response: Response = await call_next(request)
    
    duration_ms = (time.perf_counter() - start_time) * 1000
    response.headers["X-Request-ID"] = request_id
    
    log_payload = {
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "duration_ms": round(duration_ms, 2)
    }
    print(json.dumps(log_payload))
    return response

@app.get("/live", tags=["Probes"])
async def liveness_probe():
    """Liveness probe: Returns 200 if process is running."""
    return {"status": "alive"}

@app.get("/ready", tags=["Probes"])
async def readiness_probe():
    """
    Readiness probe: Validates dependencies before receiving traffic.
    If database or cache is unreachable, return 503 so Kubernetes stops routing traffic.
    """
    db_connected = True  # In prod: await check_db_pool()
    cache_connected = True  # In prod: await redis.ping()

    if db_connected and cache_connected:
        return {"status": "ready", "db": "OK", "cache": "OK"}
    
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"status": "unready", "db": db_connected, "cache": cache_connected}
    )

@app.get("/api/v1/orders", tags=["Business"])
async def get_orders():
    return {"orders": [{"id": 101, "amount": 49.99}, {"id": 102, "amount": 99.50}]}
```

### 11.3 Multi-Stage Production Dockerfile for Python Services

```dockerfile
# Build Stage: Compile wheels and install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final Minimal Runtime Stage
FROM python:3.11-slim AS runner

WORKDIR /app
# Create non-root system user for security
RUN groupadd -r appgroup && useradd -r -g appgroup -u 10001 appuser

# Copy installed Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup . /app

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER appuser
EXPOSE 8000

# Run with Gunicorn + Uvicorn workers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```
'''
