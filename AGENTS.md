# AGENTS.md - OpenCode & AI Agent Instructions

> Standing instructions, operating rules, and skill definitions for OpenCode and compatible AI coding agents.

---

## 🛡️ Critical Global Rules (P0)

1. **Evidence Before Assertions:**
   - Always run verification tests and inspect actual outputs before claiming a feature works or a bug is fixed.
   - Never finalize a task without 100% test pass confirmation.

2. **Strict Read-Only During Audits:**
   - When requested to audit, review, or inspect code, analyze files in **read-only mode**.
   - Provide exact file and line references (`path/to/file:L123-L145`).
   - Do NOT modify any code during an audit unless the user explicitly requests automatic remediation.

3. **Read → Understand → Apply:**
   - Read the relevant rules and references before proposing architecture or modifying critical systems.

---

## ⚡ Available Tools & Skills

### Codebase Audit Skill
- **Location:** `skills/codebase-audit/SKILL.md`
- **Audit References:** `skills/codebase-audit/references/` (01 to 10 covering Security, DB, Tests, Performance, Code Quality, UX/UI, Accessibility, Docs, DevOps, Compliance).
- **Static Scanner:**
  ```bash
  python skills/codebase-audit/scripts/audit_scan.py <project_root>
  ```

### How to run an audit in OpenCode:
- When asked to perform an audit, read the corresponding reference file from `skills/codebase-audit/references/` based on the user's focus (e.g. `01_bezpecnost.md` for security, `04_vykon.md` for performance).
- First run `python skills/codebase-audit/scripts/audit_scan.py .` for instant static analysis.
- Produce a structured Markdown audit report with:
  1. Executive Summary & Health Score (0–100%)
  2. Findings grouped by severity (Critical / High / Medium / Low / Info) with exact `file:line` locations
  3. Actionable remediation plan prioritized by risk
