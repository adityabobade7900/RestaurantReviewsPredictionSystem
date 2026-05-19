import pymysql
from tkinter import *
import pickle
from tkinter import messagebox
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ═══════════════════════════════════════════════════════════════════
#  DESIGN TOKENS
# ═══════════════════════════════════════════════════════════════════
BG = "#0C0C12"      # near-black base
SURFACE = "#13131C"      # slightly lifted
CARD = "#1B1B27"      # card surfaces
BORDER = "#2A2A3C"      # subtle borders
ACCENT = "#F0A030"      # warm amber / gold  (primary)
ACCENT_H = "#C07820"      # hover state of accent
RED = "#D94545"      # negative / danger
RED_H = "#A83030"
GREEN = "#3EC878"      # positive / success
GREEN_H = "#2A9A58"
TEXT = "#EDE8DF"      # warm off-white
MUTED = "#6A6A82"      # secondary text
ENTRY_BG = "#23232F"      # input field bg
ENTRY_FG = "#F0A030"      # input text color

FT_HERO = ("Georgia",   36, "bold")
FT_H1 = ("Georgia",   18, "bold")
FT_BODY = ("Helvetica", 12)
FT_BTN = ("Helvetica", 12, "bold")
FT_ENTRY = ("Helvetica", 13)
FT_SMALL = ("Helvetica",  9)

foods = [
    "Idly",          "Dosa",            "Vada",            "Roti",
    "Meals",         "Veg Biryani",     "Egg Biryani",     "Chicken Biryani",
    "Mutton Biryani", "Ice Cream",       "Noodles",         "Manchooriya",
    "Orange Juice",  "Apple Juice",     "Pineapple Juice", "Banana Juice",
]

# ═══════════════════════════════════════════════════════════════════
#  WIDGET FACTORIES
# ═══════════════════════════════════════════════════════════════════


def btn(parent, text, cmd=None, kind="primary", padx=24, pady=10, **kw):
    palette = {
        "primary": (ACCENT,  ACCENT_H, BG,   BG),
        "danger":  (RED,     RED_H,    TEXT, TEXT),
        "ghost":   (CARD,    BORDER,   ACCENT, ACCENT),
        "success": (GREEN,   GREEN_H,  BG,   BG),
        "neutral": (SURFACE, BORDER,   TEXT, TEXT),
    }
    bg, abg, fg, afg = palette.get(kind, palette["primary"])
    b = Button(parent, text=text, command=cmd,
               bg=bg, fg=fg,
               activebackground=abg, activeforeground=afg,
               relief="flat", bd=0, cursor="hand2",
               font=FT_BTN, padx=padx, pady=pady, **kw)
    b.bind("<Enter>", lambda e: b.config(bg=abg))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


def lbl(parent, text, size="body", fg=None, bg=None, **kw):
    fonts = {"hero": FT_HERO, "h1": FT_H1,
             "body": FT_BODY, "small": FT_SMALL, "btn": FT_BTN}
    _bg = bg if bg else (parent.cget("bg") if hasattr(parent, "cget") else BG)
    return Label(parent, text=text, fg=fg or TEXT, bg=_bg,
                 font=fonts.get(size, FT_BODY), **kw)


def card(parent, accent_top=True, **kw):
    """Returns (border_frame, inner_frame). Place border_frame in layout."""
    border = Frame(parent, bg=BORDER)
    inner = Frame(border, bg=CARD, **kw)
    if accent_top:
        Frame(inner, bg=ACCENT, height=3).pack(fill=X, side=TOP)
    inner.pack(fill=BOTH, expand=True, padx=1, pady=(0, 1))
    return border, inner


def sep(parent, color=BORDER, height=1, pad_y=(8, 8)):
    f = Frame(parent, bg=color, height=height)
    f.pack(fill=X, pady=pad_y)
    return f


def field(parent, textvariable=None, show=None, width=30):
    e = Entry(parent, textvariable=textvariable,
              bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ACCENT,
              relief="flat", font=FT_ENTRY, width=width,
              highlightthickness=1,
              highlightbackground=BORDER,
              highlightcolor=ACCENT)
    if show:
        e.config(show=show)
    return e


