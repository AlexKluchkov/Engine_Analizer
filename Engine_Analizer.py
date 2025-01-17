from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QMenuBar, QMenu, QStatusBar, QAction, QLabel

import sys
import librosa
import librosa.display
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        font = QtGui.QFont()
        font.setPointSize(10)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(0, 0, 800, 21)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setTitle("Файл")
        self.menuAnalize = QMenu(self.menubar)
        self.menuAnalize.setTitle("Проаналізувати")

        self.actionAnalize = QAction()
        self.actionAnalize.setText("Порівняти")
        self.actionAnalize.triggered.connect(self.compare_spectrogram)
        self.menuAnalize.addAction(self.actionAnalize)

        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.actionDownload = QAction()
        self.actionDownload.setText("Завантажити файл")
        self.actionDownload.triggered.connect(self.load_file)
        self.menuFile.addAction(self.actionDownload)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAnalize.menuAction())
        
        self.label = QLabel(self)
        self.label.move(0, 20)
        self.label.resize(640, 480)

        self.label2 = QLabel(self)
        self.label2.move(self.label.width() + 5, 20)
        self.label2.resize(0, 0)

        self.setWindowTitle("Аналіз спектрограми двигуна")
        self.resize(800, 500)


    def download_file(self, label):
        # Діалог вибору файла
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Виберіть файл", "", "Усі файли (*);;Текстові файли (*.txt)", options=options)
        if file_path:
            #обчислення спектрограми
            y, sr = librosa.load(file_path, sr=None)
            D = librosa.stft(y)
            S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
            # Візуализація спектрограми
            fig, ax = plt.subplots(1)
            librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log', cmap='magma')
            plt.colorbar(format='%+2.0f дБ')
            plt.title('Спектрограма')
            plt.xlabel('Час')
            plt.ylabel('Частота')
            
            fig.savefig("spectrum.png")
            pixmap = QtGui.QPixmap("spectrum.png")
            label.setPixmap(pixmap)
            label.setScaledContents(True) #маштабування зображення до розміру label
    def load_file(self):
        self.download_file(self.label)
    
    def compare_spectrogram(self):
        self.download_file(self.label2)
        self.label.resize(320, 240)
        self.label2.move(self.label.width(), 20)
        self.label2.resize(320, 240)
        self.resize(700, 500)

    def resizeEvent(self, event):
        self.resize_label()
        super().resizeEvent(event)

    def resize_label(self):
        if(self.label2.width() != 0):
            delta_width = self.width() - (self.label.width() + self.label2.width() + 5)
            delta_height = self.height() - (self.label.height() + 20)
            png_width = self.label.width() + int(min(delta_width, delta_height)/2)  # Зміна ширини (2 малюнки)
            png_height = self.label.height() + int(min(delta_width, delta_height)/2)  # Зміна висоти
            self.label.resize(png_width, png_height)  # width, height
            self.label2.move(self.label.width() + 5, 20)
            self.label2.resize(png_width, png_height)  # width, height
        else:
            delta_width = self.width() - self.label.width()
            delta_height = self.height() - (self.label.height() + 20)
            png_width = self.label.width() + min(delta_width, delta_height)  # Зміна ширини
            png_height = self.label.height() + min(delta_width, delta_height)  # Зміна висоти
            self.label.resize(png_width, png_height)  # width, height

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Engine_Analizer_App = Window()
    Engine_Analizer_App.show()
    sys.exit(app.exec_())
