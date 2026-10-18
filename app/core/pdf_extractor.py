"""
Document and Image Text Extraction Module for CareBridge AI.
Supports PDF (digital and scanned via OCR), JPG, JPEG, PNG (prescription photos and scans),
and plain text (TXT) files.
Uses PyMuPDF (fitz) for PDF parsing and RapidOCR with multi-pass spatial grouping for optical character recognition.
Strict safety rules: Never invents or guesses medical information when text extraction fails.
"""

import io
import os
import logging
from typing import Tuple, Dict, Any, Optional
import numpy as np
import cv2
from PIL import Image
import fitz  # PyMuPDF

logger = logging.getLogger("carebridge.extractor")

# Lazy-loaded RapidOCR engine singleton
_ocr_engine = None


class DocumentExtractionError(Exception):
    """Custom exception raised when document extraction fails, is corrupted, or unsupported."""
    pass


def get_ocr_engine():
    """Lazily instantiates and returns the RapidOCR engine with high-resolution support for fine handwriting."""
    global _ocr_engine
    if _ocr_engine is None:
        try:
            from rapidocr_onnxruntime import RapidOCR
            # limit_side_len=2000 prevents downsampling high-resolution scans/photos.
            # box_thresh=0.2 and text_score=0.2 detects lighter pen strokes in handwritten prescriptions.
            _ocr_engine = RapidOCR(limit_side_len=2000, box_thresh=0.2, text_score=0.2)
            logger.info("RapidOCR engine initialized successfully with high-resolution settings.")
        except Exception as e:
            logger.error(f"Failed to initialize RapidOCR engine: {e}")
            raise DocumentExtractionError(
                f"OCR engine is not available on this system: {str(e)}"
            )
    return _ocr_engine


def perform_spatial_ocr(img_bgr: np.ndarray) -> str:
    """
    Performs multi-pass OCR on an image and reconstructs text preserving spatial line layout.
    Pass 1: Original BGR image (captures standard printed/colored text).
    Pass 2: CLAHE contrast-enhanced green channel (isolates blue/purple handwritten ink from paper).
    Items are clustered vertically into lines and sorted horizontally (left to right).
    """
    engine = get_ocr_engine()
    
    # Pass 1: Raw image
    try:
        res1, _ = engine(img_bgr)
    except Exception as e:
        logger.warning(f"OCR Pass 1 failed: {e}")
        res1 = None

    # Pass 2: Contrast-enhanced green channel
    try:
        g = cv2.split(img_bgr)[1]
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enh = clahe.apply(g)
        enh_3ch = cv2.cvtColor(enh, cv2.COLOR_GRAY2BGR)
        res2, _ = engine(enh_3ch)
    except Exception as e:
        logger.warning(f"OCR Pass 2 failed: {e}")
        res2 = None

    all_items = []
    seen = set()

    for res in [res1, res2]:
        if not res:
            continue
        for item in res:
            if not item or len(item) < 2:
                continue
            box = item[0]
            text = str(item[1]).strip()
            score = float(item[2]) if len(item) > 2 and item[2] else 0.0
            if not text:
                continue

            pts = np.array(box, dtype=np.float32)
            yc = float(np.mean(pts[:, 1]))
            xc = float(np.mean(pts[:, 0]))
            h = float(np.max(pts[:, 1]) - np.min(pts[:, 1]))

            # Fuzzy deduplication key based on vertical band and word prefix
            key = (round(yc / 16.0), round(xc / 32.0), text.lower()[:6])
            if key not in seen:
                seen.add(key)
                all_items.append({
                    "yc": yc,
                    "xc": xc,
                    "h": h,
                    "text": text,
                    "score": score
                })

    if not all_items:
        return ""

    # Sort vertically
    all_items.sort(key=lambda it: it["yc"])

    # Cluster into horizontal lines
    lines = []
    curr_line = []
    for it in all_items:
        if not curr_line:
            curr_line.append(it)
        else:
            avg_yc = sum(x["yc"] for x in curr_line) / len(curr_line)
            avg_h = sum(x["h"] for x in curr_line) / len(curr_line)
            threshold = max(18.0, avg_h * 0.6)
            if abs(it["yc"] - avg_yc) <= threshold:
                curr_line.append(it)
            else:
                curr_line.sort(key=lambda x: x["xc"])
                # Deduplicate consecutive identical words
                words = []
                for w in curr_line:
                    wt = w["text"]
                    if not words or words[-1].lower() != wt.lower():
                        words.append(wt)
                if words:
                    lines.append(" ".join(words))
                curr_line = [it]

    if curr_line:
        curr_line.sort(key=lambda x: x["xc"])
        words = []
        for w in curr_line:
            wt = w["text"]
            if not words or words[-1].lower() != wt.lower():
                words.append(wt)
        if words:
            lines.append(" ".join(words))

    return "\n".join(lines).strip()


