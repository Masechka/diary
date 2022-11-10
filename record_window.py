from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QDialog, QTextEdit, QInputDialog, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QTimer
import sqlite3
import time
import shutil
from photo_dialog import PhotoDialog


class RecordDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_date)
        self.buf_date = ''
        self.mood = 0
        self.valid_date = ''
        self.photo1_name = 'photos/photo140.png'
        self.photo2_name = 'photos/photo140.png'
        self.timer.start()
        self.initUI()

    def initUI(self):
        # Создаётся интефейс
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground)

        self.setGeometry(720, 100, 400, 800)
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
        self.close_btn.move(350, 0)
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
        self.collapse_btn.move(300, 0)
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

        self.yyyymmdd = QLineEdit(self)
        self.yyyymmdd.move(50, 40)
        self.yyyymmdd.resize(155, 40)
        self.yyyymmdd.setPlaceholderText('ГГГГ-ММ-ДД')
        self.yyyymmdd.setStyleSheet("""
                    color: white;
                    font-family: Impact;
                    background-color: rgb(20, 43, 22);
                    font-size: 30px;
                    border: transparent;
                """)

        self.warning = QLabel(self)
        self.warning.setStyleSheet("""
                                    color: white;
                                    font-family: Impact;
                                    font-size: 14px;
                                    border: transparent;
                                """)
        self.warning.move(220, 50)
        self.warning.resize(170, 17)

        self.text1 = QLabel(self)
        self.text1.setText('Настроение в этот день')
        self.text1.setStyleSheet("""
                    color: white;
                    font-family: Impact;
                    font-size: 30px;
                    border: transparent;
                """)
        self.text1.move(50, 90)

        self.mood_btn = QPushButton(self)
        self.mood_btn.resize(150, 150)
        self.mood_btn.move(50, 140)
        self.mood_btn.setIcon(QIcon('unknown_mood.png'))
        self.mood_btn.setIconSize(QSize(150, 150))
        self.mood_btn.setStyleSheet("""
                    QPushButton {color: white;
                            background-color: rgb(10, 10, 10);
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
        self.mood_btn.clicked.connect(self.change_mood)

        self.text1 = QLabel(self)
        self.text1.setText('Запись')
        self.text1.setStyleSheet("""
                            color: white;
                            font-family: Impact;
                            font-size: 30px;
                            border: transparent;
                        """)
        self.text1.move(50, 300)

        self.day_description = QTextEdit(self)
        self.day_description.move(50, 350)
        self.day_description.resize(300, 90)
        self.day_description.setPlaceholderText('Введите текст')
        self.day_description.setStyleSheet("""
                                    color: white;
                                    font-family: Impact;
                                    background-color: rgb(20, 43, 22);
                                    font-size: 20px;
                                    border: transparent;
                                """)

        self.text2 = QLabel(self)
        self.text2.setText('Фотографии')
        self.text2.setStyleSheet("""
                                    color: white;
                                    font-family: Impact;
                                    font-size: 30px;
                                    border: transparent;
                                """)
        self.text2.move(50, 450)

        self.photo1_btn = QPushButton(self)
        self.photo1_btn.move(50, 500)
        self.photo1_btn.setIcon(QIcon('photos/photo140.png'))
        self.photo1_btn.setIconSize(QSize(140, 140))
        self.photo1_btn.resize(140, 140)
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
        self.photo2_btn.move(210, 500)
        self.photo2_btn.setIcon(QIcon('photos/photo140.png'))
        self.photo2_btn.setIconSize(QSize(140, 140))
        self.photo2_btn.resize(140, 140)
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
        self.add_photo1_btn.move(98, 655)
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
        self.add_photo2_btn.move(261, 655)
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

        self.save_btn = QPushButton(self)
        self.save_btn.move(50, 715)
        self.save_btn.resize(300, 50)
        self.save_btn.setText('Сохранить изменения')
        self.save_btn.setStyleSheet("""
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
        self.save_btn.clicked.connect(self.save_data)

        self.warning2 = QLabel(self)
        self.warning2.setStyleSheet("""
                                            color: white;
                                            font-family: Impact;
                                            font-size: 14px;
                                            border: transparent;
                                        """)
        self.warning2.move(50, 770)
        self.warning2.resize(300, 17)


    def check_date(self):
        self.date = self.yyyymmdd.text()
        if not self.buf_date == self.date:
            if len(self.date) == 10:
                # Дата проверяется на правильносьб длины
                ydm = self.date.split('-')
                if self.date.count('-') == 2 and len(ydm[0]) == 4 and len(ydm[1]) == 2 and len(ydm[2]) == 2:
                    # Дата проверяется на правильность написания
                    self.warning.setText('')
                    ydm = list(''.join(self.date.split('-')))
                    if ydm == list(filter(lambda num: num in self.NUMBERS, ydm)):
                        # Дата проверяется на наличие неправильных символов
                        try:
                            self.valid_date = time.strptime(self.date, '%Y-%m-%d')
                        except ValueError:
                            self.warning.setText('Дата введена некоректно!!!')
                            self.valid_date = ''
                            return
                        # Дата проверяется на существование
                        self.warning.setText('')
                        self.warning2.setText('')
                        con = sqlite3.connect("diary.sqlite")
                        cur = con.cursor()
                        self.list_of_dates = cur.execute("""SELECT date FROM data_table WHERE date""").fetchall()
                        for i in range(len(self.list_of_dates)):
                            self.list_of_dates[i] = self.list_of_dates[i][0]
                        if str(self.date) in self.list_of_dates:
                            # Дата проверяется на наличие в БД
                            # Данные из БД выводятся на экран
                            self.buf_date = self.valid_date
                            query = "SELECT * FROM data_table WHERE date = '{date}'".format(date=str(self.date))
                            day_information = cur.execute(query).fetchall()[0]

                            if day_information[1] == 5:
                                self.mood_btn.setIcon(QIcon('perfect_mood.png'))
                                self.mood_btn.setIconSize(QSize(150, 150))
                            elif day_information[1] == 4:
                                self.mood_btn.setIcon(QIcon('good_mood.png'))
                                self.mood_btn.setIconSize(QSize(150, 150))
                            elif day_information[1] == 3:
                                self.mood_btn.setIcon(QIcon('normal_mood.png'))
                                self.mood_btn.setIconSize(QSize(150, 150))
                            elif day_information[1] == 2:
                                self.mood_btn.setIcon(QIcon('so-so_mood.png'))
                                self.mood_btn.setIconSize(QSize(150, 150))
                            elif day_information[1] == 1:
                                self.mood_btn.setIcon(QIcon('bad_mood.png'))
                                self.mood_btn.setIconSize(QSize(150, 150))

                            if day_information[2]:
                                self.day_description.setText(day_information[2])

                            self.photo1_btn.setIcon(QIcon(day_information[3]))
                            self.photo1_btn.setIconSize(QSize(140, 140))

                            self.photo2_btn.setIcon(QIcon(day_information[4]))
                            self.photo2_btn.setIconSize(QSize(140, 140))

                            self.mood = day_information[1]
                            self.photo1_name = day_information[3]
                            self.photo2_name = day_information[4]
                            self.buf_date = self.date
                        else:
                            # Окно приводится к начальному виду
                            self.mood = 0
                            self.photo1_name = 'photos/photo140.png'
                            self.photo2_name = 'photos/photo140.png'

                            self.mood_btn.setIcon(QIcon('unknown_mood.png'))
                            self.mood_btn.setIconSize(QSize(150, 150))

                            self.day_description.setText('')

                            self.photo1_btn.setIcon(QIcon(self.photo1_name))
                            self.photo1_btn.setIconSize(QSize(140, 140))

                            self.photo2_btn.setIcon(QIcon(self.photo2_name))
                            self.photo2_btn.setIconSize(QSize(140, 140))
                            self.buf_date = self.date
                    else:
                        self.valid_date = ''
                        self.warning.setText('Дата введена некорректно!!!')
                else:
                    self.valid_date = ''
                    self.warning.setText('Дата введена некорректно!!!')
            else:
                self.valid_date = ''
                self.buf_date = self.valid_date
                return
        else:
            self.warning2.setText('')
            return

    def change_mood(self):
        # Изменение настроения на выбранное пользователем
        inp_dlg = QInputDialog(self)
        inp_dlg.setStyleSheet(""""background-color: rgb(20, 43, 22);""")
        mood, ok_pressed = inp_dlg.getItem(
            self, "Выберите настроение", "Выберете настроение",
            ("Прекрасное", "Хорошее", "Нормальное", "Такое себе", "Плохое"), 1, False)
        if ok_pressed:
            if mood == "Прекрасное":
                self.mood_btn.setIcon(QIcon('perfect_mood.png'))
                self.mood_btn.setIconSize(QSize(150, 150))
                self.mood = 5
            elif mood == "Хорошее":
                self.mood_btn.setIcon(QIcon('good_mood.png'))
                self.mood_btn.setIconSize(QSize(150, 150))
                self.mood = 4
            elif mood == "Нормальное":
                self.mood_btn.setIcon(QIcon('normal_mood.png'))
                self.mood_btn.setIconSize(QSize(150, 150))
                self.mood = 3
            elif mood == "Такое себе":
                self.mood_btn.setIcon(QIcon('so-so_mood.png'))
                self.mood_btn.setIconSize(QSize(150, 150))
                self.mood = 2
            elif mood == "Плохое":
                self.mood_btn.setIcon(QIcon('bad_mood.png'))
                self.mood_btn.setIconSize(QSize(150, 150))
                self.mood = 1

    def save_data(self):
        # Сохранение изменений в БД
        if self.valid_date:
            if self.mood:
                self.warning2.setText('')

                date = self.date
                mood = self.mood
                note = self.day_description.toPlainText()
                photo1 = str(self.photo1_name)
                photo2 = str(self.photo2_name)

                if str(self.date) in self.list_of_dates:
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
            else:
                self.warning2.setText('Настроение не выбрано! Выберите настроение')
                return
        else:
            self.warning2.setText('Дата введена некорректно!!! Введите другую')
            return

    def add_photo(self):
        # Изменение фотографии на выбранную пользователем, перенос фотографии в папку photos
        if self.sender() == self.add_photo1_btn:
            self.photo1_name = QFileDialog.getOpenFileName(
                self, 'Выбрать картинку', '',
                'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
            self.photo1_btn.setIcon(QIcon(self.photo1_name))
            self.photo1_btn.setIconSize(QSize(140, 140))
            shutil.copyfile(self.photo1_name, "./photos/" + self.photo1_name.split("/")[-1])
            self.photo1_name = 'photos/' +  self.photo1_name.split("/")[-1]
        elif self.sender() == self.add_photo2_btn:
            self.photo2_name = QFileDialog.getOpenFileName(
                self, 'Выбрать картинку', '',
                'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
            self.photo2_btn.setIcon(QIcon(self.photo2_name))
            self.photo2_btn.setIconSize(QSize(140, 140))
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
