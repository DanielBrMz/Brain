---
title: "cache-ec2 — AWS EC2 Instance"
type: infrastructure
status: active
created: 2026-03-22
updated: 2026-03-22
tags: [infrastructure, aws, ec2, cache, sidepocket]
---

# cache-ec2 — AWS EC2 Instance

> Bare EC2 instance — no application code, no Redis, no Docker.

## Overview

| Field | Value |
|-------|-------|
| **Access** | SSH via `sp-python-cache.pem` |
| **OS** | Amazon Linux 2023 |
| **RAM** | 7.8 GB |
| **Disk** | 8 GB (58% used) |
| **Purpose** | Minimal instance — currently bare |

## Current State

- **No Redis** installed or running
- **No Docker** installed
- **No running services** beyond SSH, AWS CLI, VS Code Remote server
- Used as a **dev workbench** for Redis→S3 migration prototyping (TECH-3828/3830/3831)

## Python Environments

3 Python installations present (system Python 3.9, pip-installed packages):
- boto3, redis, botocore — for S3/Redis migration scripts
- No conda/virtualenv — bare pip installs

## Migration Scripts

Located in home directory — prototypes for the Redis→S3 cache migration:

| Script | Purpose |
|--------|---------|
| `migrate_redis_to_s3.py` | Core migration logic — reads Redis keys, serializes to S3 Parquet/JSON |
| `test_s3_cache.py` | Validates S3 cache reads match Redis source data |
| `speed_diff_test.py` | Benchmarks Redis vs S3 read latency (v1) |
| `speed_diff_v2.py` | Improved latency benchmark with batch operations |

> **Context:** These scripts support the TECH-3828/3830/3831 tickets for migrating NAV cache from Redis to S3. See [[../030-Projects/sidepocket-engineering|Sidepocket Engineering]] for formula details.

## Access

```bash
ssh -i ~/.ssh/sp-python-cache.pem ec2-user@<host>
```

## Related

- [[dev-ubuntu|Dev-Ubuntu Microservices Server]]
- [[../030-Projects/sidepocket-engineering|Sidepocket Engineering Notes]]
- [[../030-Projects/sidepocket-backend|Sidepocket Backend]]
