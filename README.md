# App Tracker

App Tracker lets you measure how long you spend on the computer or in
selected applications. It features a dark themed interface, larger fonts and
simple controls for starting and stopping timers.

## Features

- Start and stop overall PC usage tracking.
- Track an app by entering its name.
- A real-time timer is shown while tracking.
- Times are shown in `HH:MM:SS` format.
- View tracked data for any day in a table.
- Calculate total app usage for the day with **Sum Apps**.
- Clear all records for a specific date using **Reset Date**.
- Save displayed data using the **Print Track** button which writes to
  `PC-Track-YYYY-MM-DD.txt`.
- Dark themed interface with a larger window and improved layout.

## Usage

Install the requirements and run `main.py`:

```bash
pip install -r requirements.txt
python main.py
```

Use **Track PC** to measure total PC time or **Track App** to monitor a single
application by name. A live timer shows progress while tracking. In the
**Show Data** view you can review totals for any day, calculate the sum of all
app usage, press **Reset Date** to clear a day's records, and use **Print Track**
to save the table to a text file.
