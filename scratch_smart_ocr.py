import cv2
import numpy as np
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR(limit_side_len=2000, box_thresh=0.2, text_score=0.2)
img = cv2.imread('raw_prescription_extracted.jpeg')

# Pass 1: raw image
res1, _ = ocr(img)

# Pass 2: CLAHE on green channel
g = cv2.split(img)[1]
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
enh = clahe.apply(g)
enh_3ch = cv2.cvtColor(enh, cv2.COLOR_GRAY2BGR)
res2, _ = ocr(enh_3ch)

all_items = []
seen = set()

for res in [res1, res2]:
    if not res:
        continue
    for box, text, score in res:
        t = text.strip()
        if not t:
            continue
        pts = np.array(box, dtype=np.float32)
        ymin = float(np.min(pts[:, 1]))
        ymax = float(np.max(pts[:, 1]))
        xmin = float(np.min(pts[:, 0]))
        xmax = float(np.max(pts[:, 0]))
        yc = (ymin + ymax) / 2.0
        xc = (xmin + xmax) / 2.0
        
        key = (round(yc / 20.0), round(xc / 40.0), t.lower()[:8])
        if key not in seen:
            seen.add(key)
            all_items.append({
                'ymin': ymin, 'ymax': ymax, 'xmin': xmin, 'xmax': xmax,
                'yc': yc, 'xc': xc, 'text': t, 'score': float(score)
            })

all_items.sort(key=lambda it: it['yc'])

print(f"Total merged OCR items: {len(all_items)}")
for it in all_items:
    safe_t = it['text'].encode('ascii', 'replace').decode('ascii')
    print(f"y={it['yc']:.0f}, x={it['xc']:.0f}: {safe_t} (score: {it['score']:.2f})")
