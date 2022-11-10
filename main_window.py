import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt
from day_dialog import DayDialog
from statistic_window import StatisticsDialog
from record_window import RecordDialog
from all_records_dlg import AllRecordsDialog


class Diary(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Создаётся интерфейс

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground)

        self.setGeometry(100, 100, 600, 480)
        self.setWindowTitle('Дневник настроений')
        self.setStyleSheet("""
            background: rgb(10, 10, 10);
            border: 2px solid rgb(108, 148, 112);
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
        self.close_btn.clicked.connect(sys.exit)

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

        self.text1 = QLabel(self)
        self.text1.setText('Как ваше настроение?')
        self.text1.setStyleSheet("""
            color: white;
            font-family: Impact;
            font-size: 50px;
            border: transparent;
        """)
        self.text1.move(50, 30)

        self.add_btn = QPushButton(self)
        self.add_btn.move(250, 110)
        self.add_btn.resize(100, 100)
        self.add_btn.setText('+')
        self.add_btn.setStyleSheet("""
                QPushButton {color: rgb(20, 43, 22);
                    background-color: white;
                    font-family: Impact;
                    font-size: 100px;
                    border: transparent;
                    }
                QPushButton:hover {
                    color: white;
                    background-color: rgb(108, 148, 112);
                }
                QPushButton:pressed {
                    color: white;
                    background-color: rgb(78, 118, 82);
                }
             """)
        self.add_btn.clicked.connect(self.summon_day_dialog)

        self.statistics_btn = QPushButton(self)
        self.statistics_btn.move(50, 240)
        self.statistics_btn.resize(500, 60)
        self.statistics_btn.setText('Статистика')
        self.statistics_btn.setStyleSheet("""
            QPushButton {color: white;
                    background-color: rgb(20, 43, 22);
                    font-family: Impact;
                    font-size: 40px;
                    border: transparent;;
                }
                QPushButton:hover {
                    background-color: rgb(40, 63, 42);
                }
                QPushButton:pressed {
                    background-color: rgb(70, 93, 72);
                }
                     """)
        self.statistics_btn.clicked.connect(self.summon_statistic_dialog)

        self.record_btn = QPushButton(self)
        self.record_btn.move(50, 320)
        self.record_btn.resize(500, 60)
        self.record_btn.setText('Посмотреть/изменить записи')
        self.record_btn.setStyleSheet("""
            QPushButton {color: white;
                    background-color: rgb(20, 43, 22);
                    font-family: Impact;
                    font-size: 35px;
                    border: transparent;;
                }
                QPushButton:hover {
                    background-color: rgb(40, 63, 42);
                }
                QPushButton:pressed {
                    background-color: rgb(70, 93, 72);
                }
                     """)
        self.record_btn.clicked.connect(self.summon_record_dialog)

        self.all_records_btn = QPushButton(self)
        self.all_records_btn.move(50, 400)
        self.all_records_btn.resize(500, 60)
        self.all_records_btn.setText('Все записи')
        self.all_records_btn.setStyleSheet("""
                    QPushButton {color: white;
                            background-color: rgb(20, 43, 22);
                            font-family: Impact;
                            font-size: 35px;
                            border: transparent;;
                        }
                        QPushButton:hover {
                            background-color: rgb(40, 63, 42);
                        }
                        QPushButton:pressed {
                            background-color: rgb(70, 93, 72);
                        }
                             """)
        self.all_records_btn.clicked.connect(self.summon_all_records_dialog)

    def summon_day_dialog(self):
        # Вызывается окно DayDialog
        day_dlg = DayDialog(self)
        day_dlg.exec()

    def summon_statistic_dialog(self):
        # Вызывается окно StatisticsDialog
        statistic_dlg = StatisticsDialog(self)
        statistic_dlg.exec()

    def summon_record_dialog(self):
        # Вызывается окно RecordDialog
        record_dlg = RecordDialog(self)
        record_dlg.exec()

    def summon_all_records_dialog(self):
        # Вызывается окно AllRecordsDialog
        all_records_dlg = AllRecordsDialog(self)
        all_records_dlg.exec()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Diary()
    ex.show()
    sys.exit(app.exec())