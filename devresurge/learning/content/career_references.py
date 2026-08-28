"""Role-specific reference link blocks for career interview roadmaps."""

REF_DATA_ENGINEERING = """## Data engineering references

- [Fundamentals of Data Engineering (book)](https://www.fundamentals-of-data-engineering.com/)
- [dbt documentation](https://docs.getdbt.com/)
- [Apache Airflow docs](https://airflow.apache.org/docs/)
- [Apache Spark documentation](https://spark.apache.org/docs/latest/)
- [Kafka documentation](https://kafka.apache.org/documentation/)
- [Delta Lake](https://docs.delta.io/latest/index.html)
- [DevResurge quiz: SQL fundamentals](/quizzes/sql-fundamentals/)
- [DevResurge quiz: Databases internals](/quizzes/databases-internals/)
"""

REF_QA_SDET = """## QA / SDET references

- [ISTQB syllabus overview](https://www.istqb.org/certifications/certified-tester-foundation-level)
- [Ministry of Testing](https://www.ministryoftesting.com/)
- [Playwright documentation](https://playwright.dev/docs/intro)
- [Testing Trophy (Kent C. Dodds)](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
- [DevResurge quiz: Testing fundamentals](/quizzes/testing-fundamentals/)
- [DevResurge quiz: CI/CD DevOps](/quizzes/cicd-devops/)
"""

REF_BACKEND = """## Backend engineering references

- [DevResurge — Backend engineering roadmap](/learn/backend-engineering/)
- [HTTP APIs quiz](/quizzes/http-apis/)
- [SQL fundamentals quiz](/quizzes/sql-fundamentals/)
- [System design basics quiz](/quizzes/system-design-basics/)
- [MDN HTTP guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
- [Twelve-Factor App](https://12factor.net/)
"""

REF_CLOUD = """## Cloud engineering references

- [AWS Skill Builder](https://skillbuilder.aws/)
- [Azure Learn paths](https://learn.microsoft.com/en-us/training/azure/)
- [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [DevResurge — DevOps & SRE roadmap](/learn/devops-sre/)
"""

REF_DATA_SCIENCE = """## Data science references

- [Statistical Learning (ESL)](https://hastie.su.domains/ElemStatLearn/)
- [scikit-learn documentation](https://scikit-learn.org/stable/user_guide.html)
- [Causal Inference: The Mixtape (Huntington-Klein)](https://mixtape.scunning.com/)
- [Trustworthy Online Controlled Experiments (Kohavi et al.)](https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/)
- [Made With ML — MLOps primer](https://madewithml.com/)
- [DevResurge quiz: SQL fundamentals](/quizzes/sql-fundamentals/)
- [DevResurge quiz: Python fundamentals](/quizzes/python-fundamentals/)
- [DevResurge quiz: Data structures](/quizzes/data-structures/)
"""

REF_DEVSECOPS = """## DevSecOps references

- [OWASP DevSecOps guideline](https://owasp.org/www-project-devsecops-guideline/)
- [NIST SSDF](https://csrc.nist.gov/publications/detail/white-paper/2022/02/04/ssdf-v1-1-final/draft)
- [SLSA supply-chain levels](https://slsa.dev/)
- [Cosign — container signing](https://docs.sigstore.dev/cosign/overview/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [DevResurge — DevOps interview sprint](/learn/devops-interview/)
- [DevResurge quiz: Security basics](/quizzes/security-basics/)
- [DevResurge quiz: CI/CD DevOps](/quizzes/cicd-devops/)
"""

REF_DATA_SHARED = """## Shared data fundamentals (DE + DS)

- [Mode SQL tutorial](https://mode.com/sql-tutorial/)
- [pandas documentation](https://pandas.pydata.org/docs/user_guide/index.html)
- [DevResurge quiz: SQL fundamentals](/quizzes/sql-fundamentals/)
- [DevResurge quiz: Python fundamentals](/quizzes/python-fundamentals/)
- [Data engineering sprint](/learn/data-eng-interview/) · [Data science sprint](/learn/data-science-interview/)
"""

REF_QUESTIONS_DATA = """## Common data engineering interview questions

1. Design a batch pipeline from raw logs to analytics-ready tables.
2. Batch vs streaming — when would you pick each?
3. Explain idempotent backfills and late-arriving data.
4. How do you test data pipelines?
5. Star schema vs OBT — trade-offs?
6. Handle schema evolution in a warehouse.
7. Exactly-once semantics in Kafka — practical meaning?
8. SLAs for data freshness — how do you monitor?

**Spine:** sources → ingest → storage zones → transform → serve → monitor.
"""

