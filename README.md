<div align="center">

# Hi, I'm Shubhan 👋

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=900&color=7AA2F7&center=true&vCenter=true&width=640&lines=Backend+%26+Distributed+Systems+Engineer+%40+Entrupy;Event-driven+services+%7C+Payments+%26+billing+infra;Built+a+distributed+cache+in+Go+from+scratch;LLM+observability+%C2%B7+Kafka+%E2%86%92+ClickHouse+pipelines;Python+%C2%B7+Go+%C2%B7+AWS" alt="Typing SVG" />
</a>

<p>
  <a href="https://shubhanmehrotra.com"><img src="https://img.shields.io/badge/Portfolio-shubhanmehrotra.com-1f6feb?style=for-the-badge&logo=firefox&logoColor=white" alt="Portfolio"/></a>
  <a href="https://linkedin.com/in/shubhanmehrotra"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
  <a href="mailto:shubhanmehrotra@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
  <a href="./resume/shubhan-mehrotra-resume.pdf"><img src="https://img.shields.io/badge/Résumé-PDF-2ea043?style=for-the-badge&logo=readdotcv&logoColor=white" alt="Resume"/></a>
  <img src="https://komarev.com/ghpvc/?username=onyxmytrojin&style=for-the-badge&color=7aa2f7&label=PROFILE+VIEWS" alt="Profile views"/>
</p>

</div>

---

## 🛠️ Tech I reach for most

<div align="center">

<img src="https://skillicons.dev/icons?i=python,go,typescript,java,cpp,fastapi,django,react,postgres,mysql,redis,kafka&perline=12" alt="skills row 1" />
<br/>
<img src="https://skillicons.dev/icons?i=aws,docker,kubernetes,nginx,linux,bash,git,github,vercel,graphql,cloudflare,grafana&perline=12" alt="skills row 2" />

</div>

**Languages** &nbsp;
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white)
![C++](https://img.shields.io/badge/C%2B%2B-00599C?style=flat-square&logo=cplusplus&logoColor=white)

**Backend** &nbsp;
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Django](https://img.shields.io/badge/Django%2FDRF-092E20?style=flat-square&logo=django&logoColor=white)
![REST](https://img.shields.io/badge/REST%20APIs-005571?style=flat-square&logo=fastapi&logoColor=white)
![Microservices](https://img.shields.io/badge/Microservices-6DB33F?style=flat-square&logo=spring&logoColor=white)

**Data &amp; infra** &nbsp;
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![DynamoDB](https://img.shields.io/badge/DynamoDB-4053D6?style=flat-square&logo=amazondynamodb&logoColor=white)
![ClickHouse](https://img.shields.io/badge/ClickHouse-FFCC01?style=flat-square&logo=clickhouse&logoColor=black)
![Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)

**Cloud &amp; DevOps** &nbsp;
![AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-FF9900?style=flat-square&logo=awslambda&logoColor=white)
![SQS](https://img.shields.io/badge/Amazon%20SQS-FF4F8B?style=flat-square&logo=amazonsqs&logoColor=white)
![EventBridge](https://img.shields.io/badge/EventBridge-FF4F8B?style=flat-square&logo=amazoneventbridge&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)

---

## ⚡ Currently

- **Software Engineer @ Entrupy** — building FastAPI microservices behind a customer-facing analytics dashboard (**10K+ daily users**); designing an event-driven payment-recovery engine on **AWS Lambda + SQS FIFO + EventBridge**; shipped a server-side **RBAC** framework with JWT token-exchange for row-level data isolation.
- Rewrote a cold-cache analytical query into a parallelized two-pass pipeline — **p99 endpoint latency down 95%+** for large accounts.

## 📌 Selected work

| Project | What it is | Stack | Links |
|---|---|---|---|
| **[phoneix](https://github.com/onyxmytrojin/phoneix)** | A self-healing distributed cache built from scratch — consistent hashing (150 vnodes/peer), gossip failure detection, zero-downtime rebalancing — plus a personal API + live dashboard, all running on a Pixel 7a. | `Go` `FastAPI` `vanilla JS` | [Live](https://shubhanmehrotra.com) · [Kill-a-node demo](https://shubhanmehrotra.com/cluster) |
| **[ollive-inference-logger](https://github.com/onyxmytrojin/ollive-inference-logger)** | LLM inference observability. A decorator auto-instruments any provider call (latency, tokens, I/O) with zero call-site code; logs flow HTTP → Kafka → ClickHouse, decoupled from the request path. PII redacted before it leaves the process. | `Django/DRF` `React` `Kafka` `ClickHouse` `Postgres` `K8s` | [Live](https://ollive-inference-logger-black.vercel.app) |
| **[pixel-server](https://github.com/onyxmytrojin/pixel-server)** | A Pixel 7a turned into a 24/7 headless Debian server — GrapheneOS + Magisk + proot, public routing via Cloudflare Tunnel (no static IP), Docker Compose services under a 6GB RAM budget, ~3–5W idle. | `Linux` `Shell` `Docker` `Nginx` `Cloudflare` | — |
| **[securelife-crm](https://github.com/onyxmytrojin/securelife-crm)** | AI insurance CRM: a chatbot qualifies leads through conversation, Claude extracts policy details from uploaded PDFs, an LLM persona generates coverage-gap analysis, and a Kanban board tracks the pipeline. | `Next.js` `TypeScript` `Supabase` `Groq` `Claude` | [Live](https://securelife-crm.vercel.app) |

<sub>Also on the résumé: agentic RAG / retrieval-evaluation work (Inter-IIT Tech Meet 13.0), and dataset + training-throughput work at TCS Research.</sub>

---

## 📊 GitHub

<div align="center">

<img height="170" src="https://github-readme-stats.vercel.app/api?username=onyxmytrojin&show_icons=true&hide_border=true&include_all_commits=true&count_private=true&theme=tokyonight&icon_color=7aa2f7&title_color=7aa2f7" alt="stats" />
<img height="170" src="https://github-readme-stats.vercel.app/api/top-langs/?username=onyxmytrojin&layout=compact&hide_border=true&langs_count=8&hide=html,jupyter%20notebook,css&theme=tokyonight&title_color=7aa2f7" alt="top languages" />

<img width="98%" src="https://github-readme-activity-graph.vercel.app/graph?username=onyxmytrojin&bg_color=1a1b27&color=7aa2f7&line=7aa2f7&point=bb9af7&area=true&hide_border=true" alt="activity graph" />

<img src="https://github-readme-streak-stats.herokuapp.com/?user=onyxmytrojin&hide_border=true&theme=tokyonight&ring=7aa2f7&fire=bb9af7&currStreakLabel=7aa2f7" alt="streak" />

</div>
