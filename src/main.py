import tkinter as tk

from src.app.GUI import EventDetectionUI


def main() :
    root = tk.Tk()
    EventDetectionUI(root)
    root.mainloop()


if __name__ == "__main__" :
    main()
