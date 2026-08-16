from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
    Border,
    Side
)


def title_font():

    return Font(
        name="Calibri",
        size=24,
        bold=True,
        color="FFFFFF"
    )


def subtitle_font():

    return Font(
        size=12,
        italic=True,
        color="555555"
    )


def card_title_font():

    return Font(
        size=11,
        bold=True,
        color="666666"
    )


def metric_font():

    return Font(
        size=22,
        bold=True,
        color="222222"
    )


def insight_font():

    return Font(
        size=11
    )


def center():

    return Alignment(
        horizontal="center",
        vertical="center"
    )


def left():

    return Alignment(
        horizontal="left",
        vertical="center"
    )


def fill(color):

    return PatternFill(
        fill_type="solid",
        start_color=color
    )


def border():

    side = Side(
        style="thin",
        color="DDDDDD"
    )

    return Border(
        left=side,
        right=side,
        top=side,
        bottom=side
    )
def header_font():

    return Font(
        name="Calibri",
        size=24,
        bold=True,
        color="FFFFFF"
    )
def centered():
    return Alignment(
        horizontal="center",
        vertical="center"
    )


# Aliases expected by other modules
def card_fill(color):
    return fill(color)


def thin_border():
    return border()