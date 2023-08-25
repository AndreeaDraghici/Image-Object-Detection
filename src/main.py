import logging
import tkinter as tk

from src.LoadLoggingConfig import load_logging_config
from src.app.EventDetectionUI import EventDetectionUI


def main() :
    # Load the logging configuration
    load_logging_config()

    # Get the logger for the 'staging' logger
    logger = logging.getLogger('staging')

    try :
        # Create a new Tkinter root window
        root = tk.Tk()

        # Initialize the EventDetectionUI with the root window
        EventDetectionUI(root)

        # Start the Tkinter main event loop
        root.mainloop()
    except Exception as e :
        # Handle exceptions that might occur during the application's execution
        raise RuntimeError("An error occurred:", e)
    else :
        # Log a success message if the application runs successfully
        logger.info("Application run successfully.")


# Entry point of the script
if __name__ == "__main__" :
    # Call the main function to start the application
    main()

