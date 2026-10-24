import numpy as np
import pandas as pd

def generate_ecg_beat(n_samples=187, heart_rate=75, beat_type="Normal", noise_level=0.03):
    t = np.linspace(0, 1, n_samples)
    signal = np.zeros(n_samples)
    
    if beat_type == "Normal":
        # P wave
        signal += 0.15 * np.exp(-((t - 0.20) ** 2) / (2 * (0.03 ** 2)))
        # Q wave
        signal -= 0.15 * np.exp(-((t - 0.35) ** 2) / (2 * (0.015 ** 2)))
        # R wave
        signal += 1.20 * np.exp(-((t - 0.40) ** 2) / (2 * (0.02 ** 2)))
        # S wave
        signal -= 0.25 * np.exp(-((t - 0.45) ** 2) / (2 * (0.018 ** 2)))
        # T wave
        signal += 0.35 * np.exp(-((t - 0.70) ** 2) / (2 * (0.06 ** 2)))
    elif beat_type == "Arrhythmia":
        # PVC / wide inverted or aberrant QRS complex
        signal += 0.05 * np.exp(-((t - 0.15) ** 2) / (2 * (0.04 ** 2)))
        # Wide and distorted R wave
        signal += 0.85 * np.exp(-((t - 0.38) ** 2) / (2 * (0.06 ** 2)))
        # Deep S wave
        signal -= 0.65 * np.exp(-((t - 0.50) ** 2) / (2 * (0.04 ** 2)))
        # Inverted T wave
        signal -= 0.30 * np.exp(-((t - 0.72) ** 2) / (2 * (0.07 ** 2)))
    
    # Add mild noise
    signal += np.random.normal(0, noise_level, n_samples)
    return signal

def create_dataset():
    records = []
    np.random.seed(42)
    # 50 Normal records
    for _ in range(50):
        beat = generate_ecg_beat(187, beat_type="Normal", noise_level=0.04)
        records.append(list(np.round(beat, 4)) + ["Normal"])
    
    # 50 Arrhythmia records
    for _ in range(50):
        beat = generate_ecg_beat(187, beat_type="Arrhythmia", noise_level=0.04)
        records.append(list(np.round(beat, 4)) + ["Arrhythmia"])
    
    df = pd.DataFrame(records)
    df.to_csv("ecg_dataset.csv", index=False, header=False)
    print("Created ecg_dataset.csv with 100 labeled records.")

def create_sample_signals():
    np.random.seed(101)
    # Continuous signal: 8 beats stitched together with slight variation
    normal_signal = []
    for _ in range(8):
        normal_signal.extend(generate_ecg_beat(150, beat_type="Normal", noise_level=0.03))
    df_normal = pd.DataFrame(np.round(normal_signal, 4))
    df_normal.to_csv("sample_normal_ecg.csv", index=False, header=False)
    print("Created sample_normal_ecg.csv with", len(normal_signal), "samples.")

    arrhythmia_signal = []
    for _ in range(8):
        arrhythmia_signal.extend(generate_ecg_beat(150, beat_type="Arrhythmia", noise_level=0.03))
    df_arrhythmia = pd.DataFrame(np.round(arrhythmia_signal, 4))
    df_arrhythmia.to_csv("sample_arrhythmia_ecg.csv", index=False, header=False)
    print("Created sample_arrhythmia_ecg.csv with", len(arrhythmia_signal), "samples.")

if __name__ == "__main__":
    create_dataset()
    create_sample_signals()
