import json
import os
import tkinter as tk
from datetime import date
from tkinter import font as tkfont, messagebox, ttk

# PRE//BOARD — Class XII syllabus tracker
EXAM_DATE = date(2026, 11, 16)
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "preboard_progress.json")

SYLLABUS = {
    "English Core": [
        "The Last Lesson", "Lost Spring", "Deep Water", "The Rattrap",
        "Indigo", "Poets and Pancakes", "The Interview", "Going Places",
        "My Mother at Sixty-Six", "Keeping Quiet", "A Thing of Beauty",
        "A Roadside Stand", "Aunt Jennifer's Tigers", "The Third Level",
        "The Tiger King", "Journey to the End of the Earth", "The Enemy",
        "On the Face of It", "Memories of Childhood", "Reading Comprehension",
        "Notice Writing", "Invitations and Replies",
        "Letters: Editor / Job Application", "Article and Report Writing"
    ],
    "Physics": [
        "Electric Charges and Fields", "Electrostatic Potential and Capacitance",
        "Current Electricity", "Moving Charges and Magnetism",
        "Magnetism and Matter", "Electromagnetic Induction",
        "Alternating Current", "Electromagnetic Waves",
        "Ray Optics and Optical Instruments", "Wave Optics",
        "Dual Nature of Radiation and Matter", "Atoms", "Nuclei",
        "Semiconductor Electronics"
    ],
    "Chemistry": [
        "Solutions", "Electrochemistry", "Chemical Kinetics",
        "The d- and f-Block Elements", "Coordination Compounds",
        "Haloalkanes and Haloarenes", "Alcohols, Phenols and Ethers",
        "Aldehydes, Ketones and Carboxylic Acids", "Amines", "Biomolecules"
    ],
    "Mathematics": [
        "Relations and Functions", "Inverse Trigonometric Functions",
        "Matrices", "Determinants", "Continuity and Differentiability",
        "Applications of Derivatives", "Integrals", "Applications of Integrals",
        "Differential Equations", "Vector Algebra",
        "Three-Dimensional Geometry", "Linear Programming", "Probability"
    ],
    "Computer Science": [
        "Python Revision", "Functions", "Exception Handling",
        "Text File Handling", "Binary File Handling", "CSV File Handling",
        "Stack Data Structure", "Computer Networks",
        "Network Devices, Protocols and Web Services", "Database Concepts",
        "SQL Queries and Functions", "Python-SQL Connectivity"
    ],
}

SHORT = {
    "ENG": "English Core", "PHY": "Physics", "CHEM": "Chemistry",
    "MATH": "Mathematics", "CS": "Computer Science"
}

# Minimal black + green palette
BG = "#0a0a0a"
PANEL = "#111411"
ROW = "#0d0f0d"
HOVER = "#152015"
LINE = "#1e2b1e"
TEXT = "#d7e6d9"
DIM = "#718273"
GREEN = "#39d96b"
DARK_GREEN = "#1a7a36"

def load_progress():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, ValueError):
        return {}
    if not isinstance(raw, dict):
        return {}
    clean = {}
    for subject, chapters in raw.items():
        if isinstance(chapters, dict):
            clean[subject] = {chapter: bool(value)
                              for chapter, value in chapters.items()}
    return clean

progress = load_progress()
autosave_enabled = True
save_job = None
has_unsaved_changes = False

def is_done(subject, chapter):
    return bool(progress.get(subject, {}).get(chapter, False))

def stats(subject):
    chapters = SYLLABUS[subject]
    done = sum(is_done(subject, c) for c in chapters)
    return done, len(chapters), round(done * 100 / len(chapters)) if chapters else 0

def totals():
    done = sum(stats(s)[0] for s in SYLLABUS)
    total = sum(len(chapters) for chapters in SYLLABUS.values())
    return done, total, round(done * 100 / total) if total else 0

def block_bar(pct, width=18):
    filled = round(pct / 100 * width)
    return "█" * filled + "░" * (width - filled)

