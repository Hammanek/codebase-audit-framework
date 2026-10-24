### ÚLOHA: Kompletní audit soukromí, compliance a ochrany osobních údajů (READ-ONLY)

Tvým cílem je prověřit aplikaci z hlediska ochrany osobních údajů (GDPR, CCPA), zacházení s citlivými daty (PII - Personally Identifiable Information), čistoty aplikačních logů, správy souhlasů (cookies/trackery) a auditovatelnosti kritických operací.

Architekturu, moduly ukládající uživatelská data, logovací subsystémy i klientské trackery si zjisti sám z repozitáře (DB moduly, loggery, Sentry/analytics integrace, frontendové cookie handlery, exportní/mazací rutiny).

---

#### ⛔ STRIKTNÍ PRAVIDLA AUDITU:
1. **REŽIM POUZE PRO ČTENÍ (READ-ONLY):** Za žádných okolností neměň kód, nespouštěj databázové skripty ani nesahej do reálných uživatelských dat.
2. **ŽÁDNÉ ZÁSAHY BEZ POTVRZENÍ:** Žádné úpravy schémat, logování ani cookie mechanismů nesmí být provedeny bez předchozího předložení reportu a výslovného souhlasu uživatele.
3. **DŮKAZY, NE DOMNĚNKY:** Každý nález dolož odkazem `soubor:řádek` a vysvětlením, jak k porušení ochrany soukromí dochází (např. v jaké situaci se heslo, e-mail nebo IP adresa zapíše do nekódovaného logu).
4. **ZÁKAZ LOGOVÁNÍ REÁLNÝCH PII:** Pokud při auditu narazíš na reálná osobní data (v testovacích datasetech, seedech nebo konfiguracích), v reportu je maskuj (např. `j***@example.com`).
5. **KONEC ÚLOHY:** Tvůj výstup končí předložením strukturovaného reportu a čekáním na instrukce.

---

#### ROZSAH ANALÝZY:
Projdi aplikaci, API endpointy, databázi, logovací mechanismy a klientský frontend z pohledu těchto oblastí:

1. **Logování a informační úniky (PII in Logs):**
   - **Logování citlivých parametrů:** Zapisují se do aplikačních logů (či externích služeb typu Datadog, Sentry, CloudWatch) hesla v otevřeném tvaru, platební údaje (čísla karet, CVV), API klíče, session tokeny, rodná čísla nebo zdravotní údaje?
   - **IP adresy a metadata v logu:** Jsou IP adresy uživatelů anonymizovány / zkracovány (např. pro statistiky), nebo ukládány v plném znění bez právního titulu a retenční politiky?
   - **URL Query parametry:** Nepředávají se citlivé údaje (tokeny, reset hesla, e-maily) v URL adrese dotazů (`GET /reset?token=...`), které se pak ukládají do access logů proxy serverů, CDN a historie prohlížeče?
   - **Stacktraces:** Neunikají v produkčních chybových hlášeních citlivé parametry SQL dotazů či hodnoty proměnných?

2. **Ukládání a minimalizace osobních údajů (Data Minimization):**
   - Dodržuje aplikace princip minimalizace (ukládá se pouze to, co je nezbytné pro danou službu)?
   - Šifrování citlivých osobních údajů v databázi (Encryption at Rest — hashování hesel je samozřejmost, ale jsou šifrována např. bankovní spojení či osobní dokumenty)?
   - Jsou přístupová práva k PII v kódu omezena (RBAC — má k nim přístup jen ten modul/uživatel, který je nezbytně potřebuje)?

3. **Životní cyklus dat a retenční politika (Retention & Deletion):**
   - **Právo na výmaz (Right to be Forgotten):** Má aplikace implementován bezpečný a kompletní proces smazání uživatele ze všech tabulek, cache a záložních úložišť?
   - **Soft-delete vs. Hard-delete:** Pokud aplikace používá `is_deleted = true`, dochází po uplynutí zákonné lhůty k fyzickému hard-delete či anonymizaci, nebo data zůstávají v DB navždy?
   - **Expirace neaktivních účtů a dočasných dat:** Mazání neověřených registrací, expirovaných reset tokenů, starých session a audit logů po uplynutí retenční lhůty.

4. **Právo na přístup a přenositelnost dat (Data Portability):**
   - Poskytuje aplikace možnost exportu uživatelských dat (Data Takeout, např. JSON/CSV export)?
   - Nezahrnuje export citlivá interní systémová data (např. interní poznámky administrátorů, fraud skóre, hashe hesel)?

5. **Cookies, souhlasy a sledování (Cookies & Consent):**
   - **Striktní kategorizace:** Jsou cookies rozděleny na nezbytné (technické), analytické a marketingové?
   - **Odložené načítání trackerů:** Jsou skripty třetích stran (Google Analytics, Meta Pixel, Hotjar atd.) blokovány až do udělení explicitního souhlasu (Opt-In), nebo se načítají okamžitě při vstupu na stránku?
   - **Stejná dostupnost odmítnutí:** Umožňuje cookie banner stejně snadné odmítnutí jako přijetí (zákaz "dark patterns")?

6. **Audit Trail a neměnnost záznamů (Audit Logging):**
   - Jsou kritické operace (změna práv, přístup k citlivým PII, změna hesla/e-mailu, export dat) auditovány (kdo, kdy, jaká akce, z jaké IP)?
   - Je auditní log chráněn proti přepsání či smazání samotnými administrátory (Append-only princip)?

---

#### POŽADOVANÝ FORMÁT VÝSTUPU:

### 1. Rychlé shrnutí stavu
- Celkové hodnocení souladu s ochranou osobních údajů (škála: **kritická rizika pokut a úniků / vážné nedostatky / dobrý stav ochrany soukromí**).
- TOP 3–5 rizik (např. „hesla a tokeny v plaintextu v aplikačním logu", „analytika spuštěná před udělením souhlasu", „chybějící proces pro výmaz dat").

### 2. Matice nálezů
U každého nálezu uveď:
- **ID:** PRIV-XX
- **Soubor a řádek:** `cesta/k/souboru:radek`
- **Závažnost:** kritická / vysoká / střední / nízká / informační
- **Kategorie:** (PII Logging, Minimalizace, Právo na výmaz, Cookies & Consent, Audit Trail, Šifrování)
- **Popis + ověření v kódu**
- **Scénář selhání / riziko:** jak k úniku nebo porušení předpisů dochází
- **Dopad:** právní riziko, pokuta, reputační škoda, ohrožení soukromí uživatelů
- **Navrhovaná náprava:** jak kód upravit (sanitizace, anonymizace, implementace consent gatingu)

### 3. Rychlé opravy (Quick Wins)
- Okamžité opravy nevyžadující změnu architektury (např. odfiltrování citlivých klíčů v loggeru).

### 4. Doporučené dávky oprav
- Rozdělení do dávek s vyhodnocením složitosti a rizika regrese.

### 5. Pozitivní posudek
- Co je v oblasti soukromí a minimalizace dat implementováno vzorně.

---
Po vygenerování reportu se zastav a počkej, až ti jednotlivé dávky schválím. Neimplementuj nic.
