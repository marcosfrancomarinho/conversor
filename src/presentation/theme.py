from tkinter import ttk


ACCENT = "#2563EB"
ACCENT_ACTIVE = "#1D4ED8"
SUCCESS = "#15803D"
TEXT = "#0F172A"
MUTED = "#64748B"
SURFACE = "#FFFFFF"
SURFACE_ALT = "#F8FAFC"
BORDER = "#CBD5E1"


def configure_theme(style: ttk.Style) -> None:
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(".", font=("Segoe UI", 10))
    style.configure("App.TFrame", background=SURFACE_ALT)
    style.configure("Card.TFrame", background=SURFACE)

    style.configure(
        "Title.TLabel",
        background=SURFACE_ALT,
        foreground=TEXT,
        font=("Segoe UI Semibold", 20),
    )
    style.configure(
        "Subtitle.TLabel",
        background=SURFACE_ALT,
        foreground=MUTED,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Section.TLabel",
        foreground=TEXT,
        font=("Segoe UI Semibold", 10),
    )
    style.configure(
        "Muted.TLabel",
        foreground=MUTED,
        font=("Segoe UI", 9),
    )
    style.configure(
        "Status.TLabel",
        background=SURFACE_ALT,
        foreground=MUTED,
        font=("Segoe UI", 9),
    )
    style.configure(
        "Success.TLabel",
        background=SURFACE_ALT,
        foreground=SUCCESS,
        font=("Segoe UI Semibold", 9),
    )

    style.configure("TButton", padding=(12, 8), font=("Segoe UI", 10))
    style.configure(
        "Primary.TButton",
        padding=(16, 10),
        background=ACCENT,
        foreground="white",
        font=("Segoe UI Semibold", 10),
        borderwidth=0,
    )
    style.map(
        "Primary.TButton",
        background=[
            ("disabled", "#93C5FD"),
            ("active", ACCENT_ACTIVE),
            ("pressed", ACCENT_ACTIVE),
        ],
        foreground=[("disabled", "#F8FAFC")],
    )
    style.configure("Compact.TButton", padding=(8, 5), font=("Segoe UI", 9))
    style.configure("TRadiobutton", font=("Segoe UI", 10))
    style.configure("TLabelframe", background=SURFACE_ALT)
    style.configure(
        "TLabelframe.Label",
        foreground=TEXT,
        font=("Segoe UI Semibold", 10),
    )
    style.configure(
        "Treeview",
        rowheight=30,
        fieldbackground=SURFACE,
        background=SURFACE,
        foreground=TEXT,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
    )
    style.configure(
        "Treeview.Heading",
        padding=(8, 7),
        font=("Segoe UI Semibold", 9),
    )
    style.map(
        "Treeview",
        background=[("selected", ACCENT)],
        foreground=[("selected", "white")],
    )
    style.configure(
        "Horizontal.TProgressbar",
        troughcolor="#E2E8F0",
        background=ACCENT,
        thickness=10,
    )
