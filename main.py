import sys
import qtmodern.windows
import qtmodern.styles
import numpy as np
from PyQt5.QtGui import QPixmap, QColor, QFont
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QLabel, QFileDialog, QPushButton, QSlider, QColorDialog, QTextEdit
from PIL import Image



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.img = ''
        self.label = QLabel(self.window())
        self.label.resize(670, 500)
        self.label.move(10, 0)
        self.pixmap = QPixmap()
        self.col = 255
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(900, 550)
        self.pos()
        self.center()
        self.setWindowTitle('Center')
        self.filename = ''

        self.choose_img = QPushButton('Открыть', self)
        self.choose_img.move(700, 0)
        self.choose_img.clicked.connect(self.open_on_click)

        self.save_img = QPushButton('Сохранить', self)
        self.save_img.move(800, 0)
        self.save_img.resize(90, 27)
        self.save_img.clicked.connect(self.save_on_click)

        self.border = QTextEdit(self)
        self.border.move(700, 50)
        self.border.resize(50, 23)
        self.border.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.border.setText('128')

        self.bin_0s_and_1s = QPushButton('0 and 1', self)
        self.bin_0s_and_1s.move(780, 50)
        self.bin_0s_and_1s.resize(110, 25)
        self.bin_0s_and_1s.clicked.connect(self.to_0s_and_1s_on_click)

        self.border1s = QTextEdit(self)
        self.border1s.move(700, 80)
        self.border1s.resize(50, 23)
        self.border1s.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.border1s.setText('128')

        self.bin_1s_and_1s = QPushButton('-1 and 1', self)
        self.bin_1s_and_1s.move(780, 80)
        self.bin_1s_and_1s.resize(110, 25)
        self.bin_1s_and_1s.clicked.connect(self.to_1s_on_click)

        self.border_from = QTextEdit(self)
        self.border_from.move(700, 115)
        self.border_from.resize(40, 25)
        self.border_from.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.border_from.setText('128')

        self.border_to = QTextEdit(self)
        self.border_to.move(750, 115)
        self.border_to.resize(40, 25)
        self.border_to.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.border_to.setText('128')

        self.bin_limit = QPushButton('Limit', self)
        self.bin_limit.move(800, 115)
        self.bin_limit.resize(90, 25)
        self.bin_limit.clicked.connect(self.to_1s_on_click)

        self.color_picker = QPushButton('Open color dialog', self)
        self.color_picker.setToolTip('Opens color dialog')
        self.color_picker.move(700, 150)
        self.color_picker.resize(190, 25)
        self.color_picker.clicked.connect(self.color_dialog_on_click)

        self.set_fonts()

        self.show()

    def set_fonts(self):
        font = 'SF Pro Display'
        self.bin_0s_and_1s.setFont(QFont(font, 11))
        self.bin_1s_and_1s.setFont(QFont(font, 11))
        self.bin_limit.setFont(QFont(font, 11))
        self.save_img.setFont(QFont(font, 11))
        self.choose_img.setFont(QFont(font, 11))
        self.color_picker.setFont(QFont(font, 11))
        self.border.setFont(QFont(font, 11))
        self.border1s.setFont(QFont(font, 11))
        self.border_from.setFont(QFont(font, 11))
        self.border_to.setFont(QFont(font, 11))

    def color_dialog_on_click(self):
        self.open_color_dialog()

    def open_color_dialog(self):
        col = QColorDialog.getColor()
        r = col.red()
        g = col.green()
        b = col.blue()
        self.col = self.to_grey_shadow(r, g, b)

    def to_grey_shadow(self, r, g, b):
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def to_0s_and_1s_on_click(self):
        col = Image.open(self.filename)
        gray = col.convert('L')
        bw = np.asarray(gray).copy()
        border = int(self.border.toPlainText())
        bw[bw < border] = 0  # Black
        bw[bw >= border] = self.col  # Color
        img = Image.fromarray(bw)
        self.label.setPixmap(img.toqpixmap().scaled(670, 500))
        self.show()
        bw[bw < border] = 0
        bw[bw >= border] = 1
        np.savetxt('binary_0s_and_1s.txt', bw, fmt='%i', delimiter=",")

    def to_1s_on_click(self):
        col = Image.open(self.filename)
        gray = col.convert('L')
        bw = np.asarray(gray).copy()
        border = int(self.border.toPlainText())
        bw[bw < border] = 0  # Black
        bw[bw >= border] = self.col  # Color
        img = Image.fromarray(bw)
        self.label.setPixmap(img.toqpixmap().scaled(670, 500))
        self.show()


        # self.w = []
        # for x in np.nditer(bw, op_flags=['readwrite']):
        #     if x == 0:
        #         self.w.extend([-1])
        #     else:
        #         self.w.extend([1])
        # print("here")
        # # print_to_
        #
        # with open("w.txt", "w") as f:
        #     for i in self.w:
        #         f.write(str(i))
        #         f.write(',')
        # f.close()

        # print("here1")
        # for i in range(len(bw)):
        #     if bw[i] == 0:
        #         print("yea")
        # print(w)

        # np.savetxt('binarys.txt', bw, fmt='%i', delimiter=",")
        # bw[bw == 0] = -1
        # bw[bw >= border] = 1


        # for i in range(len(bw)):
        #     if bw[i] == 0:
        #         bw[i] = -1
        #     else:
        #         bw[i] = 1

        # for i in bw:
        #     print(i)
        # np.savetxt('binarys_after.txt', bw, fmt='%s', delimiter=",")
        # np.savetxt('binary_1s.txt', bw, fmt='%s', delimiter=",")

    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                       "Images (*.jpg *.jpeg *.png)", options=options)
        if self.filename:
            self.pixmap = QPixmap(self.filename).scaled(670, 500)

    def open_on_click(self):
        self.open_file_name_dialog()
        self.label.setPixmap(self.pixmap)

    def save_on_click(self):
        self.save_file_dialog()

    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Images (*.jpg *.jpeg *.png)", options=options)
        if filename:
            self.label.pixmap().save(filename)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(win)
    mw.show()

    sys.exit(app.exec_())