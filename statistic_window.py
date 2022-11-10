import sys

import sqlite3
from PyQt5.QtWidgets import QWidget, QPushButton, QDialog, QMainWindow, QApplication, QHBoxLayout
from PyQt5.QtChart import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor


class StatisticsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Создаётся интефейс
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setWindowTitle('Статистика')
        self.setGeometry(720, 100, 680, 500)
        self.setWindowTitle('Дневник настроений')
        self.setStyleSheet("""
            background: rgb(10, 10, 10);
            border: 2px solid rgb(108, 148, 112);
        """)

        self.panel = QWidget(self)
        self.panel.setGeometry(0, 0, 680, 30)
        self.panel.setStyleSheet("""
                    background: rgb(108, 148, 112);
                    border: transparent;
                """)

        self.close_btn = QPushButton(self)
        self.close_btn.resize(50, 30)
        self.close_btn.move(630, 0)
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
        self.collapse_btn.move(580, 0)
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

        self.create_bar()

    def create_bar(self):
        # Создание диаграммы на основе данных из БД
        set0 = QBarSet("Настроение")
        set0.setColor(QColor(0, 255, 0))
        set1 = QBarSet(".")
        set1.setColor(QColor(255, 255, 255))

        con = sqlite3.connect("diary.sqlite")
        cur = con.cursor()
        list_of_moods = cur.execute("""SELECT mood FROM data_table WHERE date""").fetchall()
        for i in range(len(list_of_moods)):
            list_of_moods[i] = list_of_moods[i][0]
        count_perfect_mood = 0
        count_good_mood = 0
        count_normal_mood = 0
        count_soso_mood = 0
        count_bad_mood = 0
        for i in list_of_moods:
            if i == 5:
                count_perfect_mood += 1
            elif i == 4:
                count_good_mood += 1
            elif i == 3:
                count_normal_mood += 1
            elif i == 2:
                count_soso_mood += 1
            elif i == 1:
                count_bad_mood += 1

        sum1_mood = count_bad_mood + count_soso_mood + count_normal_mood + count_good_mood
        sum2_mood = count_bad_mood + count_soso_mood + count_normal_mood + count_perfect_mood
        sum3_mood = count_bad_mood + count_soso_mood + count_perfect_mood + count_good_mood
        sum4_mood = count_bad_mood + count_perfect_mood + count_normal_mood + count_good_mood
        sum5_mood = count_perfect_mood + count_soso_mood + count_normal_mood + count_good_mood

        set0 << count_perfect_mood << count_good_mood << count_normal_mood << count_soso_mood << count_bad_mood
        set1 << sum1_mood << sum2_mood << sum3_mood << sum4_mood << sum5_mood

        series = QPercentBarSeries()
        series.append(set0)
        series.append(set1)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Настроения за всё время")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ["Прекрасное", "Хорошее", "Нормальное", "Такое себе", "Плохое"]
        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart, parent=self)
        chartView.setRenderHint(QPainter.Antialiasing)
        chartView.setGeometry(0, 30, 680, 470)
        chartView.setStyleSheet("border-top: 0px;")


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
