"""Built-in developer roadmaps for common career paths.

Provides pre-configured roadmaps for AI/ML Engineer, Data Engineer,
Cloud Architect, Backend Developer, and Full-Stack Developer roles.
Each roadmap contains 10-15 skill nodes with realistic dependencies.
"""

from typing import Dict, List, Optional

from dharma.core import Roadmap, SkillNode


def _build_ai_ml_roadmap():
    # type: () -> Roadmap
    """Build the AI/ML Engineer roadmap."""
    nodes = [
        SkillNode("ml-python", "Python Programming", "fundamentals", 1,
                  [], ["docs.python.org"], "Core Python for ML", 40),
        SkillNode("ml-math", "Linear Algebra & Calculus", "fundamentals", 1,
                  [], ["3blue1brown.com"], "Math foundations for ML", 60),
        SkillNode("ml-stats", "Statistics & Probability", "fundamentals", 2,
                  ["ml-math"], ["khanacademy.org"], "Statistical foundations", 50),
        SkillNode("ml-numpy", "NumPy & Pandas", "tools", 2,
                  ["ml-python"], ["numpy.org"], "Data manipulation libraries", 30),
        SkillNode("ml-viz", "Data Visualization", "tools", 2,
                  ["ml-numpy"], ["matplotlib.org"], "Plotting and charts", 20),
        SkillNode("ml-sklearn", "Scikit-learn", "core", 3,
                  ["ml-numpy", "ml-stats"], ["scikit-learn.org"],
                  "Classical ML algorithms", 50),
        SkillNode("ml-dl-basics", "Deep Learning Fundamentals", "core", 3,
                  ["ml-sklearn", "ml-math"], ["deeplearning.ai"],
                  "Neural networks basics", 60),
        SkillNode("ml-pytorch", "PyTorch", "tools", 3,
                  ["ml-dl-basics"], ["pytorch.org"], "Deep learning framework", 50),
        SkillNode("ml-nlp", "Natural Language Processing", "specialization", 4,
                  ["ml-pytorch"], ["huggingface.co"], "Text and language AI", 60),
        SkillNode("ml-cv", "Computer Vision", "specialization", 4,
                  ["ml-pytorch"], ["opencv.org"], "Image and video AI", 60),
        SkillNode("ml-mlops", "MLOps & Deployment", "production", 4,
                  ["ml-sklearn", "ml-pytorch"], ["mlflow.org"],
                  "Model deployment pipelines", 40),
        SkillNode("ml-llm", "Large Language Models", "specialization", 5,
                  ["ml-nlp"], ["openai.com"], "Transformer architectures", 50),
        SkillNode("ml-rl", "Reinforcement Learning", "specialization", 5,
                  ["ml-dl-basics", "ml-stats"], ["spinningup.openai.com"],
                  "Agent-based learning", 60),
    ]
    return Roadmap(
        "ai-ml-engineer", "AI/ML Engineer",
        "Complete learning path from Python basics to advanced ML and AI",
        nodes,
    )


def _build_data_engineer_roadmap():
    # type: () -> Roadmap
    """Build the Data Engineer roadmap."""
    nodes = [
        SkillNode("de-python", "Python Programming", "fundamentals", 1,
                  [], ["docs.python.org"], "Python for data pipelines", 40),
        SkillNode("de-sql", "SQL & Databases", "fundamentals", 1,
                  [], ["sqlzoo.net"], "Relational databases and SQL", 40),
        SkillNode("de-linux", "Linux & Shell Scripting", "fundamentals", 1,
                  [], ["linuxcommand.org"], "Command line proficiency", 30),
        SkillNode("de-etl", "ETL Fundamentals", "core", 2,
                  ["de-python", "de-sql"], ["etl-best-practices.com"],
                  "Extract, transform, load concepts", 30),
        SkillNode("de-warehouse", "Data Warehousing", "core", 2,
                  ["de-sql"], ["cloud.google.com/bigquery"],
                  "Warehouse design and modeling", 40),
        SkillNode("de-spark", "Apache Spark", "tools", 3,
                  ["de-python", "de-etl"], ["spark.apache.org"],
                  "Distributed data processing", 50),
        SkillNode("de-kafka", "Apache Kafka", "tools", 3,
                  ["de-etl", "de-linux"], ["kafka.apache.org"],
                  "Event streaming platform", 40),
        SkillNode("de-airflow", "Apache Airflow", "tools", 3,
                  ["de-python", "de-etl"], ["airflow.apache.org"],
                  "Workflow orchestration", 35),
        SkillNode("de-dbt", "dbt (Data Build Tool)", "tools", 3,
                  ["de-sql", "de-warehouse"], ["getdbt.com"],
                  "Data transformation tool", 25),
        SkillNode("de-cloud", "Cloud Data Services", "platform", 4,
                  ["de-warehouse", "de-spark"], ["aws.amazon.com"],
                  "AWS/GCP/Azure data services", 50),
        SkillNode("de-streaming", "Real-time Processing", "advanced", 4,
                  ["de-kafka", "de-spark"], ["flink.apache.org"],
                  "Stream processing systems", 40),
        SkillNode("de-governance", "Data Governance", "advanced", 4,
                  ["de-warehouse", "de-cloud"], ["atlan.com"],
                  "Data quality and lineage", 30),
    ]
    return Roadmap(
        "data-engineer", "Data Engineer",
        "Build expertise in data pipelines, warehousing, and distributed systems",
        nodes,
    )


