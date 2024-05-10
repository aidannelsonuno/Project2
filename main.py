from logic import *

#NOTE: before submission, edit file path in logic.py (Project2/all_five_words.txt)

def main():
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()


if __name__ == "__main__":
    main()