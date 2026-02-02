# GhostTraceAI
Status: MVP Demo (Under Active Development 🚀)

Because AI chatbots don't know when their **docs** have expired.

# FOR MORE DETAILED INFO GO THROUGH THE CONTENT OF PPT IN DOCS FOLDER

***

## 🚩 Problem

Modern SaaS companies ship APIs aggressively:

```
v1.0 (2021) → v2.0 (2022) → v3.0 (2024, breaking changes)
```

**What happens:**
- Old docs, SDK guides, deprecation notices, migration guides sab knowledge base me mix
- RAG chatbot semantic similarity se docs retrieve karta hai
- Bot confidently **deprecated v1.0 API** suggest kar deta hai
- Developer code likhta hai → **production failure**
- No audit trail: "Bot ne kis purane doc ki wajah se galat jawab diya?"

**Real risks:**
```
1. Silent failures (deprecated endpoints)
2. Security holes (old auth patterns)
3. Compliance violations (outdated legal docs)
4. Developer productivity loss
```

***

## ✅ GhostTrace Solution

**Post-answer audit layer** for RAG chatbots.

**Developer asks:** "How do I charge a payment?"

**GhostTrace checks:**
1. Bot ne **kaunse docs** se answer banaya?
2. **Deprecated** docs use hue?
3. **Outdated versions** (v1.0 vs v3.0)?
4. Official **deprecation notice** ignore kiya?

**Outputs:**
```
Risk Score: 78/100 → HIGH
Reasons: 
  🚨 Deprecated: payment_api_v1.0_2021.txt
  ⚠️ Outdated: v1.0 (latest v3.0 available)
Explanation: "This can break integrations. Prioritize v3 docs."
```

***

## 🧩 Dataset: Realistic Product Company Knowledge Base

```
Core API Evolution:
├── payment_api_v1.0_2021.txt     # DEPRECATED, insecure
├── payment_api_v2.0_2022.txt     # Better, not latest
└── payment_api_v3.0_2024.txt     # LATEST, secure, tokenized

Supporting Docs:
├── auth_api_v1.0_2021.txt        # Legacy login
├── webhook_events_v3.0.txt       # v3 events
├── rate_limits_v3.0.txt          # Throttling
├── sdk_android_v2.0_guide.txt    # Client SDK
├── migration_guide_v1_to_v3.txt  # Migration steps
└── deprecation_notice_2024.txt   # "v1 disabled, migrate now"

Noise (real KB):
├── security_protocols_2023.txt
├── legal_compliance_policy.txt
└── it_infrastructure_overview.txt
```

**Why this dataset:**
- Mirrors Stripe/PayPal/Twilio API lifecycle  
- Version evolution + breaking changes + security fixes  
- Developer workflows (payment + auth + webhook + SDK)  
- Deprecation process + migration guidance  

***

## 🏗️ Architecture

```
Developer Query
       ↓
TF-IDF + FAISS Vector Search
       ↓
Risk Engine Analysis
  ├── Deprecated docs → +50
  ├── Outdated version → +25  
  ├── Ignoring notice → +15
  ├── Critical domain → ×1.3
       ↓
Human Explanation + Actions
       ↓
FastAPI → Streamlit Dashboard
```

***

## 🎯 Demo Flow

```
1. "How do I charge a payment?" → HIGH RISK (v1 deprecated)
2. "What are webhook events?" → LOW RISK (v3 latest)
3. "How to migrate v1→v3?" → MEDIUM RISK (mixed docs)
4. Judge's custom query → Live analysis
```

**Visuals:**
- Answer card  
- Risk score (big number + color)  
- Docs used table (file, version, deprecated?, doc_type)  
- Explanation paragraph  
- Action recommendations  

***

## 🛠️ Tech Stack

```
Data Pipeline:
├── Pandas + Regex → Metadata extraction
├── TF-IDF + FAISS → Vector search

Risk Engine:
├── Rule-based scoring (explainable)
└── Global metadata analysis

Demo:
├── FastAPI → Backend API
└── Streamlit → Interactive UI
```

***

## 💼 Business Value

```
✅ Developer productivity: 30% less API‑related production bugs
✅ Compliance: Audit trail for "why this wrong recommendation?"
✅ Cost savings: Proactive deprecated doc detection
✅ Customer trust: Accurate, safe dev assistant
```

**Market:**
- SaaS companies (Stripe, Twilio, SendGrid)  
- Enterprise dev portals (Confluence, Notion AI)  
- Internal RAG chatbots  

***

## 🚀 Quick Start

```bash
pip install -r requirements.txt
python data_ingestion/run_metadata.py   # ingest dataset
streamlit run dashboard/app.py          # launch
```

**One‑click demo:**
```bash
./demo/run_demo.sh
```

***

## 📈 Limitations → Roadmap

**MVP Scope:**
- Curated API docs dataset (realistic multi‑version)  
- Rule‑based risk (100% explainable)  
- Prototype RAG answers  

**v1.0 (Post‑hackathon):**
```
├── Real document stores (Confluence, Git repos)
├── Neural rerankers + LLM explanations
├── Real‑time monitoring dashboard
├── Multi‑tenant (multiple companies)
└── Plugin for LangChain / LlamaIndex
```

***

## 🏆 Why We Built This

> "AI chatbots confidently recommend **deprecated APIs** because they don't know when their knowledge expires.  
> GhostTrace makes those **silent failures visible**, **explainable**, and **actionable**."

**Built for:** Product companies shipping APIs → Internal dev teams → Support engineers.

***

## 📞 Contact

Team: Snap2Code  
Hackathon: HYPERSPACE  
Made with ❤️ for responsible AI.