REF_QUESTIONS_DATA_SCIENCE = """## Common data science interview questions

1. How would you predict customer churn? Walk through features, metric, baseline.
2. Explain bias-variance and how you'd diagnose overfitting.
3. Design an A/B test for a checkout change — sample size, guardrails, pitfalls.
4. Precision vs recall — when does each matter for fraud detection?
5. How do you detect and handle data leakage?
6. Explain a model you shipped and how you monitored it in production.
7. Correlation vs causation — when is observational data enough?
8. How would you explain a complex result to a non-technical executive?

**Spine:** business question → data → method → metric → recommendation → risks.
"""

REF_QUESTIONS_DEVSECOPS = """## Common DevSecOps interview questions

1. Where would you place security gates in a CI/CD pipeline and why?
2. Explain SBOM, artifact signing, and dependency scanning trade-offs.
3. Threat-model a microservice — STRIDE walkthrough.
4. How do you balance developer velocity vs security controls?
5. Container hardening checklist for production Kubernetes.
6. Secrets in Git history — response playbook.
7. Map controls to SOC2-style trust principles (high level).
8. Collaborate with SRE during a critical CVE — priorities and comms.

**Spine:** threat → proportional control → automation → evidence → culture.
"""

REF_QUESTIONS_QA = """## Common QA / SDET interview questions

1. Test pyramid vs trophy — where do E2E tests fit?
2. How do you test a REST API without a UI?
3. Flaky tests — root causes and fixes?
4. Design a CI test strategy for microservices.
5. Performance vs load vs stress testing?
6. Prioritize regression under time pressure?
7. Shift-left vs shift-right examples?
8. Test cases for login + MFA flow.

**Spine:** risk → test types → automation ROI → CI gates → escape rate.
"""

REF_QUESTIONS_BACKEND = """## Common backend interview questions

1. Design REST API with pagination and auth.
2. Idempotency keys in payment APIs.
3. N+1 query problem — detect and fix.
4. Caching strategies (cache-aside, write-through).
5. Database migration without downtime.
6. Rate limiting design.
7. JWT vs session cookies — trade-offs?
8. Debug p99 latency after deploy.

**Spine:** clarify → API → data model → scale → failure modes → observability.
"""

REF_QUESTIONS_CLOUD = """## Common cloud engineer interview questions

1. Design multi-account landing zone.
2. Network topology for hybrid cloud.
3. IAM least privilege for CI/CD.
4. DR — RTO/RPO planning.
5. Cost optimization without reliability loss.
6. Migrate monolith VM to managed Kubernetes.
7. Secrets rotation across environments.
8. Terraform state and drift remediation.

**Spine:** requirements → architecture → security → ops → cost → migration.
"""

REF_CAREER_MASTER = """## Career sprint master index

### Interview sprints (pick your role)

- [DevOps / SRE](/learn/devops-interview/)
- [DevSecOps](/learn/devsecops-interview/)
- [Data engineering](/learn/data-eng-interview/)
- [Data science](/learn/data-science-interview/)
- [QA / SDET](/learn/qa-interview/)
- [Backend engineering](/learn/backend-interview/)
- [Cloud engineering](/learn/cloud-interview/)

### Shared electives

- [Data fundamentals](/learn/data-fundamentals-elective/) — SQL, Python, stats refresh for DE & DS

### Regional electives (pick one country)

- [🇸🇪 Sweden](/learn/relocation-sweden/) · [🇦🇺 Australia](/learn/relocation-australia/) · [🇳🇿 New Zealand](/learn/relocation-new-zealand/) · [🇺🇸 USA](/learn/relocation-usa/) · [🇬🇧 UK](/learn/relocation-uk/)

### Migration sponsor paths (Volvo, IFS & peers)

- [🇸🇪 Sweden sponsors](/learn/sponsor-employers-sweden/) · [🇦🇺 Australia sponsors](/learn/sponsor-employers-australia/) · [🇺🇸 USA sponsors](/learn/sponsor-employers-usa/)

### Core craft roadmaps

- [Databases deep](/learn/databases-deep/) · [Backend engineering](/learn/backend-engineering/) · [DevOps & SRE](/learn/devops-sre/) · [System design](/learn/system-design/)
"""

CAREER_REF_BY_KEY: dict[str, str] = {
    "data_engineering": REF_DATA_ENGINEERING,
    "data_science": REF_DATA_SCIENCE,
    "data_shared": REF_DATA_SHARED,
    "devsecops": REF_DEVSECOPS,
    "qa_sdet": REF_QA_SDET,
    "backend_role": REF_BACKEND,
    "cloud_role": REF_CLOUD,
    "questions_data": REF_QUESTIONS_DATA,
    "questions_data_science": REF_QUESTIONS_DATA_SCIENCE,
    "questions_devsecops": REF_QUESTIONS_DEVSECOPS,
    "questions_qa": REF_QUESTIONS_QA,
    "questions_backend": REF_QUESTIONS_BACKEND,
    "questions_cloud": REF_QUESTIONS_CLOUD,
    "career_master": REF_CAREER_MASTER,
}
