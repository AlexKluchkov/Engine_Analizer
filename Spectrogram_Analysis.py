from scipy.spatial.distance import cosine

import librosa.display
import matplotlib.pyplot as plt
import numpy as np

class Spectrogram_Analysis():

    def normalize_spectrogram(spectrogram, min_val=0, max_val=1):
        spectrogram_min = spectrogram.min()
        spectrogram_max = spectrogram.max()
        normalized_spectrogram = (spectrogram - spectrogram_min) / (spectrogram_max - spectrogram_min)
        normalized_spectrogram = normalized_spectrogram * (max_val - min_val) + min_val
        return normalized_spectrogram

    def cosinus_compare_spectrgrum(self, y1, y2, sr1, sr2):

        #start_time = 0  # начало обрезки в секундах
        #if(librosa.get_duration(y = y1, sr = sr1) < librosa.get_duration(y = y2, sr = sr2)):
        #    end_time = librosa.get_duration(y = y1, sr = sr1)    # конец обрезки в секундах
        #    # Преобразуем время в индексы с учетом частоты дискретизации
        #    start_sample = librosa.time_to_samples(start_time, sr=sr2)
        #    end_sample = librosa.time_to_samples(end_time, sr=sr2)
        #    # Обрезаем аудио
        #    y2 = y2[start_sample:end_sample]     #обрезаем y2
        #elif(librosa.get_duration(y = y1, sr = sr1) > librosa.get_duration(y = y2, sr = sr2)):
        #    end_time = librosa.get_duration(y = y2, sr = sr2)    # конец обрезки в секундах
        #    # Преобразуем время в индексы с учетом частоты дискретизации
        #    start_sample = librosa.time_to_samples(start_time, sr=sr1)
        #    end_sample = librosa.time_to_samples(end_time, sr=sr1)
        #    # Обрезаем аудио
        #    y1 = y1[start_sample:end_sample] #обрезаем y1

        output_length = max(len(y1), len(y2))
        
        if len(y1) > output_length:
            y1 = y1[:output_length]  # Обрезать
        else:
            y1 = np.pad(y1, (0, output_length - len(y1)), mode='constant')  # Дополнить нулями

        if len(y2) > output_length:
            y2 = y2[:output_length]  # Обрезать
        else:
            y2 = np.pad(y2, (0, output_length - len(y2)), mode='constant')  # Дополнить нулями

        # Преобразование в спектрограммы
        S1 = librosa.stft(y1)
        S2 = librosa.stft(y2)
        # Амплитудный спектр
        S1_db = librosa.amplitude_to_db(np.abs(S1), ref=np.max)
        S2_db = librosa.amplitude_to_db(np.abs(S2), ref=np.max)

        S1_db = Spectrogram_Analysis.normalize_spectrogram(S1_db)
        S2_db = Spectrogram_Analysis.normalize_spectrogram(S2_db)

        # Перетвореня спектрограм у вектори
        vec1 = S1_db.flatten()
        vec2 = S2_db.flatten()

        cos_sim = 1 - cosine(vec1, vec2)
        print(f"Cosine Similarity: {cos_sim}")

