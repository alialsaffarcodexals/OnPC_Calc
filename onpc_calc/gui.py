"""Tkinter GUI for OnPC_Calc."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

from .database import Database
from .tracker import Tracker

FONT = ("Arial", 16)

class GUI:
    def __init__(self) -> None:
        self.db = Database()
        self.tracker: Tracker | None = None
        self.root = tk.Tk()
        self.root.title("OnPC Calc")
        self.root.geometry("400x300")
        self._build_main_menu()

    def _build_main_menu(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()
        start_btn = tk.Button(
            self.root,
            text="Start Track",
            font=FONT,
            command=self._toggle_tracking,
        )
        start_btn.pack(pady=20)
        show_btn = tk.Button(self.root, text="Show Data", font=FONT, command=self._show_data)
        show_btn.pack(pady=20)
        self.start_btn = start_btn

    def _toggle_tracking(self) -> None:
        if self.tracker and self.tracker.running:
            data = self.tracker.stop()
            for name, sec in data.items():
                self.db.add_usage(self.tracker.date, name, sec)
            messagebox.showinfo("Saved", "Tracking data saved.")
            self.start_btn.config(text="Start Track")
            self.tracker = None
        else:
            self.tracker = Tracker()
            self.tracker.start()
            self.start_btn.config(text="Stop Track")

    def _show_data(self) -> None:
        window = tk.Toplevel(self.root)
        window.title("Show Data")
        dates = self.db.list_dates()
        date_var = tk.StringVar(value=dates[0] if dates else "")
        dropdown = ttk.Combobox(window, values=dates, textvariable=date_var, font=FONT)
        dropdown.pack(pady=10)
        text = tk.Text(window, font=("Courier", 12), width=40, height=10)
        text.pack()

        def load_data() -> None:
            date = date_var.get()
            text.delete("1.0", tk.END)
            total = self.db.get_total_for_date(date)
            text.insert(tk.END, f"Total: {total} seconds\n")
            for name, sec in self.db.get_usage_for_date(date):
                text.insert(tk.END, f"{name:20} {sec} s\n")

        def print_data() -> None:
            print(text.get("1.0", tk.END))

        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        show_btn = tk.Button(btn_frame, text="Show", font=FONT, command=load_data)
        show_btn.pack(side=tk.LEFT, padx=5)
        print_btn = tk.Button(btn_frame, text="Print Track", font=FONT, command=print_data)
        print_btn.pack(side=tk.LEFT, padx=5)
        back_btn = tk.Button(btn_frame, text="Back", font=FONT, command=window.destroy)
        back_btn.pack(side=tk.LEFT, padx=5)

    def run(self) -> None:
        self.root.mainloop()
