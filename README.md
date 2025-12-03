#  Sudoku – Python / Tkinter grafikus alkalmazás

Ez a projekt egy teljes funkcionalitású, Pythonban írt grafikus **Sudoku játék**, amely a Tkinter könyvtárra épül.  
A program képes új feladványokat generálni, megoldani, ellenőrizni, pontozni, menteni és később visszatölteni a játékot.  
A Sudoku motor hátterében egy **backtracking alapú matematikai modell** működik, amely garantálja a feladványok helyes és egyedi megoldását.

---

##  Fő funkciók

- 9×9-es Sudoku rács megjelenítése
- **Új Sudoku generálása** három nehézségi szinten (könnyű / közepes / nehéz)
- **Megoldó algoritmus** (backtracking – DFS)
- **Nehézség meghatározása** az üres mezők alapján
- **Időmérés és pontozás**
- Helyes/hélytelen mezők automatikus ellenőrzése
- **Tipp kérése** (–20 pont)
- **Teljes megoldás betöltése**
- **Játék mentése** és későbbi betöltése (`savegame.txt`)
- Saját feladvány szerkesztése és elmentése (`puzzles.txt`)
- **Világos és sötét téma**

---

##  A felhasznált modell

A Sudoku működésének alapját egy **visszalépéses keresést (backtracking)** alkalmazó algoritmus adja, amely:

1. Üres mezőt keres  
2. Soronként, oszloponként és 3×3-as négyzet szerint ellenőrzi a helyességet  
3. Ha egy szám nem jó, visszalép és másik számmal próbálkozik  

A projekt további modelljei:

- **Nehézségbecslő modell** – üres mezők számából határozza meg a szintet  
- **Egyediséget ellenőrző modell** – biztosítja, hogy csak egy megoldás létezzen  
- **Sudoku-generáló modell** – teljesen kitöltött táblát készít, majd szabályosan törli belőle a mezőket  
- **Pontozási modell** – helyes, hibás lépés, tippkérés és kész megoldás alapján számol  
- **Játékállapot modell** – minden mentés egyetlen fájlban tárolódik (`savegame.txt`)


