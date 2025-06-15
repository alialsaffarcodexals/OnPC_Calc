"""Tkinter GUI for OnPC_Calc."""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from .database import Database
from .tracker import Tracker, PcTracker

FONT = ("Arial", 16)
BG = "#222222"
FG = "#eeeeee"
BTN_BG = "#444444"
BTN_FG = "#ffffff"


def format_time(seconds: int) -> str:
    """Return HH:MM string for given seconds."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"

class GUI:
    def __init__(self) -> None:
        self.db = Database()
        self.tracker: Tracker | None = None
        self.pc_tracker: PcTracker | None = None
        self.paths: list[str] = []
        self.root = tk.Tk()
        self.root.title("OnPC Calc")
        self.root.geometry("600x400")
        self.root.configure(bg=BG)
        self._build_main_menu()

    def _build_main_menu(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

        add_btn = tk.Button(
            self.root,
            text="Add Program",
            font=FONT,
            bg=BTN_BG,
            fg=BTN_FG,
            command=self._add_program,
        )
        add_btn.pack(pady=10)

        self.listbox = tk.Listbox(
            self.root,
            font=("Arial", 12),
            height=5,
            width=40,
            bg=BG,
            fg=FG,
            selectbackground=BTN_BG,
            highlightbackground=BG,
        )
        self.listbox.pack(pady=10)

        pc_btn = tk.Button(
            self.root,
            text="PC Time",
            font=FONT,
            bg=BTN_BG,
            fg=BTN_FG,
            command=self._toggle_pc_tracking,
        )
        pc_btn.pack(pady=10)

        start_btn = tk.Button(
            self.root,
            text="Start Track",
            font=FONT,
            bg=BTN_BG,
            fg=BTN_FG,
            command=self._toggle_tracking,
        )
        start_btn.pack(pady=10)

        show_btn = tk.Button(
            self.root,
            text="Show Data",
            font=FONT,
            bg=BTN_BG,
            fg=BTN_FG,
            command=self._show_data,
        )
        show_btn.pack(pady=10)

        self.start_btn = start_btn

    def _add_program(self) -> None:
        path = filedialog.askopenfilename(title="Select Program")
        if path and path not in self.paths:
            self.paths.append(path)
            self.listbox.insert(tk.END, os.path.basename(path))

    def _toggle_tracking(self) -> None:
        if self.tracker and self.tracker.running:
            data = self.tracker.stop()
            for name, sec in data.items():
                self.db.add_usage(self.tracker.date, name, sec)
            messagebox.showinfo("Saved", "Tracking data saved.")
            self.start_btn.config(text="Start Track")
            self.tracker = None
        else:
            if not self.paths:
                messagebox.showwarning("No Programs", "Add at least one program to track.")
                return
            self.tracker = Tracker(self.paths)
            self.tracker.start()
            self.start_btn.config(text="Stop Track")

    def _toggle_pc_tracking(self) -> None:
        if self.pc_tracker and self.pc_tracker.running:
            seconds = self.pc_tracker.stop()
            self.db.add_pc_usage(self.pc_tracker.date, seconds)
            messagebox.showinfo("Saved", "PC time saved.")
            self.pc_tracker = None
        else:
            self.pc_tracker = PcTracker()
            self.pc_tracker.start()

    def _show_data(self) -> None:
        window = tk.Toplevel(self.root)
        window.title("Show Data")
        window.configure(bg=BG)
        dates = self.db.list_dates()
        date_var = tk.StringVar(value=dates[0] if dates else "")
        dropdown = ttk.Combobox(window, values=dates, textvariable=date_var, font=FONT)
        dropdown.pack(pady=10)
        text = tk.Text(window, font=("Courier", 12), width=50, height=12, bg=BG, fg=FG)
        text.pack()

        def load_data() -> None:
            date = date_var.get()
            text.delete("1.0", tk.END)
            pc_total = self.db.get_pc_usage(date)
            text.insert(tk.END, f"PC Total: {format_time(pc_total)}\n")
            total = self.db.get_total_for_date(date)
            text.insert(tk.END, f"Tracked Programs: {format_time(total)}\n")
            for name, sec in self.db.get_usage_for_date(date):
                text.insert(tk.END, f"{name:20} {format_time(sec)}\n")

        def print_data() -> None:
            print(text.get("1.0", tk.END))

        btn_frame = tk.Frame(window, bg=BG)
        btn_frame.pack(pady=10)
        show_btn = tk.Button(btn_frame, text="Show", font=FONT, bg=BTN_BG, fg=BTN_FG, command=load_data)
        show_btn.pack(side=tk.LEFT, padx=5)
        print_btn = tk.Button(btn_frame, text="Print Track", font=FONT, bg=BTN_BG, fg=BTN_FG, command=print_data)
        print_btn.pack(side=tk.LEFT, padx=5)
        back_btn = tk.Button(btn_frame, text="Back", font=FONT, bg=BTN_BG, fg=BTN_FG, command=window.destroy)
        back_btn.pack(side=tk.LEFT, padx=5)

    def run(self) -> None:
        self.root.mainloop()
