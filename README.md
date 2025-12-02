# Sudoku konzolos alkalmazás (Python / VS Code)

Ez a projekt egy grafikus Sudoku játék, amely Pythonban, Tkinterrel készült.  
A program képes új Sudoku táblákat generálni különböző nehézségi szinteken, ellenőrizni a megoldást, időt mérni, pontszámot számolni és menteni/betölteni a játékot.

## Funkciók

- 9×9-es Sudoku feladvány generálása
- Nehézségválasztás: könnyű, közepes, nehéz
- Nehézség becslése (üres mezők száma alapján)
- Időmérés és pontszám megjelenítése
- Tipp kérés (-pont)
- Automatikus Sudoku-megoldás (backtracking algoritmus)
- Hibák jelzése és helyes mezők kiemelése ellenőrzéskor
- Játék mentése és betöltése
- Világos és sötét téma váltható

## A projekt által használt modell
 
A Sudoku megoldásához a projekt egy **backtracking (visszalépéses keresés) alapú matematikai modellt** alkalmaz.  
Ez egy mélységi bejáráson (DFS) alapuló algoritmus, amely megpróbál egy számot elhelyezni egy üres mezőbe, ellenőrzi a szabályok betartását, és ha a lépés hibás, visszalép az előző pontra. A modell garantálja, hogy minden érvényes Sudoku feladvány megtalálható, vagy bizonyítható róla, hogy nincs megoldása.
 
A projekt további kiegészítő modelljei:
 
- **Nehézségbecslési modell:** az üres mezők száma alapján kategorizálja a feladványt (könnyű / közepes / nehéz).
- **Megoldás-unique modell:** limitált backtracking segítségével ellenőrzi, hogy a táblának egyedi megoldása van-e.
- **Sudoku-generáló modell:** teljes megoldott tábla véletlenszerű előállítása, majd számok eltávolítása úgy, hogy a megoldás egyedi maradjon.
- **Pontozási modell:** minden helyes lépés, hibás lépés, tippkérés és befejezés meghatározott pontértékkel jár.
- **Játékállapot modell:** a játék bármikor elmenthető és később visszatölthető a `savegame.txt` fájlból.
 
Ez a modellkészlet teljesen MicroPython-kompatibilis logikai felépítésben működik, és jól szemlélteti az algoritmikus gondolkodást.
 
