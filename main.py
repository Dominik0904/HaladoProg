import time
import random
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Listbox, Scrollbar

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


def tábla_másolása(board):
    return [sor[:] for sor in board]


def üres_mezők_száma(board):
    db = 0
    for r in range(9):
        for c in range(9):
<<<<<<< HEAD
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


=======
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


>>>>>>> 56a534c (javitva)
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
        return []
    for sor in f:
        sor = sor.strip()
        if not sor or sor.startswith("#"):
            continue
        if len(sor) != 9:
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
<<<<<<< HEAD
        cél_üres = 58
<<<<<<< Updated upstream
=======
=======
        cél_üres = 60
>>>>>>> 56a534c (javitva)
>>>>>>> Stashed changes
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


<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
class SudokuApp:
=======
def játék_mentése_hozzáfűzéssel(mentés_neve, eredeti, aktuális, puzzle_index, elapsed, score):
    most = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    fejléc = f"{mentés_neve}|{puzzle_index}|{most}"
    try:
        with open(SAVEGAME_FAJL, "a", encoding="utf-8") as f:
            f.write(fejléc + "\n")
            f.write(str(elapsed) + "\n")
            f.write(str(score) + "\n")
            eredeti_str = "".join(str(eredeti[r][c]) for r in range(9) for c in range(9))
            aktuális_str = "".join(str(aktuális[r][c]) for r in range(9) for c in range(9))
            f.write(eredeti_str + "\n")
            f.write(aktuális_str + "\n")
        return True
    except OSError:
        return False


def összes_mentett_játék_betöltése():
    mentések = []
    try:
        with open(SAVEGAME_FAJL, "r", encoding="utf-8") as f:
            sorok = [s.strip() for s in f.readlines()]
    except OSError:
        return []
    for i in range(0, len(sorok), 5):
        if i + 4 >= len(sorok):
            break
        try:
            fejléc_adatok = sorok[i].split('|')
            név = fejléc_adatok[0]
            p_index = int(fejléc_adatok[1]) if len(fejléc_adatok) > 1 else -1
            dátum = fejléc_adatok[2] if len(fejléc_adatok) > 2 else "?"
            elapsed = float(sorok[i + 1])
            score = int(sorok[i + 2])
            eredeti_str = sorok[i + 3]
            aktuális_str = sorok[i + 4]
            eredeti = []
            aktuális = []
            for r in range(9):
                sor_e = []
                sor_a = []
                for c in range(9):
                    idx = r * 9 + c
                    sor_e.append(int(eredeti_str[idx]))
                    sor_a.append(int(aktuális_str[idx]))
                eredeti.append(sor_e)
                aktuális.append(sor_a)
            mentések.append({
                "név": név,
                "dátum": dátum,
                "puzzle_index": p_index,
                "elapsed": elapsed,
                "score": score,
                "eredeti": eredeti,
                "aktuális": aktuális
            })
        except (ValueError, IndexError):
            continue
    return mentések


class SudokuGUI:
>>>>>>> 56a534c (javitva)
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.geometry("800x600")

        self.entries = {}
        self.cell_frames = {}
        self.eredeti_board = [[0] * 9 for _ in range(9)]
        self.solution_board = None

        self.current_puzzle_index = -1
        self.score = 0
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> Stashed changes

        self.cells = {}
        self.cell_state = [["empty"] * 9 for _ in range(9)]
        self.current_theme = "dark"
        self.game_finished = False

        self._init_ui()
        self.uj_jatek_generalasa("közepes")
=======
        self.start_time = time.time()
        self.timer_running = False

        self.is_manual_mode = False
        self.scored_cells = set()
        self.error_cells = set()
        self.hint_cells = set()

        self.current_theme = "dark"
>>>>>>> 56a534c (javitva)

        self.control_labels = []
        self.control_buttons = []
        self.dividers = []
        self.control_frames = []

        self.vcmd = (self.root.register(self.validate), '%P')

