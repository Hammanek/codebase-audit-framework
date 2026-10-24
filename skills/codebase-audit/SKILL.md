---
name: codebase-audit
description: >-
  Use this skill whenever the user asks to perform an audit, code review, security analysis,
  database review, E2E test suite check, performance inspection, code quality/refactoring audit,
  UX/UI evaluation, accessibility (WCAG a11y) audit, DevOps/CI/CD review, compliance audit, or documentation review on a project.
---

# Codebase Audit Framework

Komplexní sada auditních metodik pro hloubkovou analýzu libovolného softwarového projektu.
Audit je vždy striktně **READ-ONLY** — zjišťuje reálný stav v kódu, identifikuje rizika a navrhuje prioritizované dávky oprav s doloženými důkazy (`soubor:řádek`).

---

## ⛔ Striktní pravidla pro všechny audity

1. **Režim pouze pro čtení (READ-ONLY):**
   - Za žádných okolností během auditu nevytvářej, nemaž, neupravuj soubory v repozitáři ani nespouštěj příkazy, které mění stav databáze či kódu.
2. **Žádné opravy bez schválení:**
   - Výstup auditu končí předložením strukturovaného reportu a čekáním na pokyny uživatele. Žádný kód se neopravuje automaticky.
3. **Důkazy, ne domněnky:**
   - Každý nález musí být doložen konkrétním odkazem na `soubor:řádek` a popisem reálného scénáře (jak se chyba projeví / jak ji lze zneužít).
4. **Citlivá data:**
   - Pokud v kódu narazíš na reálná tajemství (API klíče, hesla, tokeny), v reportu je nikdy neuváděj celé — pouze uveď typ a přesné umístění.

---

## Oblasti a šablony auditů

Detailní metodiky pro jednotlivé oblasti jsou uloženy v podadresáři `references/`:

| Oblast | Šablona | Hlavní zaměření |
| :--- | :--- | :--- |
| **01. Bezpečnost** | [01_bezpecnost.md](./references/01_bezpecnost.md) | OWASP, autentizace, session, RBAC/autorizace, SQLi, XSS, CSRF, rate limit, úniky dat, supply chain |
| **02. Databáze & Data** | [02_databaze.md](./references/02_databaze.md) | Schéma, integrita, transakce, indexy, N+1, NoSQL (MongoDB), Cache (Redis TTL), fronty (Rabbit/Celery) |
| **03. E2E testování** | [03_e2e_testovani.md](./references/03_e2e_testovani.md) | Pokrytí kritických uživatelských cest, stabilita testů, selektory, mock vs live API, CI integrace |
| **04. Výkon** | [04_vykon.md](./references/04_vykon.md) | Latence backendu, pomalé dotazy, velikost bundlu, rendering, memory leaky, caching |
| **05. Kvalita kódu** | [05_kvalita_kodu.md](./references/05_kvalita_kodu.md) | Architektura, SOLID, duplikace (DRY), mrtvý kód, chybové stavy, typová bezpečnost, tech dluh |
| **06. UX & UI** | [06_ux_ui.md](./references/06_ux_ui.md) | Navigace, formuláře a validace, stavy načítání, chybová hlášení, empty states, touch ergonomie |
| **07. Přístupnost** | [07_pristupnost.md](./references/07_pristupnost.md) | WCAG 2.2 AA, klávesová navigace, čtečky obrazovky, sémantické HTML, kontrast, tap targety |
| **08. Dokumentace** | [08_dokumentace.md](./references/08_dokumentace.md) | README, setup instrukce, API dokumentace, deployment manuál, changelog, inline komentáře |
| **09. DevOps & CI/CD** | [09_devops_cicd.md](./references/09_devops_cicd.md) | GitHub Actions/CI zranitelnosti, Dockerfile (root vs non-root), secrety v CI, branch protection |
| **10. Compliance & Soukromí** | [10_compliance_privacy.md](./references/10_compliance_privacy.md) | GDPR, PII v logách/Sentry, mazání dat (výmaz), cookie consent gating, neměnné auditní logy |

---

## Doporučený postup kompletního auditu

Pokud uživatel požaduje celkový audit projektu, postupuj v tomto pořadí priorit:

```text
1. 01_bezpecnost.md          → Nejvyšší priorita (kritická rizika je nutné identifikovat neprodleně)
2. 09_devops_cicd.md         → Build & deployment integrity (ochrana pipeline a produkčních secretů)
3. 02_databaze.md            → Integrita a ochrana dat (ztráta či poškození dat má nevratné následky)
4. 10_compliance_privacy.md  → Ochrana osobních údajů (PII v logách, právo na výmaz, consent)
5. 03_e2e_testovani.md       → Testovací záchranná síť (nutná pojistka před zahájením větších refaktoringů)
6. 04_vykon.md               → Škálovatelnost a propustnost
7. 05_kvalita_kodu.md        → Technický dluh a udržovatelnost
8. 06_ux_ui.md               → Uživatelská přívětivost
9. 07_pristupnost.md         → Přístupnost (a11y)
10. 08_dokumentace.md        → Zdokumentování aktuálního a opraveného stavu
```

---

## Pracovní postup agenta při auditu

1. **Kontext projektu:**
   - Nejdříve si samostatně prozkoumej repozitář: `package.json` / `requirements.txt`, README, strukturu složek, entry pointy serveru i klienta.
2. **Aktivace šablony:**
   - Načti příslušný referenční soubor z `references/<soubor>.md` podle oblasti zadané uživatelem.
3. **Analýza kódu:**
   - Důkladně prohledej kód pomocí vyhledávacích a čtecích nástrojů. Ověřuj každý podezřelý vzor až na úroveň řádku.
4. **Sestavení výstupního reportu:**
   - **Rychlé shrnutí stavu:** Celková známka/zhodnocení a TOP rizika.
   - **Matice nálezů:**
     - `ID`: např. `SEC-01`, `OPS-01`, `PRIV-01`, `DB-01`, `CODE-01`
     - `Soubor a řádek`: přesný odkaz `cesta/k/souboru:radek`
     - `Závažnost`: Kritická / Vysoká / Střední / Nízká / Info
     - `Kategorie`: např. SQL injection, N+1 query, Workflow Injection, PII v logu
     - `Popis a dopad`: konkrétní vysvětlení a reálný exploit/selhání
     - `Doporučená náprava`: stručný návod, jak problém vyřešit
   - **Návrh postupu oprav:** Rozdělení oprav do logických dávek (od kritických po kosmetické).
5. **Předání uživateli a čekání na schválení:**
   - Zeptej se uživatele, které nálezy chce schválit k opravě, a nezačínej implementaci bez potvrzení.