def _build_cloud_architect_roadmap():
    # type: () -> Roadmap
    """Build the Cloud Architect roadmap."""
    nodes = [
        SkillNode("ca-networking", "Networking Fundamentals", "fundamentals", 1,
                  [], ["networklessons.com"], "TCP/IP, DNS, load balancing", 40),
        SkillNode("ca-linux", "Linux Administration", "fundamentals", 1,
                  [], ["linux.org"], "Server management basics", 35),
        SkillNode("ca-cloud-basics", "Cloud Computing Basics", "fundamentals", 2,
                  ["ca-networking"], ["aws.amazon.com/training"],
                  "IaaS, PaaS, SaaS concepts", 30),
        SkillNode("ca-iam", "Identity & Access Management", "security", 2,
                  ["ca-cloud-basics"], ["docs.aws.amazon.com/IAM"],
                  "Authentication and authorization", 25),
        SkillNode("ca-compute", "Compute Services", "core", 2,
                  ["ca-cloud-basics", "ca-linux"], ["ec2.aws.amazon.com"],
                  "VMs, containers, serverless", 40),
        SkillNode("ca-storage", "Storage & Databases", "core", 3,
                  ["ca-cloud-basics"], ["aws.amazon.com/s3"],
                  "Object, block, and database storage", 35),
        SkillNode("ca-containers", "Containers & Kubernetes", "tools", 3,
                  ["ca-compute"], ["kubernetes.io"], "Container orchestration", 50),
        SkillNode("ca-iac", "Infrastructure as Code", "tools", 3,
                  ["ca-compute", "ca-storage"], ["terraform.io"],
                  "Terraform, CloudFormation", 40),
        SkillNode("ca-cicd", "CI/CD Pipelines", "devops", 3,
                  ["ca-containers"], ["github.com/features/actions"],
                  "Continuous integration and deployment", 30),
        SkillNode("ca-monitoring", "Monitoring & Observability", "devops", 4,
                  ["ca-compute", "ca-containers"], ["prometheus.io"],
                  "Logging, metrics, tracing", 35),
        SkillNode("ca-security", "Cloud Security", "security", 4,
                  ["ca-iam", "ca-networking"], ["owasp.org"],
                  "Security best practices", 40),
        SkillNode("ca-multi-cloud", "Multi-Cloud Architecture", "advanced", 5,
                  ["ca-iac", "ca-monitoring", "ca-security"],
                  ["cloud.google.com"], "Cross-provider strategies", 50),
    ]
    return Roadmap(
        "cloud-architect", "Cloud Architect",
        "Master cloud infrastructure, security, and multi-cloud strategies",
        nodes,
    )


def _build_backend_developer_roadmap():
    # type: () -> Roadmap
    """Build the Backend Developer roadmap."""
    nodes = [
        SkillNode("be-language", "Server-Side Language", "fundamentals", 1,
                  [], ["python.org"], "Python, Go, or Java", 50),
        SkillNode("be-git", "Git & Version Control", "fundamentals", 1,
                  [], ["git-scm.com"], "Source control fundamentals", 15),
        SkillNode("be-http", "HTTP & REST APIs", "fundamentals", 2,
                  ["be-language"], ["restfulapi.net"],
                  "HTTP protocol and REST design", 25),
        SkillNode("be-databases", "Relational Databases", "core", 2,
                  ["be-language"], ["postgresql.org"],
                  "SQL, indexing, transactions", 40),
        SkillNode("be-auth", "Authentication & Authorization", "core", 2,
                  ["be-http"], ["oauth.net"], "JWT, OAuth, sessions", 30),
        SkillNode("be-framework", "Web Framework", "tools", 3,
                  ["be-http", "be-databases"], ["flask.palletsprojects.com"],
                  "Django, Flask, or FastAPI", 40),
        SkillNode("be-nosql", "NoSQL Databases", "core", 3,
                  ["be-databases"], ["mongodb.com"],
                  "Document and key-value stores", 30),
        SkillNode("be-cache", "Caching Strategies", "core", 3,
                  ["be-framework"], ["redis.io"],
                  "Redis, Memcached, CDN caching", 25),
        SkillNode("be-queue", "Message Queues", "tools", 3,
                  ["be-framework"], ["rabbitmq.com"],
                  "Async processing with queues", 25),
        SkillNode("be-testing", "Testing & TDD", "practices", 3,
                  ["be-framework"], ["pytest.org"],
                  "Unit, integration, and e2e testing", 30),
        SkillNode("be-docker", "Docker & Containers", "devops", 4,
                  ["be-framework"], ["docker.com"],
                  "Containerized applications", 30),
        SkillNode("be-microservices", "Microservices Architecture", "advanced", 4,
                  ["be-docker", "be-queue", "be-cache"],
                  ["microservices.io"], "Distributed system design", 50),
        SkillNode("be-perf", "Performance Optimization", "advanced", 5,
                  ["be-microservices", "be-testing"],
                  ["loadtest.readthedocs.io"], "Profiling and tuning", 35),
    ]
    return Roadmap(
        "backend-developer", "Backend Developer",
        "From language fundamentals to microservices and performance",
        nodes,
    )


