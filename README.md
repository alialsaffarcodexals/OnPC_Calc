# OnPC_Calc

OnPcCalc is a program that calculates how much time the user spends in selected applications. It provides a simple GUI to add programs by path, start tracking, and view the stored statistics.

## Features

- Select programs to track using a file dialog.
- Start and stop tracking of the chosen programs only.
- Store daily summaries in an SQLite database.
- View tracked data for any day using a drop down menu.
- Print the displayed data.
- Dark themed interface with larger window.
- Times are shown in HH:MM format.
- Track overall PC usage time with a dedicated button.

## Usage

Install the requirements and run `main.py`:

```bash
pip install -r requirements.txt
python main.py
```

Use the **PC Time** button to record your total computer usage, regardless of the tracked applications.
