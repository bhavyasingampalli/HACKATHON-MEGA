import cv2
import numpy as np
import fitz
import re
from rapidocr_onnxruntime import RapidOCR

def perform_spatial_ocr(img_bgr):
    ocr = RapidOCR(limit_side_len=2000, box_thresh=0.2, text_score=0.2)
    res1, _ = ocr(img_bgr)
    
    # Pass 2: CLAHE on green channel
    g = cv2.split(img_bgr)[1]
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enh = clahe.apply(g)
    enh_3ch = cv2.cvtColor(enh, cv2.COLOR_GRAY2BGR)
    res2, _ = ocr(enh_3ch)

    items = []
    for res in [res1, res2]:
        if not res:
            continue
        for box, text, score in res:
            t = text.strip()
            if not t:
                continue
            pts = np.array(box, dtype=np.float32)
            yc = float(np.mean(pts[:, 1]))
            xc = float(np.mean(pts[:, 0]))
            h = float(np.max(pts[:, 1]) - np.min(pts[:, 1]))
            items.append({'yc': yc, 'xc': xc, 'h': h, 'text': t, 'score': float(score)})

    items.sort(key=lambda it: it['yc'])

    # Line clustering
    lines = []
    curr_line = []
    for it in items:
        if not curr_line:
            curr_line.append(it)
        else:
            avg_yc = sum(x['yc'] for x in curr_line) / len(curr_line)
            avg_h = sum(x['h'] for x in curr_line) / len(curr_line)
            if abs(it['yc'] - avg_yc) <= max(18.0, avg_h * 0.6):
                curr_line.append(it)
            else:
                curr_line.sort(key=lambda x: x['xc'])
                # Deduplicate consecutive identical words
                words = []
                for w in curr_line:
                    wt = w['text']
                    if not words or words[-1].lower() != wt.lower():
                        words.append(wt)
                lines.append(' '.join(words))
                curr_line = [it]

    if curr_line:
        curr_line.sort(key=lambda x: x['xc'])
        words = []
        for w in curr_line:
            wt = w['text']
            if not words or words[-1].lower() != wt.lower():
                words.append(wt)
        lines.append(' '.join(words))

    return '\n'.join(lines)

doc = fitz.open(r"C:\Users\bhavy\Downloads\prescription doctor.pdf")
page = doc[0]
img_list = page.get_images()
if img_list:
    xref = img_list[0][0]
    base_img = doc.extract_image(xref)
    nparr = np.frombuffer(base_img["image"], np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
else:
    pix = page.get_pixmap(dpi=200)
    nparr = np.frombuffer(pix.tobytes("png"), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

text = perform_spatial_ocr(img)
for line in text.splitlines():
    print("OUTPUT LINE:", line.encode('ascii', 'replace').decode('ascii'))