<<<<<<< HEAD
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
<<<<<<< Updated upstream
=======
=======
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side="left", padx=10)

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side="right", fill="y", padx=10)

        self.create_grid(self.left_frame)
        self.create_control_panel(self.right_frame)

        self.status_var = tk.StringVar()
        self.status_var.set("Üdvözöllek! Válassz egy funkciót.")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.info_var = tk.StringVar()
        self.info_var.set("Idő: 0p 0mp | Pont: 0")
        self.info_label = tk.Label(self.root, textvariable=self.info_var, font=("Arial", 12, "bold"))
        self.info_label.pack(side=tk.TOP, pady=5)

        self.apply_theme()
        self.update_timer()

    def get_theme_colors(self):
        if self.current_theme == "dark":
            return {
                "main_bg": "#121212",
                "panel_bg": "#181818",
                "grid_bg": "#000000",
                "status_bg": "#181818",
                "status_fg": "#f5f5f5",
                "info_fg": "#f5f5f5",
                "cell_bg": "#303030",
                "entry_fg": "#f5f5f5",
                "given_bg": "#2d3f64",
                "given_fg": "#74b9ff",
                "correct_bg": "#145a32",
                "correct_fg": "#ffffff",
                "error_bg": "#7f1d1d",
                "error_fg": "#ffb3b3",
                "hint_bg": "#b7950b",
                "hint_fg": "#fff9c4",
                "button_bg": "#222222",
                "button_fg": "#f5f5f5",
                "button_active_bg": "#333333",
                "label_fg": "#f5f5f5",
                "divider_bg": "#444444",
            }
        else:
            return {
                "main_bg": "#f3f3f3",
                "panel_bg": "#e0e0e0",
                "grid_bg": "#000000",
                "status_bg": "#e0e0e0",
                "status_fg": "#222222",
                "info_fg": "#222222",
                "cell_bg": "#ffffff",
                "entry_fg": "#222222",
                "given_bg": "#f0f0f0",
                "given_fg": "#0052cc",
                "correct_bg": "#ccffcc",
                "correct_fg": "#004d40",
                "error_bg": "#ffcccc",
                "error_fg": "#b71c1c",
                "hint_bg": "#fff3b0",
                "hint_fg": "#3e2723",
                "button_bg": "#ffffff",
                "button_fg": "#222222",
                "button_active_bg": "#dcdcdc",
                "label_fg": "#222222",
                "divider_bg": "#c0c0c0",
            }

    def set_theme(self, mode):
        self.current_theme = mode
        self.apply_theme()

    def apply_theme(self):
        colors = self.get_theme_colors()
        self.root.config(bg=colors["main_bg"])
        self.main_frame.config(bg=colors["main_bg"])
        self.left_frame.config(bg=colors["main_bg"])
        self.right_frame.config(bg=colors["panel_bg"])
        self.status_bar.config(bg=colors["status_bg"], fg=colors["status_fg"])
        self.info_label.config(bg=colors["main_bg"], fg=colors["info_fg"])

        for lbl in self.control_labels:
            lbl.config(bg=colors["panel_bg"], fg=colors["label_fg"])

        for fr in self.control_frames:
            fr.config(bg=colors["panel_bg"])

        for btn in self.control_buttons:
            btn.config(
                bg=colors["button_bg"],
                fg=colors["button_fg"],
                activebackground=colors["button_active_bg"],
                activeforeground=colors["button_fg"],
                bd=0,
                relief="flat",
            )

        for div in self.dividers:
            div.config(bg=colors["divider_bg"])

        for (r, c), frame in self.cell_frames.items():
            frame.config(bg=colors["grid_bg"])

        for r in range(9):
            for c in range(9):
                self.reapply_cell_theme(r, c)

    def reapply_cell_theme(self, r, c):
        colors = self.get_theme_colors()
        e = self.entries[(r, c)]

        if self.is_manual_mode:
            e.config(
                state="normal",
                bg=colors["cell_bg"],
                fg=colors["entry_fg"],
                disabledforeground=colors["entry_fg"],
            )
            return

        orig_val = self.eredeti_board[r][c]

        if orig_val != 0:
            e.config(
                state="disabled",
                bg=colors["given_bg"],
                disabledbackground=colors["given_bg"],
                disabledforeground=colors["given_fg"],
            )
            return

        if (r, c) in self.error_cells:
            e.config(
                state="normal",
                bg=colors["error_bg"],
                fg=colors["error_fg"],
            )
            return

        if (r, c) in self.scored_cells:
            if (r, c) in self.hint_cells:
                e.config(
                    state="disabled",
                    bg=colors["hint_bg"],
                    disabledbackground=colors["hint_bg"],
                    disabledforeground=colors["hint_fg"],
                )
            else:
                e.config(
                    state="disabled",
                    bg=colors["correct_bg"],
                    disabledbackground=colors["correct_bg"],
                    disabledforeground=colors["correct_fg"],
                )
            return

        e.config(state="normal", bg=colors["cell_bg"], fg=colors["entry_fg"])

    def validate(self, P):
        if P == "" or (P.isdigit() and len(P) == 1):
            return True
        return False

    def on_entry_change(self, event, r, c):
        if self.entries[(r, c)]['state'] == 'normal':
            if self.eredeti_board[r][c] == 0:
                if (r, c) in self.scored_cells:
                    self.scored_cells.remove((r, c))
                if (r, c) in self.error_cells:
                    self.error_cells.remove((r, c))
                if (r, c) in self.hint_cells:
                    self.hint_cells.remove((r, c))
                self.reapply_cell_theme(r, c)

    def create_grid(self, parent):
        colors = self.get_theme_colors()
        for r in range(9):
            for c in range(9):
                pad_y_top = 2 if r % 3 == 0 and r != 0 else 0
                pad_x_left = 2 if c % 3 == 0 and c != 0 else 0
                cell_frame = tk.Frame(parent, bg=colors["grid_bg"], bd=1)
                cell_frame.grid(row=r, column=c, padx=(pad_x_left, 0), pady=(pad_y_top, 0), sticky="nsew")
                e = tk.Entry(
                    cell_frame,
                    width=3,
                    font=("Arial", 18),
                    justify="center",
                    validate="key",
                    validatecommand=self.vcmd,
                )
                e.pack(padx=1, pady=1)
                e.bind('<KeyRelease>', lambda event, row=r, col=c: self.on_entry_change(event, row, col))
                self.entries[(r, c)] = e
                self.cell_frames[(r, c)] = cell_frame

    def add_label(self, parent, text):
        lbl = tk.Label(parent, text=text, font=("Arial", 10, "bold"))
        lbl.pack(pady=(0, 5))
        self.control_labels.append(lbl)
        return lbl

    def add_divider(self, parent):
        div = tk.Frame(parent, height=2, bd=1, relief=tk.SUNKEN)
        div.pack(fill="x", pady=10)
        self.dividers.append(div)
        return div

    def add_button(self, parent, text, command, **kwargs):
        btn = tk.Button(parent, text=text, command=command, **kwargs)
        btn.pack(fill="x", pady=2)
        self.control_buttons.append(btn)
        return btn

    def create_control_panel(self, parent):
        self.add_label(parent, "Új játék generálása")
        f1 = tk.Frame(parent)
        f1.pack(pady=5)
        self.control_frames.append(f1)
        b1 = tk.Button(f1, text="Könnyű", width=8, command=lambda: self.start_new_game("könnyű"))
        b1.pack(side="left", padx=2)
        self.control_buttons.append(b1)
        b2 = tk.Button(f1, text="Közepes", width=8, command=lambda: self.start_new_game("közepes"))
        b2.pack(side="left", padx=2)
        self.control_buttons.append(b2)
        b3 = tk.Button(f1, text="Nehéz", width=8, command=lambda: self.start_new_game("nehéz"))
        b3.pack(side="left", padx=2)
        self.control_buttons.append(b3)
        self.add_divider(parent)

        self.add_label(parent, "Fájl műveletek")
        self.add_button(parent, "Feladványok listázása", self.open_puzzle_list)
        self.add_button(parent, "Mentett játék folytatása...", self.load_saved_game_list_gui)
        self.add_button(parent, "Jelenlegi játék mentése", self.save_current_game_gui)
        self.add_divider(parent)

        self.add_label(parent, "Saját feladvány")
        self.add_button(parent, "Szerkesztő Mód Indítása", self.manual_entry_mode)
        self.add_button(parent, "Saját feladvány mentése", self.save_manual_puzzle_to_file)
        self.add_divider(parent)

        self.add_label(parent, "Játék Vezérlő")
        self.add_button(parent, "Ellenőrzés (Zárolás)", self.check_solution_with_locks)
        self.add_button(parent, "Tipp kérése (-20 pont)", self.request_hint)
        self.add_button(parent, "Megoldás mutatása", self.solve_current)
        self.add_divider(parent)

        self.add_label(parent, "Téma")
        f_theme = tk.Frame(parent)
        f_theme.pack(pady=5, fill="x")
        self.control_frames.append(f_theme)
        bt_light = tk.Button(f_theme, text="Világos mód", width=12, command=lambda: self.set_theme("light"))
        bt_light.pack(side="left", padx=2)
        self.control_buttons.append(bt_light)
        bt_dark = tk.Button(f_theme, text="Sötét mód", width=12, command=lambda: self.set_theme("dark"))
        bt_dark.pack(side="left", padx=2)
        self.control_buttons.append(bt_dark)

    def get_board_from_gui(self):
        board = [[0] * 9 for _ in range(9)]
        for r in range(9):
            for c in range(9):
                val = self.entries[(r, c)].get()
                if val.isdigit() and val != "0":
                    board[r][c] = int(val)
                else:
                    board[r][c] = 0
        return board

    def set_board_to_gui(self, board, set_original=False):
        for r in range(9):
            for c in range(9):
                e = self.entries[(r, c)]
                val = board[r][c]
                e.config(state="normal")
                e.delete(0, tk.END)
                if val != 0:
                    e.insert(0, str(val))
                if set_original:
                    self.eredeti_board[r][c] = val
        self.apply_theme()