def save_now(show_status=True):
    global save_job, has_unsaved_changes
    if save_job is not None:
        try:
            root.after_cancel(save_job)
        except tk.TclError:
            pass
        save_job = None
    try:
        temp = DATA_FILE + ".tmp"
        with open(temp, "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)
        os.replace(temp, DATA_FILE)
        has_unsaved_changes = False
        if show_status:
            status_var.set("// saved")
    except OSError as exc:
        status_var.set("// SAVE FAILED")
        messagebox.showerror("Save error", f"Progress could not be saved:\n{exc}")

def schedule_save():
    global save_job, has_unsaved_changes
    has_unsaved_changes = True
    if autosave_enabled:
        status_var.set("// saving…")
        if save_job is not None:
            try:
                root.after_cancel(save_job)
            except tk.TclError:
                pass
        save_job = root.after(300, save_now)
    else:
        status_var.set("// unsaved changes — click SAVE NOW")

def update_stats():
    done, total, pct = totals()
    total_pct.config(text=f"{pct:02d}%")
    total_bar.config(text=block_bar(pct, 38))
    total_detail.config(text=f"{done:02d} / {total:02d} tasks complete")

    for subject, widgets in cards.items():
        count_done, count_total, percent = stats(subject)
        widgets[0].config(text=block_bar(percent, 12), fg=GREEN)
        widgets[1].config(text=f"{count_done:02d}/{count_total:02d} · {percent}%")

    days = (EXAM_DATE - date.today()).days
    if days > 1:
        countdown.config(text=f"{days:02d} DAYS")
    elif days == 1:
        countdown.config(text="01 DAY")
    elif days == 0:
        countdown.config(text="EXAM DAY")
    else:
        countdown.config(text="EXAM PASSED")

    for subject, label in section_labels.items():
        d, t, p = stats(subject)
        label.config(text=f"{subject.upper()}  [{d}/{t} · {p}%]")

def style_row(subject, chapter, hover=False):
    frame, box, name = rows[(subject, chapter)]
    done = is_done(subject, chapter)
    bg = HOVER if hover else ROW
    box.config(text="[x]" if done else "[ ]",
               fg=GREEN if done else DIM, bg=bg)
    name.config(fg=DIM if done else TEXT, bg=bg,
                font=F_STRIKE if done else F_BODY)
    frame.config(bg=bg)

def refresh_list(reset_scroll=False):
    for widget in list_frame.winfo_children():
        widget.pack_forget()

    selected = state["subject"]
    status = state["status"]
    visible_subjects = list(SYLLABUS)
    if selected:
        visible_subjects = [selected]

    for subject in visible_subjects:
        shown = [chapter for chapter in SYLLABUS[subject]
                 if status == "ALL"
                 or (status == "TODO" and not is_done(subject, chapter))
                 or (status == "DONE" and is_done(subject, chapter))]
        if not shown:
            continue

        section = sections[subject]
        section.pack(fill="x", pady=(0, 9))
        section_labels[subject].pack(side="left")

        # Keep each chapter row in its section and show only filtered rows.
        for chapter in SYLLABUS[subject]:
            frame, _, _ = rows[(subject, chapter)]
            if chapter in shown:
                frame.pack(fill="x", padx=7, pady=2)
            else:
                frame.pack_forget()

    if not any(
        (state["status"] == "ALL"
         or (state["status"] == "TODO" and not is_done(s, c))
         or (state["status"] == "DONE" and is_done(s, c)))
        for s in visible_subjects for c in SYLLABUS[s]
    ):
        empty_label.pack(fill="x", pady=24)
    else:
        empty_label.pack_forget()

    if reset_scroll:
        canvas.yview_moveto(0)
    list_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def toggle(subject, chapter):
    progress.setdefault(subject, {})[chapter] = not is_done(subject, chapter)
    style_row(subject, chapter, hover=True)
    update_stats()
    schedule_save()
    if state["status"] != "ALL":
        refresh_list()

def pick_subject(key):
    state["subject"] = SHORT.get(key)
    for chip, label in subject_chips.items():
        label.config(bg=GREEN if chip == key else PANEL,
                     fg=BG if chip == key else DIM)
    refresh_list(reset_scroll=True)

def pick_status(key):
    state["status"] = key
    for chip, label in status_chips.items():
        label.config(bg=GREEN if chip == key else PANEL,
                     fg=BG if chip == key else DIM)
    refresh_list(reset_scroll=True)

def make_chips(parent, options, callback, current):
    chips = {}
    for key in options:
        label = tk.Label(parent, text=key, font=F_BOLD, padx=9, pady=5,
                         bg=GREEN if key == current else PANEL,
                         fg=BG if key == current else DIM, cursor="hand2")
        label.pack(side="left", padx=(0, 4))
        label.bind("<Button-1>", lambda _e, k=key: callback(k))
        chips[key] = label
    return chips

def toggle_autosave():
    global autosave_enabled, save_job
    autosave_enabled = bool(autosave_var.get())
    if autosave_enabled:
        if has_unsaved_changes:
            save_now()
        else:
            status_var.set("// auto-save ON")
    else:
        if save_job is not None:
            try:
                root.after_cancel(save_job)
            except tk.TclError:
                pass
            # Pending unsaved edits must not be lost when disabling auto-save.
            save_job = None
        status_var.set("// auto-save OFF — use SAVE NOW")

def reset_progress():
    if not messagebox.askyesno(
        "Wipe everything?",
        "This clears every checkmark in all five subjects.\n\nContinue?"
    ):
        return
    progress.clear()
    update_stats()
    for subject, chapter in rows:
        style_row(subject, chapter)
    schedule_save()
    refresh_list(reset_scroll=True)

def close_app():
    global save_job
    if save_job is not None:
        try:
            root.after_cancel(save_job)
        except tk.TclError:
            pass
        save_job = None
    if has_unsaved_changes:
        choice = messagebox.askyesnocancel(
            "Unsaved progress",
            "You have unsaved changes.\n\n"
            "Yes = Save and close\nNo = Discard changes\nCancel = Keep app open"
        )
        if choice is None:
            return
        if choice:
            save_now(show_status=False)
    root.destroy()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("PRE//BOARD")
root.geometry("960x780")
root.minsize(760, 620)
root.configure(bg=BG)

families = set(tkfont.families())
MONO = next((f for f in ("JetBrains Mono", "Consolas", "Menlo",
                         "DejaVu Sans Mono", "Courier New") if f in families),
            "Courier")
F_BODY = (MONO, 10)
F_SMALL = (MONO, 9)
F_BOLD = (MONO, 9, "bold")
F_STRIKE = tkfont.Font(family=MONO, size=10, overstrike=True)

style = ttk.Style()
style.theme_use("clam")
style.configure("Vertical.TScrollbar", background=LINE, troughcolor=BG,
                bordercolor=BG, arrowcolor=DIM, lightcolor=LINE,
                darkcolor=LINE)
style.map("Vertical.TScrollbar", background=[("active", DARK_GREEN)])

PAD = 20

head = tk.Frame(root, bg=BG)
head.pack(fill="x", padx=PAD, pady=(18, 8))
left = tk.Frame(head, bg=BG)
left.pack(side="left")
tk.Label(left, text="PRE//BOARD", font=(MONO, 26, "bold"),
         fg=GREEN, bg=BG).pack(anchor="w")
tk.Label(left, text="class xii · cbse · 5 subjects · one target",
         font=F_SMALL, fg=DIM, bg=BG).pack(anchor="w")

right = tk.Frame(head, bg=BG)
right.pack(side="right")
countdown = tk.Label(right, text="", font=(MONO, 24, "bold"),
                     fg=TEXT, bg=BG)
countdown.pack(anchor="e")
tk.Label(right, text=f"exam · {EXAM_DATE.strftime('%d %b %Y').upper()}",
         font=F_SMALL, fg=DIM, bg=BG).pack(anchor="e")

stripe = tk.Canvas(root, height=4, bg=BG, highlightthickness=0)
stripe.pack(fill="x", padx=PAD, pady=(0, 12))
def draw_stripe(event):
    stripe.delete("all")
    stripe.create_rectangle(0, 0, event.width, 4, fill=LINE, outline=LINE)
    stripe.create_rectangle(0, 0, event.width * totals()[2] / 100, 4,
                            fill=GREEN, outline=GREEN)
stripe.bind("<Configure>", draw_stripe)

total_panel = tk.Frame(root, bg=PANEL, highlightbackground=LINE,
                       highlightthickness=1, padx=14, pady=10)
total_panel.pack(fill="x", padx=PAD)
t_top = tk.Frame(total_panel, bg=PANEL)
t_top.pack(fill="x")
tk.Label(t_top, text="TOTAL PROGRESS", font=F_BOLD, fg=DIM,
         bg=PANEL).pack(side="left")
total_pct = tk.Label(t_top, text="00%", font=(MONO, 20, "bold"),
                     fg=GREEN, bg=PANEL)
total_pct.pack(side="right")
total_bar = tk.Label(total_panel, text="", font=(MONO, 12),
                     fg=GREEN, bg=PANEL, anchor="w")
total_bar.pack(fill="x")
total_detail = tk.Label(total_panel, text="", font=F_SMALL, fg=DIM,
                        bg=PANEL, anchor="w")
total_detail.pack(fill="x")

cards_frame = tk.Frame(root, bg=BG)
cards_frame.pack(fill="x", padx=PAD, pady=(8, 0))
cards = {}
for i, subject in enumerate(SYLLABUS):
    cards_frame.grid_columnconfigure(i, weight=1, uniform="c")
    card = tk.Frame(cards_frame, bg=PANEL, highlightbackground=LINE,
                    highlightthickness=1, padx=7, pady=7)
    card.grid(row=0, column=i, sticky="nsew",
              padx=(0 if i == 0 else 3, 0 if i == len(SYLLABUS) - 1 else 3))
    tk.Label(card, text=subject.upper(), font=(MONO, 8, "bold"),
             fg=TEXT, bg=PANEL, anchor="w").pack(fill="x")
    bar = tk.Label(card, text="", font=(MONO, 8), fg=GREEN,
                   bg=PANEL, anchor="w")
    bar.pack(fill="x")
    count = tk.Label(card, text="", font=(MONO, 8), fg=DIM,
                     bg=PANEL, anchor="w")
    count.pack(fill="x")
    cards[subject] = (bar, count)

toolbar = tk.Frame(root, bg=BG)
toolbar.pack(fill="x", padx=PAD, pady=(12, 6))
tk.Label(toolbar, text="SUBJECT", font=F_BOLD, fg=DIM, bg=BG).pack(
    side="left", padx=(0, 8))
state = {"subject": None, "status": "ALL"}
subject_chips = make_chips(toolbar, ["ALL"] + list(SHORT), pick_subject, "ALL")
tk.Frame(toolbar, bg=LINE, width=1, height=22).pack(side="left", padx=10)
tk.Label(toolbar, text="STATUS", font=F_BOLD, fg=DIM, bg=BG).pack(
    side="left", padx=(0, 8))
status_chips = make_chips(toolbar, ["ALL", "TODO", "DONE"], pick_status, "ALL")

footer = tk.Frame(root, bg=BG)
footer.pack(side="bottom", fill="x", padx=PAD, pady=(6, 12))
status_var = tk.StringVar(value="// loaded")
tk.Label(footer, textvariable=status_var, font=F_SMALL, fg=DIM,
         bg=BG).pack(side="left")

autosave_var = tk.BooleanVar(value=True)
tk.Checkbutton(
    footer, text="AUTO-SAVE", variable=autosave_var, command=toggle_autosave,
    bg=BG, fg=TEXT, activebackground=BG, activeforeground=GREEN,
    selectcolor=PANEL, font=F_BOLD, bd=0, highlightthickness=0
).pack(side="right", padx=(8, 0))

save_btn = tk.Label(footer, text="[ SAVE NOW ]", font=F_BOLD,
                    fg=GREEN, bg=BG, cursor="hand2", padx=7)
save_btn.pack(side="right")
save_btn.bind("<Button-1>", lambda _e: save_now())

reset_btn = tk.Label(footer, text="[ WIPE ALL ]", font=F_BOLD,
                     fg=DIM, bg=BG, cursor="hand2", padx=7)
reset_btn.pack(side="right")
reset_btn.bind("<Button-1>", lambda _e: reset_progress())
reset_btn.bind("<Enter>", lambda _e: reset_btn.config(fg="#ff6666"))
reset_btn.bind("<Leave>", lambda _e: reset_btn.config(fg=DIM))

shell = tk.Frame(root, bg=BG)
shell.pack(fill="both", expand=True, padx=PAD, pady=(4, 0))
canvas = tk.Canvas(shell, bg=BG, highlightthickness=0, bd=0,
                   yscrollincrement=20)
scroll = ttk.Scrollbar(shell, orient="vertical", command=canvas.yview)
list_frame = tk.Frame(canvas, bg=BG)
list_frame.grid_columnconfigure(0, weight=1)
win = canvas.create_window((0, 0), window=list_frame, anchor="nw")
list_frame.bind("<Configure>",
                lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind("<Configure>", lambda e: canvas.itemconfigure(win, width=e.width))
canvas.configure(yscrollcommand=scroll.set)
canvas.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

def on_wheel(event):
    if getattr(event, "num", None) == 4:
        step = -2
    elif getattr(event, "num", None) == 5:
        step = 2
    else:
        step = -2 if event.delta > 0 else 2
    canvas.yview_scroll(step, "units")
for event_name in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
    canvas.bind_all(event_name, on_wheel)

sections = {}
section_labels = {}
rows = {}
for subject in SYLLABUS:
    section = tk.Frame(list_frame, bg=PANEL, highlightbackground=LINE,
                       highlightthickness=1, padx=10, pady=8)
    sections[subject] = section
    header = tk.Frame(section, bg=PANEL)
    header.pack(fill="x", pady=(0, 5))
    section_labels[subject] = tk.Label(
        header, text=subject.upper(), font=F_BOLD, fg=GREEN,
        bg=PANEL, anchor="w"
    )
    # The header label is packed by refresh_list so section headers remain visible.
    for chapter in SYLLABUS[subject]:
        row = tk.Frame(section, bg=ROW, padx=7, pady=5)
        box = tk.Label(row, text="[ ]", font=F_BOLD, fg=DIM, bg=ROW,
                       cursor="hand2", width=4)
        box.pack(side="left")
        name = tk.Label(row, text=chapter, font=F_BODY, fg=TEXT, bg=ROW,
                        anchor="w", justify="left", wraplength=700, cursor="hand2")
        name.pack(side="left", fill="x", expand=True)
        rows[(subject, chapter)] = (row, box, name)
        for widget in (row, box, name):
            widget.bind("<Button-1>",
                        lambda _e, s=subject, c=chapter: toggle(s, c))
            widget.bind("<Enter>",
                        lambda _e, s=subject, c=chapter: style_row(s, c, True))
            widget.bind("<Leave>",
                        lambda _e, s=subject, c=chapter: style_row(s, c, False))

empty_label = tk.Label(list_frame, text="No chapters in this filter.",
                       font=F_BODY, fg=DIM, bg=BG)

def refresh_list(reset_scroll=False):
    for subject, section in sections.items():
        section.pack_forget()
        for chapter in SYLLABUS[subject]:
            rows[(subject, chapter)][0].pack_forget()

    selected = state["subject"]
    status = state["status"]
    visible_subjects = [selected] if selected else list(SYLLABUS)
    visible_total = 0

    for subject in visible_subjects:
        shown = [c for c in SYLLABUS[subject]
                 if status == "ALL"
                 or (status == "TODO" and not is_done(subject, c))
                 or (status == "DONE" and is_done(subject, c))]
        if not shown:
            continue
        section = sections[subject]
        section.pack(fill="x", pady=(0, 9))
        section_labels[subject].pack(side="left")
        done, total, pct = stats(subject)
        section_labels[subject].config(
            text=f"{subject.upper()}  [{done}/{total} · {pct}%]")
        for chapter in shown:
            rows[(subject, chapter)][0].pack(fill="x", padx=7, pady=2)
            style_row(subject, chapter)
            visible_total += 1

    if visible_total:
        empty_label.pack_forget()
    else:
        empty_label.pack(fill="x", pady=24)
    if reset_scroll:
        canvas.yview_moveto(0)
    list_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def toggle(subject, chapter):
    progress.setdefault(subject, {})[chapter] = not is_done(subject, chapter)
    style_row(subject, chapter, hover=True)
    update_stats()
    schedule_save()
    if state["status"] != "ALL":
        refresh_list()

def update_stats():
    done, total, pct = totals()
    total_pct.config(text=f"{pct:02d}%")
    total_bar.config(text=block_bar(pct, 38))
    total_detail.config(text=f"{done:02d} / {total:02d} tasks complete")
    for subject, widgets in cards.items():
        count_done, count_total, percent = stats(subject)
        widgets[0].config(text=block_bar(percent, 12), fg=GREEN)
        widgets[1].config(text=f"{count_done:02d}/{count_total:02d} · {percent}%")
    days = (EXAM_DATE - date.today()).days
    countdown.config(text=f"{days:02d} DAYS" if days > 1 else
                     "01 DAY" if days == 1 else
                     "EXAM DAY" if days == 0 else "EXAM PASSED")
    for subject, label in section_labels.items():
        d, t, p = stats(subject)
        label.config(text=f"{subject.upper()}  [{d}/{t} · {p}%]")

# Initial render
update_stats()
refresh_list()
root.protocol("WM_DELETE_WINDOW", close_app)
root.mainloop()
