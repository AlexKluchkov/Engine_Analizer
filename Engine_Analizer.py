from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QMenuBar, QMenu, QStatusBar, QAction, QLabel

import sys
import librosa
import librosa.display
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np

import Spectrogram_Analysis
import Console

class Window(QMainWindow):
    top_indent = 20                     #Відступ зверху зображення спектограм
    indent_between_spectrogram = 10     #Відступ між двума зображеннями спектограм при порівнянні

    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        font = QtGui.QFont()
        font.setPointSize(10)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(0, 0, 800, self.top_indent)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setTitle("Файл")
        self.menuAnalize = QMenu(self.menubar)
        self.menuAnalize.setTitle("Проаналізувати")

        self.actionAnalize = QAction()
        self.actionAnalize.setText("Порівняти")
        self.actionAnalize.triggered.connect(self.compare_spectrogram)
        self.menuAnalize.addAction(self.actionAnalize)
        self.actionSpectr = QAction()
        self.actionSpectr.setText("Спектр")
        self.actionSpectr.triggered.connect(self.spectr)
        self.menuAnalize.addAction(self.actionSpectr)

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
        self.label.move(0, self.top_indent)
        self.label.resize(640, 480)

        self.label2 = QLabel(self)
        self.label2.move(self.label.width() + 5, self.top_indent)
        self.label2.resize(0, 0)

        self.setWindowTitle("Аналіз спектрограми двигуна")
        self.resize(800, 500)

        self.ConsoleWindow = Console.Console()
        self.ConsoleWindow.show()


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
            return y, sr
        else:
            return None, None


    def spectr(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Виберіть файл", "", "Усі файли (*);;Текстові файли (*.txt)", options=options)
        if file_path:
            #обчислення спектра
            y, sr = librosa.load(file_path, sr=None)
            n = len(y)
            fft = np.fft.fft(y)
            magnitude = np.abs(fft)  # Амплитуди
            frequency = np.fft.fftfreq(n, 1/sr)  # Частоти
    
            # Лишаємо тільки позитивні частоти
            positive_freqs = frequency[:n//2]
            positive_magnitude = magnitude[:n//2]
        
            # Візуалізація спектра
            fig, ax = plt.subplots(1)
            plt.plot(positive_freqs, positive_magnitude, color='blue')
            plt.title("Залежність інтенсивності сигналу від частоти")
            plt.xlabel("Частота (Гц)")
            plt.ylabel("Інтенсивність (Амплітуда)")
            fig.savefig("spectrum.png")
            pixmap = QtGui.QPixmap("spectrum.png")
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True) #маштабування зображення до розміру label

    def load_file(self):
        self.y, self.sr = self.download_file(self.label)
    
    def compare_spectrogram(self):
        if(self.label.pixmap() is not None):            # Якщо є перше зображення
            y2, sr2= self.download_file(self.label2)             # завантажуємо друге
            if(self.label2.pixmap() is not None):       # Якщо є друге зображення
                self.label.resize(int(self.width() / 2), int(self.height() / 2))    #змінюємо розмір
                self.label2.move(self.label.width(), self.top_indent)
                self.label2.resize(self.label.width(), self.label.height())

                SpectrAnalysis = Spectrogram_Analysis.Spectrogram_Analysis()
                cos_sim = SpectrAnalysis.cosinus_compare_spectrgrum(self.y, y2, self.sr, sr2)
                self.ConsoleWindow.GetAnswer(f"Cosine Similarity: {cos_sim}")

        else:
            self.ConsoleWindow.GetAnswer("Помилка! Завантажте файл!")
            

    def resizeEvent(self, event):
        self.resize_label()
        super().resizeEvent(event)

    def resize_label(self):
        if(self.label2.width() != 0):
            delta_width = self.width() - (self.label.width() + self.label2.width() + 5)
            delta_height = self.height() - (self.label.height() + self.top_indent)
            png_width = self.label.width() + int(min(delta_width, delta_height)/2)  # Зміна ширини (2 малюнки)
            png_height = self.label.height() + int(min(delta_width, delta_height)/2)  # Зміна висоти
            self.label.resize(png_width, png_height)
            self.label2.move(self.label.width() + self.indent_between_spectrogram, self.top_indent)
            self.label2.resize(png_width, png_height)  # width, height
        else:
            delta_width = self.width() - self.label.width()
            delta_height = self.height() - (self.label.height() + self.top_indent)
            png_width = self.label.width() + min(delta_width, delta_height)  # Зміна ширини
            png_height = self.label.height() + min(delta_width, delta_height)  # Зміна висоти
            self.label.resize(png_width, png_height)  # width, height

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Engine_Analizer_App = Window()
    Engine_Analizer_App.show()
    sys.exit(app.exec_())
