### ÚLOHA: Kompletní E2E Playwright audit pro 100% náhradu manuálního testování (READ-ONLY)

Tvým cílem je navrhnout takovou sadu End-to-End (a souvisejících integračních) testů v **Playwrightu**, aby **kompletně odpadla nutnost jakéhokoliv manuálního testování aplikace** před nasazením do produkce.

Stack, stávající testy i moduly aplikace si zjisti sám z repozitáře (README, `package.json`, složky `tests/`, `e2e/`, stávající test soubory a konfigurace `playwright.config.*`).

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
   - **Offline chování / ztráta spojení v průběhu akce** (simulace přes `context.setOffline(true)`).
6. **Konkurence a opakované akce:**
   - Double-click na submit tlačítko (disabled stav při odesílání).
   - Paralelní editační okna (stejná entita editovaná na dvou místech současně ve více browser contextech).
   - Refresh stránky během ukládání.
   - Race conditions (akce A a B ve stejnou chvíli na stejném datech).
7. **Playwright Architektura a Best Practices:**
   - **Uživatelsky orientované lokátory:** Striktní zákaz křehkých XPathů a generovaných CSS tříd; audit využití `page.getByRole()`, `page.getByLabel()`, `page.getByPlaceholder()` a `data-testid`.
   - **Web-First Assertions & Zero-Flakiness:** Zákaz umělých pauz (`page.waitForTimeout()`, `time.sleep()`). Všechny asserty musí využívat auto-waiting (`await expect(locator).toBeVisible()`, `toHaveText()`, `toBeEnabled()`).
   - **Auth State Reuse (`storageState`):** Využití Playwright setup projektů (`auth.setup.ts`) pro uložení stavu přihlášení do JSON souborů, aby se eliminovalo opakované přihlašování přes UI v každém testu.
   - **Page Object Model (POM):** Logické rozdělení obrazovek a komponent do znovupoužitelných tříd s jasnými metodami.
   - **Responzivita a mobilní emulace:** Audit pokrytí mobilních viewportů (Mobile Chrome / Mobile Safari emulace v Playwrightu).
   - **Trace Viewer & CI Artefakty:** Správné nastavení pořizování stop (`trace: 'on-first-retry'` nebo `'retain-on-failure'`), screenshotů a videí pro rychlé ladění selhání.
8. **Testovací data a hygiena:**
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
- **Audit kvality stávajících testů:** flaky testy, `waitForTimeout` zpoždění, křehké selektory, testy s prázdnými/slabými asserty, mrtvé testy (skip/only/commented), testy závislé na pořadí či sdíleném stavu.

### 2. Kompletní matice chybějících testů (připraveno pro automatizaci)
U každého navrženého testu uveď:
- **Modul / Obrazovka**
- **Typ testu:** (Happy Path / Negativní test / Validace / Edge Case / Oprávnění / Síťový stav / Konkurence / Responzivita)
- **Priorita:** P0 (kritický flow, blokátor release) / P1 (vysoká) / P2 (střední) / P3 (nice-to-have)
- **Scénář:** název scénáře
- **Kroky & Očekávaný výsledek:**
  1. Výchozí stav (včetně použitého auth stavu z `storageState`)
  2. Provedená akce (kliknutí, vyplnění, síťový zásah)
  3. Ověření / Assert (Playwright web-first assert)
- **Riziko absence testu:** Co přesně hrozí, pokud tento test chybí a netestuje se ručně.

### 3. Návrh Playwright Architektury & Page Object Modelu (POM)
- **Struktura Page Objectů:** Navrhni strukturu tříd (např. `LoginPage`, `DashboardPage`, `SettingsPage`) a jejich metody.
- **Strategie autentizace:** Návrh setup projektu (`auth.setup.ts`) pro generování `storageState` pro jednotlivé role (Admin, Běžný uživatel, Host).
- **Custom Fixtures (`test.extend`):** Návrh vlastních fixtures pro automatický seed a úklid dat.
- **Konfigurace `playwright.config.ts`:** Doporučená konfigurace timeoutů, workerů pro paralelní běh, reportérů a nastavení Trace Vieweru.

### 4. Izolace a hygiena testovacích dat
- **Úklid po testech:** záruka, že každý test po sobě smaže svá data (teardown hook, API cleanup endpoint, reset DB).
- **Reset stavu:** jaký mechanismus resetuje stav účtů/zámků mezi testy, aby chyby z předchozích testů neblokovaly následné scénáře.

### 5. Definice hotova (DoD) pro E2E sadu
- Měřitelná kritéria, kdy je sada kompletní (např. 100 % P0/P1 scénářů pokryto, nula flaky pádů v 5 po sobě jdoucích bězích v CI, čas běhu pod X minut).

---
Po vygenerování tohoto reportu se zastav a počkej, až ti jednotlivé navržené bloky schválím.
