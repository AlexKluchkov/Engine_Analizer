from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenuBar, QMenu, QAction, QLabel

import os
import sys
import librosa
import librosa.display
import matplotlib.pyplot as plt

import numpy as np

import Spectrogram_Analysis
import Console

class Engine_Analizer(QMainWindow):
    top_indent = 20                     
    indent_between_spectrogram = 10    

    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        font = QtGui.QFont()
        font.setPointSize(10)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(0, 0, 800, self.top_indent)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setTitle("File")
        self.menuAnalize = QMenu(self.menubar)
        self.menuAnalize.setTitle("Analyze")

        self.actionAnalize = QAction()
        self.actionAnalize.setText("Recording analysis")
        self.actionAnalize.triggered.connect(self.analize_spectrogram)
        self.menuAnalize.addAction(self.actionAnalize)
        self.actionСompareSpectrogrum = QAction()
        self.actionСompareSpectrogrum.setText("Compare spectrograms")
        self.actionСompareSpectrogrum.triggered.connect(self.compare_spectrogram)
        self.menuAnalize.addAction(self.actionСompareSpectrogrum)
        self.actionСompareSpectr = QAction()
        self.actionСompareSpectr.setText("Compare spectra")
        self.actionСompareSpectr.triggered.connect(self.compareSpectr)
        self.menuAnalize.addAction(self.actionСompareSpectr)

        self.setMenuBar(self.menubar)

        #self.statusbar = QStatusBar()
        #self.setStatusBar(self.statusbar)

        self.actionDownload = QAction()
        self.actionDownload.setText("Download file as spectrogram")
        self.actionDownload.triggered.connect(self.load_spectrogram)
        self.menuFile.addAction(self.actionDownload)
        self.actionSpectr = QAction()
        self.actionSpectr.setText("Download file as spectrum")
        self.actionSpectr.triggered.connect(self.load_spectr)
        self.menuFile.addAction(self.actionSpectr)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAnalize.menuAction())
        
        self.label = QLabel(self)
        self.label.move(0, self.top_indent)
        self.label.resize(640, 480)

        self.label2 = QLabel(self)
        self.label2.move(self.label.width() + 5, self.top_indent)
        self.label2.resize(0, 0)

        self.setWindowTitle("Analysis of the spectrogram of the car's operation")
        self.resize(800, 500)

        self.ConsoleWindow = Console.Console()
        self.ConsoleWindow.show()


    def download_spectrogrum(self, label):
        # Діалог вибору файла
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "Sound files (*.mp3)", options=options)
        if file_path:
            #calculate spectrogram
            y, sr = librosa.load(file_path, sr=None)
            D = librosa.stft(y)
            S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
            # Spectrogram visualization
            fig, ax = plt.subplots(1)
            librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log', cmap='magma')
            plt.colorbar(format='%+2.0f dB')
            plt.title(os.path.basename(file_path))
            plt.ylabel('Frequency')
            
            fig.savefig("spectrum.png")
            pixmap = QtGui.QPixmap("spectrum.png")
            label.setPixmap(pixmap)
            label.setScaledContents(True)   
            return y, sr
        else:
            return None, None

    def download_spectr(self, label):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "Sound files (*.mp3)", options=options)
        if file_path:
            #spectrum calculation
            y, sr = librosa.load(file_path, sr=None)
            n = len(y)
            fft = np.fft.fft(y)
            magnitude = np.abs(fft)  # Амплитуди
            frequency = np.fft.fftfreq(n, 1/sr)  # Частоти
    
            positive_freqs = frequency[:n//2]
            positive_magnitude = magnitude[:n//2]
        
            # Spectrum visualization
            fig, ax = plt.subplots(1)
            plt.plot(positive_freqs, positive_magnitude, color='blue')
            #plt.xscale('log')
            plt.yscale('log')
            plt.title(os.path.basename(file_path))
            plt.xlabel("Частота (Гц)")
            plt.ylabel("Інтенсивність (Амплітуда)")
            fig.savefig("spectrum.png")
            pixmap = QtGui.QPixmap("spectrum.png")
            label.setPixmap(pixmap)
            label.setScaledContents(True) #маштабування зображення до розміру label
            return y, sr
        else:
            return None, None

    def load_spectr(self):
        self.y, self.sr = self.download_spectr(self.label)

    def compareSpectr(self):
        if(self.label.pixmap() is not None):            
            y2, sr2 = self.download_spectr(self.label2)
            if(self.label2.pixmap() is not None):       
                self.label.resize(int(self.width() / 2), int(self.height() / 2))    
                self.label2.move(self.label.width(), self.top_indent)
                self.label2.resize(self.label.width(), self.label.height())
                SpectrAnalysis = Spectrogram_Analysis.Spectrogram_Analysis()
                cos_sim = SpectrAnalysis.cosinus_compare_spectrgrum(self.y, y2, self.sr, sr2)
                self.ConsoleWindow.GetAnswer(f"Spectra are {cos_sim} % similar")
        else:
            self.ConsoleWindow.GetAnswer("Error! Load spectrum!")

    def load_spectrogram(self):
        self.y, self.sr = self.download_spectrogrum(self.label)
    
    def compare_spectrogram(self):
        if(self.label.pixmap() is not None):            
            y2, sr2= self.download_spectrogrum(self.label2)             
            if(self.label2.pixmap() is not None):       
                self.label.resize(int(self.width() / 2), int(self.height() / 2))    #змінюємо розмір
                self.label2.move(self.label.width(), self.top_indent)
                self.label2.resize(self.label.width(), self.label.height())

                SpectrAnalysis = Spectrogram_Analysis.Spectrogram_Analysis()
                cos_sim = SpectrAnalysis.cosinus_compare_spectrgrum(self.y, y2, self.sr, sr2)
                self.ConsoleWindow.GetAnswer(f"Spectrograms are {cos_sim * 100} % similar")
        else:
            self.ConsoleWindow.GetAnswer("Error! Load spectrogram!")
            
    def analize_spectrogram(self):
        if(self.label.pixmap() is not None):            
            Breakdowns = []
            SpectrAnalysis = Spectrogram_Analysis.Spectrogram_Analysis()
            Breakdowns = SpectrAnalysis.Breakdown_Analysis(self.y, self.sr)
            if len(Breakdowns) != 0:
                self.ConsoleWindow.GetAnswer("Problem found ! " + ", ".join(Breakdowns) + "!")
            else:
                self.ConsoleWindow.GetAnswer(f"No problems!")
        else:
            self.ConsoleWindow.GetAnswer("Error! Load spectrogram!")

    def resizeEvent(self, event):
        self.resize_label()
        super().resizeEvent(event)

    def resize_label(self):
        if(self.label2.width() != 0):
            delta_width = self.width() - (self.label.width() + self.label2.width() + 5)
            delta_height = self.height() - (self.label.height() + self.top_indent)
            png_width = self.label.width() + int(min(delta_width, delta_height)/2)  
            png_height = self.label.height() + int(min(delta_width, delta_height)/2)  
            self.label.resize(png_width, png_height)
            self.label2.move(self.label.width() + self.indent_between_spectrogram, self.top_indent)
            self.label2.resize(png_width, png_height)  # width, height
        else:
            delta_width = self.width() - self.label.width()
            delta_height = self.height() - (self.label.height() + self.top_indent)
            png_width = self.label.width() + min(delta_width, delta_height)  
            png_height = self.label.height() + min(delta_width, delta_height)  
            self.label.resize(png_width, png_height)  # width, height


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Engine_Analizer_App = Engine_Analizer()
    Engine_Analizer_App.show()
    sys.exit(app.exec_())
