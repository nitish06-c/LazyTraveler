import sys
from dotenv import load_dotenv
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

# Load environment variables from .env file
load_dotenv()

# Example: Access the OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
