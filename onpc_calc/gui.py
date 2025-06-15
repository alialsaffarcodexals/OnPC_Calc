"""Tkinter GUI for App Tracker."""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from .database import Database
from .tracker import PcTracker, ProgramTracker

FONT = ("Arial", 16)
BG = "#222222"
FG = "#eeeeee"
BTN_BG = "#444444"
BTN_FG = "#ffffff"
WINDOW_SIZE = "800x600"


def format_time(seconds: int) -> str:
    """Return HH:MM:SS string for given seconds."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


class GUI:
    """Main application GUI."""

    def __init__(self) -> None:
        self.db = Database()
        self.root = tk.Tk()
        self.root.title("App Tracker")
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=BG)
        self.current_frame: tk.Frame | None = None
        self.pc_tracker: PcTracker | None = None
        self.prog_tracker: ProgramTracker | None = None
        self.timer_var = tk.StringVar(value="00:00:00")
        self._show_main_menu()

    # utility ---------------------------------------------------------------
    def _clear_frame(self) -> None:
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, bg=BG)
        self.current_frame.pack(expand=True, fill="both")

    def _update_timer(self) -> None:
        if self.pc_tracker and self.pc_tracker.running:
            self.timer_var.set(format_time(self.pc_tracker.seconds))
        elif self.prog_tracker and self.prog_tracker.running:
            self.timer_var.set(format_time(self.prog_tracker.seconds))
        if self.pc_tracker and self.pc_tracker.running or (
            self.prog_tracker and self.prog_tracker.running
        ):
            self.root.after(1000, self._update_timer)

    # main menu -------------------------------------------------------------
    def _show_main_menu(self) -> None:
        self._clear_frame()
        frame = self.current_frame

        pc_btn = tk.Button(
            frame,
            text="Track PC",
            font=FONT,
            bg=BTN_BG,
            fg=BTN_FG,
            command=self._pc_view,
        )
        pc_btn.pack(pady=20)

        prog_btn = tk.Button(
            frame,
            text="Track App",
            font=FONT,
            bg=BTN_BG,
            fg=BTN_FG,
            command=self._program_view,
        )
        prog_btn.pack(pady=20)

        show_btn = tk.Button(
            frame,
            text="Show Data",
            font=FONT,
            bg=BTN_BG,
            fg=BTN_FG,
            command=self._show_data_view,
        )
        show_btn.pack(pady=20)

    # PC tracking -----------------------------------------------------------
    def _pc_view(self) -> None:
        self._clear_frame()
        frame = self.current_frame

        label = tk.Label(frame, text="PC Tracker", font=FONT, bg=BG, fg=FG)
        label.pack(pady=10)
        if self.pc_tracker:
            self.timer_var.set(format_time(self.pc_tracker.seconds))
        else:
            self.timer_var.set("00:00:00")
        timer = tk.Label(frame, textvariable=self.timer_var, font=FONT, bg=BG, fg=FG)
        timer.pack(pady=10)
        if self.pc_tracker and self.pc_tracker.running:
            self._update_timer()

        start_btn = tk.Button(
            frame,
            text="Start" if not self.pc_tracker else "Stop",
            font=FONT,
            bg=BTN_BG,
            fg=BTN_FG,
        )
        start_btn.pack(pady=20)

        def toggle() -> None:
            nonlocal start_btn
            if self.pc_tracker and self.pc_tracker.running:
                secs = self.pc_tracker.stop()
                self.db.add_pc_usage(self.pc_tracker.date, secs)
                messagebox.showinfo("Saved", "PC time saved")
                self.pc_tracker = None
                start_btn.config(text="Start")
            else:
                self.pc_tracker = PcTracker()
                self.timer_var.set("00:00:00")
                self.pc_tracker.start()
                self._update_timer()
                messagebox.showinfo("Started", "PC tracking started!")
                start_btn.config(text="Stop")

        start_btn.config(command=toggle)

        back_btn = tk.Button(
            frame,
            text="Return to Main Menu",
            font=FONT,
            bg=BTN_BG,
            fg=BTN_FG,
            command=self._show_main_menu,
        )
        back_btn.pack(pady=10)

    # program tracking ------------------------------------------------------
    def _program_view(self) -> None:
        self._clear_frame()
        frame = self.current_frame

        header = tk.Label(frame, text="App Tracker", font=FONT, bg=BG, fg=FG)
        header.pack(pady=10)

        path_var = tk.StringVar()
        entry = tk.Entry(frame, textvariable=path_var, font=FONT, width=50)
        entry.pack(pady=10)
        entry.insert(0, "app path")

        def browse() -> None:
            path = filedialog.askopenfilename()
            if path:
                path_var.set(path)

        browse_btn = tk.Button(frame, text="Browse", font=FONT, bg=BTN_BG, fg=BTN_FG, command=browse)
        browse_btn.pack(pady=5)

        label = tk.Label(frame, textvariable=self.timer_var, font=FONT, bg=BG, fg=FG)
        label.pack(pady=10)

        start_btn = tk.Button(frame, text="Start", font=FONT, bg=BTN_BG, fg=BTN_FG)
        start_btn.pack(pady=20)

        def toggle() -> None:
            nonlocal start_btn
            path = path_var.get().strip()
            if not path:
                messagebox.showerror("Error", "App path required")
                return
            if self.prog_tracker and self.prog_tracker.running:
                secs = self.prog_tracker.stop()
                self.db.add_program_usage(path, self.prog_tracker.date, secs)
                messagebox.showinfo("Saved", f"{os.path.basename(path)} time saved")
                self.prog_tracker = None
                start_btn.config(text="Start")
            else:
                self.prog_tracker = ProgramTracker(path)
                self.timer_var.set("00:00:00")
                self.prog_tracker.start()
                self._update_timer()
                messagebox.showinfo("Started", f"{os.path.basename(path)} tracker started!")
                start_btn.config(text="Stop")

        start_btn.config(command=toggle)

        back_btn = tk.Button(
            frame,
            text="Return to Main Menu",
            font=FONT,
            bg=BTN_BG,
            fg=BTN_FG,
            command=self._show_main_menu,
        )
        back_btn.pack(pady=10)

    # show data -------------------------------------------------------------
    def _show_data_view(self) -> None:
        self._clear_frame()
        frame = self.current_frame

        dates = self.db.list_dates()
        date_var = tk.StringVar(value=dates[0] if dates else "")
        dropdown = ttk.Combobox(frame, values=dates, textvariable=date_var, font=FONT)
        dropdown.pack(pady=10)

        tree = ttk.Treeview(frame, columns=("app", "time"), show="headings", height=10)
        tree.heading("app", text="App Name")
        tree.heading("time", text="Time Spent")
        tree.column("app", width=200)
        tree.column("time", width=150)
        tree.pack(pady=10)

        def load() -> None:
            tree.delete(*tree.get_children())
            date = date_var.get()
            if not date:
                return
            pc_total = self.db.get_pc_usage(date)
            tree.insert("", tk.END, values=("PC Total", format_time(pc_total)))
            for name, secs in self.db.get_program_usage(date):
                tree.insert("", tk.END, values=(os.path.basename(name), format_time(secs)))

        def save() -> None:
            date = date_var.get()
            if not date:
                messagebox.showerror("Error", "No date selected")
                return
            filename = f"PC-Track-{date}.txt"
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("App Name\tTime Spent\n")
                    pc_total = self.db.get_pc_usage(date)
                    f.write(f"PC Total\t{format_time(pc_total)}\n")
                    for name, secs in self.db.get_program_usage(date):
                        f.write(f"{os.path.basename(name)}\t{format_time(secs)}\n")
                messagebox.showinfo("Saved", f"Data saved to {filename}")
            except OSError as exc:
                messagebox.showerror("Error", str(exc))

        btn_frame = tk.Frame(frame, bg=BG)
        btn_frame.pack(pady=10)
        show_btn = tk.Button(btn_frame, text="Show", font=FONT, bg=BTN_BG, fg=BTN_FG, command=load)
        show_btn.pack(side=tk.LEFT, padx=5)
        print_btn = tk.Button(btn_frame, text="Print Track", font=FONT, bg=BTN_BG, fg=BTN_FG, command=save)
        print_btn.pack(side=tk.LEFT, padx=5)
        def total_programs() -> None:
            date = date_var.get()
            if not date:
                messagebox.showerror("Error", "No date selected")
                return
            total = sum(secs for _, secs in self.db.get_program_usage(date))
            messagebox.showinfo("Total App Time", f"Total app usage: {format_time(total)}")

        def reset_date() -> None:
            date = date_var.get()
            if not date:
                messagebox.showerror("Error", "No date selected")
                return
            if not messagebox.askyesno("Confirm", f"Clear data for {date}?"):
                return
            self.db.reset_date(date)
            load()
            dates = self.db.list_dates()
            dropdown["values"] = dates
            date_var.set(dates[0] if dates else "")
            messagebox.showinfo("Reset", f"Data for {date} cleared")

        sum_btn = tk.Button(btn_frame, text="Sum Apps", font=FONT, bg=BTN_BG, fg=BTN_FG, command=total_programs)
        sum_btn.pack(side=tk.LEFT, padx=5)
        reset_btn = tk.Button(btn_frame, text="Reset Data", font=FONT, bg=BTN_BG, fg=BTN_FG, command=reset_date)
        reset_btn.pack(side=tk.LEFT, padx=5)
        back_btn = tk.Button(btn_frame, text="Return to Main Menu", font=FONT, bg=BTN_BG, fg=BTN_FG, command=self._show_main_menu)
        back_btn.pack(side=tk.LEFT, padx=5)

    # run -------------------------------------------------------------------
    def run(self) -> None:
        self.root.mainloop()
