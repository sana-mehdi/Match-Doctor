"""CSC111 Winter 2023 Course Project

===============================
This Python module contains the helper functions for the user interface.

Copyright and Usage Information
===============================
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Nicolas Dias Martins, Sana-E-Zehra Mehdi, Rohan Patra, and Maleeha Rahman.
"""
from __future__ import annotations
import csv
from tkinter.constants import LEFT, NW, X
from typing import Any, Optional
import ttkbootstrap as ttk


def info_row(info: ttk.Frame | ttk.LabelFrame, text: str) -> None:
    """
    This function creates each label to display patient information.
    """
    row = ttk.Frame(info, padding=5)
    row.pack(anchor=NW)

    lbl = ttk.Label(row, text=text, font='Modern 15', wraplength=300)
    lbl.pack(side=LEFT)


def validate_length(text: str) -> bool:
    """
    Validate that the length of the text is between 6 and 8 characters in length.
    """
    if 6 <= len(text) <= 8:
        return True
    else:
        return False


def form_entry(label: str, variable: Any, frame: ttk.LabelFrame, validate_func: ttk.Toplevel.register) -> None:
    """
    This function creates a general form entry.
    """
    cont = ttk.Frame(frame)
    cont.pack(fill=X, pady=5)

    lbl = ttk.Label(master=cont, text=label, width=20, font="Modern 15")
    lbl.pack(side=LEFT)

    if validate_func is not None:
        entry = ttk.Entry(master=cont, textvariable=variable, width=5, validatecommand=(validate_func, '%P'),
                          validate='focus')
    else:
        entry = ttk.Entry(master=cont, textvariable=variable, width=5)

    entry.pack(side=LEFT, fill=X, ipadx=80)


def combo(label: str, frame: ttk.LabelFrame, values: list) -> ttk.Combobox:
    """
    This function creates and returns a gneeral combo box.
    """
    cont = ttk.Frame(frame)
    cont.pack(fill=X, pady=5)

    lbl = ttk.Label(master=cont, text=label, width=20, font="Modern 15")
    lbl.pack(side=LEFT)

    comb = ttk.Combobox(master=cont, values=values)

    comb.current(0)
    comb.pack(side=LEFT, fill=X, ipadx=5)

    return comb


def validate_text(text: str) -> bool:
    """
    Validate that the text consists of only alphabet letters
    """
    if all(x.isalpha() or x == ',' or x == ' ' for x in text):
        return True
    else:
        return False


def validate_email(text: str) -> bool:
    """
    Validate that the text contains an @ symbol
    """
    if '@' in text:
        return True
    else:
        return False


def validate_phone(phone: str) -> bool:
    """
    Validate that the text contains only numbers
    """
    if all(x.isdigit() for x in phone) and len(phone) == 10:
        return True
    else:
        return False


def check_user(text: str, file: str) -> Optional[list]:
    """
    Checks if the username is in the patient csv file.
    """
    with open(file) as csv_file:
        for row in csv.reader(csv_file):
            if row[0] == text:
                return row

    return None


def check_pass(passw: str, row: list[str]) -> bool:
    """
    Validate that the password matches the patient that corresponds to the username.
    """
    if row[1] == passw:
        return True
    else:
        return False


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['csv', 'tkinter.constants', 'ttkbootstrap'],
        'disable': ['forbidden-IO-function']
    })
