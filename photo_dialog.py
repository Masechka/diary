from PyQt5.QtWidgets import QWidget, QPushButton, QDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image


class PhotoDialog(QDialog):
    def __init__(self, parent, photo_name):
        super().__init__(parent)
        self.photo_name = photo_name
        im = Image.open(self.photo_name)
        self.x, self.y = im.size
        self.initUI()

    def initUI(self):
        # Создание окна размером с фотографию и отображение фотографии
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground)

        self.setGeometry(100, 100, self.x, self.y + 30)
        self.setWindowTitle('Дневник настроений')
        self.setStyleSheet("""
            background: rgb(10, 10, 10);
            border: 2px solid rgb(108, 148, 112);
        """)

        self.panel = QWidget(self)
        self.panel.setGeometry(0, 0, self.x, 30)
        self.panel.setStyleSheet("""
                    background: rgb(108, 148, 112);
                    border: transparent;
                """)

        self.close_btn = QPushButton(self)
        self.close_btn.resize(50, 30)
        self.close_btn.move(self.x - 50, 0)
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
        self.collapse_btn.move(self.x - 100, 0)
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

        self.pixmap = QPixmap(self.photo_name)
        self.photo = QLabel(self)
        self.photo.move(0, 30)
        self.photo.resize(self.x, self.y)
        self.photo.setPixmap(self.pixmap)

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