def extract_text_from_image(image_bytes: bytes, filename: str = "image.jpg") -> Tuple[str, Dict[str, Any]]:
    """
    Extracts clinical text from image files (JPG, JPEG, PNG) using high-resolution spatial OCR.
    
    Safety Rules:
    - Verifies image integrity (detects corrupted or truncated files).
    - Uses multi-pass OCR to extract readable printed or written text.
    - Never hallucinates or invents medical facts if extraction fails.
    """
    if not image_bytes or len(image_bytes) == 0:
        raise DocumentExtractionError("The uploaded file is empty (0 bytes). Please upload a valid image.")

    # 10 MB maximum safety limit
    if len(image_bytes) > 10 * 1024 * 1024:
        raise DocumentExtractionError("File size exceeds 10 MB limit. Please upload a smaller image file.")

    # Verify image integrity with PIL
    try:
        with Image.open(io.BytesIO(image_bytes)) as pil_img:
            pil_img.verify()
            img_format = pil_img.format or "IMAGE"
    except Exception as e:
        raise DocumentExtractionError(
            f"Unable to read image file '{filename}'. The file may be corrupted, truncated, or not a valid image: {str(e)}"
        )

    # Decode image to OpenCV BGR array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise DocumentExtractionError(f"Failed to decode image data for '{filename}'.")

    height, width, _ = img_bgr.shape
    full_text = perform_spatial_ocr(img_bgr)

    if not full_text:
        raise DocumentExtractionError(
            "No readable clinical text could be detected from this image. "
            "Please ensure the prescription or document photo is clear, well-lit, in focus, and contains legible text."
        )

    detected_lines = [l for l in full_text.splitlines() if l.strip()]

    metadata = {
        "format": f"IMAGE ({img_format})",
        "filename": filename,
        "width": width,
        "height": height,
        "total_chars": len(full_text),
        "page_count": 1,
        "ocr_applied": True,
        "lines_detected": len(detected_lines)
    }

    return full_text, metadata


def extract_text_from_pdf(pdf_bytes: bytes, filename: str = "document.pdf") -> Tuple[str, Dict[str, Any]]:
    """
    Extracts text from PDF bytes using PyMuPDF.
    If a page contains low or zero direct text (e.g. scanned document or photo prescription),
    automatically applies high-resolution spatial OCR.
    
    Safety Rules:
    - Never silently process an empty or corrupted document.
    - Seamlessly OCRs scanned pages without guessing.
    """
    if not pdf_bytes or len(pdf_bytes) == 0:
        raise DocumentExtractionError("The uploaded file is empty (0 bytes). Please upload a valid document.")
    
    # 10 MB maximum safety limit
    if len(pdf_bytes) > 10 * 1024 * 1024:
        raise DocumentExtractionError("File size exceeds 10 MB limit. Please upload a smaller discharge summary.")

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise DocumentExtractionError(f"Unable to parse PDF file. The file may be corrupted or password-protected: {str(e)}")

    if doc.page_count == 0:
        doc.close()
        raise DocumentExtractionError("The PDF contains 0 pages.")

    full_text_pages = []
    total_chars = 0
    total_images = 0
    ocr_applied_pages = 0

    for page_idx in range(doc.page_count):
        page = doc.load_page(page_idx)
        page_text = page.get_text("text").strip()
        img_list = page.get_images()
        num_images = len(img_list)
        total_images += num_images

        # If page has very little or no direct text, run spatial OCR
        if len(page_text) < 30:
            ocr_text = ""
            # If the page contains an embedded raw image (like a scanned photo), extract it directly
            if img_list:
                try:
                    xref = img_list[0][0]
                    base_img = doc.extract_image(xref)
                    raw_bytes = base_img.get("image")
                    if raw_bytes:
                        nparr = np.frombuffer(raw_bytes, np.uint8)
                        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        if img_bgr is not None:
                            ocr_text = perform_spatial_ocr(img_bgr)
                except Exception as err:
                    logger.warning(f"Error extracting embedded image on page {page_idx + 1}: {err}")

            # Fallback or alternative: render page pixmap at 200 DPI
            if not ocr_text or len(ocr_text) < 15:
                try:
                    pix = page.get_pixmap(dpi=200)
                    pix_bytes = pix.tobytes("png")
                    nparr = np.frombuffer(pix_bytes, np.uint8)
                    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    if img_bgr is not None:
                        pix_ocr_text = perform_spatial_ocr(img_bgr)
                        if len(pix_ocr_text) > len(ocr_text):
                            ocr_text = pix_ocr_text
                except Exception as err:
                    logger.warning(f"Pix OCR error on page {page_idx + 1}: {err}")

            if len(ocr_text) > len(page_text):
                page_text = ocr_text
                ocr_applied_pages += 1

        full_text_pages.append(page_text)
        total_chars += len(page_text)

    metadata = {
        "page_count": doc.page_count,
        "total_chars": total_chars,
        "total_images": total_images,
        "format": "PDF",
        "title": doc.metadata.get("title", "") if doc.metadata else "",
        "ocr_applied": ocr_applied_pages > 0,
        "ocr_pages_count": ocr_applied_pages
    }
    doc.close()

    full_text = "\n\n".join(filter(None, full_text_pages)).strip()

    if not full_text:
        raise DocumentExtractionError(
            "The PDF document does not contain readable clinical text even after OCR processing. "
            "Please verify the document contains legible discharge summary instructions."
        )

    return full_text, metadata


def extract_text_from_file(file_bytes: bytes, filename: str) -> Tuple[str, Dict[str, Any]]:
    """
    Universal dispatcher for PDF, image (JPG, JPEG, PNG), and plain text (TXT) files.
    """
    if not filename:
        filename = "document"

    lower_name = filename.lower()
    
    if lower_name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes, filename)
    elif lower_name.endswith((".jpg", ".jpeg", ".png")):
        return extract_text_from_image(file_bytes, filename)
    elif lower_name.endswith(".txt"):
        try:
            text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            text = file_bytes.decode("latin-1", errors="replace")
        
        clean_text = text.strip()
        if not clean_text:
            raise DocumentExtractionError("Text document is empty. Please upload a file containing discharge instructions.")
        
        return clean_text, {"format": "TXT", "total_chars": len(clean_text), "page_count": 1}
    else:
        ext = os.path.splitext(filename)[1] or "unknown"
        raise DocumentExtractionError(
            f"Unsupported file format '{ext}'. CareBridge AI accepts PDF documents, image files (.jpg, .jpeg, .png), and text files (.txt)."
        )
