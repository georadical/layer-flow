# 🤖 Backend Development Subagents – NexusCouncil

**Purpose:**  
This document describes all specialized Codex subagents that collaborate to build and maintain the Django REST API backend for NexusCouncil.  
Each subagent operates atomically—one small, clear task at a time—and communicates through standardized prompts.

### 1️⃣ Model Agent
**Role:** Generate Django models and relations.  
**Creates:** `models/*.py`  
**Tasks:**  
- Define models with fields, relationships, `Meta` options.  
- Handle migrations automatically.  
- Follow naming convention `snake_case.py`.  

---

### 2️⃣ Serializer Agent
**Role:** Build `ModelSerializer` classes for REST exposure.  
**Creates:** `serializers/*.py`  
**Tasks:**  
- Include read-only and computed fields.  
- Handle nested serializers and validation logic.  

---

### 3️⃣ Viewset Agent
**Role:** Generate REST ViewSets for CRUD logic.  
**Creates:** `views/*.py`  
**Tasks:**  
- Implement list, retrieve, create, update, destroy.  
- Support filters, search, ordering, and pagination.  

---

### 4️⃣ Router Agent
**Role:** Register routes in `urls.py`.  
**Creates/Updates:** `urls.py`  
**Tasks:**  
- Use `DefaultRouter`.  
- Organize routes under `/api/<app_name>/`.  

---

### 5️⃣ Schema Agent
**Role:** Manage API schema and documentation.  
**Creates:** `schema.py` or integrates `drf-spectacular`.  
**Tasks:**  
- Auto-generate `/schema/` and `/docs/` endpoints.  

---

### 6️⃣ Auth Agent
**Role:** Implement authentication and permissions.  
**Creates/Updates:** `auth.py`, `permissions.py`.  
**Tasks:**  
- Configure JWT or Token Auth.  
- Enforce role-based access.  

---

### 7️⃣ Validation Agent
**Role:** Create reusable validation logic.  
**Creates:** `validators/*.py`  
**Tasks:**  
- Cross-field and model-level validation.  
- Reuse inside serializers and forms.  

---

### 8️⃣ Fixture Agent
**Role:** Produce mock data for testing and seeding.  
**Creates:** `fixtures/*.json`  
**Tasks:**  
- Generate demo data per app.  
- Support `loaddata` command for dev setup.  

---

### 9️⃣ Test Agent
**Role:** Automate backend testing.  
**Creates:** `tests/test_*.py`  
**Tasks:**  
- Unit and integration tests using `pytest`.  
- Validate endpoints, serializers, and models.  

---

### 🔟 CMS Sync Agent
**Role:** Keep frontend (Next.js) synchronized with backend CMS.  
**Creates/Updates:** `views/api_sync.py`  
**Tasks:**  
- Expose endpoints with cache and CORS.  
- Serve `SiteSettings`, `NavigationMenu`, and `PageSections` data to frontend.  

---

## Maintenance Notes
- Each subagent operates independently; Codex executes one prompt per agent.  
- Prompts must follow the atomic format (one task per file).  
- Integration order: Model → Serializer → Viewset → Router → Tests.  
- Shared utilities live under `nexus_council/core/utils/`.  


## Project-Specific Rules (from `tfs-backend-rules.md`)
- Commit format: `[YYYY-MM-DD] Brief summary`; include a bullet list of detailed changes in the body when committing.
- Code comments: add a descriptive English comment, immediately followed by its Spanish equivalent on the next line.
- Environment commands: provide Windows 11 Command Prompt-compatible commands for installs, file ops, and tooling.
- Unit tests: for every new function or class, add a corresponding `pytest` test under `tests/`; cover typical inputs and edge cases. If `tests/` does not exist yet, create it; do not relocate existing tests unless explicitly requested.
- Code style: PEP 8 conventions, `snake_case`, 4-space indents, max line length 88, and docstrings (Google/NumPy style) for every function and class.