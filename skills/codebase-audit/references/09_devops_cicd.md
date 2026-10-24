### ÚLOHA: Kompletní audit DevOps, CI/CD a kontejnerizace (READ-ONLY)

Tvým cílem je provést důkladný audit CI/CD pipeline, buildovacích skriptů, kontejnerizace (Docker), správy tajemství a infrastructure-as-code (IaC). Odhalit slabiny, které by útočníkovi umožnily kompromitovat buildovací prostředí, propašovat škodlivý kód do produkce nebo odcizit produkční tajemství.

CI/CD platformu (GitHub Actions, GitLab CI, Bitbucket Pipelines), Dockerfile, compose soubory i deployment skripty si zjisti sám z repozitáře (`.github/workflows`, `.gitlab-ci.yml`, `Dockerfile`, `docker-compose.yml`, Helm charty, Makefile, `deploy.sh` atd.).

---

#### ⛔ STRIKTNÍ PRAVIDLA AUDITU:
1. **REŽIM POUZE PRO ČTENÍ (READ-ONLY):** Za žádných okolností neměň workflow soubory, nespouštěj buildy, neměň tagy ani netlač commity do repozitáře.
2. **ŽÁDNÉ ZÁSAHY BEZ POTVRZENÍ:** Žádná změna konfigurace CI/CD nesmí být provedena bez předložení reportu a výslovného souhlasu uživatele.
3. **DŮKAZY, NE DOMNĚNKY:** Každý nález dolož odkazem `soubor:řádek` a popisem reálného scénáře (např. jak by útočník přes Pull Request získal produkční secret).
4. **ZÁKAZ UVÁDĚNÍ SECRETŮ:** Pokud v repozitáři nebo workflow souboru narazíš na hardcoded tajemství, v reportu ho nikdy neuváděj celé — pouze uveď typ a přesné umístění.
5. **KONEC ÚLOHY:** Tvůj výstup končí předložením strukturovaného reportu a čekáním na instrukce.

---

#### ROZSAH ANALÝZY:
Projdi kompletně veškerou buildovací a konfigurační infrastrukturu projektu z pohledu těchto oblastí:

1. **GitHub Actions / CI/CD Workflow Security:**
   - **Trigger události a PR bezpečnost:** Zneužití `pull_request_target` v kombinaci s `checkout` kódu z forku (umožňuje spuštění cizího škodlivého kódu s přístupem k produkčním secretům repozitáře).
   - **Práva tokenu (`permissions`):** Jsou práva `GITHUB_TOKEN` omezena na minimum (`permissions: read-all` / `contents: read`), nebo má workflow implicitně plná práva k zápisu do repozitáře (`write`)?
   - **Pinning akcí a závislostí:** Používají třetí strany v `uses:` neměnný commit SHA hash (např. `actions/checkout@b4ffde...`), nebo pouze pohyblivý tag/větev (`@v4`, `@main`), který může útočník přepsat (Supply Chain Poisoning)?
   - **Script Injection ve workflows:** Vkládání uživatelských vstupů (např. `${{ github.event.issue.title }}`, branch name) přímo do `run:` bloků (Command Injection v runneru).

2. **Správa tajemství a prostředí (Secrets Management):**
   - Jsou tajemství (API klíče, deploy klíče, tokeny) uložena v zabezpečeném vaultu / Environment Secrets, nebo jsou hardcoded v compose/workflow souborech?
   - Ochrana před únikem secretů do build logů (nebezpečné `set-output`, `echo "$SECRET"`, tisk proměnných prostředí přes `env`).
   - Jsou produkční secrety chráněny vyžadovaným schválením před nasazením (Environment Protection Rules / Reviewers)?

