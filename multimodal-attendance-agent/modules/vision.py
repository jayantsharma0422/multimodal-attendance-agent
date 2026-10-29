import tempfile
import os
import cv2

def analyze_video(uploaded_file, sample_every=5):
    path = None
    cap = None
    try:
        suffix = os.path.splitext(uploaded_file.name)[1] or ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            path = tmp.name
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            return {"error": "Could not open this video. Try an MP4 or AVI file."}
        fps = cap.get(cv2.CAP_PROP_FPS) or 0
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
        duration = frame_count / fps if fps > 0 else 0
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        sampled = 0
        with_people = 0
        maximum = 0
        frame_idx = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if frame_idx % max(1, int(sample_every)) == 0:
                sampled += 1
                h, w = frame.shape[:2]
                scale = min(1.0, 640 / max(w, h))
                if scale < 1:
                    frame = cv2.resize(frame, (int(w*scale), int(h*scale)))
                rects, weights = hog.detectMultiScale(frame, winStride=(8, 8), padding=(8, 8), scale=1.05)
                count = len(rects)
                maximum = max(maximum, count)
                if count:
                    with_people += 1
            frame_idx += 1
        return {"frames_sampled": sampled, "frames_with_people": with_people,
                "max_people": maximum, "duration_seconds": duration}
    except Exception as exc:
        return {"error": f"Video analysis failed: {exc}"}
    finally:
        if cap is not None:
            cap.release()
        if path and os.path.exists(path):
            os.remove(path)