>>>>>>> 56a534c (javitva)
>>>>>>> Stashed changes

    def update_timer(self):
        if self.timer_running:
            elapsed = time.time() - self.start_time
            perc = int(elapsed // 60)
            mp = int(elapsed % 60)
            self.info_var.set(f"Idő: {perc}p {mp}mp | Pont: {self.score}")
        self.root.after(1000, self.update_timer)

    def start_new_game(self, fokozat):
        self.status_var.set("Generálás...")
        self.root.update()
        megoldott = generál_kitöltött_táblát()
        self.solution_board = megoldott
        puzzle = készít_feladvány_megoldásból(megoldott, fokozat)
        self.scored_cells = set()
        self.error_cells = set()
        self.hint_cells = set()
        self.set_board_to_gui(puzzle, set_original=True)
        self.score = 0
        self.start_time = time.time()
        self.timer_running = True
        self.is_manual_mode = False
        self.current_puzzle_index = -1
        self.status_var.set(f"Új {fokozat} játék indult.")

<<<<<<< HEAD
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
=======
    def open_puzzle_list(self):
        táblák = feladványok_betöltése(PUZZLE_FAJL)
        if not táblák:
            messagebox.showerror("Hiba", "Nem sikerült betölteni a feladványokat.")
            return
        top = Toplevel(self.root)
        top.title("Feladványok listája")
        top.geometry("300x400")
        listbox = Listbox(top)
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar = Scrollbar(top, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)
        for i, _ in enumerate(táblák):
            listbox.insert(tk.END, f"{i + 1}. feladvány")

        def load_selected():
            sel = listbox.curselection()
            if not sel:
                return
            idx = sel[0]
            puzzle = táblák[idx]
            temp_board = tábla_másolása(puzzle)
            sudoku_megoldása(temp_board)
            self.solution_board = temp_board
            self.scored_cells = set()
            self.error_cells = set()
            self.hint_cells = set()
            self.set_board_to_gui(puzzle, set_original=True)
            self.score = 0
            self.start_time = time.time()
            self.timer_running = True
            self.is_manual_mode = False
            self.current_puzzle_index = idx + 1
            self.status_var.set(f"{idx + 1}. feladvány betöltve.")
            top.destroy()

        tk.Button(top, text="Betöltés", command=load_selected).pack(side="bottom", fill="x", pady=5)

    def load_saved_game_list_gui(self):
        mentések = összes_mentett_játék_betöltése()
        if not mentések:
            messagebox.showinfo("Infó", "Nincs mentett játék a savegame.txt fájlban.")
            return
        top = Toplevel(self.root)
        top.title("Mentett játékok betöltése")
        top.geometry("400x400")
        listbox = Listbox(top)
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar = Scrollbar(top, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)
        for i, m in enumerate(reversed(mentések)):
            kijelző_szöveg = f"{m['név']} | Dátum: {m['dátum']} | Pont: {m['score']}"
            listbox.insert(tk.END, kijelző_szöveg)

        def load_selected_save():
            sel = listbox.curselection()
            if not sel:
                return
            reversed_idx = sel[0]
            valodi_idx = len(mentések) - 1 - reversed_idx
            adatok = mentések[valodi_idx]
            self.eredeti_board = adatok["eredeti"]
            self.set_board_to_gui(adatok["aktuális"], set_original=False)
            temp_board = tábla_másolása(self.eredeti_board)
            sudoku_megoldása(temp_board)
            self.solution_board = temp_board
            self.scored_cells = set()
            self.error_cells = set()
            self.hint_cells = set()
            for r in range(9):
                for c in range(9):
                    if self.eredeti_board[r][c] == 0 and adatok["aktuális"][r][c] != 0:
                        self.scored_cells.add((r, c))
            self.score = adatok["score"]
            self.start_time = time.time() - adatok["elapsed"]
            self.current_puzzle_index = adatok["puzzle_index"]
            self.timer_running = True
            self.is_manual_mode = False
            self.status_var.set(f"'{adatok['név']}' betöltve.")
            self.apply_theme()
            top.destroy()

        tk.Button(top, text="Kiválasztott mentés betöltése", command=load_selected_save).pack(
            side="bottom", fill="x", pady=5
        )

    def save_current_game_gui(self):
        if not self.timer_running or self.is_manual_mode:
            messagebox.showinfo("Info", "Nincs aktív játék amit menteni lehetne.")
            return
        mentés_neve = simpledialog.askstring("Mentés", "Adj nevet a mentésnek:", initialvalue="Játékom")
        if not mentés_neve:
            return
        elapsed = time.time() - self.start_time
        tiszta_board = [[0] * 9 for _ in range(9)]
        for r in range(9):
            for c in range(9):
                if self.eredeti_board[r][c] != 0:
                    tiszta_board[r][c] = self.eredeti_board[r][c]
                else:
                    e = self.entries[(r, c)]
                    val_str = e.get()
                    if e['state'] == 'disabled' and val_str.isdigit():
                        tiszta_board[r][c] = int(val_str)
                    else:
                        tiszta_board[r][c] = 0
        siker = játék_mentése_hozzáfűzéssel(
            mentés_neve, self.eredeti_board, tiszta_board, self.current_puzzle_index, elapsed, self.score
        )
        if siker:
            messagebox.showinfo("Siker", "Játék elmentve (csak a biztos számokkal).")
>>>>>>> 56a534c (javitva)
        else:
            messagebox.showerror("Hiba", "Hiba történt a mentéskor.")

<<<<<<< HEAD
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
=======
    def manual_entry_mode(self):
        self.timer_running = False
        self.is_manual_mode = True
        self.solution_board = None
        self.scored_cells = set()
        self.error_cells = set()
        self.hint_cells = set()
        self.status_var.set("SZERKESZTŐ MÓD: Írd be a számokat, majd mentsd el.")
        for r in range(9):
            for c in range(9):
                e = self.entries[(r, c)]
                e.config(state="normal")
                e.delete(0, tk.END)
                self.eredeti_board[r][c] = 0
        self.apply_theme()

    def save_manual_puzzle_to_file(self):
        if not self.is_manual_mode:
            messagebox.showwarning("Figyelem", "Először kattints a 'Szerkesztő Mód Indítása' gombra!")
            return
        board = self.get_board_from_gui()
        if üres_mezők_száma(board) == 81:
            messagebox.showwarning("Hiba", "Üres táblát nem érdemes menteni.")
            return
        if not tábla_érvényes(board):
            messagebox.showwarning("Hiba", "A feladvány szabálytalan.")
            return
        try:
            with open(PUZZLE_FAJL, "a") as f:
                f.write("\n# Kézzel felvett feladvány (GUI)\n")
                for sor in board:
                    f.write("".join(str(n) for n in sor) + "\n")
            messagebox.showinfo("Siker", "Feladvány mentve a puzzles.txt fájlba!")
            self.is_manual_mode = False
            self.status_var.set("Feladvány mentve. Válassz új játékot.")
        except OSError:
            messagebox.showerror("Hiba", "Nem sikerült írni a fájlba.")

    def check_solution_with_locks(self):
        if self.is_manual_mode:
            board = self.get_board_from_gui()
            if tábla_érvényes(board):
                messagebox.showinfo("OK", "A tábla szabályosnak tűnik.")
            else:
                messagebox.showerror("Hiba", "Ütközés van a táblán!")
            return
        if self.solution_board is None:
            messagebox.showerror("Hiba", "Nem található a megoldókulcs.")
            return

        current_board = self.get_board_from_gui()
        pont_valtozas = 0
        hibak_szama = 0
        jo_talalatok = 0
        self.error_cells = set()

        for r in range(9):
            for c in range(9):
                if self.eredeti_board[r][c] != 0:
                    continue
                user_val = current_board[r][c]
                if user_val == 0:
                    continue
                correct_val = self.solution_board[r][c]
                if user_val == correct_val:
                    jo_talalatok += 1
                    if (r, c) not in self.scored_cells:
                        pont_valtozas += 10
                        self.scored_cells.add((r, c))
                else:
                    hibak_szama += 1
                    pont_valtozas -= 5
                    self.error_cells.add((r, c))
                    if (r, c) in self.scored_cells:
                        self.scored_cells.remove((r, c))
                    if (r, c) in self.hint_cells:
                        self.hint_cells.remove((r, c))

        self.score += pont_valtozas
        self.status_var.set(f"Ellenőrzés: {jo_talalatok} zárolt, {hibak_szama} hibás. Pont: {self.score}")
        self.apply_theme()

        if hibak_szama == 0 and üres_mező_keresése(current_board) is None:
            messagebox.showinfo("Gratulálok", "A tábla teljesen kész és hibátlan!")
            self.timer_running = False

    def request_hint(self):
        if self.is_manual_mode:
            messagebox.showinfo("Infó", "Szerkesztő módban nem kérhetsz tippet.")
            return
        if self.solution_board is None:
            messagebox.showerror("Hiba", "Nincs megoldókulcs a tipphez.")
            return

        board = self.get_board_from_gui()
        üresek = [
            (r, c)
            for r in range(9)
            for c in range(9)
            if self.eredeti_board[r][c] == 0 and board[r][c] == 0
        ]
        if not üresek:
            messagebox.showinfo("Infó", "Nincs üres mező, amire tippet adhatnék.")
            return

        r, c = random.choice(üresek)
        helyes = self.solution_board[r][c]
        e = self.entries[(r, c)]
        e.config(state="normal")
        e.delete(0, tk.END)
        e.insert(0, str(helyes))

        self.scored_cells.add((r, c))
        self.hint_cells.add((r, c))
        if (r, c) in self.error_cells:
            self.error_cells.remove((r, c))

        self.score -= 20
        self.status_var.set(f"Tipp megadva a(z) ({r+1},{c+1}) mezőre. -20 pont.")
        self.apply_theme()

    def solve_current(self):
        if self.is_manual_mode:
            messagebox.showinfo("Infó", "Szerkesztő módban nincs mit megoldani.")
            return
        if not messagebox.askyesno("Feladás", "Biztosan feladod?"):
            return
        if self.solution_board:
            self.set_board_to_gui(self.solution_board, set_original=False)
            self.timer_running = False
            self.scored_cells = set()
            self.error_cells = set()
            self.hint_cells = set()
            self.status_var.set("Megoldás betöltve.")
        else:
            temp = self.get_board_from_gui()
            if sudoku_megoldása(temp):
                self.set_board_to_gui(temp, set_original=False)
                self.timer_running = False
                self.scored_cells = set()
                self.error_cells = set()
                self.hint_cells = set()
                self.status_var.set("Megoldás betöltve.")
>>>>>>> 56a534c (javitva)

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
<<<<<<< HEAD
    app = SudokuApp(root)
<<<<<<< Updated upstream
=======
=======
    gui = SudokuGUI(root)
>>>>>>> 56a534c (javitva)
>>>>>>> Stashed changes
    root.mainloop()
