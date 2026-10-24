### ÚLOHA: Kompletní audit UX/UI konzistence a použitelnosti aplikace (READ-ONLY)

Tvým cílem je odhalit všechna místa, kde aplikace působí nedotaženě, zmatečně, neintuitivně nebo nekonzistentně — a navrhnout konkrétní UX/UI vylepšení.

Typ uživatele, cílová zařízení a hlavní flow aplikace si zjisti sám z repozitáře (README, hlavní obrazovky, routing, uživatelské role).

---

#### ⛔ STRIKTNÍ PRAVIDLA AUDITU:
1. **REŽIM POUZE PRO ČTENÍ (READ-ONLY):** Za žádných okolností nevytvářej, nemaž, needituj ani nespouštěj zápisové operace v repozitáři.
2. **ŽÁDNÉ REDESIGNY BEZ POTVRZENÍ:** Žádná změna HTML/CSS/JS nesmí být provedena bez mého výslovného souhlasu.
3. **KONKRÉTNOST:** Ne „vylepšit design", ale „na obrazovce X, prvek Y dělá Z, měl by dělat W".
4. **KONEC ÚLOHY:** Tvůj výstup končí předložením strukturovaného reportu a čekáním na instrukce.

---

#### ROZSAH ANALÝZY:
Projdi všechny obrazovky a flow aplikace z pohledu těchto oblastí:

1. **Navigace a informační architektura:**
   - Je jasné, kde se uživatel nachází a kam může jít? Konzistentní menu, breadcrumbs, URL odpovídající stavu, minimální počet kliků k cíli.
2. **Formuláře:**
   - Logické seskupení polí, jasné labely, rozumné defaulty, pořadí tabulace, validace v reálném čase (ne až na submit), konkrétní chybové hlášky, jasná zpětná vazba při úspěchu.
3. **Zpětná vazba (feedback):**
   - Každá akce má viditelnou reakci (spinner, success toast, disabled tlačítko při odesílání), absence ticha při dlouhé operaci, konfirmace u destruktivních akcí.
4. **Prázdné a chybové stavy:**
   - Co vidí uživatel, když nemá žádná data (empty states)? Co při chybě serveru? Co při loading?
5. **Vizuální konzistence:**
   - Barvy, typografie, velikosti a styly tlačítek, ikony, spacing — konzistentní napříč obrazovkami. Konzistentní naming akcí (Uložit vs. Potvrdit vs. OK) a umístění akčních tlačítek.
6. **Onboarding a pomoc:**
   - Je zjevné, co má uživatel dělat při prvním použití? Kontextové nápovědy/tooltipy na správných místech?
7. **Ošetření chyb:**
   - Chybové stránky (404, 500), offline stav, lidské zprávy (ne „Error 500 Internal Server Error"), možnost retry/návratu.
8. **Responzivita a zařízení:**
   - Mobil/tablet/desktop/kiosk: čitelnost textu, velikost dotykových cílů (min. 44×44 px), absence horizontálního scrollu (kromě tabulek), správný `meta viewport`.
9. **Jazyk a texty:**
   - Diakritika, konzistentní terminologie (ne „položka" zde a „záznam" tam), délka textů, formální vs. neformální oslovování.
10. **Subjektivní rychlost UI:**
    - Skeleton states místo spinnerů tam, kde to dává smysl. Optimistic UI tam, kde selhání je nepravděpodobné.

---

#### POŽADOVANÝ FORMÁT VÝSTUPU:

### 1. Rychlé shrnutí stavu
- Celkové hodnocení UX/UI (škála: **kritické použitelnostní problémy / významné tření / dobrý UX s drobnými chybami**).
- TOP 3–5 problémů, které nejvíce frustrují uživatele nebo brání dokončení klíčových flow.

### 2. Matice nálezů
U každého nálezu uveď:
- **ID:** UX-XX
- **Obrazovka / Flow:** konkrétní stránka nebo krok procesu
- **Kategorie:** (Navigace / Formulář / Feedback / Empty state / Konzistence / Jazyk / Responzivita / …)
- **Závažnost:** kritická (brání dokončení flow) / vysoká / střední / nízká / kosmetická
- **Popis + konkrétní prvek/oblast**
- **Navrhovaná oprava:** krátce, bez implementace

### 3. Rychlé výhry (quick wins)
- Nálezy, kde oprava < 15 minut a dopad výrazný.

### 4. Inventura empty/error stavů
- Tabulka všech obrazovek a jejich prázdných / chybových / loading stavů — co tam je dnes vs. co tam má být.

### 5. Doporučené dávky vylepšení
- Logické celky podle flow/obrazovek, každý samostatně schvalovatelný.

---
Po vygenerování reportu se zastav a počkej, až ti jednotlivé dávky schválím. Neimplementuj nic.
