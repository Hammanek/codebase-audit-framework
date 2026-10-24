### ÚLOHA: Kompletní E2E a integrační audit pro 100% náhradu manuálního testování (READ-ONLY)

Tvým cílem je navrhnout takovou sadu End-to-End (a souvisejících integračních) testů, aby **kompletně odpadla nutnost jakéhokoliv manuálního testování aplikace** před nasazením do produkce.

Stack, testovací framework i moduly aplikace si zjisti sám z repozitáře (README, `package.json`, složky `tests/`, `e2e/`, stávající test soubory).

---

#### ⛔ STRIKTNÍ BEZPEČNOSTNÍ PRAVIDLA:
1. **REŽIM POUZE PRO ČTENÍ (READ-ONLY):** Za žádných okolností nevytvářej, nemaž, needituj ani nespouštěj zápisové operace v repozitáři.
2. **ŽÁDNÝ KÓD BEZ POTVRZENÍ:** Žádný test nesmí být naimplementován bez předchozího předložení tohoto auditu a mého výslovného souhlasu.
3. **DŮKAZY, NE DOMNĚNKY:** Každé tvrzení o pokrytí či mezeře dolož konkrétním testovacím souborem nebo chybějícím testem s popisem scénáře.
4. **KONEC ÚLOHY:** Tvůj výstup končí předložením strukturovaného reportu a čekáním na instrukce.

---

#### ROZSAH ANALÝZY:
Projdi kompletně celý kód aplikace (frontend, backendové API kontrakty, routování, middleware, schémata formulářů a DB modely) a stávající testovací sadu. Hledej mezery ve všech těchto oblastech:

1. **Happy Paths & Core Flows:**
   - Kompletní průchody od startu do konce (např. registrace → onboarding → práce s daty/CRUD → export/dokončení akce → odhlášení).
2. **Validace a chybové stavy formulářů:**
   - Každé pole: prázdné vstupy, mezní délky, nevalidní formáty (XSS/SQLi payloady v polích, regex validace), zobrazení správných chybových hlášek, chování tlačítek (disabled stavy při odesílání – double click ochrana).
3. **Role, oprávnění a autentizace (RBAC):**
   - Co se stane, když nepřihlášený přistoupí na privátní URL?
   - Přístup uživatele s nízkými právy k admin route/funkcím (přímá URL i API/UI prvky).
   - Expirace tokenu/session a chování aplikace při odhlášení na jiné záložce.
4. **Edge Cases a datové anomálie:**
   - Prázdné stavy (Empty states) na všech seznamech a dashboardech.
   - Paginace, řazení, vyhledávání, kombinované filtry.
   - Mazání entit s vazbami (kaskády, varovné modály).
5. **Síť a asynchronní stavy:**
   - Reakce UI na chyby serveru (HTTP 400, 401, 403, 404, 500, timeout).
   - Zobrazení skeletonů / spinnerů při pomalém načítání.
   - Toast/Alert notifikace (úspěch vs. chyba).
   - **Offline chování / ztráta spojení v průběhu akce** (u PWA povinné).
6. **Konkurence a opakované akce:**
   - Double-click na submit tlačítko (disabled stav při odesílání).
   - Paralelní editační okna (stejná entita editovaná na dvou místech současně).
   - Refresh stránky během ukládání.
   - Race conditions (akce A a B ve stejnou chvíli na stejném datech).
7. **Testovací data a hygiena:**
   - Každý test po sobě uklidí — smaže své testovací záznamy, soubory, sessions a storage, aby po běhu sady nezůstala žádná testovací data v DB ani na disku.
   - Testy používají izolovanou databázi / izolované prostředí (jiný port, jiný DB soubor, in-memory DB, tmp složky).
   - Testy nemají oprávnění přistupovat k ostré databázi produkce.
   - Testovací data se poznají (jasný název, prefix `test_`, dedikovaná DB) — nikdy se nesmí smíchat s ostrými daty.
   - Testy běží v izolovaném adresáři, mimo produkční soubory.

---

#### POŽADOVANÝ FORMÁT VÝSTUPU:

### 1. Rychlý audit stávajícího stavu
- Které části aplikace mají testy a jaké je jejich reálné pokrytí (odhad v % pro každý modul).
- Které moduly jsou v současnosti zcela bez testů (slepá místa).
- **Audit kvality stávajících testů:** flaky testy, testy s prázdnými/slabými asserty, mrtvé testy (skip/only/commented), testy závislé na pořadí či sdíleném stavu.

### 2. Kompletní matice chybějících testů (připraveno pro automatizaci)
U každého navrženého testu uveď:
- **Modul / Obrazovka**
- **Typ testu:** (Happy Path / Negativní test / Validace / Edge Case / Oprávnění / Síťový stav / Konkurence)
- **Priorita:** P0 (kritický flow, blokátor release) / P1 (vysoká) / P2 (střední) / P3 (nice-to-have)
- **Scénář:** název scénáře
- **Kroky & Očekávaný výsledek:**
  1. Výchozí stav
  2. Provedená akce
  3. Ověření/Assert
- **Riziko absence testu:** Co přesně hrozí, pokud tento test chybí a netestuje se ručně.

### 3. Návrh sdílených utilit / fixtures
- Jaké testovací pomocníky (fixtures, seed skripty, mocky, custom lokátory) bude potřeba vytvořit, aby testy běžely stabilně a bez závislosti na náhodných datech.
- **Izolace testů:** jak zajistit, aby testy na sebe neměly vliv (DB, network, storage, port).
- **Úklid po testech:** záruka, že každý test po sobě smaže svá data (teardown/hook) a testovací sada nikdy nezasáhne produkční databázi. Popiš konkrétní mechanismus (např. `afterEach`/`afterAll`, in-memory DB, tmp složky, cleanup utility).
- **Reset stavu:** jaký mechanismus resetuje stav účtů/zámků mezi testy (např. testovací `unlock` endpoint), aby chyby z předchozích testů neblokovaly následné scénáře.

### 4. Definice hotova (DoD) pro testovací sadu
- Navrhni měřitelná kritéria, kdy je sada kompletní.

---
Po vygenerování tohoto reportu se zastav a počkej, až ti jednotlivé navržené bloky schválím.
