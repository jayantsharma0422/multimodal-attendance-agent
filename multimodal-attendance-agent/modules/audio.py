import tempfile
import os
import numpy as np
import soundfile as sf

def analyze_audio(uploaded_file, threshold=0.05):
    path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.getvalue())
            path = tmp.name
        signal, sample_rate = sf.read(path, dtype="float32", always_2d=False)
        if signal.size == 0:
            return {"error": "The audio file is empty."}
        if signal.ndim > 1:
            signal = signal.mean(axis=1)
        signal = np.nan_to_num(signal)
        duration = len(signal) / float(sample_rate)
        rms = float(np.sqrt(np.mean(np.square(signal)))) if signal.size else 0.0
        frame_size = max(1, int(sample_rate * 0.02))
        usable = signal[:(len(signal)//frame_size)*frame_size]
        if usable.size:
            frames = usable.reshape(-1, frame_size)
            energies = np.sqrt(np.mean(np.square(frames), axis=1))
            cutoff = max(float(threshold) * float(np.max(energies)), 0.005)
            active_percent = float(np.mean(energies > cutoff) * 100)
        else:
            active_percent = 0.0
        interpretation = ("High sound activity detected; review the recording context."
                          if active_percent >= 50 else
                          "Lower or intermittent sound activity detected; review the recording context.")
        return {"duration_seconds": duration, "rms": rms,
                "active_percent": active_percent, "interpretation": interpretation}
    except Exception as exc:
        return {"error": f"Audio analysis failed. Please use a standard PCM WAV file. Details: {exc}"}
    finally:
        if path and os.path.exists(path):
            os.remove(path)
