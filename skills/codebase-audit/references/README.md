# Audit šablony — návod k použití

Sada READ-ONLY audit šablon pro kompletní analýzu aplikace. Agent si stack, moduly a kontext zjistí sám z repozitáře — soubory stačí zkopírovat do projektu a předat agentovi.

## Soubory

| Soubor | Oblast | Hlavní zaměření |
| :--- | :--- | :--- |
| `01_bezpecnost.md` | Bezpečnost | OWASP, auth, RBAC, injekce, XSS, CSRF, rate limit |
| `02_databaze.md` | Databáze & Data | Schéma, integrita, transakce, migrace, zálohy, NoSQL, Cache (Redis), fronty (Rabbit/Celery) |
| `03_e2e_testovani.md` | E2E testování | E2E testy — náhrada manuálního testování, CI integrace |
| `04_vykon.md` | Výkon | Backend, DB, bundle, rendering, memory leaky, async event loop |
| `05_kvalita_kodu.md` | Kvalita kódu | SOLID, duplikace, mrtvý kód, architektura, typová bezpečnost |
| `06_ux_ui.md` | UX & UI | Navigace, formuláře, feedback, stavy načítání, empty states |
| `07_pristupnost.md` | Přístupnost | WCAG 2.2 AA, klávesnice, čtečky, sémantika, kontrast |
| `08_dokumentace.md` | Dokumentace | README, API docs, deployment manuál, changelog |
| `09_devops_cicd.md` | DevOps & CI/CD | GitHub Actions, secrets v CI, Dockerfile (root vs user), lockfile integrity |
| `10_compliance_privacy.md` | Soukromí & Compliance | GDPR, PII v logách/Sentry, právo na výmaz, cookie consent, audit trail |

## Doporučený postup kompletní analýzy

### 1. Pořadí auditů (od kritických po kosmetické)

```text
1. 01_bezpecnost.md          → Bezpečnost má nejvyšší prioritu (kritická rizika se řeší hned)
2. 09_devops_cicd.md         → Build & deployment pipeline (ochrana CI/CD a produkčních secretů)
3. 02_databaze.md            → Integrita dat (ztráta dat = nevratné škody)
4. 10_compliance_privacy.md  → Ochrana osobních údajů (pokuty, úniky PII v logách)
5. 03_e2e_testovani.md       → Testovací záchranná síť = pojistka pro všechny další opravy
6. 04_vykon.md               → Škálovatelnost a propustnost
7. 05_kvalita_kodu.md        → Technický dluh a udržovatelnost
8. 06_ux_ui.md               → Uživatelská přívětivost
9. 07_pristupnost.md         → Přístupnost (a11y)
10. 08_dokumentace.md        → Dokumentace nakonec (dokumentuješ už opravený a finální stav)
```

### 2. Proces pro každý audit

1. **Spusť audit** — předej agentovi MD soubor, počkej na report (READ-ONLY, nic se nemění).
2. **Vyhodnoť report** — projdi matici nálezů, označ co schvaluješ / zamítáš / odkládáš.
3. **Schvaluj dávky** — nech opravovat po jednotlivých dávkách, ne vše najednou.
4. **Ověř regresi** — po každé dávce spusť lint + verify + test suite projektu.
5. **Teprve pak další dávka / další audit**.

### 3. Klíčové pravidlo: testy před velkým refaktoringem

Audity **01 (bezpečnost)**, **09 (CI/CD)** a **02 (databáze)** udělej a oprav **před** velkým refaktoringem z **05 (kvalita kódu)**. Pro bezpečný refaktoring ale potřebuješ testovací síť z **03 (e2e)** — jinak poznáš regresi až v produkci.

### 4. Poznámky

- Každý audit spouštěj v **nové konverzaci** (čistý kontext, agent není ovlivněn předchozími nálezy).
- Reporty ukládej do projektu (např. `audit/reporty/RRRR-MM-<oblast>.md`) — sleduješ pokrok a předejdeš opakování.
- Audity **01, 09 a 02** po dokončení oprav **zopakuj** — ověří, že opravy nezavedly nové problémy.
- Všechny šablony vynucují READ-ONLY režim, doložené nálezy (`soubor:řádek`) a čekání na schválení před jakoukoliv implementací.
