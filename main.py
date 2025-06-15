"""Entry point for OnPC_Calc."""

from onpc_calc.gui import GUI


def main() -> None:
    gui = GUI()
    gui.run()


if __name__ == "__main__":
    main()