def _build_fullstack_developer_roadmap():
    # type: () -> Roadmap
    """Build the Full-Stack Developer roadmap."""
    nodes = [
        SkillNode("fs-html-css", "HTML & CSS", "frontend", 1,
                  [], ["developer.mozilla.org"], "Web fundamentals", 30),
        SkillNode("fs-javascript", "JavaScript", "frontend", 1,
                  [], ["javascript.info"], "Core JavaScript language", 50),
        SkillNode("fs-git", "Git & GitHub", "tools", 1,
                  [], ["git-scm.com"], "Version control basics", 15),
        SkillNode("fs-react", "React", "frontend", 2,
                  ["fs-javascript", "fs-html-css"], ["react.dev"],
                  "Component-based UI framework", 50),
        SkillNode("fs-node", "Node.js", "backend", 2,
                  ["fs-javascript"], ["nodejs.org"],
                  "Server-side JavaScript runtime", 35),
        SkillNode("fs-typescript", "TypeScript", "frontend", 2,
                  ["fs-javascript"], ["typescriptlang.org"],
                  "Typed JavaScript superset", 30),
        SkillNode("fs-databases", "Databases", "backend", 2,
                  ["fs-node"], ["postgresql.org"],
                  "SQL and NoSQL databases", 40),
        SkillNode("fs-api", "REST & GraphQL APIs", "backend", 3,
                  ["fs-node", "fs-databases"], ["graphql.org"],
                  "API design and implementation", 35),
        SkillNode("fs-state", "State Management", "frontend", 3,
                  ["fs-react"], ["redux.js.org"],
                  "Redux, Zustand, or Context API", 25),
        SkillNode("fs-auth", "Authentication", "backend", 3,
                  ["fs-api"], ["auth0.com"],
                  "Auth flows and session management", 30),
        SkillNode("fs-testing", "Full-Stack Testing", "practices", 3,
                  ["fs-react", "fs-api"], ["jestjs.io"],
                  "Frontend and backend testing", 30),
        SkillNode("fs-deploy", "Deployment & CI/CD", "devops", 4,
                  ["fs-api", "fs-react"], ["vercel.com"],
                  "Cloud hosting and pipelines", 30),
        SkillNode("fs-perf", "Performance & SEO", "advanced", 4,
                  ["fs-deploy", "fs-state"], ["web.dev"],
                  "Core Web Vitals and optimization", 25),
        SkillNode("fs-mobile", "Mobile Development", "advanced", 5,
                  ["fs-react", "fs-typescript"], ["reactnative.dev"],
                  "React Native cross-platform apps", 50),
    ]
    return Roadmap(
        "fullstack-developer", "Full-Stack Developer",
        "End-to-end web development from HTML to deployment and mobile",
        nodes,
    )


# Registry of all built-in roadmap builders
_ROADMAP_BUILDERS = {
    "ai-ml-engineer": _build_ai_ml_roadmap,
    "data-engineer": _build_data_engineer_roadmap,
    "cloud-architect": _build_cloud_architect_roadmap,
    "backend-developer": _build_backend_developer_roadmap,
    "fullstack-developer": _build_fullstack_developer_roadmap,
}


def get_roadmap(role_id):
    # type: (str) -> Optional[Roadmap]
    """Get a built-in roadmap by role ID.

    Args:
        role_id: One of 'ai-ml-engineer', 'data-engineer',
                 'cloud-architect', 'backend-developer',
                 'fullstack-developer'.

    Returns:
        The roadmap if found, None otherwise.
    """
    builder = _ROADMAP_BUILDERS.get(role_id)
    if builder is None:
        return None
    return builder()


def get_all_roadmaps():
    # type: () -> Dict[str, Roadmap]
    """Return all built-in roadmaps keyed by their role ID."""
    return {rid: builder() for rid, builder in _ROADMAP_BUILDERS.items()}


def list_available_roles():
    # type: () -> List[str]
    """Return a sorted list of available role IDs."""
    return sorted(_ROADMAP_BUILDERS.keys())
