### ÚLOHA: Kompletní audit výkonu a optimalizace aplikace (READ-ONLY)

Tvým cílem je odhalit všechna místa, kde aplikace plytvá výkonem, přenáší zbytečná data nebo se zpomaluje s rostoucími daty — a navrhnout konkrétní, ověřitelné optimalizace.

Stack, cílová zařízení a typickou zátěž aplikace si zjisti sám z repozitáře (README, DB schéma, build config, lighthouse reporty, pokud existují).

---

#### ⛔ STRIKTNÍ PRAVIDLA AUDITU:
1. **REŽIM POUZE PRO ČTENÍ (READ-ONLY):** Za žádných okolností nevytvářej, nemaž, needituj ani nespouštěj zápisové operace v repozitáři.
2. **ŽÁDNÁ OPTIMALIZACE BEZ POTVRZENÍ:** Žádná změna kódu, indexu, query rewrite ani build config nesmí být aplikována bez mého výslovného souhlasu.
3. **MĚŘENÍ PŘED DOMNĚNKAMI:** Problém dolož konkrétním zdůvodněním (počet dotazů, velikost dat, absence indexu, velikost souborů). Nestřílej od boku.
4. **KONEC ÚLOHY:** Tvůj výstup končí předložením strukturovaného reportu a čekáním na instrukce.

---

#### ROZSAH ANALÝZY:
Projdi celý kód aplikace z pohledu těchto oblastí:

1. **Backend výkon:**
   - N+1 dotazy, chybějící indexy na často dotazovaných sloupcích, `SELECT *`, synchronní I/O v hot paths, absence cache, zbytečné dotazy v cyklech.
2. **Databáze:**
   - Schéma (typy sloupců, nadbytečné NULL), indexy (chybějící, nepoužívané, duplicitní), transakce (příliš velké, zbytečné zamykání), paginace (`LIMIT`/`OFFSET` vs. keyset).
3. **API:**
   - Velikost payloadů (over/under-fetching), absence gzip/brotli komprese, chybějící HTTP cache hlavičky, serializace velkých struktur.
4. **Frontend bundle a loading:**
   - Velikost JS/CSS, nepotřebné knihovny, absence code-splitting/lazy loading, synchronní skripty blokující render, nadbytečné webfonty, unminifikované soubory v produkci.
5. **Rendering a UI výkon:**
   - Velké DOM stromy, layout thrashing, chybějící debounce/throttle na eventech, zbytečné re-rendery, memory leaky (nesmíšené listenery, intervaly, closures).
6. **Statické prostředky:**
   - Velikost obrázků (ne WebP/AVIF, absence `loading="lazy"`), velikost fontů, `Cache-Control` hlavičky, cache-busting strategie po release.
7. **Service Worker / PWA:**
   - Co se cachuje, cachování citlivých API odpovědí, strategie update, velikost cache, fallbacky.
8. **Škálování s daty:**
   - Jak se aplikace chová při 10×/100× větším objemu dat — dotazy rostoucí lineárně/exponenciálně.

---

#### POŽADOVANÝ FORMÁT VÝSTUPU:

### 1. Rychlé shrnutí stavu
- Celkové hodnocení výkonu (škála: **kritické problémy / významné rezervy / dobře optimalizováno**).
- TOP 3–5 výkonových problémů, které uživatel reálně pozná.

### 2. Matice nálezů
U každého nálezu uveď:
- **ID:** PERF-XX
- **Modul / Soubor:** včetně `soubor:řádek`
- **Vážnost:** kritická / vysoká / střední / nízká
- **Popis + konkrétní zdůvodnění problému**
- **Dopad:** měřitelný dopad (např. „+2 s načtení", „+500 KB bundle", „100 SQL dotazů místo 1")
- **Navrhovaná oprava:** krátce, bez implementace

### 3. Rychlé výhry (quick wins)
- Nálezy, kde oprava < 30 minut a dopad výrazný.

### 4. Doporučené dávky optimalizací
- Logické celky s odhadovaným rizikem regrese.

### 5. Metriky k měření po opravě
- Jak budeme po opravě měřit úspěch (metriky, nástroje, cílové hodnoty).

---
Po vygenerování reportu se zastav a počkej, až ti jednotlivé dávky schválím. Neimplementuj nic.
