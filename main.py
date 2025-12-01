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
            if szam == 0:
                return False
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
        self.cell_state = [["empty"] * 9 for _ in range(9)]
        self.current_theme = "dark"
        self.game_finished = False

        self._init_ui()
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
        self.action_menu = action_menu
        self.menu_check_index = action_menu.index("end")
        action_menu.add_command(label="Megoldás mutatása", command=self.megoldas_mutatasa)
        action_menu.add_command(label="Tipp kérése (-20 pont)", command=self.tipp_kerese)

        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Téma", menu=theme_menu)
        theme_menu.add_command(label="Világos mód", command=lambda: self.set_theme("light"))
        theme_menu.add_command(label="Sötét mód", command=lambda: self.set_theme("dark"))

        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)
        self.info_frame = info_frame
        self.lbl_time = tk.Label(info_frame, text="Idő: 00:00", font=("Segoe UI", 13, "bold"))
        self.lbl_time.pack(side=tk.LEFT, padx=30)
        self.lbl_score = tk.Label(info_frame, text="Pontszám: 0", font=("Segoe UI", 13, "bold"))
        self.lbl_score.pack(side=tk.LEFT, padx=30)

        grid_frame = tk.Frame(self.root)
        grid_frame.pack(pady=10, padx=10)
        self.grid_frame = grid_frame

        self.blocks = [[None for _ in range(3)] for _ in range(3)]
        for br in range(3):
            for bc in range(3):
                f = tk.Frame(grid_frame, bd=3, relief="solid", highlightthickness=0)
                f.grid(row=br, column=bc, padx=2, pady=2)
                self.blocks[br][bc] = f

        validate_cmd = (self.root.register(self.validate_entry), "%P", "%W")

        for r in range(9):
            for c in range(9):
                parent = self.blocks[r // 3][c // 3]
                row_in_block = r % 3
                col_in_block = c % 3
                e = tk.Entry(
                    parent,
                    width=2,
                    font=("Segoe UI", 20, "bold"),
                    justify="center",
                    validate="key",
                    validatecommand=validate_cmd,
                    bd=0,
                    relief="flat",
                )
                e.grid(row=row_in_block, column=col_in_block, padx=3, pady=3, ipadx=4, ipady=4)
                e.bind("<KeyRelease>", lambda event, row=r, col=c: self.on_cell_change(event, row, col))
                self.cells[(r, c)] = e

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=25)
        self.btn_frame = btn_frame
        self.btn_check = tk.Button(btn_frame, text="Ellenőrzés", command=self.ellenorzes, width=12)
        self.btn_check.pack(side=tk.LEFT, padx=10)
        # Itt változott: a gomb most a nehézség-választó popupot hívja
        self.btn_new = tk.Button(
            btn_frame,
            text="Új Generálása",
            command=self.valassz_nehezseget_popup,
            width=12,
        )
        self.btn_new.pack(side=tk.LEFT, padx=10)

    def validate_entry(self, new_value, widget_name):
        if new_value == "":
            return True
        if new_value.isdigit() and 1 <= int(new_value) <= 9 and len(new_value) == 1:
            return True
        return False

    def uj_jatek_generalasa(self, nehezseg):
        teljes = generál_kitöltött_táblát()
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
        self.set_game_finished(False)

        for r in range(9):
            for c in range(9):
                if self.eredeti_board[r][c] != 0:
                    self.cell_state[r][c] = "fixed"
                else:
                    self.cell_state[r][c] = "empty"

        self.redraw_board()
        self.set_theme(self.current_theme)

    def redraw_board(self):
        for r in range(9):
            for c in range(9):
                val = self.jelenlegi_board[r][c]
                entry = self.cells[(r, c)]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                if val != 0:
                    entry.insert(0, str(val))
                if self.eredeti_board[r][c] != 0:
                    entry.config(state="readonly")
        self.update_score_label()

    def on_cell_change(self, event, row, col):
        entry = self.cells[(row, col)]
        if entry.cget("state") == "readonly":
            return
        val_str = entry.get()
        try:
            val = int(val_str) if val_str else 0
        except ValueError:
            val = 0
        self.jelenlegi_board[row][col] = val
        if self.eredeti_board[row][col] == 0:
            if val == 0:
                self.cell_state[row][col] = "empty"
            else:
                self.cell_state[row][col] = "filled"
        self.set_theme(self.current_theme)

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
        if self.game_finished:
            messagebox.showinfo("Játék vége", "Ezt a feladványt már befejezted. Válassz új játékot.")
            return

        hibak = 0
        ures = 0
        for r in range(9):
            for c in range(9):
                val = self.jelenlegi_board[r][c]
                if val == 0:
                    if self.eredeti_board[r][c] == 0:
                        self.cell_state[r][c] = "empty"
                    ures += 1
                elif self.eredeti_board[r][c] == 0:
                    if val != self.megoldás_board[r][c]:
                        self.cell_state[r][c] = "error"
                        hibak += 1
                    else:
                        self.cell_state[r][c] = "correct"
        self.set_theme(self.current_theme)

        if hibak == 0 and ures == 0:
            self.timer_running = False
            self.score += 500
            self.update_score_label()
            self.set_game_finished(True)
            if messagebox.askyesno(
                "Gratulálok!",
                f"Sikeresen megoldottad!\nPontszám: {self.score}\n\nSzeretnél új játékot indítani?"
            ):
                self.valassz_nehezseget_popup()
        elif hibak > 0:
            self.score -= hibak * 5
            self.update_score_label()
            messagebox.showwarning("Ellenőrzés", f"{hibak} hibát találtam!")
        else:
            messagebox.showinfo("Ellenőrzés", "Eddig jó, de még nincs kész.")

    def tipp_kerese(self):
        if self.game_finished:
            messagebox.showinfo("Játék vége", "A játék befejeződött. Indíts új játékot.")
            return
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
        self.cell_state[r][c] = "tip"
        self.score -= 20
        self.update_score_label()
        self.set_theme(self.current_theme)

    def megoldas_mutatasa(self):
        if self.game_finished:
            return
        if not messagebox.askyesno("Feladom", "Biztosan feladod?"):
            return
        self.timer_running = False
        self.jelenlegi_board = tábla_másolása(self.megoldás_board)
        for r in range(9):
            for c in range(9):
                if self.eredeti_board[r][c] != 0:
                    self.cell_state[r][c] = "fixed"
                else:
                    self.cell_state[r][c] = "solved"
        self.redraw_board()
        self.set_game_finished(True)
        self.set_theme(self.current_theme)

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
                eredeti.append([int(ch) for ch in eredeti_str[i * 9:(i + 1) * 9]])
                aktualis.append([int(ch) for ch in aktualis_str[i * 9:(i + 1) * 9]])
            self.jatek_inditasa(eredeti)
            self.jelenlegi_board = aktualis
            self.score = score
            self.start_time = time.time() - elapsed
            for r in range(9):
                for c in range(9):
                    if self.eredeti_board[r][c] != 0:
                        self.cell_state[r][c] = "fixed"
                    elif self.jelenlegi_board[r][c] == 0:
                        self.cell_state[r][c] = "empty"
                    else:
                        self.cell_state[r][c] = "filled"
            self.redraw_board()
            self.set_theme(self.current_theme)
            messagebox.showinfo("Betöltés", "Játék betöltve.")
        except Exception:
            messagebox.showerror("Hiba", "Nincs mentés.")

    def set_theme(self, mode):
        self.current_theme = mode

        if mode == "dark":
            bg_main = "#121212"
            bg_block = "#000000"
            bg_cell = "#3f3f3f"
            fg_text = "#f5f5f5"
            readonly_bg = "#2d3f64"
            fixed_fg = "#74b9ff"
            tip_bg = "#8d6e00"
            tip_fg = "#ffec99"
            err_bg = "#d63031"
            err_fg = "#ffffff"
            ok_bg = "#00b894"
            ok_fg = "#ffffff"
            solved_fg = "#ffffff"
            solved_bg = "#3f3f3f"
            button_bg = "#1f1f1f"
            button_fg = "#f5f5f5"
            button_active_bg = "#2e2e2e"
        else:
            bg_main = "#f3f3f3"
            bg_block = "#000000"
            bg_cell = "#ffffff"
            fg_text = "#222222"
            readonly_bg = "#d6e8ff"
            fixed_fg = "#0052cc"
            tip_bg = "#ffeaa7"
            tip_fg = "#4b3b00"
            err_bg = "#ff7675"
            err_fg = "#ffffff"
            ok_bg = "#55efc4"
            ok_fg = "#004d40"
            solved_fg = "#222222"
            solved_bg = "#ffffff"
            button_bg = "#ffffff"
            button_fg = "#222222"
            button_active_bg = "#e0e0e0"

        self.root.config(bg=bg_main)
        self.info_frame.config(bg=bg_main)
        self.lbl_time.config(bg=bg_main, fg=fg_text)
        self.lbl_score.config(bg=bg_main, fg=fg_text)

        self.grid_frame.config(bg=bg_main)

        for br in range(3):
            for bc in range(3):
                block = self.blocks[br][bc]
                block.config(bg=bg_block)

        for r in range(9):
            for c in range(9):
                entry = self.cells[(r, c)]
                state = self.cell_state[r][c]

                if self.eredeti_board[r][c] != 0:
                    entry.config(state="readonly")
                else:
                    if entry.cget("state") == "readonly":
                        entry.config(state="normal")

                if state == "fixed":
                    entry.config(
                        fg=fixed_fg,
                        bg=readonly_bg,
                        readonlybackground=readonly_bg,
                        insertbackground=fixed_fg,
                    )
                elif state == "tip":
                    entry.config(
                        fg=tip_fg,
                        bg=tip_bg,
                        insertbackground=tip_fg,
                    )
                elif state == "error":
                    entry.config(
                        fg=err_fg,
                        bg=err_bg,
                        insertbackground=err_fg,
                    )
                elif state == "correct":
                    entry.config(
                        fg=ok_fg,
                        bg=ok_bg,
                        insertbackground=ok_fg,
                    )
                elif state == "solved":
                    entry.config(
                        fg=solved_fg,
                        bg=solved_bg,
                        insertbackground=solved_fg,
                    )
                else:
                    entry.config(
                        fg=fg_text,
                        bg=bg_cell,
                        insertbackground=fg_text,
                    )

        self.btn_frame.config(bg=bg_main)
        for btn in (self.btn_check, self.btn_new):
            btn.config(
                bg=button_bg,
                fg=button_fg,
                activebackground=button_active_bg,
                activeforeground=button_fg,
                bd=0,
                relief="flat",
                font=("Segoe UI", 11, "bold"),
                padx=10,
                pady=5,
            )

    def set_game_finished(self, finished: bool):
        self.game_finished = finished
        state = "disabled" if finished else "normal"
        self.btn_check.config(state=state)
        if hasattr(self, "action_menu"):
            self.action_menu.entryconfig(self.menu_check_index, state=state)

    def valassz_nehezseget_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Új játék nehézség")
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        tk.Label(
            win,
            text="Válassz nehézséget a következő játékhoz:",
            font=("Segoe UI", 11)
        ).pack(padx=20, pady=10)

        frame = tk.Frame(win)
        frame.pack(pady=10)

        def indit(diff):
            win.destroy()
            self.uj_jatek_generalasa(diff)

        tk.Button(frame, text="Könnyű", width=10, command=lambda: indit("könnyű")).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Közepes", width=10, command=lambda: indit("közepes")).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Nehéz", width=10, command=lambda: indit("nehéz")).pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
