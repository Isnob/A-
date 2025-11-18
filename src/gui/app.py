import sys

from PyQt6.QtWidgets import QApplication

from src.gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # TODO: поменяй путь на свой файл с лабиринтами, если нужно
    config_path = "config/config.yaml"

    window = MainWindow(config_path=config_path)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
