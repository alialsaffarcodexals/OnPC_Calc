"""Tkinter GUI for OnPC_Calc."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

from .database import Database
from .tracker import PcTracker

FONT = ("Arial", 16)
BG = "#222222"
FG = "#eeeeee"
BTN_BG = "#444444"
BTN_FG = "#ffffff"


def format_time(seconds: int) -> str:
    """Return HH:MM:SS string for given seconds."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

class GUI:
    def __init__(self) -> None:
        self.db = Database()
        self.pc_tracker: PcTracker | None = None
        self.root = tk.Tk()
        self.root.title("OnPC Calc")
        self.root.geometry("700x500")
        self.root.configure(bg=BG)
        self._build_main_menu()

    def _build_main_menu(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(expand=True)

        pc_btn = tk.Button(
            frame,
            text="Track PC",
            font=FONT,
            bg=BTN_BG,
            fg=BTN_FG,
            command=self._toggle_pc_tracking,
        )
        pc_btn.pack(pady=20)

        show_btn = tk.Button(
            frame,
            text="Show Data",
            font=FONT,
            bg=BTN_BG,
            fg=BTN_FG,
            command=self._show_data,
        )
        show_btn.pack(pady=20)


    def _toggle_pc_tracking(self) -> None:
        if self.pc_tracker and self.pc_tracker.running:
            seconds = self.pc_tracker.stop()
            self.db.add_pc_usage(self.pc_tracker.date, seconds)
            messagebox.showinfo("Saved", "PC time saved.")
            self.pc_tracker = None
        elif self.pc_tracker and not self.pc_tracker.running:
            messagebox.showerror("Error", "Tracking already stopped.")
        else:
            self.pc_tracker = PcTracker()
            self.pc_tracker.start()
            messagebox.showinfo("Started", "PC tracking started!")

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

        def print_data() -> None:
            date = date_var.get()
            if not date:
                messagebox.showerror("Error", "No date selected")
                return
            filename = f"PC-Track-{date}.txt"
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(text.get("1.0", tk.END))
                messagebox.showinfo("Saved", f"Data saved to {filename}")
            except OSError as exc:
                messagebox.showerror("Error", str(exc))

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
