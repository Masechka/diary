from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QDialog, QCheckBox, QTextEdit, QFileDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
import sqlite3
from photo_dialog import PhotoDialog
import datetime
import shutil


class DayDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.mood = 0
        self.photo1_name = 'photos/photo140.png'
        self.photo2_name = 'photos/photo140.png'
        self.date = datetime.date.today()
        self.initUI()

    def initUI(self):
        # Создаётся интефейс
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground)

        self.setGeometry(720, 100, 600, 580)
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

        self.text1 = QLabel(self)
        self.text1.setText('Выберите настроение')
        self.text1.setStyleSheet("""
                    color: white;
                    font-family: Impact;
                    font-size: 50px;
                    border: transparent;
                """)
        self.text1.move(50, 30)

        self.pixmap = QPixmap('moods.png')
        self.moods_pic = QLabel(self)
        self.moods_pic.move(0, 100)
        self.moods_pic.resize(600, 100)
        self.moods_pic.setPixmap(self.pixmap)
        self.moods_pic.setStyleSheet("""
            border-top: 0px;
            border-bottom: 0px;
        """)

        self.checkbox1 = QCheckBox(self)
        self.checkbox1.move(55, 215)
        self.checkbox1.resize(17, 17)
        self.checkbox1.stateChanged.connect(self.uncheck)
        self.checkbox2 = QCheckBox(self)
        self.checkbox2.move(175, 215)
        self.checkbox2.resize(17, 17)
        self.checkbox2.stateChanged.connect(self.uncheck)
        self.checkbox3 = QCheckBox(self)
        self.checkbox3.move(295, 215)
        self.checkbox3.resize(17, 17)
        self.checkbox3.stateChanged.connect(self.uncheck)
        self.checkbox4 = QCheckBox(self)
        self.checkbox4.move(415, 215)
        self.checkbox4.resize(17, 17)
        self.checkbox4.stateChanged.connect(self.uncheck)
        self.checkbox5 = QCheckBox(self)
        self.checkbox5.move(535, 215)
        self.checkbox5.resize(17, 17)
        self.checkbox5.stateChanged.connect(self.uncheck)

        self.text1 = QLabel(self)
        self.text1.setText('Как прошёл день?')
        self.text1.setStyleSheet("""
                            color: white;
                            font-family: Impact;
                            font-size: 30px;
                            border: transparent;
                        """)
        self.text1.move(50, 240)

        self.day_description = QTextEdit(self)
        self.day_description.move(50, 290)
        self.day_description.resize(500, 60)
        self.day_description.setPlaceholderText('Введите текст')
        self.day_description.setStyleSheet("""
                            color: white;
                            font-family: Impact;
                            background-color: rgb(20, 43, 22);
                            font-size: 20px;
                            border: transparent;
                        """)


        self.done_btn = QPushButton(self)
        self.done_btn.move(370, 375)
        self.done_btn.resize(180, 180)
        self.done_btn.setText('Готово')
        self.done_btn.setStyleSheet("""
                        QPushButton {color: rgb(20, 43, 22);
                            background-color: white;
                            font-family: Impact;
                            font-size: 50px;
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
        self.done_btn.clicked.connect(self.add_day_to_db)

        self.photo1_btn = QPushButton(self)
        self.photo1_btn.move(50, 375)
        self.photo1_btn.setIcon(QIcon('photos/photo130.png'))
        self.photo1_btn.setIconSize(QSize(130, 130))
        self.photo1_btn.resize(130, 130)
        self.photo1_btn.setStyleSheet("""
                    QPushButton {color: white;
                            background-color: rgb(10, 10, 10);
                            font-family: Impact;
                            font-size: 100px;
                            border: transparent;;
                        }
                        QPushButton:hover {
                            background-color: rgb(40, 63, 42);
                        }
                        QPushButton:pressed {
                            background-color: rgb(70, 93, 72);
                        }
                             """)
        self.photo1_btn.clicked.connect(self.open_photo)

        self.photo2_btn = QPushButton(self)
        self.photo2_btn.move(205, 375)
        self.photo2_btn.setIcon(QIcon('photos/photo130.png'))
        self.photo2_btn.setIconSize(QSize(130, 130))
        self.photo2_btn.resize(130, 130)
        self.photo2_btn.setStyleSheet("""
                            QPushButton {color: white;
                                    background-color: rgb(10, 10, 10);
                                    font-family: Impact;
                                    font-size: 100px;
                                    border: transparent;;
                                }
                                QPushButton:hover {
                                    background-color: rgb(40, 63, 42);
                                }
                                QPushButton:pressed {
                                    background-color: rgb(70, 93, 72);
                                }
                                     """)
        self.photo2_btn.clicked.connect(self.open_photo)

        self.add_photo1_btn = QPushButton(self)
        self.add_photo1_btn.move(98, 520)
        self.add_photo1_btn.resize(40, 40)
        self.add_photo1_btn.setText('+')
        self.add_photo1_btn.setStyleSheet("""
                                QPushButton {color: rgb(20, 43, 22);
                                    background-color: white;
                                    font-family: Impact;
                                    font-size: 30px;
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
        self.add_photo1_btn.clicked.connect(self.add_photo)

        self.add_photo2_btn = QPushButton(self)
        self.add_photo2_btn.move(251, 520)
        self.add_photo2_btn.resize(40, 40)
        self.add_photo2_btn.setText('+')
        self.add_photo2_btn.setStyleSheet("""
                                        QPushButton {color: rgb(20, 43, 22);
                                            background-color: white;
                                            font-family: Impact;
                                            font-size: 30px;
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
        self.add_photo2_btn.clicked.connect(self.add_photo)

        # Проверка на наличие даты в БД
        con = sqlite3.connect("diary.sqlite")
        cur = con.cursor()
        self.list_of_dates = cur.execute("""SELECT date FROM data_table WHERE date""").fetchall()
        for i in range(len(self.list_of_dates)):
            self.list_of_dates[i] = self.list_of_dates[i][0]

        if str(self.date) in self.list_of_dates:
            # Данные из БД выводятся на экран
            self.day_in_DB = True
            con = sqlite3.connect("diary.sqlite")
            cur = con.cursor()
            query = "SELECT * FROM data_table WHERE date = '{date}'".format(date=str(self.date))
            day_information = cur.execute(query).fetchall()[0]

            if day_information[1] == 5:
                self.checkbox1.setCheckState(True)
            elif day_information[1] == 4:
                self.checkbox2.setCheckState(True)
            elif day_information[1] == 3:
                self.checkbox3.setCheckState(True)
            elif day_information[1] == 2:
                self.checkbox4.setCheckState(True)
            elif day_information[1] == 1:
                self.checkbox5.setCheckState(True)

            if day_information[2]:
                self.day_description.setText(day_information[2])

            self.photo1_btn.setIcon(QIcon(day_information[3]))
            self.photo1_btn.setIconSize(QSize(130, 130))

            self.photo2_btn.setIcon(QIcon(day_information[4]))
            self.photo2_btn.setIconSize(QSize(130, 130))

            self.mood = day_information[1]
            self.photo1_name = day_information[3]
            self.photo2_name = day_information[4]
        else:
            self.day_in_DB = False

    def add_day_to_db(self):
        # Добавление данных в БД
        date = self.date
        mood = self.mood
        note = self.day_description.toPlainText()
        photo1 = str(self.photo1_name)
        photo2 = str(self.photo2_name)

        if self.day_in_DB:
            query = "UPDATE data_table " \
                    "SET mood = {mood}, note = '{note}', photo_1 = '{photo1}', photo_2 = '{photo2}' " \
                    "WHERE date = '{date}'".format(date=date,
                                                 mood=mood,
                                                 note=note,
                                                 photo1=photo1,
                                                 photo2=photo2)
        else:
            query = "INSERT INTO data_table(date, mood, note, photo_1, photo_2) " \
                    "VALUES('{date}', {mood}, '{note}', '{photo1}', '{photo2}')".format(date=date,
                                                                                        mood=mood,
                                                                                        note=note,
                                                                                        photo1=photo1,
                                                                                        photo2=photo2)
        con = sqlite3.connect("diary.sqlite")
        cur = con.cursor()

        cur.execute(query)
        con.commit()
        self.close()

    def uncheck(self, state):
        # Выбирается только одно настроение
        if state == Qt.Checked:
            if self.sender() == self.checkbox1:
                self.mood = 5
                self.checkbox2.setChecked(False)
                self.checkbox3.setChecked(False)
                self.checkbox4.setChecked(False)
                self.checkbox5.setChecked(False)
            elif self.sender() == self.checkbox2:
                self.mood = 4
                self.checkbox1.setChecked(False)
                self.checkbox3.setChecked(False)
                self.checkbox4.setChecked(False)
                self.checkbox5.setChecked(False)
            elif self.sender() == self.checkbox3:
                self.mood = 3
                self.checkbox1.setChecked(False)
                self.checkbox2.setChecked(False)
                self.checkbox4.setChecked(False)
                self.checkbox5.setChecked(False)
            elif self.sender() == self.checkbox4:
                self.mood = 2
                self.checkbox1.setChecked(False)
                self.checkbox3.setChecked(False)
                self.checkbox2.setChecked(False)
                self.checkbox5.setChecked(False)
            elif self.sender() == self.checkbox5:
                self.mood = 1
                self.checkbox1.setChecked(False)
                self.checkbox3.setChecked(False)
                self.checkbox4.setChecked(False)
                self.checkbox2.setChecked(False)

    def add_photo(self):
        # Изменение фотографии на выбранную пользователем, перенос фотографии в папку photos
        if self.sender() == self.add_photo1_btn:
            self.photo1_name = QFileDialog.getOpenFileName(
                self, 'Выбрать картинку', '',
                'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
            self.photo1_btn.setIcon(QIcon(self.photo1_name))
            self.photo1_btn.setIconSize(QSize(130, 130))
            shutil.copyfile(self.photo1_name, "./photos/" + self.photo1_name.split("/")[-1])
            self.photo1_name = 'photos/' +  self.photo1_name.split("/")[-1]
        elif self.sender() == self.add_photo2_btn:
            self.photo2_name = QFileDialog.getOpenFileName(
                self, 'Выбрать картинку', '',
                'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
            self.photo2_btn.setIcon(QIcon(self.photo2_name))
            self.photo2_btn.setIconSize(QSize(130, 130))
            shutil.copyfile(self.photo2_name, "./photos/" + self.photo2_name.split("/")[-1])
            self.photo2_name = 'photos/' +  self.photo2_name.split("/")[-1]

    def open_photo(self):
        # Фотогорафия открывается в полном размере в отдельном окне
        if self.sender() == self.photo1_btn:
            photo_dlg = PhotoDialog(self, self.photo1_name)
            photo_dlg.exec()
        elif self.sender() == self.photo2_btn:
            photo_dlg = PhotoDialog(self, self.photo2_name)
            photo_dlg.exec()

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
