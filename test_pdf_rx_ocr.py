import cv2
import numpy as np
import fitz
import re
from rapidocr_onnxruntime import RapidOCR

def run_prescription_ocr(pdf_path: str):
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    # Try getting embedded image first
    img_list = page.get_images()
    pil_img = None
    if img_list:
        xref = img_list[0][0]
        base_img = doc.extract_image(xref)
        img_bytes = base_img["image"]
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    else:
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    ocr = RapidOCR(limit_side_len=2000, box_thresh=0.2, text_score=0.2)
    
    # Pass 1: Raw
    res1, _ = ocr(img)
    
    # Pass 2: CLAHE on green channel
    g = cv2.split(img)[1]
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enh = clahe.apply(g)
    enh_3ch = cv2.cvtColor(enh, cv2.COLOR_GRAY2BGR)
    res2, _ = ocr(enh_3ch)

    # Collect and sort
    items = []
    seen = set()
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
            key = (round(yc / 20.0), round(xc / 40.0), t.lower()[:6])
            if key not in seen:
                seen.add(key)
                items.append({'yc': yc, 'xc': xc, 'text': t, 'score': float(score)})

    items.sort(key=lambda it: it['yc'])
    for it in items:
        safe_t = it['text'].encode('ascii', 'replace').decode('ascii')
        print(f"y={it['yc']:.0f}, x={it['xc']:.0f}: {safe_t}")

if __name__ == "__main__":
    run_prescription_ocr(r"C:\Users\bhavy\Downloads\prescription doctor.pdf")
