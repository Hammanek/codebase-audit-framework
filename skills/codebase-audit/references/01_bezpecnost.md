### ÚLOHA: Kompletní bezpečnostní audit aplikace (READ-ONLY)

Tvým cílem je provést kompletní bezpečnostní audit aplikace a předložit strukturovaný report nálezů seřazených podle závažnosti. Aplikace musí po opravách odolávat reálným útokům, ne představám o nich.

Stack, architekturu i klíčové moduly aplikace si zjisti sám z repozitáře (README, `package.json`, entry pointy serveru, API routy, auth middleware).

---

#### ⛔ STRIKTNÍ PRAVIDLA AUDITU:
1. **REŽIM POUZE PRO ČTENÍ (READ-ONLY):** Za žádných okolností nevytvářej, nemaž, needituj ani nespouštěj zápisové operace v repozitáři.
2. **ŽÁDNÉ OPRAVY BEZ POTVRZENÍ:** Žádná bezpečnostní oprava nesmí být implementována bez předchozího předložení reportu a mého výslovného souhlasu.
3. **DŮKAZY, NE DOMNĚNKY:** Každý nález dolož odkazem `soubor:řádek` a popisem reálného exploit scénáře.
4. **ZÁKAZ LOGOVÁNÍ CITLIVÉHO:** Pokud v kódu najdeš skutečné tajemství, v reportu ho NEuváděj celé — pouze popiš, kde je a jakého typu.
5. **KONEC ÚLOHY:** Tvůj výstup končí předložením strukturovaného reportu a čekáním na instrukce.

---

#### ROZSAH ANALÝZY:
Projdi kompletně celý kód aplikace (backend, frontend, konfigurace, build skripty, závislosti, docker/batch soubory) z pohledu těchto oblastí:

1. **Autentizace a správa session:**
   - Uložení hesel (hash algoritmus, sůl, work factor), práce s tokeny/sessions (expirace, rotace, invalidace), cookie flags (HttpOnly, Secure, SameSite), JWT validace, ochrana před bruteforce, reset hesla.
2. **Autorizace a RBAC:**
   - Server-side kontrola oprávnění na každém endpointu (ne jen skrytí v UI), IDOR / přímý přístup k cizím objektům přes ID v URL, horizontální i vertikální eskalace práv, admin funkce.
3. **Validace vstupů:**
   - SQL injection (parametrizované dotazy vs. string concat), command injection, path traversal (upload/download), mass assignment, velikost a typ vstupu, header injection.
4. **Escaping a UI bezpečnost (anti-XSS):**
   - Každé místo, kde jde user data → `innerHTML` / `document.write` / `eval` / inline event handlery, centrální escape utilita a její konzistentní použití, `textContent` vs `innerHTML` sinks, CSP hlavičky.
5. **CSRF a API bezpečnost:**
   - CSRF tokeny u state-changing operací, CORS konfigurace, podpisy webhooků.
6. **Rate limiting a DoS ochrana:**
   - Limity na login, drahé operace (export, reset), lockout policy, max velikost payloadu, timeouty.
7. **Informační úniky:**
   - Stacktraces v produkčních odpovědích, přístupné `*.bak`, `.env`, `node_modules`, debug endpointy, verbose logy, komentáře s hesly/IP.
8. **Soubory, statické serving a storage:**
   - Blacklist vs. whitelist přístupů k souborům, upload souboru (typ, velikost, storage mimo webroot), `path.join` traversal.
9. **Kryptografie:**
   - TLS, slabé algoritmy (MD5, SHA1, DES), domácí krypto místo osvědčených knihoven, zdroj entropie.
10. **Závislosti a supply chain:**
    - Vulnerable packages, nepoužívané balíčky, existence lock file, pinned verze.
11. **Bezpečnostní hlavičky a PWA specifika:**
    - CSP, HSTS, X-Frame-Options, Referrer-Policy, Service Worker cache strategy (cachování citlivých API dat), storage citlivých dat v `localStorage`.
12. **Business logika a zneužití:**
    - Race conditions při zápisu, záporné hodnoty, bypass validace v klonování objektu, TOCTOU.

---

#### POŽADOVANÝ FORMÁT VÝSTUPU:

### 1. Rychlé shrnutí stavu
- Celkové hodnocení bezpečnosti (škála: **kritická rizika / vážné nedostatky / dobrý stav s drobnými riziky**).
- TOP 3–5 rizik, která při zneužití způsobí reálnou škodu.

### 2. Matice nálezů
U každého nálezu uveď:
- **ID:** SEC-XX
- **Modul / Soubor:** včetně `soubor:řádek`
- **Závažnost:** kritická / vysoká / střední / nízká / informační
- **Kategorie:** (IDOR, XSS, Injekce, Konfigurace, Citlivé údaje, CSRF, Auth, …)
- **Popis + ověření v kódu**
- **Exploit scénář:** jak by útočník postupoval krok za krokem
- **Dopad:** co přesně získá
- **Navrhovaná náprava:** krátce, bez implementace

### 3. Rychlé opravy (low-hanging fruit)
- Nálezy, kde oprava < 15 minut práce, dopad výrazný.

### 4. Doporučené dávky oprav
- Rozdělení nálezů do logických celků s odhadovým rizikem regrese (nízké/střední/vysoké).

### 5. Pozitivní posudek
- Co je uděláno dobře a stojí za to zachovat.

---
Po vygenerování reportu se zastav a počkej, až ti jednotlivé nálezy schválím. Neimplementuj nic.
