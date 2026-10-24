### ÚLOHA: Kompletní audit přístupnosti aplikace (READ-ONLY)

Tvým cílem je odhalit všechny překážky přístupnosti pro uživatele se zrakovým, motorickým, sluchovým či kognitivním postižením, a zajistit, aby aplikace byla plně použitelná bez myši, na dotykovém zařízení i se screen readerem. Cílový standard: **WCAG 2.2 úroveň AA**.

Typ aplikace, cílová zařízení i existující přístupnostní prvky si zjisti sám z repozitáře (HTML šablony, CSS, `meta viewport`, existující ARIA atributy).

---

#### ⛔ STRIKTNÍ PRAVIDLA AUDITU:
1. **REŽIM POUZE PRO ČTENÍ (READ-ONLY):** Za žádných okolností nevytvářej, nemaž, needituj ani nespouštěj zápisové operace v repozitáři.
2. **ŽÁDNÉ OPRAVY BEZ POTVRZENÍ:** Žádná změna HTML/CSS/JS nesmí být aplikována bez mého výslovného souhlasu.
3. **OVĚŘENÍ V KÓDU:** Každý nález dolož konkrétním HTML/CSS prvkem (tag, třída, atribut). U barevného kontrastu uveď konkrétní hodnoty (např. `#6b7280` na `#ffffff` = 4.8:1).
4. **KONEC ÚLOHY:** Tvůj výstup končí předložením strukturovaného reportu a čekáním na instrukce.

---

#### ROZSAH ANALÝZY:
Projdi všechny obrazovky, modály, formuláře, notifikace, grafy a tabulky z pohledu těchto oblastí:

1. **Sémantické HTML:**
   - Správné tagy (`button` místo `div onclick`, `nav`, `main`, `header`, `footer`), hierarchie `h1`–`h6`, landmarky, `label` u všech formulářových polí, `fieldset/legend` u skupin.
2. **Klávesnicová navigace:**
   - Každá interaktivní funkce dosažitelná tabulátorem, logické pořadí, skip-to-content link, viditelný focus indikátor (žádné `outline: none` bez náhrady), Escape z modálů, focus management po otevření/zavření dialogu.
3. **Screen reader:**
   - Smysluplné `alt` texty u obrázků, `aria-label`/`aria-labelledby` u ikonových tlačítek, `aria-live` u dynamických změn (toasty, loading), `aria-expanded`/`aria-controls`, stavové atributy (`aria-invalid`, `aria-required`, `aria-disabled`).
4. **Barva a kontrast:**
   - Text/pozadí min. 4.5:1 (malý text) / 3:1 (velký text), interaktivní prvky min. 3:1, informace nepřenášené pouze barvou (ikona + text), oba režimy (light/dark) kontrastní.
5. **Dotykové cíle a rozložení:**
   - Min. 44×44 CSS px, dostatečné mezery mezi cíli, žádné neúmyslné dotyky.
6. **Formuláře a chybové stavy:**
   - Inline validace srozumitelná i screen readeru, chybové hlášky spojené s polem (`aria-describedby`), konkrétní texty (ne „Chyba"), potvrzení úspěchu oznámeno.
7. **Média a dynamický obsah:**
   - Video/audio: titulky, transkript, ovládání klávesnicí. Animace: respektování `prefers-reduced-motion`.
8. **Zoom a layout:**
   - Použitelnost při 200% zoomu, žádné horizontální scrollování (kromě tabulek), správný `meta viewport`.

---

#### POŽADOVANÝ FORMÁT VÝSTUPU:

### 1. Rychlé shrnutí stavu
- Celkové hodnocení přístupnosti (škála: **kritické bariéry / významné překážky / dobrá přístupnost s drobnými chybami**).
- TOP 3–5 překážek, které brání největší skupině uživatelů aplikaci vůbec používat.

### 2. Matice nálezů
U každého nálezu uveď:
- **ID:** A11Y-XX
- **Obrazovka / Soubor:** včetně `soubor:řádek` nebo odkazu na konkrétní prvek
- **WCAG kritérium:** (např. 1.1.1, 2.1.1, 4.1.2)
- **Úroveň:** A / AA / AAA
- **Závažnost:** kritická (nelze použít) / vysoká / střední / nízká
- **Popis + konkrétní prvek**
- **Navrhovaná oprava:** krátce, bez implementace

### 3. Rychlé opravy (quick wins)
- Nálezy, kde oprava < 15 minut a dopad výrazný.

### 4. Doporučené dávky oprav
- Logické celky podle modulů/obrazovek.

### 5. Testovací postup po opravě
- Čím a jak ověřit opravy (axe DevTools, Lighthouse, NVDA/VoiceOver, ruční klávesnicová navigace).

---
Po vygenerování reportu se zastav a počkej, až ti jednotlivé dávky schválím. Neimplementuj nic.
