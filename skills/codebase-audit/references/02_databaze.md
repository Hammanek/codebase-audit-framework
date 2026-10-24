### ÚLOHA: Kompletní audit databáze a datové vrstvy aplikace (READ-ONLY)

Tvým cílem je prověřit databázovou a datovou vrstvu — schéma, dotazy, transakce, migrace, zálohování, integritu dat, NoSQL úložiště, cache a fronty zpráv — a odhalit vše, co ohrožuje dostupnost, konzistenci nebo výkon dat.

DB engine (PostgreSQL, MySQL, SQLite, MongoDB, Redis atd.), ORM/query builder, migrační strategii i worker infrastrukturu si zjisti sám z repozitáře (DB moduly, migrační skripty, seed skripty, DB access layer, queue handlery).

---

#### ⛔ STRIKTNÍ PRAVIDLA AUDITU:
1. **REŽIM POUZE PRO ČTENÍ (READ-ONLY):** Za žádných okolností nevytvářej, nemaž, needituj ani nespouštěj zápisové operace do databáze ani repozitáře. Ani „jen ověřovací" INSERT/UPDATE/DELETE.
2. **ŽÁDNÉ MIGRACE / INDEXY BEZ POTVRZENÍ:** Žádná změna schématu ani přidání indexu nesmí být provedena bez mého výslovného souhlasu.
3. **PRODUKČNÍ DATA:** Pokud audit přistupuje k reálným datům, nesmí být kopírována, exportována ani logována.
4. **KONEC ÚLOHY:** Tvůj výstup končí předložením strukturovaného reportu a čekáním na instrukce.

---

#### ROZSAH ANALÝZY:
Projdi databázové schéma, všechny dotazy v kódu, DB konfiguraci, migrační skripty, seed skripty, caching a logiku zpráv z pohledu těchto oblastí:

1. **Schéma a modelování (SQL):**
   - Správné datové typy, NULL/NOT NULL, DEFAULT hodnoty, unique constraints, absence nebo nadbytek PK/FK.
2. **Integrita dat:**
   - Foreign keys (existují a jsou vynuceny?), ON DELETE/UPDATE akce, check constraints, triggery.
3. **Dotazy:**
   - N+1 dotazy, chybějící `WHERE` v `UPDATE`/`DELETE` (ovlivní celou tabulku), `SELECT *`, absence indexů na JOIN/WHERE sloupcích, `LIKE '%…%'` (full table scan), korelované subdotazy.
4. **Transakce a concurrency:**
   - Multi-step zápisy bez transakcí, race conditions (read → modify → write bez zámku), dlouhotrvající transakce (connection/lock exhaustion), riziko deadlocků, atomické operace.
5. **Migrace:**
   - Konzistentní migrační historie (sériové číslování, žádné skoky), migrace idempotentní (bezpečné spustit dvakrát?), zpětná kompatibilita, validační krok po migraci.
6. **Zálohování a obnova:**
   - Je zálohování implementováno a automatizováno? Bylo testováno skutečné obnovení? Validace záloh (korupce)? Kde jsou zálohy uloženy (stejný disk = žádná záloha)?
7. **Výkon a škálování:**
   - Chybějící/nepoužívané/duplicitní indexy, paginace (offset vs. cursor-based), tabulky rostoucí bez archivace, query plány (EXPLAIN u kritických dotazů).
8. **Bezpečnost dat:**
   - Citlivé sloupce (hesla, tokeny) — hashování/správné uložení? PII — přístup omezený? Úniky v logách nebo error odpovědích?
9. **Seed a testovací data:**
   - Seed data konzistentní s produkčními daty, testy používají izolované DB, žádná test data neproniknou do produkce.
10. **NoSQL a Document Stores (MongoDB, DynamoDB, Firestore):**
    - Absence schématové validace na úrovni DB/aplikace, nebezpečné JSON dotazy (NoSQL Injection přes objekty `$gt`, `$ne`, `$where`), neindexované dotazy v polích a subdokumentech, riziko překročení limitu velikosti dokumentu (např. 16 MB u MongoDB).
11. **Caching vrstva (Redis, Memcached):**
    - Chybějící TTL (hrozba nekonečného růstu paměti a OOM pádu), Cache Invalidation strategie (jak se aktualizuje cache při změně v DB?), Cache Stampede (dog-piling efekt při expiraci klíče pod vysokou zátěží), nebezpečná deserializace (např. ukládání surového Python `pickle` objektu do Redisu).
12. **Fronty zpráv a Background Workery (RabbitMQ, Kafka, Celery, BullMQ):**
    - Zajištění idempotence konzumenta (co nastane, když je stejná zpráva doručena opakovaně?), Poison Pill zprávy (zpráva shazující worker, která se nekonečně vrací do fronty), nastavení Dead Letter Queue (DLQ), správné ošetření výpadku spojení a backpressure.

---

#### POŽADOVANÝ FORMÁT VÝSTUPU:

### 1. Rychlé shrnutí stavu
- Celkové hodnocení databázové vrstvy (škála: **kritická rizika ztráty dat / vážné nedostatky / zdravá DB vrstva**).
- TOP 3–5 rizik (např. „žádné zálohy", „transakce bez atomicity", „chybějící TTL u cache", „nekonečná smyčka ve frontě zpráv").

### 2. Matice nálezů
U každého nálezu uveď:
- **ID:** DB-XX
- **Soubor / Oblast:** `soubor:řádek` nebo název DB objektu (tabulka, index, dotaz, queue)
- **Kategorie:** (Schéma / Integrita / Dotazy / Transakce / Migrace / Zálohy / Výkon / Bezpečnost / NoSQL / Cache / Fronty)
- **Závažnost:** kritická (hrozí ztráta/korupce dat) / vysoká / střední / nízká
- **Popis + konkrétní ukázka (dotaz, část schématu, kód)**
- **Dopad:** co přesně hrozí
- **Navrhovaná oprava:** krátce, bez implementace

### 3. Rychlé opravy (quick wins)
- Nálezy, kde oprava < 15 minut a dopad výrazný.

### 4. Doporučené dávky oprav
- Logické celky, každý samostatně schvalovatelný. U každé dávky: riziko regrese a riziko ztráty dat.

### 5. Provozní checklist
- Co monitorovat (velikost DB, paměť Redisu, velikost front zpráv, pomalé dotazy, pády workerů), jak často zálohovat, jak ověřit integritu po incidentu.

---
Po vygenerování reportu se zastav a počkej, až ti jednotlivé dávky schválím. Neimplementuj nic.