# ═══════════════════════════════════════════════════════════════════
#  GLOBAL STATE
# ═══════════════════════════════════════════════════════════════════
variables = []


# ═══════════════════════════════════════════════════════════════════
#  ESTIMATE / REVIEW LOGIC
# ═══════════════════════════════════════════════════════════════════
def estimate(review_text, result_lbl_widget):
    if not review_text.strip():
        messagebox.showinfo(
            "Empty Review", "Please write a review before submitting.")
        return

    try:
        with open("cvmodel", "rb") as f:
            cv = pickle.load(f)
        with open("lgmodel", "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError as e:
        messagebox.showerror("Model Error", f"Could not load model file:\n{e}")
        return

    arr = cv.transform([review_text.lower()])
    result = model.predict(arr)[0]

    if 'not' in review_text.lower():
        result = abs(result - 1)

    if result == 1:
        result_lbl_widget.config(text="✅  Positive Review", fg=GREEN)
    else:
        result_lbl_widget.config(text="❌  Negative Review", fg=RED)

    selected = [foods[i] for i in range(len(foods)) if variables[i].get() == 1]
    if not selected:
        return

    try:
        conn = pymysql.connect(user="root", password="root@7900",
                               host="localhost", database="rest_review_db")
        mycur = conn.cursor()
        mycur.execute("SELECT * FROM reviews_table")
        rows = mycur.fetchall()

        for row in rows:
            food_name, good, bad, count = row[0], row[1], row[2], row[3]
            if food_name in selected:
                count += 1
                good = good + 1 if result == 1 else good
                bad = bad + 1 if result == 0 else bad
                mycur.execute(
                    "UPDATE reviews_table "
                    "SET good_review=%s, bad_review=%s, customer=%s "
                    "WHERE food=%s",
                    (good, bad, count, food_name)
                )
        conn.commit()
        mycur.close()
        conn.close()
    except Exception as ex:
        messagebox.showerror("Database Error", str(ex))


# ═══════════════════════════════════════════════════════════════════
#  TAKE REVIEW WINDOW
# ═══════════════════════════════════════════════════════════════════
def take_review():
    global variables

    w = Toplevel()
    w.geometry("1200x760")
    w.configure(bg=BG)
    w.title("Restaurant Review — Submit Review")
    w.resizable(False, False)

    # ── Header ──────────────────────────────────────────────────────
    hdr = Frame(w, bg=SURFACE)
    hdr.pack(fill=X)
    Frame(hdr, bg=ACCENT, height=4).pack(fill=X, side=TOP)
    lbl(hdr, "🍽  RESTAURANT REVIEW ANALYSIS SYSTEM",
        size="hero", bg=SURFACE).pack(pady=(20, 4))
    lbl(hdr, "Tell us about your experience today",
        size="body", fg=MUTED, bg=SURFACE).pack(pady=(0, 18))

    # ── Body ────────────────────────────────────────────────────────
    body = Frame(w, bg=BG, padx=36, pady=28)
    body.pack(fill=BOTH, expand=True)
    body.columnconfigure(0, weight=1)
    body.columnconfigure(1, weight=1)
    body.rowconfigure(0, weight=1)

    # ── LEFT: Food checkboxes ──
    lb, lf = card(body, padx=24, pady=20)
    lb.grid(row=0, column=0, sticky="nsew", padx=(0, 14), pady=4)

    lbl(lf, "Select Items You Ordered", size="h1").pack(
        anchor="w", pady=(10, 16))
    sep(lf)

    grid_frame = Frame(lf, bg=CARD)
    grid_frame.pack(fill=X, padx=4, pady=4)

    variables = []
    for i, food in enumerate(foods):
        var = IntVar()
        variables.append(var)
        r, c = divmod(i, 4)
        Checkbutton(
            grid_frame, text=food, variable=var,
            bg=CARD, fg=TEXT, selectcolor=SURFACE,
            activebackground=CARD, activeforeground=ACCENT,
            font=("Helvetica", 11), cursor="hand2",
            highlightthickness=0
        ).grid(row=r, column=c, sticky="w", padx=10, pady=7)

    # ── RIGHT: Review input ──
    rb, rf = card(body, padx=24, pady=20)
    rb.grid(row=0, column=1, sticky="nsew", padx=(14, 0), pady=4)

    lbl(rf, "Write Your Review", size="h1").pack(anchor="w", pady=(10, 6))
    lbl(rf, "Tip: Use 'not' instead of \"n't\"  (e.g. was not good)",
        size="small", fg=MUTED).pack(anchor="w")
    sep(rf)

    rev_var = StringVar()
    rev_entry = field(rf, textvariable=rev_var, width=46)
    rev_entry.pack(fill=X, ipady=9, pady=(4, 28))

    result_display = Label(
        rf, text="——  Awaiting submission  ——",
        bg=CARD, fg=MUTED,
        font=("Georgia", 15, "italic"), pady=14
    )
    result_display.pack()

    sep(rf, pad_y=(16, 16))

    btn(rf, "  ✔  Submit Review  ",
        cmd=lambda: estimate(rev_var.get(), result_display),
        kind="primary", padx=36, pady=14).pack()
    btn(rf, "← Back to Home", cmd=w.destroy,
        kind="ghost", padx=16, pady=8).pack(pady=(14, 0))


# ═══════════════════════════════════════════════════════════════════
#  OWNER DASHBOARD
# ═══════════════════════════════════════════════════════════════════
def open_dashboard():
    dash = Toplevel()
    dash.state('zoomed')
    dash.configure(bg=BG)
    dash.title("Restaurant Review — Owner Dashboard")

    chart_refs = {"canvas": None, "label": None}

    # ── Header ──────────────────────────────────────────────────────
    hdr = Frame(dash, bg=SURFACE)
    hdr.pack(fill=X)
    Frame(hdr, bg=ACCENT, height=4).pack(fill=X, side=TOP)
    lbl(hdr, "📊  OWNER DASHBOARD", size="hero", bg=SURFACE).pack(pady=(18, 4))
    lbl(hdr, "Real-time review analytics at a glance",
        size="body", fg=MUTED, bg=SURFACE).pack(pady=(0, 16))

    # ── Body ────────────────────────────────────────────────────────
    body = Frame(dash, bg=BG, padx=28, pady=22)
    body.pack(fill=BOTH, expand=True)
    body.columnconfigure(0, weight=1, minsize=520)
    body.columnconfigure(1, weight=1, minsize=620)
    body.rowconfigure(0, weight=1)

    # ── LEFT: Chart panel ──
    lb, lf = card(body, padx=18, pady=18)
    lb.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

    lbl(lf, "Review Percentage Chart", size="h1").pack(anchor="w", pady=(8, 14))

    ctrl = Frame(lf, bg=CARD)
    ctrl.pack(fill=X, pady=(0, 10))
    lbl(ctrl, "Select Food :", fg=MUTED, bg=CARD).pack(side=LEFT, padx=(0, 10))

    s = ttk.Style()
    s.theme_use("clam")
    s.configure("R.TCombobox",
                fieldbackground=ENTRY_BG, background=ENTRY_BG,
                foreground=TEXT, selectbackground=BORDER,
                bordercolor=BORDER, arrowcolor=ACCENT,
                padding=6)

    n_var = StringVar()
    food_cb = ttk.Combobox(ctrl, textvariable=n_var, state="readonly",
                           values=foods, width=24, style="R.TCombobox")
    food_cb.current(0)
    food_cb.pack(side=LEFT, ipady=4)

    chart_area = Frame(lf, bg=CARD, height=300)
    chart_area.pack(fill=BOTH, expand=True)

    def plot_chart(data_list):
        if chart_refs["canvas"]:
            chart_refs["canvas"].get_tk_widget().destroy()
            chart_refs["canvas"] = None
        if chart_refs["label"]:
            chart_refs["label"].destroy()
            chart_refs["label"] = None

        if sum(data_list) == 0:
            nl = lbl(chart_area, "No reviews recorded yet.",
                     fg=MUTED, bg=CARD, size="h1")
            nl.place(relx=0.5, rely=0.5, anchor="center")
            chart_refs["label"] = nl
            return

        fig = Figure(figsize=(5, 3.4), dpi=96, facecolor=CARD)
        ax = fig.add_subplot(111)
        ax.set_facecolor(CARD)
        ax.pie(data_list,
               labels=["Positive", "Negative"],
               autopct="%0.1f%%",
               shadow=False,
               explode=[0.06, 0.06],
               colors=[GREEN, RED],
               textprops={"color": TEXT, "fontsize": 11})
        fig.tight_layout()

        c = FigureCanvasTkAgg(fig, master=chart_area)
        c.draw()
        c.get_tk_widget().pack(fill=BOTH, expand=True)
        chart_refs["canvas"] = c

    def get_percentages():
        try:
            conn = pymysql.connect(user="root", password="root@7900",
                                   host="localhost", database="rest_review_db")
            mycur = conn.cursor()
            mycur.execute("SELECT * FROM reviews_table")
            rows = mycur.fetchall()
            mycur.close()
            conn.close()
            out = {}
            for row in rows:
                t = row[3]
                out[row[0]] = (
                    round((row[1] / t) * 100, 1) if t else 0,
                    round((row[2] / t) * 100, 1) if t else 0,
                )
            return out
        except Exception as ex:
            messagebox.showerror("Database Error", str(ex))
            return {}

    def per_show():
        data = get_percentages()
        food = food_cb.get()
        if food in data:
            plot_chart(list(data[food]))

    def clear_chart():
        if chart_refs["canvas"]:
            chart_refs["canvas"].get_tk_widget().destroy()
            chart_refs["canvas"] = None
        if chart_refs["label"]:
            chart_refs["label"].destroy()
            chart_refs["label"] = None

    sep(lf, pad_y=(10, 10))
    btn_row = Frame(lf, bg=CARD)
    btn_row.pack()
    btn(btn_row, "Show Chart",  cmd=per_show,    kind="primary",
        padx=20, pady=8).pack(side=LEFT, padx=6)
    btn(btn_row, "Clear Chart", cmd=clear_chart, kind="ghost",
        padx=20, pady=8).pack(side=LEFT, padx=6)

    # ── RIGHT: Table panel ──
    rb, rf = card(body, padx=18, pady=18)
    rb.grid(row=0, column=1, sticky="nsew", padx=(14, 0))

    lbl(rf, "Review Count Table", size="h1").pack(anchor="w", pady=(8, 14))

    ts = ttk.Style()
    ts.configure("Dark.Treeview",
                 background=SURFACE, foreground=TEXT,
                 fieldbackground=SURFACE,
                 bordercolor=BORDER, rowheight=30,
                 font=("Helvetica", 11))
    ts.configure("Dark.Treeview.Heading",
                 background=CARD, foreground=ACCENT,
                 font=("Helvetica", 11, "bold"),
                 bordercolor=BORDER, relief="flat")
    ts.map("Dark.Treeview",
           background=[("selected", BORDER)],
           foreground=[("selected", ACCENT)])

    cols = ("food", "good", "bad", "total")
    treev = ttk.Treeview(rf, columns=cols, show="headings",
                         height=20, style="Dark.Treeview")
    treev.heading("food",  text="Food Item")
    treev.heading("good",  text="✅  Positive")
    treev.heading("bad",   text="❌  Negative")
    treev.heading("total", text="👤  Customers")

    treev.column("food",  width=170, anchor="w")
    treev.column("good",  width=110, anchor="center")
    treev.column("bad",   width=110, anchor="center")
    treev.column("total", width=120, anchor="center")

    vsb = ttk.Scrollbar(rf, orient="vertical", command=treev.yview)
    treev.configure(yscrollcommand=vsb.set)
    treev.pack(side=LEFT, fill=BOTH, expand=True)
    vsb.pack(side=RIGHT, fill=Y)

    def load_table():
        treev.delete(*treev.get_children())
        try:
            conn = pymysql.connect(user="root", password="root@7900",
                                   host="localhost", database="rest_review_db")
            mycur = conn.cursor()
            mycur.execute("SELECT * FROM reviews_table")
            for row in mycur.fetchall():
                treev.insert("", "end", values=row)
            mycur.close()
            conn.close()
        except Exception as ex:
            messagebox.showerror("Database Error", str(ex))

    def clear_table():
        treev.delete(*treev.get_children())

    sep(rf, pad_y=(10, 10))
    tbl_btns = Frame(rf, bg=CARD)
    tbl_btns.pack()
    btn(tbl_btns, "Load Table",       cmd=load_table,
        kind="primary", padx=18, pady=8).pack(side=LEFT, padx=6)
    btn(tbl_btns, "Clear Table",      cmd=clear_table,
        kind="ghost",   padx=18, pady=8).pack(side=LEFT, padx=6)
    btn(tbl_btns, "Close Dashboard",  cmd=dash.destroy,
        kind="danger",  padx=18, pady=8).pack(side=LEFT, padx=6)


# ═══════════════════════════════════════════════════════════════════
#  LOGIN HANDLER
# ═══════════════════════════════════════════════════════════════════
def login():
    user = a1.get()
    pwd = a2.get()
    a1.set("")
    a2.set("")
    if user == "Aditya" and pwd == "7900":
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")


# ═══════════════════════════════════════════════════════════════════
#  WELCOME / ROOT WINDOW
# ═══════════════════════════════════════════════════════════════════
root1 = Tk()
root1.state('zoomed')
root1.configure(bg=BG)
root1.title("Restaurant Review Analysis System")

# ── Header ──────────────────────────────────────────────────────────
hdr = Frame(root1, bg=SURFACE)
hdr.pack(fill=X)
Frame(hdr, bg=ACCENT, height=4).pack(fill=X, side=TOP)
lbl(hdr, "🍽  RESTAURANT REVIEW ANALYSIS SYSTEM",
    size="hero", bg=SURFACE).pack(pady=(24, 6))
lbl(hdr, "Your feedback fuels our kitchen",
    size="body", fg=MUTED, bg=SURFACE).pack(pady=(0, 20))

# ── Main content: two cards side by side ────────────────────────────
content = Frame(root1, bg=BG, padx=60, pady=40)
content.pack(fill=BOTH, expand=True)
content.columnconfigure(0, weight=1)
content.columnconfigure(1, weight=1)
content.rowconfigure(0, weight=1)

# ─ Customer Card ─────────────────────────────────────────────────
cb_, cf = card(content, padx=32, pady=28)
cb_.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

lbl(cf, "🧑  Customer", size="h1").pack(pady=(14, 8))
sep(cf)
lbl(cf, "Tried something today?", fg=MUTED).pack(pady=6)
lbl(cf,
    "Select your items and share what you\n"
    "thought. Your voice shapes what we serve.",
    fg=MUTED, justify="center").pack(pady=(0, 22))
btn(cf, "  Write a Review  ", cmd=take_review,
    kind="primary", padx=36, pady=14).pack(pady=(10, 18))

# ─ Owner Card ────────────────────────────────────────────────────
ob_, of = card(content, padx=32, pady=28)
ob_.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

lbl(of, "🔒  Owner Login", size="h1").pack(pady=(14, 8))
sep(of)

a1 = StringVar()
a2 = StringVar()

u_wrap = Frame(of, bg=CARD)
u_wrap.pack(fill=X, pady=(10, 6))
lbl(u_wrap, "Username", fg=MUTED, bg=CARD).pack(anchor="w", pady=(0, 4))
field(u_wrap, textvariable=a1, width=28).pack(fill=X, ipady=7)

p_wrap = Frame(of, bg=CARD)
p_wrap.pack(fill=X, pady=6)
lbl(p_wrap, "Password", fg=MUTED, bg=CARD).pack(anchor="w", pady=(0, 4))
field(p_wrap, textvariable=a2, show="*", width=28).pack(fill=X, ipady=7)

btn(of, "  Login to Dashboard  ", cmd=login,
    kind="primary", padx=30, pady=14).pack(pady=(22, 10))

# ── Footer ──────────────────────────────────────────────────────────
footer = Frame(root1, bg=SURFACE, pady=10)
footer.pack(fill=X, side=BOTTOM)
Frame(footer, bg=BORDER, height=1).pack(fill=X, side=TOP)
lbl(footer, "Restaurant Review Analysis System  ·  All rights reserved",
    size="small", fg=MUTED, bg=SURFACE).pack(pady=4)

root1.mainloop()
