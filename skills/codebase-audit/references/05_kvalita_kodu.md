### ÚLOHA: Kompletní audit kvality kódu aplikace (READ-ONLY)

Tvým cílem je posoudit dlouhodobou udržovatelnost, čitelnost a konzistenci kódu — a navrhnout, kde technologický dluh nejvíce brzdí budoucí vývoj.

Stack, konvence a existující lint/formátovací nástroje si zjisti sám z repozitáře (`package.json` scripts, `.eslintrc`, `.prettierrc`, tsconfig, husky, CI config).

---

#### ⛔ STRIKTNÍ PRAVIDLA AUDITU:
1. **REŽIM POUZE PRO ČTENÍ (READ-ONLY):** Za žádných okolností nevytvářej, nemaž, needituj ani nespouštěj zápisové operace v repozitáři.
2. **ŽÁDNÝ REFAKTORING BEZ POTVRZENÍ:** Žádná změna kódu, přejmenování ani přesun souboru nesmí být provedena bez mého výslovného souhlasu.
3. **HLEDEJ SYSTEMATICKÉ VZORCE:** Nejednotlivé chyby, ale opakující se problémy — copy-paste bloky, inkonzistence pojmenování, smíchané konvence vedle sebe.
4. **KONEC ÚLOHY:** Tvůj výstup končí předložením strukturovaného reportu a čekáním na instrukce.

---

#### ROZSAH ANALÝZY:
Projdi celý kód aplikace z pohledu těchto oblastí:

1. **Struktura a architektura:**
   - Logická skladba souborů a složek, dependency direction, coupling mezi moduly, circular dependencies, separace concerns (prezentace vs. business logika vs. data access).
2. **SOLID a principy:**
   - Single Responsibility (funkce/moduly s jednou odpovědností), tight coupling vs. dependency injection, god objects, funkce s příliš mnoha vedlejšími efekty.
3. **Konzistence kódu:**
   - Pojmenovací konvence (proměnné, funkce, soubory, konstanty), import/export styl, formátování, typové anotace (JSDoc / TypeScript) — konzistentní nebo smíchané?
4. **Duplikace:**
   - Copy-paste bloky, near-duplicates utility funkcí, konstanty roztroušené místo centralizovaných, podobné handlery na různých místech.
5. **Mrtvý a nepotřebný kód:**
   - Unused exports, nepoužívané funkce a utility, commented-out bloky, importy které se nevolají, deprecated API, mrtvé CSS třídy.
6. **Chybové ošetření a logování:**
   - Prázdné `catch` bloky, `try/catch` které polykají chyby bez zprávy, nekonzistentní error objekty, logování citlivých dat, absence kontextu v chybových hláškách.
7. **Komplexita funkcí:**
   - Funkce > 50 řádků, příliš mnoho parametrů (>4), hluboká vnoření podmínek (>3 úrovně), vysoká cyklomatická složitost.
8. **Komentáře a dokumentace:**
   - Chybějící kontext u netriviální logiky, nadbytečné komentáře („přičte 1 k i"), TODO/FIXME/HACK bez vlastníka a data.
9. **Type safety:**
   - `any`/dynamické typy tam, kde lze statické, chybějící validace vstupů u serializace/deserializace, implicitní `undefined`/`null` handling.
10. **Build a konfigurace:**
    - Konzistence env proměnných, build warnings, dependency hygiene (staré verze, nepoužívané balíčky, chybějící lock file).

---

#### POŽADOVANÝ FORMÁT VÝSTUPU:

### 1. Rychlé shrnutí stavu
- Celkové hodnocení (škála: **kritický technologický dluh / vyžaduje refaktoring / zdravý kód**).
- TOP 3–5 oblastí, kde kvalita kódu nejvíce brzdí vývoj nebo zvyšuje riziko chyb.

### 2. Matice nálezů
U každého nálezu uveď:
- **ID:** CODE-XX
- **Soubor / Oblast:** včetně `soubor:řádek` nebo popis rozsáhlejšího systémového problému
- **Kategorie:** (Duplikace / Komplexita / Coupling / Konvence / Mrtvý kód / Error handling / Dokumentace / Type safety / Build)
- **Závažnost:** kritický dluh / vysoký / střední / nízký
- **Popis + konkrétní příklad**
- **Navrhovaná oprava:** krátce, bez implementace

### 3. Rychlé opravy (quick wins)
- Nálezy, kde oprava < 15 minut, bez rizika regrese.

### 4. Doporučené dávky refaktoringu
- Logické celky, každý samostatně schvalovatelný. U každé dávky: riziko regrese, dopad na čitelnost.

### 5. Pravidla do budoucna (style guide draft)
- 5–10 konkrétních pravidel platných pro všechny nové změny (pojmenování, velikost funkcí, zakázané vzorce, …).

---
Po vygenerování reportu se zastav a počkej, až ti jednotlivé dávky schválím. Neimplementuj nic.
