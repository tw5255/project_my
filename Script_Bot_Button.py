from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFrame, QLabel, QMessageBox, QPlainTextEdit
from PyQt5.QtGui import QPalette, QPixmap, QBrush
from script_bot import find_element_with_navigation
import sys
from PyQt5.QtCore import Qt


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(1100, 300, 700, 600)
        self.setWindowTitle("SmmBot")

        # Установить фон окна
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("D:/urokipython/fon.png")))
        self.setPalette(palette)

        # Создать шапку
        header = QFrame(self)
        header.setGeometry(0, 0, 700, 50)
        header.setStyleSheet("background-color: #333; color: #fff;")

        # Создать кнопку в шапке
        button_header = QPushButton("Настройки", header)
        button_header.setGeometry(2, 10, 100, 30)
        # button_header.clicked.connect(self.run_script)

        # Создать кнопки и текстовые поля в основном окне
        self.label1 = QLabel("Введите домен без префикса:", self)
        self.label1.move(2, 55)
        self.label1.show()

        self.text_input1 = QLineEdit(self)
        self.text_input1.move(2, 70)
        self.text_input1.show()

        self.label2 = QLabel("Выберите поисковую систему (Yandex 1 или Google 2):", self)
        self.label2.move(2, 110)
        self.label2.show()

        self.text_input2 = QLineEdit(self)
        self.text_input2.move(2, 130)
        self.text_input2.show()

        self.label3 = QLabel("Количество повторений:", self)
        self.label3.move(2, 180)
        self.label3.show()

        self.text_input3 = QLineEdit(self)
        self.text_input3.move(2, 200)
        self.text_input3.show()

        self.label4 = QLabel("Минимальное время между выполнениями скрипта (в секундах):", self)
        self.label4.move(2, 240)
        self.label4.show()

        self.text_input4 = QLineEdit(self)
        self.text_input4.move(2, 260)
        self.text_input4.show()

        self.label5 = QLabel("Максимальное время между выполнениями скрипта (в секундах):", self)
        self.label5.move(2, 300)
        self.label5.show()

        self.text_input5 = QLineEdit(self)
        self.text_input5.move(2, 320)
        self.text_input5.show()

        self.label6 = QLabel("Минимальное время нахождения на сайте (в секундах):", self)
        self.label6.move(2, 360)
        self.label6.show()

        self.text_input6 = QLineEdit(self)
        self.text_input6.move(2, 380)
        self.text_input6.show()

        self.label7 = QLabel("Максимальное время нахождения на сайте (в секундах):", self)
        self.label7.move(2, 420)
        self.label7.show()

        self.text_input7 = QLineEdit(self)
        self.text_input7.move(2, 440)
        self.text_input7.show()

        # Создать текстовую область для вывода сообщений
        self.text_output = QPlainTextEdit(self)
        self.text_output.setGeometry(350, 55, 345, 300)
        self.text_output.setReadOnly(True)

        # Создать кнопку запуска скрипта
        button_run_script = QPushButton('Запустить скрипт', self)
        button_run_script.setGeometry(2, 480, 100, 30)
        button_run_script.clicked.connect(self.run_script)

        # Создать кнопку повтора скрипта
        button_repeat_script = QPushButton('Повторить скрипт', self)
        button_repeat_script.setGeometry(2, 520, 100, 30)
        button_repeat_script.clicked.connect(self.repeat_script)

        # Создать кнопку закрытия окна
        button_close = QPushButton('Закрыть', self)
        button_close.setGeometry(600, 10, 80, 30)
        button_close.clicked.connect(self.close)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Вы уверены, что хотите закрыть окно?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def repeat_script(self):
        exit_choice = QMessageBox.question(self, 'Повтор скрипта', 'Хотите повторить скрипт?',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if exit_choice == QMessageBox.Yes:
            QMessageBox.information(self, 'Повтор скрипта', 'Вы выбрали "Да"')
            return self.run_script()
        elif exit_choice == QMessageBox.No:
            QMessageBox.information(self, 'Повтор скрипта', 'Вы выбрали "Нет" для выхода из приложения нажмите "Закрыть"')
            return False  # Изменено на False для завершения работы скрипта
        else:
            pass



    def run_script(self):
        search_queries_file = "C:/Users/Admin/Desktop/autocar_requests.txt"
        domain = self.text_input1.text()
        search_engine = self.text_input2.text()
        repetitions = int(self.text_input3.text())
        min_interval = int(self.text_input4.text())
        max_interval = int(self.text_input5.text())
        min_time = int(self.text_input6.text())
        max_time = int(self.text_input7.text())

        find_element_with_navigation(search_queries_file, domain, search_engine, repetitions,
                                     min_interval, max_interval, min_time, max_time)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())








