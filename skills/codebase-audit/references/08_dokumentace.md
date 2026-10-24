### ÚLOHA: Kompletní audit dokumentace a znalostní báze aplikace (READ-ONLY)

Tvým cílem je zajistit, aby kdokoliv nový (vývojář, admin, podpora) pochopil aplikaci pouze z dokumentace — bez nutnosti číst zdrojový kód.

Typ aplikace a cílové publikum dokumentace si zjisti sám z repozitáře (README, stávající `.md` soubory, složka `docs/`, docstringy).

---

#### ⛔ STRIKTNÍ PRAVIDLA AUDITU:
1. **REŽIM POUZE PRO ČTENÍ (READ-ONLY):** Za žádných okolností nevytvářej, nemaž, needituj ani nespouštěj zápisové operace v repozitáři.
2. **ŽÁDNÉ ZMĚNY BEZ POTVRZENÍ:** Žádný soubor nesmí být vytvořen/upraven bez mého výslovného souhlasu.
3. **DŮKAZY, NE DOMNĚNKY:** Každý nález dolož odkazem na konkrétní soubor (nebo jeho absenci).
4. **KONEC ÚLOHY:** Tvůj výstup končí předložením strukturovaného reportu a čekáním na instrukce.

---

#### ROZSAH ANALÝZY:
Projdi celý repozitář a všechny existující dokumentační artefakty z pohledu těchto oblastí:

1. **README a onboarding:**
   - Aktuální README obsahující: co aplikace dělá, stack, prerekvizity, jak spustit (dev i produkce), jak testovat, kde jsou entry pointy.
2. **Dokumentace architektury:**
   - Popis adresářové struktury (proč je co kde), klíčová design rozhodnutí (proč tento přístup), textový popis flow dat (request → middleware → handler → DB → response).
3. **API dokumentace:**
   - Seznam endpointů, request/response formáty, chybové kódy, příklady volání (curl / fetch), verzování API.
4. **Deployment a operace:**
   - Jak se aplikace nasazuje, konfigurace env proměnných a jejich význam, monitoring, zálohování, rollback postup, relevantní skripty.
5. **Datový model:**
   - Schéma DB (tabulky, vztahy, vysvětlení entit a jejich životního cyklu).
6. **Bezpečnost a compliance:**
   - Popis autentizačního/autorizačního flow, zacházení s citlivými údaji, GDPR aspekty (pokud relevantní).
7. **Inline komentáře:**
   - Public API funkce zdokumentovány (JSDoc/docstring), netriviální business logika má kontext, TODO/FIXME mají vlastníka a datum.
8. **Uživatelská dokumentace:**
   - Uživatelská příručka, FAQ, popis funkcí, screenshoty — pokud jsou pro typ aplikace relevantní.
9. **Changelog:**
   - Je udržován? Release poznámky srozumitelné uživatelům? Verzování konzistentní napříč projektem?

---

#### POŽADOVANÝ FORMÁT VÝSTUPU:

### 1. Rychlé shrnutí stavu
- Celkové hodnocení dokumentace (škála: **žádná dokumentace = kritický stav / fragmentovaná / dobře zdokumentováno**).
- TOP 3–5 mezer, které nejvíce brání novému člověku zapojit se do projektu.

### 2. Matice nálezů
U každého nálezu uveď:
- **ID:** DOC-XX
- **Soubor / Oblast:** co chybí nebo je chybné
- **Kategorie:** (Onboarding / Architektura / API / Deployment / Datový model / Komentáře / Uživatelská / Changelog)
- **Závažnost:** kritická (nezbytná pro spuštění/udržování) / vysoká / střední / nízká
- **Popis + co přesně chybí / je špatně**
- **Navrhovaná náprava:** co doplnit / opravit / přesunout

### 3. Rychlé výhry (quick wins)
- Návrhy, kde oprava < 30 minut.

### 4. Cílová struktura dokumentace
- Konkrétní návrh, jak má dokumentace vypadat po dokončení oprav (seznam souborů a jejich obsahu).

### 5. Doporučené dávky
- Logické celky, každý samostatně schvalovatelný.

---
Po vygenerování reportu se zastav a počkej, až ti jednotlivé dávky schválím. Neimplementuj nic.
