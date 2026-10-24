# Codebase Audit Framework & Agent Protocol 🛡️⚡

> **Kompletní produkční sada auditních metodik, statických skenerů a globálních pravidel pro AI vývojové asistenty (Antigravity, OpenCode, Cursor, Claude Code, Windsurf).**

Tento repozitář obsahuje ucelenou sadu 10 auditních šablon, rychlý statický analyzátor a striktní procesní pravidla garantující, že AI agent provádí analýzy na základě reálných důkazů (`soubor:řádek`), nezpůsobuje regrese a nepouští se do změn kódu bez předchozího otestování.

---

## 📋 Obsah repozitáře

```text
├── AGENTS.md                        # Nativní instrukce a pravidla pro OpenCode & kompatibilní agenty
├── opencode.json                    # Konfigurace instrukcí pro OpenCode CLI / IDE
├── skills/
│   └── codebase-audit/
│       ├── SKILL.md                 # Hlavní instrukční soubor pro AI agenty
│       ├── scripts/
│       │   └── audit_scan.py        # Rychlý Python skener pro statickou kontrolu
│       └── references/              # 10 specializovaných auditních šablon
│           ├── README.md            # Návod k použití a procesní řetězec
│           ├── 01_bezpecnost.md     # OWASP 2025, Auth, CSRF, CSP, Injekce
│           ├── 02_databaze.md       # SQL, NoSQL (MongoDB), Redis cache, Fronty
│           ├── 03_e2e_testovani.md  # E2E testovací záchranná síť, Playwright
│           ├── 04_vykon.md          # Latence, memory leaky, DOM thrashing, Async
│           ├── 05_kvalita_kodu.md   # SOLID, DRY, mrtvý kód, architektura
│           ├── 06_ux_ui.md          # Ergonomie, formuláře, loading states
│           ├── 07_pristupnost.md    # WCAG 2.2 AA, klávesnice, kontrast
│           ├── 08_dokumentace.md    # README, API docs, deployment manuál
│           ├── 09_devops_cicd.md    # GitHub Actions, Docker, secret leakage
│           └── 10_compliance_privacy.md # GDPR, PII v logách, cookie consent
└── rules/
    ├── 00_global_rules.md           # Povinné testování & evidence before assertions
    ├── 01_core_protocol.md          # Read -> Understand -> Apply metodika
    └── 02_universal_rules.md        # Clean Code & komunikační standardy
```

---

## 🎯 10 Auditních pilířů

| # | Oblast | Šablona | Hlavní zaměření |
| :-: | :--- | :--- | :--- |
| **01** | **Bezpečnost** | [`01_bezpecnost.md`](skills/codebase-audit/references/01_bezpecnost.md) | OWASP Top 10, autentizace, session, RBAC, SQLi, XSS, CSRF, rate limit |
| **02** | **DevOps & CI/CD** | [`09_devops_cicd.md`](skills/codebase-audit/references/09_devops_cicd.md) | GitHub Actions, Docker (root vs non-root), secrety v CI, lockfile integrita |
| **03** | **Databáze & Data** | [`02_databaze.md`](skills/codebase-audit/references/02_databaze.md) | Schéma, cizí klíče, transakce, NoSQL (MongoDB), Redis TTL, RabbitMQ fronty |
| **04** | **Soukromí & GDPR** | [`10_compliance_privacy.md`](skills/codebase-audit/references/10_compliance_privacy.md) | PII v logách, právo na výmaz, consent gating, audit trail |
| **05** | **E2E testování** | [`03_e2e_testovani.md`](skills/codebase-audit/references/03_e2e_testovani.md) | Pokrytí kritických uživatelských cest, stabilita selektorů, CI běh |
| **06** | **Výkon** | [`04_vykon.md`](skills/codebase-audit/references/04_vykon.md) | Latence backendu, memory leaky, DOM layout thrashing, unblocking event loop |
| **07** | **Kvalita kódu** | [`05_kvalita_kodu.md`](skills/codebase-audit/references/05_kvalita_kodu.md) | SOLID principy, DRY, mrtvý kód, typová bezpečnost, technický dluh |
| **08** | **UX & UI** | [`06_ux_ui.md`](skills/codebase-audit/references/06_ux_ui.md) | Navigace, validace formulářů, zpětná vazba, chybová hlášení, empty states |
| **09** | **Přístupnost (a11y)** | [`07_pristupnost.md`](skills/codebase-audit/references/07_pristupnost.md) | WCAG 2.2 AA, navigace z klávesnice, čtečky obrazovky, barevný kontrast |
| **10** | **Dokumentace** | [`08_dokumentace.md`](skills/codebase-audit/references/08_dokumentace.md) | README, setup instrukce, API dokumentace, deployment manuál |

