# Shubhan Mehrotra

**Backend & Distributed Systems Engineer** — I build event-driven services, billing/payments infrastructure, and systems software (a distributed cache in Go, an LLM observability pipeline). Mostly Python, Go, and AWS.

📍 Bangalore, India &nbsp;·&nbsp; 🌐 [shubhanmehrotra.com](https://shubhanmehrotra.com) &nbsp;·&nbsp; 💼 [LinkedIn](https://linkedin.com/in/shubhanmehrotra) &nbsp;·&nbsp; ✉️ shubhanmehrotra@gmail.com &nbsp;·&nbsp; 📄 [Resume](./resume/shubhan-mehrotra-resume.pdf)

---

### Currently

- **Software Engineer @ Entrupy** — building FastAPI microservices behind a customer-facing analytics dashboard (10K+ daily users); designing an event-driven payment-recovery engine on AWS Lambda + SQS FIFO + EventBridge; shipped a server-side RBAC framework with JWT token-exchange for row-level data isolation.
- Rewrote a cold-cache analytical query into a parallelized two-pass pipeline — **p99 endpoint latency down 95%+** for large accounts.

### Selected work

| Project | What it is | Stack | Links |
|---|---|---|---|
| **[phoneix](https://github.com/onyxmytrojin/phoneix)** | A self-healing distributed cache built from scratch — consistent hashing (150 vnodes/peer), gossip failure detection, zero-downtime rebalancing — plus a personal API + live dashboard, all running on a Pixel 7a. | Go, FastAPI, vanilla JS | [Live](https://shubhanmehrotra.com) · [Kill-a-node demo](https://shubhanmehrotra.com/cluster) |
| **[ollive-inference-logger](https://github.com/onyxmytrojin/ollive-inference-logger)** | LLM inference observability platform. A decorator auto-instruments any provider call (latency, tokens, I/O) with zero call-site code; logs flow HTTP → Kafka → ClickHouse, decoupled from the request path. PII redacted before it leaves the process. | Django/DRF, React, Kafka, ClickHouse, Postgres, K8s | [Live](https://ollive-inference-logger-black.vercel.app) |
| **[pixel-server](https://github.com/onyxmytrojin/pixel-server)** | A Pixel 7a turned into a 24/7 headless Debian server — GrapheneOS + Magisk + proot, public routing via Cloudflare Tunnel (no static IP), Docker Compose services under a 6GB RAM budget, ~3–5W idle. | Linux, Shell, Docker, Nginx, Cloudflare | — |
| **[securelife-crm](https://github.com/onyxmytrojin/securelife-crm)** | AI insurance CRM: a chatbot qualifies leads through conversation, Claude extracts policy details from uploaded PDFs, an LLM persona generates coverage-gap analysis, and a Kanban board tracks the pipeline. | Next.js, TypeScript, Supabase, Groq, Claude | [Live](https://securelife-crm.vercel.app) |

### Stack

**Languages** Python · Go · TypeScript · SQL · Java · C/C++
**Backend** FastAPI · Django/DRF · REST · microservices · billing systems
**Data & infra** PostgreSQL · DynamoDB · ClickHouse · Kafka · SQS · Redis-style caching
**Cloud & DevOps** AWS (Lambda, SQS, EventBridge, ECS, S3, IAM, CloudWatch) · Docker · Kubernetes · CI/CD

---

<sub>Also on the resume: RAG/retrieval-evaluation work (Inter-IIT Tech Meet 13.0), dataset & training-throughput work at TCS Research.</sub>
