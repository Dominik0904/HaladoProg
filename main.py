import tkinter as tk
from tkinter import messagebox
import time
import random

PUZZLE_FAJL = "puzzles.txt"
SAVEGAME_FAJL = "savegame.txt"

def üres_mező_keresése(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None


def szám_elhelyezhető(board, row, col, num):
    for c in range(9):
        if board[row][c] == num and c != col:
            return False

    for r in range(9):
        if board[r][col] == num and r != row:
            return False

    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num and (r != row or c != col):
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


def tábla_másolása(board):
    return [sor[:] for sor in board]


def tábla_validálása_teljes(board):
    for r in range(9):
        for c in range(9):
            szam = board[r][c]
            if szam == 0: return False

            board[r][c] = 0
            if not szám_elhelyezhető(board, r, c, szam):
                print(f"KRITIKUS HIBA a validálásnál: Sor {r}, Oszlop {c}, Érték {szam} ütközik!")
                board[r][c] = szam
                return False
            board[r][c] = szam
    return True


def generál_kitöltött_táblát():

    max_probalkozas = 50
    for i in range(max_probalkozas):
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

        siker = backtrack_fill()

        if siker:
            if tábla_validálása_teljes(board):
                return board
            else:
                print(f"Generálás {i + 1}. próba: Érvénytelen tábla, eldobva.")
        else:
            print(f"Generálás {i + 1}. próba: Nem sikerült kitölteni.")

    print("Végzetes hiba: Nem sikerült valid táblát generálni.")
    return [[0] * 9 for _ in range(9)]


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


def készít_feladvány_megoldásból(megoldott, fokozat):
    if fokozat == "könnyű":
        cél_üres = 30
    elif fokozat == "közepes":
        cél_üres = 45
    else:
        cél_üres = 58

    puzzle = tábla_másolása(megoldott)
    pozíciók = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(pozíciók)

    eltávolítva = 0
    for r, c in pozíciók:
        if eltávolítva >= cél_üres:
            break
        temp = puzzle[r][c]
        puzzle[r][c] = 0
        másolat = tábla_másolása(puzzle)

        db = megoldások_száma(másolat, limit=2)
        if db != 1:
            puzzle[r][c] = temp
        else:
            eltávolítva += 1
    return puzzle


#GUI

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.geometry("600x750")

        self.eredeti_board = [[0] * 9 for _ in range(9)]
        self.jelenlegi_board = [[0] * 9 for _ in range(9)]
        self.megoldás_board = None
        self.start_time = None
        self.timer_running = False
        self.score = 0
        self.cells = {}

        self._init_ui()

        print("Alkalmazás indítása... Első generálás...")
        self.uj_jatek_generalasa("közepes")

    def _init_ui(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Játék", menu=game_menu)
        game_menu.add_command(label="Új játék (Könnyű)", command=lambda: self.uj_jatek_generalasa("könnyű"))
        game_menu.add_command(label="Új játék (Közepes)", command=lambda: self.uj_jatek_generalasa("közepes"))
        game_menu.add_command(label="Új játék (Nehéz)", command=lambda: self.uj_jatek_generalasa("nehéz"))
        game_menu.add_separator()
        game_menu.add_command(label="Játék mentése", command=self.mentes)
        game_menu.add_command(label="Betöltés", command=self.betoltes)
        game_menu.add_separator()
        game_menu.add_command(label="Kilépés", command=self.root.quit)

        action_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Műveletek", menu=action_menu)
        action_menu.add_command(label="Ellenőrzés", command=self.ellenorzes)
        action_menu.add_command(label="Megoldás mutatása", command=self.megoldas_mutatasa)
        action_menu.add_command(label="Tipp kérése (-20 pont)", command=self.tipp_kerese)

        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)
        self.lbl_time = tk.Label(info_frame, text="Idő: 00:00", font=("Arial", 12))
        self.lbl_time.pack(side=tk.LEFT, padx=20)
        self.lbl_score = tk.Label(info_frame, text="Pontszám: 0", font=("Arial", 12))
        self.lbl_score.pack(side=tk.LEFT, padx=20)

        grid_frame = tk.Frame(self.root, bg="black", bd=2)
        grid_frame.pack(pady=10, padx=10)

        self.blocks = [[None for _ in range(3)] for _ in range(3)]
        for br in range(3):
            for bc in range(3):
                f = tk.Frame(grid_frame, bd=1, highlightbackground="black", highlightthickness=2, bg="white")
                f.grid(row=br, column=bc, padx=1, pady=1)
                self.blocks[br][bc] = f

        validate_cmd = (self.root.register(self.validate_entry), '%P', '%W')

        for r in range(9):
            for c in range(9):
                parent = self.blocks[r // 3][c // 3]

                row_in_block = r % 3
                col_in_block = c % 3

                e = tk.Entry(parent, width=2, font=("Arial", 20, "bold"), justify="center",
                             validate="key", validatecommand=validate_cmd, bd=1, relief="solid")

                e.grid(row=row_in_block, column=col_in_block, padx=1, pady=1)

                e.bind('<KeyRelease>', lambda event, row=r, col=c: self.on_cell_change(event, row, col))
                self.cells[(r, c)] = e

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Ellenőrzés", command=self.ellenorzes, bg="#dddddd").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Új Generálása", command=lambda: self.uj_jatek_generalasa("közepes"),
                  bg="#dddddd").pack(side=tk.LEFT, padx=5)

    def validate_entry(self, new_value, widget_name):
        if new_value == "": return True
        if new_value.isdigit() and 1 <= int(new_value) <= 9 and len(new_value) == 1:
            return True
        return False

    def uj_jatek_generalasa(self, nehezseg):
        print(f"\n--- ÚJ JÁTÉK GENERÁLÁSA ({nehezseg}) ---")

        teljes = generál_kitöltött_táblát()

        print("Generált TELJES tábla (Ellenőrzéshez):")
        for sor in teljes:
            print(sor)

        puzzle = készít_feladvány_megoldásból(teljes, nehezseg)
        self.jatek_inditasa(puzzle)

    def jatek_inditasa(self, board_matrix):
        self.eredeti_board = tábla_másolása(board_matrix)
        self.jelenlegi_board = tábla_másolása(board_matrix)

        self.megoldás_board = tábla_másolása(self.eredeti_board)
        sudoku_megoldása(self.megoldás_board)

        self.score = 0
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
        self.redraw_board()

    def redraw_board(self):
        for r in range(9):
            for c in range(9):
                val = self.jelenlegi_board[r][c]
                entry = self.cells[(r, c)]

                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.config(bg="white")

                if val != 0:
                    entry.insert(0, str(val))

                if self.eredeti_board[r][c] != 0:
                    entry.config(fg="blue", bg="#e0e0e0", state="readonly")
                else:
                    entry.config(fg="black", bg="white", state="normal")

        self.update_score_label()

    def on_cell_change(self, event, row, col):
        entry = self.cells[(row, col)]
        if entry.cget('state') == 'readonly':
            return

        val_str = entry.get()
        try:
            val = int(val_str) if val_str else 0
        except ValueError:
            val = 0
        if self.jelenlegi_board[row][col] != val:
            self.jelenlegi_board[row][col] = val

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            mins = elapsed // 60
            secs = elapsed % 60
            self.lbl_time.config(text=f"Idő: {mins:02d}:{secs:02d}")
            self.root.after(1000, self.update_timer)

    def update_score_label(self):
        self.lbl_score.config(text=f"Pontszám: {self.score}")

    def ellenorzes(self):
        hibak = 0
        ures = 0
        for r in range(9):
            for c in range(9):
                val = self.jelenlegi_board[r][c]
                entry = self.cells[(r, c)]

                if val == 0:
                    ures += 1
                    if self.eredeti_board[r][c] == 0:
                        entry.config(bg="white")
                elif self.eredeti_board[r][c] == 0:
                    if val != self.megoldás_board[r][c]:
                        entry.config(bg="#ffcccc")
                        hibak += 1
                    else:
                        entry.config(bg="#ccffcc")

        if hibak == 0 and ures == 0:
            self.timer_running = False
            self.score += 500
            self.update_score_label()
            messagebox.showinfo("Gratulálok!", f"Sikeresen megoldottad!\nPontszám: {self.score}")
        elif hibak > 0:
            self.score -= (hibak * 5)
            self.update_score_label()
            messagebox.showwarning("Ellenőrzés", f"{hibak} hibát találtam!")
        else:
            messagebox.showinfo("Ellenőrzés", "Eddig jó, de még nincs kész.")

    def tipp_kerese(self):
        ures_helyek = [(r, c) for r in range(9) for c in range(9) if self.jelenlegi_board[r][c] == 0]
        if not ures_helyek:
            messagebox.showinfo("Info", "Nincs üres mező.")
            return
        r, c = random.choice(ures_helyek)
        helyes_szam = self.megoldás_board[r][c]

        self.jelenlegi_board[r][c] = helyes_szam
        entry = self.cells[(r, c)]
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, str(helyes_szam))
        entry.config(bg="yellow")

        self.score -= 20
        self.update_score_label()

    def megoldas_mutatasa(self):
        if not messagebox.askyesno("Feladom", "Biztosan feladod?"):
            return
        self.timer_running = False
        self.jelenlegi_board = tábla_másolása(self.megoldás_board)
        self.redraw_board()

    def mentes(self):
        elapsed = time.time() - self.start_time
        try:
            with open(SAVEGAME_FAJL, "w") as f:
                f.write("0\n")
                f.write(str(elapsed) + "\n")
                f.write(str(self.score) + "\n")
                f.write("".join(str(self.eredeti_board[r][c]) for r in range(9) for c in range(9)) + "\n")
                f.write("".join(str(self.jelenlegi_board[r][c]) for r in range(9) for c in range(9)) + "\n")
            messagebox.showinfo("Mentés", "Játék mentve.")
        except Exception as e:
            messagebox.showerror("Hiba", f"Mentés sikertelen: {e}")

    def betoltes(self):
        try:
            with open(SAVEGAME_FAJL, "r") as f:
                sorok = [s.strip() for s in f.readlines()]
            elapsed = float(sorok[1])
            score = int(sorok[2])
            eredeti_str = sorok[3]
            aktualis_str = sorok[4]
            eredeti = []
            aktualis = []
            for i in range(9):
                eredeti.append([int(ch) for ch in eredeti_str[i * 9: (i + 1) * 9]])
                aktualis.append([int(ch) for ch in aktualis_str[i * 9: (i + 1) * 9]])

            self.jatek_inditasa(eredeti)
            self.jelenlegi_board = aktualis
            self.score = score
            self.start_time = time.time() - elapsed

            self.redraw_board()
            messagebox.showinfo("Betöltés", "Játék betöltve.")
        except Exception as e:
            messagebox.showerror("Hiba", "Nincs mentés.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()