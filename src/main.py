import tkinter as tk

from src.app.EventDetectionUI import EventDetectionUI


def main() :
    try :
        root = tk.Tk()
        EventDetectionUI(root)
        root.mainloop()
    except Exception as e :
        RuntimeError("An error occurred:", e)
    else :
        print("Application run successfully.")


if __name__ == "__main__" :
    main()
