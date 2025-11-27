import time
import random

PUZZLE_FAJL = "puzzles.txt"
SAVEGAME_FAJL = "savegame.txt"

SZIN_RESET = "\033[0m"
SZIN_KEK = "\033[94m"
SZIN_ZOLD = "\033[92m"
SZIN_PIROS = "\033[91m"
SZIN_SARGA = "\033[93m"
SZIN_HALVANY = "\033[2m"

def üres_mező_keresése(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None


def szám_elhelyezhető(board, row, col, num):
    for c in range(9):
        if board[row][c] == num:
            return False
    for r in range(9):
        if board[r][col] == num:
            return False
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False
    return True


def sudoku_megoldása(board):
    üres = üres_mező_keresése(board)
    if üres is None:
        return True
    row, col = üres
    for num in range(1, 10):
        if szám_elhelyezhető(board, row, col, num):
            board[row][col] = num
            if sudoku_megoldása(board):
                return True
            board[row][col] = 0
    return False


def tábla_megjelenítése(board):
    print("+-------+-------+-------+")
    for r in range(9):
        sor_elemek = []
        for c in range(9):
            érték = board[r][c]
            if érték == 0:
                sor_elemek.append(".")
            else:
                sor_elemek.append(str(érték))
        print("| {} {} {} | {} {} {} | {} {} {} |".format(
            sor_elemek[0], sor_elemek[1], sor_elemek[2],
            sor_elemek[3], sor_elemek[4], sor_elemek[5],
            sor_elemek[6], sor_elemek[7], sor_elemek[8]
        ))
        if (r + 1) % 3 == 0:
            print("+-------+-------+-------+")


def tábla_megjelenítése_színes(board, eredeti=None, hibák=None):
    """Színes tábla: eredeti számok kékkel, felhasználói zölddel, hibák pirossal."""
    if eredeti is None:
        eredeti = [[0] * 9 for _ in range(9)]
    if hibák is None:
        hibák = set()

    print("+-------+-------+-------+")
    for r in range(9):
        sor_str = "| "
        for c in range(9):
            érték = board[r][c]
            szoveg = "."
            szin = SZIN_RESET
            if (r, c) in hibák and érték != 0:
                szin = SZIN_PIROS
                szoveg = str(érték)
            elif érték != 0:
                szoveg = str(érték)
                if eredeti[r][c] != 0:
                    szin = SZIN_KEK  
                else:
                    szin = SZIN_ZOLD 
            else:
                szin = SZIN_HALVANY

            sor_str += f"{szin}{szoveg}{SZIN_RESET} "
            if (c + 1) % 3 == 0:
                sor_str += "| "

        print(sor_str)
        if (r + 1) % 3 == 0:
            print("+-------+-------+-------+")


def tábla_másolása(board):
    return [sor[:] for sor in board]


def üres_mezők_száma(board):
    db = 0
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                db += 1
    return db


def nehézség_meghatározása(board):
    ures = üres_mezők_száma(board)
    if ures <= 30:
        kategória = "könnyű"
    elif ures <= 50:
        kategória = "közepes"
    else:
        kategória = "nehéz"
    return ures, kategória


def tábla_érvényes(board):
    for r in range(9):
        for c in range(9):
            érték = board[r][c]
            if érték != 0:
                board[r][c] = 0
                if not szám_elhelyezhető(board, r, c, érték):
                    board[r][c] = érték
                    return False
                board[r][c] = érték
    return True


def megoldások_száma(board, limit=2):
    számláló = [0]

    def backtrack():
        if számláló[0] >= limit:
            return
        üres = üres_mező_keresése(board)
        if üres is None:
            számláló[0] += 1
            return
        row, col = üres
        for num in range(1, 10):
            if szám_elhelyezhető(board, row, col, num):
                board[row][col] = num
                backtrack()
                board[row][col] = 0

    backtrack()
    return számláló[0]

def feladványok_betöltése(fájlnév):
    táblák = []
    aktuális = []
    try:
        f = open(fájlnév, "r")
    except OSError:
        print("Nem tudom megnyitni a fájlt:", fájlnév)
        return []

    for sor in f:
        sor = sor.strip()
        if not sor or sor.startswith("#"):
            continue
        if len(sor) != 9:
            print("Hibás sor a fájlban (nem 9 karakter):", sor)
            continue
        sor_lista = []
        for ch in sor:
            if ch.isdigit():
                sor_lista.append(int(ch))
            else:
                sor_lista.append(0)
        aktuális.append(sor_lista)
        if len(aktuális) == 9:
            táblák.append(aktuális)
            aktuális = []
    f.close()
    return táblák


def új_feladvány_hozzáadása(táblák):
    print("\n--- Új Sudoku feladvány felvétele ---")
    print("Add meg a 9 sort, soronként 9 karakterrel (0-9 vagy '.'),")
    print("ahol a '0' vagy '.' jelenti az üres mezőt.\n")

    új_tábla = []
    for i in range(9):
        while True:
            sor = input(f"{i + 1}. sor: ").strip()
            if len(sor) != 9 or any(ch not in "0123456789." for ch in sor):
                print("Hibás sor. Pontosan 9 karakter kell (0-9 vagy '.'). Próbáld újra.")
            else:
                break
        sor_lista = []
        for ch in sor:
            if ch in "0.":
                sor_lista.append(0)
            else:
                sor_lista.append(int(ch))
        új_tábla.append(sor_lista)

    táblák.append(új_tábla)

    try:
        f = open(PUZZLE_FAJL, "a")
        f.write("\n# Új feladvány felvéve a programból\n")
        for sor_lista in új_tábla:
            f.write("".join(str(n) for n in sor_lista) + "\n")
        f.close()
        print("Feladvány sikeresen elmentve a puzzles.txt fájlba.")
    except OSError:
        print("Figyelem: a feladványt nem sikerült fájlba menteni.")

    print("Új feladvány hozzáadva.")

def játék_mentése(eredeti, aktuális, puzzle_index, elapsed, score):
    try:
        with open(SAVEGAME_FAJL, "w") as f:
            f.write(str(puzzle_index) + "\n")
            f.write(str(elapsed) + "\n")
            f.write(str(score) + "\n")
            eredeti_str = "".join(str(eredeti[r][c]) for r in range(9) for c in range(9))
            aktuális_str = "".join(str(aktuális[r][c]) for r in range(9) for c in range(9))
            f.write(eredeti_str + "\n")
            f.write(aktuális_str + "\n")
        print("Játék elmentve a savegame.txt fájlba.")
    except OSError:
        print("Hiba: a mentést nem sikerült elvégezni.")


def játék_betöltése():
    try:
        with open(SAVEGAME_FAJL, "r") as f:
            sorok = [s.strip() for s in f.readlines()]
    except OSError:
        print("Nincs mentett játék (savegame.txt).")
        return None

    if len(sorok) < 5:
        print("Hibás mentés fájl.")
        return None

    try:
        puzzle_index = int(sorok[0])
        elapsed = float(sorok[1])
        score = int(sorok[2])
        eredeti_str = sorok[3]
        aktuális_str = sorok[4]
        if len(eredeti_str) != 81 or len(aktuális_str) != 81:
            print("Hibás tábla a mentésben.")
            return None
        eredeti = []
        aktuális = []
        for i in range(9):
            sor_e = []
            sor_a = []
            for j in range(9):
                idx = i * 9 + j
                sor_e.append(int(eredeti_str[idx]))
                sor_a.append(int(aktuális_str[idx]))
            eredeti.append(sor_e)
            aktuális.append(sor_a)
    except ValueError:
        print("Hibás adatok a mentésben.")
        return None

    return {
        "puzzle_index": puzzle_index,
        "elapsed": elapsed,
        "score": score,
        "eredeti": eredeti,
        "aktuális": aktuális,
    }

def generál_kitöltött_táblát():
    board = [[0] * 9 for _ in range(9)]

    def backtrack_fill():
        üres = üres_mező_keresése(board)
        if üres is None:
            return True
        r, c = üres
        számok = list(range(1, 10))
        random.shuffle(számok)
        for num in számok:
            if szám_elhelyezhető(board, r, c, num):
                board[r][c] = num
                if backtrack_fill():
                    return True
                board[r][c] = 0
        return False

    backtrack_fill()
    return board


def készít_feladvány_megoldásból(megoldott, fokozat):
    if fokozat == "könnyű":
        cél_üres = 40
    elif fokozat == "közepes":
        cél_üres = 50
    else:
        cél_üres = 60

    puzzle = tábla_másolása(megoldott)
    pozíciók = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(pozíciók)

    eltávolítva = 0
    for r, c in pozíciók:
        if eltávolítva >= cél_üres:
            break
        temp = puzzle[r][c]
        if temp == 0:
            continue
        puzzle[r][c] = 0
        másolat = tábla_másolása(puzzle)
        db = megoldások_száma(másolat, limit=2)
        if db == 1:
            eltávolítva += 1
        else:
            puzzle[r][c] = temp

    return puzzle


def új_sudoku_generálása():
    print("\n--- Új Sudoku generálása ---")
    print("Választható nehézség:")
    print("1 - könnyű")
    print("2 - közepes")
    print("3 - nehéz")
    v = input("Választás: ").strip()
    if v == "1":
        fok = "könnyű"
    elif v == "2":
        fok = "közepes"
    elif v == "3":
        fok = "nehéz"
    else:
        print("Ismeretlen választás.")
        return

    print("Teljes tábla generálása...")
    megoldott = generál_kitöltött_táblát()
    print("Feladvány készítése...")
    puzzle = készít_feladvány_megoldásból(megoldott, fok)
    print(f"Új {fok} Sudoku feladvány generálva. Indulhat a játék!")
    interaktív_játék(puzzle)

def feladvány_listázása(táblák):
    print("\n--- Elérhető feladványok ---")
    if not táblák:
        print("Nincs egyetlen feladvány sem betöltve.")
        return
    for index in range(len(táblák)):
        print(f"{index + 1}. feladvány")
    print("-----------------------------")


def feladvány_megtekintése(táblák):
    if not táblák:
        print("Nincs betöltött feladvány.")
        return
    try:
        s = input("Melyik feladványt szeretnéd látni? (sorszám): ")
        idx = int(s) - 1
    except ValueError:
        print("Hibás sorszám.")
        return
    if idx < 0 or idx >= len(táblák):
        print("Nincs ilyen sorszámú feladvány.")
        return
    print(f"\n--- {idx + 1}. feladvány ---")
    tábla_megjelenítése(táblák[idx])


def feladvány_megoldása(táblák):
    if not táblák:
        print("Nincs betöltött feladvány.")
        return
    try:
        s = input("Melyik feladványt szeretnéd megoldani? (sorszám): ")
        idx = int(s) - 1
    except ValueError:
        print("Hibás sorszám.")
        return
    if idx < 0 or idx >= len(táblák):
        print("Nincs ilyen sorszámú feladvány.")
        return

    tábla = tábla_másolása(táblák[idx])
    print(f"\n--- {idx + 1}. feladvány (eredeti) ---")
    tábla_megjelenítése(tábla)
    print("\nMegoldás folyamatban...\n")
    kezdet = time.time()
    siker = sudoku_megoldása(tábla)
    idő = time.time() - kezdet
    if siker:
        print("--- MEGOLDOTT TÁBLA ---")
        tábla_megjelenítése(tábla)
        print(f"\nA megoldás ideje: {idő:.3f} másodperc.")
    else:
        print("Ennek a feladványnak nincs megoldása.")


def feladvány_nehézségének_becslése(táblák):
    if not táblák:
        print("Nincs betöltött feladvány.")
        return
    try:
        s = input("Melyik feladvány nehézségét szeretnéd? (sorszám): ")
        idx = int(s) - 1
    except ValueError:
        print("Hibás sorszám.")
        return
    if idx < 0 or idx >= len(táblák):
        print("Nincs ilyen sorszámú feladvány.")
        return
    ures, kategória = nehézség_meghatározása(táblák[idx])
    print(f"\nA {idx + 1}. feladvány becsült nehézsége: {kategória} (üres mezők száma: {ures})")


def feladvány_egyediségének_ellenőrzése(táblák):
    if not táblák:
        print("Nincs betöltött feladvány.")
        return
    try:
        s = input("Melyik feladvány egyediségét ellenőrizzük? (sorszám): ")
        idx = int(s) - 1
    except ValueError:
        print("Hibás sorszám.")
        return
    if idx < 0 or idx >= len(táblák):
        print("Nincs ilyen sorszámú feladvány.")
        return
    tábla = tábla_másolása(táblák[idx])
    print("\nMegoldások számának vizsgálata (max. 2-ig számolunk)...")
    kezdet = time.time()
    db = megoldások_száma(tábla, limit=2)
    idő = time.time() - kezdet
    if db == 0:
        print("Ennek a feladványnak NINCS megoldása.")
    elif db == 1:
        print("Ennek a feladványnak PONTOSAN EGY megoldása van (egyedi).")
    else:
        print("Ennek a feladványnak TÖBB megoldása is van.")
    print(f"Vizsgálat ideje: {idő:.3f} másodperc.")

def interaktív_játék(eredeti, aktuális=None, elapsed_before=0.0, score_before=0, puzzle_index=-1):
    aktuális = tábla_másolása(aktuális) if aktuális is not None else tábla_másolása(eredeti)

    megoldás = tábla_másolása(eredeti)
    if not sudoku_megoldása(megoldás):
        megoldás = None
        print("Figyelem: a feladványnak nincs kiszámított megoldása, így tippek korlátozottak.")

    start_time = time.time() - elapsed_before
    score = score_before
    hibák = set()

    while True:
        elapsed = time.time() - start_time
        perc = int(elapsed // 60)
        mp = int(elapsed % 60)
        print(f"\nJelenlegi tábla (pontszám: {score}, idő: {perc} perc {mp} mp):")
        tábla_megjelenítése_színes(aktuális, eredeti, hibák)

        print("\nInteraktív mód – almenü:")
        print("1 - Szám beírása / módosítása")
        print("2 - Mező törlése")
        print("3 - Jelenlegi állapot ellenőrzése")
        print("4 - Tipp kérése (egy helyes mező felfedése)")
        print("5 - Hibás mezők kiemelése")
        print("6 - Idő és pontszám megjelenítése")
        print("7 - Játék mentése")
        print("8 - Játék feladása (megoldás megmutatása)")
        print("0 - Vissza a főmenübe")
        választás = input("Válassz: ").strip()
        hibák = set()

        if választás == "0":
            print("Vissza a főmenübe...")
            break

        elif választás == "1":
            try:
                sor = int(input("Sor (1-9): ")) - 1
                oszlop = int(input("Oszlop (1-9): ")) - 1
                érték = int(input("Szám (1-9): "))
            except ValueError:
                print("Hibás bevitel.")
                continue

            if not (0 <= sor < 9 and 0 <= oszlop < 9 and 1 <= érték <= 9):
                print("Sor/oszlop/szám tartományon kívül.")
                continue

            if eredeti[sor][oszlop] != 0:
                print("Ezt a mezőt nem módosíthatod (eredeti, adott szám).")
                continue

            régi = aktuális[sor][oszlop]
            aktuális[sor][oszlop] = 0 

            if not szám_elhelyezhető(aktuális, sor, oszlop, érték):
                aktuális[sor][oszlop] = régi
                score -= 5
                print("Ez a lépés sérti a Sudoku szabályait. (-5 pont)")
            else:
                aktuális[sor][oszlop] = érték

                score += 5
                üzenet = "Szabályos lépés! (+5 pont)"

                if megoldás is not None and megoldás[sor][oszlop] == érték:
                    score += 5
                    üzenet = "Teljesen jó szám, egyezik a megoldással is! (+10 pont)"

                print(üzenet)
                print(f"Jelenlegi pontszám: {score}")


        elif választás == "2":
            try:
                sor = int(input("Sor (1-9): ")) - 1
                oszlop = int(input("Oszlop (1-9): ")) - 1
            except ValueError:
                print("Hibás bevitel.")
                continue
            if not (0 <= sor < 9 and 0 <= oszlop < 9):
                print("Sor/oszlop tartományon kívül.")
                continue
            if eredeti[sor][oszlop] != 0:
                print("Ezt a mezőt nem törölheted (eredeti, adott szám).")
                continue
            aktuális[sor][oszlop] = 0
            print("Mező törölve.")

        elif választás == "3":
            if not tábla_érvényes(aktuális):
                print("A jelenlegi állapotban HIBA van (szabályt sért).")
            else:
                üres = üres_mező_keresése(aktuális)
                if üres is None:
                    if megoldás is not None:
                        if aktuális == megoldás:
                            elapsed = time.time() - start_time
                            perc = int(elapsed // 60)
                            mp = int(elapsed % 60)
                            score += 500
                            print("GRATULÁLOK! A Sudoku-t helyesen megoldottad! (+500 pont)")
                            print(f"Összidő: {perc} perc {mp} mp")
                            print(f"Végső pontszám: {score}")
                            break
                        else:
                            print("A tábla kitöltött, de nem egyezik a megoldással.")
                    else:
                        másolat = tábla_másolása(aktuális)
                        if sudoku_megoldása(másolat):
                            print("A tábla kitöltött és érvényes megoldásnak tűnik.")
                            break
                        else:
                            print("A tábla kitöltött, de nincs rá megoldás.")
                else:
                    print("Eddig minden szabályos, de a tábla még nincs kész.")

        elif választás == "4":
            if megoldás is None:
                print("Nem áll rendelkezésre megoldás, nem tudok tippet adni.")
                continue
            üres_helyek = [(r, c) for r in range(9) for c in range(9)
                           if aktuális[r][c] == 0]
            if not üres_helyek:
                print("Nincs üres mező, nincs mire tippet adni.")
                continue
            r, c = random.choice(üres_helyek)
            aktuális[r][c] = megoldás[r][c]
            print(f"Tipp: a ({r+1}, {c+1}) mező helyes értéke: {megoldás[r][c]}. (-20 pont)")
            score -= 20

        elif választás == "5":
            if megoldás is None:
                print("Nem áll rendelkezésre megoldás, nem tudom a hibákat kiemelni.")
                continue
            hibák = set()
            for r in range(9):
                for c in range(9):
                    if aktuális[r][c] != 0 and aktuális[r][c] != megoldás[r][c]:
                        hibák.add((r, c))
            if not hibák:
                print("Jelenleg nincs eltérés a megoldástól azokon a mezőkön, ahol már írtál számot.")
            else:
                print("A pirossal jelölt mezők eltérnek a megoldástól.")

        elif választás == "6":
            elapsed = time.time() - start_time
            perc = int(elapsed // 60)
            mp = int(elapsed % 60)
            print(f"Eltelt idő: {perc} perc {mp} mp")
            print(f"Jelenlegi pontszám: {score}")

        elif választás == "7":
            elapsed = time.time() - start_time
            játék_mentése(eredeti, aktuális, puzzle_index, elapsed, score)
        

        elif választás == "8":
            if megoldás is not None:
                print("\n--- A feladvány egy helyes megoldása ---")
                tábla_megjelenítése(megoldás)
            else:
                print("Nem sikerült megoldást számítani ehhez a feladványhoz.")
            print("Visszatérés a főmenübe.")
            break

        else:
            print("Ismeretlen menüpont, próbáld újra.")


def felhasználói_játék_puzzle_választással(táblák):
    if not táblák:
        print("Nincs betöltött feladvány.")
        return
    try:
        s = input("Melyik feladvánnyal szeretnél játszani? (sorszám): ")
        idx = int(s) - 1
    except ValueError:
        print("Hibás sorszám.")
        return
    if idx < 0 or idx >= len(táblák):
        print("Nincs ilyen sorszámú feladvány.")
        return
    eredeti = tábla_másolása(táblák[idx])
    puzzle_index = idx + 1
    interaktív_játék(eredeti, puzzle_index=puzzle_index)

def mentett_játék_indítása():
    adatok = játék_betöltése()
    if adatok is None:
        return
    print("Mentett játék betöltve, folytatás...")
    interaktív_játék(
        eredeti=adatok["eredeti"],
        aktuális=adatok["aktuális"],
        elapsed_before=adatok["elapsed"],
        score_before=adatok["score"],
        puzzle_index=adatok["puzzle_index"],
    )


def menü_megjelenítése():
    print("\n==============================")
    print("   SUDOKU MEGOLDÓ ALKALMAZÁS")
    print("==============================")
    print("1 - Feladványok listázása")
    print("2 - Feladvány megtekintése")
    print("3 - Feladvány automatikus megoldása")
    print("4 - Új feladvány felvétele kézzel")
    print("5 - Feladvány nehézségének becslése")
    print("6 - Ellenőrzés: egyedi-e a feladvány megoldása?")
    print("7 - Felhasználói megoldás próbálása (interaktív játék)")
    print("8 - Mentett játék betöltése")
    print("9 - Új Sudoku generálása (könnyű/közepes/nehéz)")
    print("0 - Kilépés")
    print("==============================")


def main():
    táblák = feladványok_betöltése(PUZZLE_FAJL)

    while True:
        menü_megjelenítése()
        választás = input("Válassz menüpontot: ").strip()

        if választás == "1":
            feladvány_listázása(táblák)
        elif választás == "2":
            feladvány_megtekintése(táblák)
        elif választás == "3":
            feladvány_megoldása(táblák)
        elif választás == "4":
            új_feladvány_hozzáadása(táblák)
        elif választás == "5":
            feladvány_nehézségének_becslése(táblák)
        elif választás == "6":
            feladvány_egyediségének_ellenőrzése(táblák)
        elif választás == "7":
            felhasználói_játék_puzzle_választással(táblák)
        elif választás == "8":
            mentett_játék_indítása()
        elif választás == "9":
            új_sudoku_generálása()
        elif választás == "0":
            print("Kilépés...")
            break
        else:
            print("Ismeretlen menüpont, próbáld újra.")


if __name__ == "__main__":
    main()
