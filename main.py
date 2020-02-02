import fire
from view.commands import Commands
from controller.controller import Controller
from controller.validator import InputException
import sqlite3
import sys

if __name__ == "__main__":
    sys.path.append('')
    c = Controller()
    try:
        fire.Fire(Commands(c))
    except InputException as e:
        print("Incorrect input")
        print(e)
    except sqlite3.IntegrityError as e:
        print("Incorrect input")
        if "FOREIGN" in str(e):
            print("Office with current id is not exist")
