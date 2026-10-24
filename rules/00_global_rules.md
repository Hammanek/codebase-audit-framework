# Globální pravidla agenta (Global Rules)

## 1. Povinné testování při každé změně kódu a nové funkci
- **Při jakékoliv úpravě kódu, refaktoringu nebo implementaci nové funkce** je agent povinen:
  1. **Přidat nebo aktualizovat testy** (backendové unit/integrační testy i frontendové E2E / integrační testy).
  2. **Testy spustit a fyzicky ověřit jejich 100% průchod** před dokončením úkolu a předáním odpovědi uživateli.
  3. Žádná funkce nesmí být považována za dokončenou bez reálného ověření funkčnosti (Evidence before assertions).

## 2. Režim pouze pro čtení při auditech (READ-ONLY)
- Při provádění jakéhokoliv auditu či revize kódu je agent v striktním **READ-ONLY** režimu:
  1. Nesmí vytvářet, modifikovat ani mazat soubory v projektu.
  2. Každé zjištění musí být podloženo přesným odkazem `soubor:řádek` a popisem reálného scénáře selhání.
  3. Výstupem auditu je strukturovaný report a návrh prioritizovaných dávek oprav — implementace začíná až po výslovném schválení uživatelem.
