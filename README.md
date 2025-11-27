# Sudoku konzolos alkalmazás (Python / VS Code)

Ez a projekt egy **konzolos Sudoku játék és megoldó** Python nyelven, amely VS Code-ban futtatható.  
A program kezeli a feladványokat, képes azokat automatikusan megoldani, a felhasználóval interaktívan játszani, pontozni és menteni a játékállást.

## Fő funkciók

- Sudoku feladványok betöltése `puzzles.txt` fájlból
- Feladványok listázása és megtekintése
- Automatikus Sudoku-megoldás (backtracking algoritmus)
- Nehézség becslése (üres mezők száma alapján)
- Megoldás egyediségének ellenőrzése (van-e több megoldás)
- **Interaktív játék mód** (a felhasználó oldja meg a táblát)
  - pontozás (helyes / hibás lépések, tippek, befejezés)
  - időmérés
  - hibás mezők kiemelése
  - tipp kérés (egy helyes mező felfedése)
- Játék mentése és betöltése (`savegame.txt`)
- Új Sudoku feladvány generálása (könnyű / közepes / nehéz)
- Színes konzolos megjelenítés (fix, felhasználói és hibás mezők külön színnel)
