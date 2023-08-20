import logging
import tkinter as tk

from src.LoadLoggingConfig import load_logging_config
from src.app.EventDetectionUI import EventDetectionUI


def main() :
    load_logging_config()
    logger = logging.getLogger('staging')

    try :
        root = tk.Tk()
        EventDetectionUI(root)
        root.mainloop()
    except Exception as e :
        RuntimeError("An error occurred:", e)
    else :
        logger.info("Application run successfully.")


if __name__ == "__main__" :
    main()
