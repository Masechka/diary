import sqlite3
from PyQt5.QtWidgets import QWidget, QPushButton, QDialog, QTextEdit
from PyQt5.QtCore import Qt



class AllRecordsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Создаётся интефейс
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground)

        self.setGeometry(720, 100, 600, 600)
        self.setWindowTitle('Дневник настроений')
        self.setStyleSheet("""
                    background: rgb(10, 10, 10);
                    border: 2px solid rgb(108, 148, 112);
                    color: white;
                """)

        self.panel = QWidget(self)
        self.panel.setGeometry(0, 0, 600, 30)
        self.panel.setStyleSheet("""
                    background: rgb(108, 148, 112);
                    border: transparent;
                """)

        self.close_btn = QPushButton(self)
        self.close_btn.resize(50, 30)
        self.close_btn.move(550, 0)
        self.close_btn.setText('✕')
        self.close_btn.setStyleSheet("""
                        QPushButton {color: white;
                                    background-color: rgb(78, 118, 82);
                                    font-family: Impact;
                                    font-size: 20px;
                                }
                                QPushButton:hover {
                                    background-color: rgb(255, 0, 0);
                                }
                                QPushButton:pressed {
                                    background-color: rgb(148, 0, 0);
                                }
                     """)
        self.close_btn.clicked.connect(self.close)

        self.collapse_btn = QPushButton(self)
        self.collapse_btn.resize(50, 30)
        self.collapse_btn.move(500, 0)
        self.collapse_btn.setText('━')
        self.collapse_btn.setStyleSheet("""
                                QPushButton {color: white;
                                    background-color: rgb(78, 118, 82);
                                    font-family: Impact;
                                    font-size: 20px;
                                }
                                QPushButton:hover {
                                    background-color: rgb(180, 180, 180);
                                }
                                QPushButton:pressed {
                                    background-color: rgb(160, 160, 160);
                                }
                             """)
        self.collapse_btn.clicked.connect(self.showMinimized)

        self.text_widget = QTextEdit(self)
        self.text_widget.setReadOnly(True)
        self.text_widget.move(10, 30)
        self.text_widget.resize(580, 565)
        self.text_widget.setStyleSheet("""
                            color: white;
                            font-family: Impact;
                            font-size: 20px;
                            border: transparent;
                        """)

        # Получение из БД всех данных, перевод их в нужный формат
        con = sqlite3.connect("diary.sqlite")
        cur = con.cursor()
        list_of_days = cur.execute("""SELECT * FROM data_table WHERE date""").fetchall()
        days_string = ''
        for i in range(len(list_of_days)):
            list_information = list(list_of_days[i])
            list_information[1] = str(list_information[1])
            information = '\n'.join(list_information)
            days_string = days_string + information + '\n' + '\n'

        # Записть данных в тексновый файл и отображение данных из текстового файла в окно
        file = open("all_records.txt", 'w')
        file.write(days_string)
        file.close()
        file = open("all_records.txt", 'r')
        text = file.read()
        self.text_widget.setText(text)
        file.close()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        try:
            if Qt.LeftButton and self.moveFlag:
                self.move(event.globalPos() - self.movePosition)
                event.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event):
        self.moveFlag = False
