from scipy.spatial.distance import cosine

import librosa.display
import matplotlib.pyplot as plt
import numpy as np

import Console

class Spectrogram_Analysis():

    def normalize_spectrogram(spectrogram, min_val=0, max_val=1):
        spectrogram_min = spectrogram.min()
        spectrogram_max = spectrogram.max()
        normalized_spectrogram = (spectrogram - spectrogram_min) / (spectrogram_max - spectrogram_min)
        normalized_spectrogram = normalized_spectrogram * (max_val - min_val) + min_val
        return normalized_spectrogram


    def cosinus_compare_spectrgrum(self, y1, y2, sr1, sr2):

        if len(y1) > len(y2):
            y1 = y1[:len(y2)]
        elif len(y1) < len(y2):
            y2 = y2[:len(y1)]

        # Претворення в спектрограми
        S1 = librosa.stft(y1)
        S2 = librosa.stft(y2)
        # Амплітудний спектр
        S1_db = librosa.amplitude_to_db(np.abs(S1), ref=np.max)
        S2_db = librosa.amplitude_to_db(np.abs(S2), ref=np.max)

        S1_db = Spectrogram_Analysis.normalize_spectrogram(S1_db)
        S2_db = Spectrogram_Analysis.normalize_spectrogram(S2_db)

        # Перетвореня спектрограм у вектори
        vec1 = S1_db.flatten()
        vec2 = S2_db.flatten()

        cos_sim = 1 - cosine(vec1, vec2)

        return cos_sim
