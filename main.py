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

        self.choose_img = QPushButton('Open', self)
        self.choose_img.move(700, 0)
        self.choose_img.clicked.connect(self.open_on_click)

        self.save_img = QPushButton('Save', self)
        self.save_img.move(800, 0)
        self.save_img.resize(90, 27)
        self.save_img.clicked.connect(self.save_on_click)

        self.border = QTextEdit(self)
        self.border.move(700, 50)
        self.border.resize(50, 23)
        self.border.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.border.setText('128')

        self.bin_0s_and_1s = QPushButton('Binarization', self)
        self.bin_0s_and_1s.move(780, 50)
        self.bin_0s_and_1s.resize(110, 25)
        self.bin_0s_and_1s.clicked.connect(self.to_0s_and_1s_on_click)

        self.border1s = QTextEdit(self)
        self.border1s.move(700, 80)
        self.border1s.resize(50, 23)
        self.border1s.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.border1s.setText('128')

        self.bin_1s_and_1s = QPushButton('Bipol', self)
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
        self.bin_limit.clicked.connect(self.bounds_on_click)

        self.color_picker = QPushButton('Open color dialog', self)
        self.color_picker.setToolTip('Opens color dialog')
        self.color_picker.move(700, 150)
        self.color_picker.resize(190, 25)
        self.color_picker.clicked.connect(self.color_dialog_on_click)

        self.scale_from = QTextEdit(self)
        self.scale_from.move(50, 470)
        self.scale_from.resize(80, 25)
        self.scale_from.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scale_to = QTextEdit(self)
        self.scale_to.move(150, 470)
        self.scale_to.resize(80, 25)
        self.scale_to.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.choose_file = QPushButton('Choose File', self)
        self.choose_file.move(50, 500)
        self.choose_file.clicked.connect(self.choose_file_on_click)

        self.scale = QPushButton('Scale File', self)
        self.scale.move(150, 500)
        self.scale.clicked.connect(self.scale_on_click)

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
        self.choose_file.setFont(QFont(font, 11))
        self.scale.setFont(QFont(font, 11))
        self.scale_from.setFont(QFont(font, 11))
        self.scale_to.setFont(QFont(font, 11))

    def color_dialog_on_click(self):
        self.open_color_dialog()

    def open_color_dialog(self):
        color = QColorDialog.getColor()
        r = color.red()
        g = color.green()
        b = color.blue()
        # self.col = color.
        self.col = self.to_grey_shadow(r, g, b)

    def to_grey_shadow(self, r, g, b):
        return r * 299/1000 + g * 587/1000 + b * 114/1000

    def to_0s_and_1s_on_click(self):
        color = Image.open(self.filename)
        gray = color.convert('L')
        bw = np.asarray(gray).copy()
        border = int(self.border.toPlainText())
        bw[abs(bw[...] - self.col) >= border] = 0
        bw[abs(bw[...] - self.col) < border] = 255

        img = Image.fromarray(bw)
        self.label.setPixmap(img.toqpixmap().scaled(670, 500))
        self.show()
        bw[bw < border] = 1
        bw[bw >= border] = 0
        np.savetxt('binarization.txt', bw, fmt='%i', delimiter=",")

    def to_1s_on_click(self):
        col = Image.open(self.filename)
        gray = col.convert('L')
        bw = np.asarray(gray).copy()
        border = int(self.border.toPlainText())

        bw[abs(bw[...] - self.col) >= border] = 0
        bw[abs(bw[...] - self.col) < border] = 255

        b = bw.astype(int)
        b[b == 0] = -1
        b[b == 255] = 1
        np.savetxt('bipol.txt', b, fmt='%i', delimiter=",")

        img = Image.fromarray(bw)
        self.label.setPixmap(img.toqpixmap().scaled(670, 500))
        self.show()

    def bounds_on_click(self):
        col = Image.open(self.filename)
        gray = col.convert('L')
        bw = np.asarray(gray).copy()
        left_bound = int(self.border_from.toPlainText())
        print(left_bound)
        right_bound = int(self.border_to.toPlainText())
        sc = (right_bound - left_bound) / 255
        ca = bw.astype(float).copy()
        ra = left_bound + (255 - ca) * sc
        np.savetxt('after_a_b.txt', ra, fmt='%.2f', delimiter=",")

    def scale_on_click(self):
        scale = (int(self.scale_to.toPlainText()) - int(self.scale_from.toPlainText())) * 1.0 / (max(self.data) - min(self.data))
        ret_data = []
        for i in range(len(self.data)):
            c = int(self.scale_from.toPlainText()) + (self.data[i] - min(self.data)) * scale
            ret_data.append(c)
        with open('scale_data.txt', 'w') as file:
            for i in ret_data:
                file.write(str(i))
                file.write(' ')

    def choose_file_on_click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.scale_filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                       "Txt files (*.txt)", options=options)
        with open(self.scale_filename) as file:
            self.data = file.read().split(',')
        self.data = [x.strip(' ') for x in self.data]
        self.data = [int(x) for x in self.data]

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