3. **Kontejnerizace a Dockerfile:**
   - **Root vs. Non-Root:** Běží aplikace v kontejneru pod neprivilegovaným uživatelem (`USER appuser`), nebo jako `root`?
   - **Základní obrazy (Base images):** Používají se minimalizované a udržované obrazy (Alpine, Distroless, slim), s pinned konkrétní verzí (ne `:latest`)?
   - **Multi-stage builds:** Jsou buildovací nástroje (kompilátory, zdrojové kódy, SDK) odděleny od finálního runtime obrazu?
   - **`.dockerignore`:** Existuje soubor `.dockerignore`? Zabraňuje odeslání `.git`, `.env`, lokálních logů, privátních klíčů a `node_modules` do Docker build kontextu?
   - **Healthcheck:** Obsahuje Dockerfile instrukci `HEALTHCHECK` pro včasnou detekci zaseknutí kontejneru?

4. **Docker Compose & Lokální orchestrační prostředí:**
   - Jsou porty služeb (databáze, cache) vystaveny do všech rozhraní (`0.0.0.0:5432`), nebo jsou izolovány na interní síti kontejnerů / `127.0.0.1`?
   - Používají se výchozí hesla (např. `POSTGRES_PASSWORD=postgres`), která by mohla uniknout do produkce?
   - Omezení zdrojů: Jsou nastaveny limity na CPU a paměť (`limits: cpus, memory`), aby kontejner nemohl vyhladovět hostitele (OOM DoS)?

5. **Artefakty, závislosti a dodavatelský řetězec (Supply Chain):**
   - Jsou závislosti v projektu striktně uzamčeny lockfilem (`package-lock.json`, `poetry.lock`, `pnpm-lock.yaml`, `Pipfile.lock`, `Cargo.lock`)?
   - Používá CI/CD příkazy garantující shodu s lockfilem (`npm ci` místo `npm install`, `poetry install --frozen` apod.)?
   - Automatická kontrola zranitelností závislostí v CI (`npm audit`, `pip-audit`, `trivy`, `snyk`, `dependabot`).

6. **Branch Protection a integrita repozitáře:**
   - Je hlavní větev (`main`/`master`) chráněna proti přímému pushování (`branch protection` / `required pull request reviews`)?
   - Vyžaduje se úspěšný průchod testů a linteru před mergem?
   - Je vynuceno podepisování commitů (Signed commits)?

---

#### POŽADOVANÝ FORMÁT VÝSTUPU:

### 1. Rychlé shrnutí stavu
- Celkové hodnocení DevOps a CI/CD bezpečnosti (škála: **kritická rizika / vážné nedostatky / zabezpečený pipeline**).
- TOP 3–5 nejzávažnějších rizik (např. „potenciální RCE přes pull_request_target", „unikající secret v logu", „kontejner běžící pod rootem").

### 2. Matice nálezů
U každého nálezu uveď:
- **ID:** OPS-XX
- **Soubor a řádek:** `cesta/k/souboru:radek` (např. `.github/workflows/deploy.yml:34`)
- **Závažnost:** kritická / vysoká / střední / nízká / informační
- **Kategorie:** (Workflow Injection, Secrets, Docker, Supply Chain, Permissions, Network)
- **Popis + ověření v kódu**
- **Exploit scénář:** jak přesně by útočník slabinu zneužil (krok za krokem)
- **Dopad:** co útočník získá (např. kompromitace produkčního serveru, odcizení AWS/DB klíčů)
- **Navrhovaná náprava:** stručný popis správné konfigurace

### 3. Rychlé opravy (Quick Wins)
- Nálezy, kde je oprava otázkou několika řádků konfigurace a má okamžitý bezpečnostní dopad.

### 4. Doporučené dávky oprav
- Rozdělení do logických celků (Priorita P0 až P2) s odhadem rizika regrese.

### 5. Pozitivní posudek
- Co je v CI/CD a infrastruktuře nastaveno správně a odpovídá osvědčeným postupům.

---
Po vygenerování reportu se zastav a počkej, až ti jednotlivé dávky schválím. Neimplementuj nic.