---

## ⚡ Rychlý statický skener (`audit_scan.py`)

Součástí frameworku je samostatný Python skript pro okamžitou prověrku projektu bez externích závislostí:

```bash
python skills/codebase-audit/scripts/audit_scan.py /cesta/k/projektu
```

Skener automaticky detekuje:
- Otevřené síťové vystavení (`0.0.0.0`) bez autentizace
- Příkazy spouštěné přes `subprocess` s rizikovým `shell=True`
- Volání `subprocess.run` bez explicitního `timeout` (hrozba DoS a zablokování vláken)
- Nebezpečnou deserializaci (`pickle.loads`, `eval`)
- Dockerfile běžící pod neprivilegovaným uživatelem vs. `root`
- Nepinnuté GitHub Actions tagy náchylné k Supply Chain útokům

---

## 🧠 Globální pravidla agenta (Agent Rules)

Základní filozofie, kterou tento repozitář prosazuje pro spolupráci s AI agenty:

1. **Evidence Before Assertions:** Agent nesmí tvrdit, že kód funguje, dokud fyzicky nespustí testy a neověří jejich 100% průchod.
2. **Striktní READ-ONLY při auditu:** Při analýze agent pouze čte kód a reportuje nálezy s přesným odkazem `soubor:řádek`. Neupravuje ani řádek kódu bez předchozího schválení uživatelem.
3. **Prioritní řetězec:** Opravy se vždy provádějí v logických dávkách: nejdříve bezpečnost a databáze, poté testovací záchranná síť, a teprve poté refaktoring.

---

## 📥 Jak integrovat do vývojového prostředí

### 1. OpenCode (`opencode`)
OpenCode automaticky detekuje instrukce a pravidla v kořeni repozitáře i globálně:

* **Projektová integrace:**
  - V kořeni tvého projektu nechej soubor `AGENTS.md` a `opencode.json` (nebo do něj přidej cestu k `rules/*.md`).
  - Pro načítání skillů nakopíruj nebo nalinkuj složku skillu do `.opencode/skills/`:
    ```bash
    mkdir -p .opencode/skills
    cp -r skills/codebase-audit .opencode/skills/
    ```
  - OpenCode skilly automaticky objeví v `.opencode/skills/` i `.agents/skills/`.

* **Globální konfigurace pro všechny projekty:**
  - Zkopíruj `AGENTS.md` do globálního adresáře OpenCode:
    - Linux / macOS: `~/.config/opencode/AGENTS.md`
    - Windows: `%USERPROFILE%\.config\opencode\AGENTS.md`

### 2. Google Antigravity
Zkopíruj složku `skills/codebase-audit` do tvého konfiguračního adresáře:
```bash
cp -r skills/codebase-audit ~/.gemini/config/skills/
```

### 3. Claude Code / Cursor / Windsurf
Přidej obsah souborů z `rules/` do tvých instrukcí pro asistenta (`.cursorrules`, `CLAUDE.md` nebo system promptu) a přilož příslušné šablony z `references/` před zahájením auditu.

---

## 📄 Licence
Tento framework je k dispozici pro osobní a komerční vývojové účely.
