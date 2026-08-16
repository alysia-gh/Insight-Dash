import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from branding import theme

COLORS = {
    "primary": f"#{theme.PRIMARY}",
    "secondary": f"#{theme.SECONDARY}",
    "success": f"#{theme.SUCCESS}",
    "warning": f"#{theme.WARNING}",
    "danger": f"#{theme.DANGER}",
    "background": f"#{theme.BACKGROUND}",
    "text": f"#{theme.TEXT}",
    "light_text": f"#{theme.LIGHT_TEXT}",
    "grid": f"#{theme.GRID}",
}

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans", "sans-serif"],
    "font.size": 10,
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "legend.fontsize": 10,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": COLORS["grid"],
    "axes.grid": False,
    "xtick.color": COLORS["text"],
    "ytick.color": COLORS["text"],
    "text.color": COLORS["text"],
    "axes.titlecolor": COLORS["text"],
    "axes.labelcolor": COLORS["text"],
    "legend.frameon": False,
})


def create_figure(figsize=(9, 4), dpi=160):
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    return fig, ax


def clean_axis(ax, grid=True, show_x=True, show_y=True):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLORS["grid"])
    ax.spines["bottom"].set_color(COLORS["grid"])
    ax.tick_params(axis="x", colors=COLORS["text"])
    ax.tick_params(axis="y", colors=COLORS["text"])

    if grid:
        ax.grid(axis="y", color=COLORS["grid"], linestyle="--", linewidth=0.5, alpha=0.35)
        ax.set_axisbelow(True)

    if not show_x:
        ax.xaxis.set_visible(False)
    if not show_y:
        ax.yaxis.set_visible(False)


def compact_currency(value):
    if value is None:
        return ""

    try:
        value = float(value)
    except (TypeError, ValueError):
        return str(value)

    sign = "-" if value < 0 else ""
    value = abs(value)

    if value >= 1_000_000:
        return f"{sign}${value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{sign}${value / 1_000:.1f}K"
    return f"{sign}${value:,.0f}"


def compact_percent(value):
    if value is None:
        return ""

    try:
        value = float(value)
    except (TypeError, ValueError):
        return str(value)

    return f"{value:.1f}%"


def format_month_labels(items):
    """
    Accept an iterable of date-like items and return a list of formatted
    month labels. If the number of items is greater than 12, include the
    year in the label (e.g. "Jan 24"); otherwise use abbreviated month
    names (e.g. "Jan").
    """
    labels = []
    try:
        total = len(items)
    except TypeError:
        # Not sized; fall back to iterating and counting
        items = list(items)
        total = len(items)

    for item in items:
        if hasattr(item, "strftime"):
            labels.append(item.strftime("%b %y") if total > 12 else item.strftime("%b"))
            continue

        if hasattr(item, "to_timestamp"):
            ts = item.to_timestamp()
            labels.append(ts.strftime("%b %y") if total > 12 else ts.strftime("%b"))
            continue

        labels.append(str(item))

    return labels


def save_figure_to_bytes(fig):
    buffer = io.BytesIO()
    fig.savefig(
        buffer,
        format="png",
        dpi=200,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )
    buffer.seek(0)
    plt.close(fig)
    return buffer


def value_formatter(currency=False, percent=False):
    if currency:
        return FuncFormatter(lambda x, _: compact_currency(x))
    if percent:
        return FuncFormatter(lambda x, _: compact_percent(x))
    return None
