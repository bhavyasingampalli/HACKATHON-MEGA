"""
Tests for PDF, Image (JPG/PNG), OCR extraction, and file validation.
"""

import io
import pytest
import fitz
from PIL import Image, ImageDraw

from app.core.pdf_extractor import (
    extract_text_from_pdf,
    extract_text_from_image,
    extract_text_from_file,
    DocumentExtractionError
)


def test_pdf_extraction_success():
    # Create valid in-memory PDF using PyMuPDF
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 100), "DISCHARGE SUMMARY\nPatient: John Doe\nDiagnosis: Hypertension\nTab. Amlodipine 5 mg OD")
    pdf_bytes = doc.tobytes()
    doc.close()

    text, meta = extract_text_from_pdf(pdf_bytes, "test_summary.pdf")
    assert "John Doe" in text
    assert "Amlodipine" in text
    assert meta["page_count"] == 1


def test_scanned_pdf_rejection():
    # Create empty/blank PDF with virtually 0 text
    doc = fitz.open()
    doc.new_page()
    pdf_bytes = doc.tobytes()
    doc.close()

    with pytest.raises(DocumentExtractionError) as exc_info:
        extract_text_from_pdf(pdf_bytes, "scanned_blank.pdf")
    
    assert "readable" in str(exc_info.value).lower() or "scanned" in str(exc_info.value).lower()


def test_empty_bytes_rejection():
    with pytest.raises(DocumentExtractionError):
        extract_text_from_file(b"", "empty.pdf")
    with pytest.raises(DocumentExtractionError):
        extract_text_from_file(b"", "empty.jpg")


def test_unsupported_file_extension():
    with pytest.raises(DocumentExtractionError) as exc_info:
        extract_text_from_file(b"some content", "patient_records.docx")
    assert "unsupported" in str(exc_info.value).lower()


def test_corrupted_image_rejection():
    corrupted_bytes = b"NOT_A_VALID_IMAGE_HEADER_OR_DATA_XYZ123"
    with pytest.raises(DocumentExtractionError) as exc_info:
        extract_text_from_file(corrupted_bytes, "prescription.jpg")
    assert "corrupted" in str(exc_info.value).lower() or "unable" in str(exc_info.value).lower()


def test_image_extraction_jpg():
    # Create in-memory JPG with clear clinical text
    img = Image.new("RGB", (600, 150), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((20, 20), "Rx: Tab Metformin 500 mg OD", fill=(0, 0, 0))
    draw.text((20, 70), "Warning: Contact clinic if dizziness occurs", fill=(0, 0, 0))

    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    jpg_bytes = buf.getvalue()

    text, meta = extract_text_from_file(jpg_bytes, "prescription.jpg")
    assert "Metformin" in text or "500" in text
    assert meta["ocr_applied"] is True
    assert meta["page_count"] == 1


def test_image_extraction_png():
    # Create in-memory PNG with clinical text
    img = Image.new("RGB", (600, 150), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((20, 20), "Tab Atorvastatin 20 mg HS", fill=(0, 0, 0))
    draw.text((20, 70), "Review in 2 weeks at Cardiology", fill=(0, 0, 0))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    text, meta = extract_text_from_file(png_bytes, "discharge_photo.png")
    assert "Atorvastatin" in text or "20" in text
    assert meta["ocr_applied"] is True


def test_scanned_pdf_with_ocr():
    # Create an image-only (scanned) PDF with clinical instructions
    img = Image.new("RGB", (600, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((30, 40), "Hospital Discharge Note: Patient Ramesh Rao", fill=(0, 0, 0))
    draw.text((30, 90), "Tab Pantoprazole 40 mg OD before food", fill=(0, 0, 0))

    buf = io.BytesIO()
    img.save(buf, format="PNG")

    doc = fitz.open()
    page = doc.new_page(width=600, height=200)
    page.insert_image(page.rect, stream=buf.getvalue())
    pdf_bytes = doc.tobytes()
    doc.close()

    text, meta = extract_text_from_file(pdf_bytes, "scanned_discharge.pdf")
    assert "Pantoprazole" in text or "40" in text or "Ramesh" in text
    assert meta["ocr_applied"] is True


def test_short_text_accepted():
    # Text under 30 characters should now be accepted without error
    short_text = "Tab PCM 500mg OD"  # 16 characters
    text, meta = extract_text_from_file(short_text.encode("utf-8"), "rx.txt")
    assert text == short_text
    assert meta["format"] == "TXT"
