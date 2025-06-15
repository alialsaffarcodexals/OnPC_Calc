# OnPC_Calc

OnPcCalc lets you track how long you spend on the computer each day.  It comes
with a dark themed interface, larger fonts and an easy way to start or stop the
timer.

## Features

- Start and stop overall PC usage tracking.
- Times are shown in `HH:MM:SS` format.
- View tracked data for any day using a drop down menu.
- Save displayed data using the **Print Track** button which writes to
  `PC-Track-YYYY-MM-DD.txt` rather than printing to the terminal.
- Dark themed interface with a larger window and improved layout.

## Usage

Install the requirements and run `main.py`:

```bash
pip install -r requirements.txt
python main.py
```

Use the **Track PC** button to start or stop counting how long your computer was
used for the day. When you start or stop tracking you will see a success
message.

From the **Show Data** window you can press **Print Track** to save the
displayed totals to a text file.
