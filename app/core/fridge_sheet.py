"""
One-Page Printable Fridge Sheet Generator for CareBridge AI.
Generates an A4 patient adherence sheet with daily check-boxes,
emergency contacts, follow-up dates, and safety disclaimers.
Generates both PDF (via ReportLab) and print-ready HTML.
"""

import io
from typing import Dict, Any, List
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm


def generate_fridge_sheet_pdf(
    care_plan_data: Dict[str, Any],
    lang: str = "en"
) -> bytes:
    """
    Generates a clean, high-contrast, 1-page A4 PDF using ReportLab.
    Includes medication tracking check-boxes, follow-up date, and warning signs.
    """
    buffer = io.BytesIO()
    
    # 12mm margins for max printable A4 space
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'FridgeTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#0f766e'),
        alignment=1, # Center
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'FridgeSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=6
    )

    section_heading = ParagraphStyle(
        'SectionHead',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0f766e'),
        spaceBefore=4,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'FridgeBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    )

    warning_style = ParagraphStyle(
        'FridgeWarning',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#b91c1c')
    )

    disclaimer_style = ParagraphStyle(
        'FridgeDisclaimer',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#64748b'),
        alignment=1
    )

    elements = []

    # Header Banner
    title_text = "CareBridge AI — Patient Daily Care & Fridge Sheet" if lang == "en" else "CareBridge AI — రోజువారీ రోగి సంరక్షణ ఫ్రిజ్ షీట్"
    subtitle_text = "Keep this sheet on your refrigerator or medicine cabinet for daily tracking."
    elements.append(Paragraph(title_text, title_style))
    elements.append(Paragraph(subtitle_text, subtitle_style))

    # Patient & Diagnosis Summary Bar
    patient_name = care_plan_data.get("patient_name", "Patient")
    condition = care_plan_data.get("condition", "Medical Discharge Recovery")
    
    pat_table_data = [
        [
            Paragraph(f"<b>Patient:</b> {patient_name}", body_style),
            Paragraph(f"<b>Primary Condition:</b> {condition}", body_style),
        ]
    ]
    pat_table = Table(pat_table_data, colWidths=[65 * mm, 120 * mm])
    pat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdfa')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#99f6e4')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(pat_table)
    elements.append(Spacer(1, 4))

    # Section 1: Medication Checklist with Checkboxes
    elements.append(Paragraph("1. MEDICINE DAILY CHECKLIST", section_heading))
    
    meds = care_plan_data.get("medicines", [])
    
    med_table_data = [
        [
            Paragraph("<b>Medicine Name</b>", body_style),
            Paragraph("<b>Dose</b>", body_style),
            Paragraph("<b>How Often / Timing</b>", body_style),
            Paragraph("<b>Morning</b><br/>[ ]", body_style),
            Paragraph("<b>Noon</b><br/>[ ]", body_style),
            Paragraph("<b>Night</b><br/>[ ]", body_style),
        ]
    ]

    for m in meds[:8]: # Fit neatly on 1 page
        name = m.get("name", "")
        dose = m.get("dose_and_unit", "")
        freq = m.get("frequency", "")
        timing = m.get("timing", "")
        short_timing = timing.replace("Please confirm with your healthcare professional.", "As advised")
        
        med_table_data.append([
            Paragraph(f"<b>{name}</b>", body_style),
            Paragraph(dose, body_style),
            Paragraph(f"{freq}<br/><i>{short_timing}</i>", body_style),
            Paragraph("[  ]", body_style),
            Paragraph("[  ]", body_style),
            Paragraph("[  ]", body_style),
        ])

    med_table = Table(med_table_data, colWidths=[52 * mm, 28 * mm, 55 * mm, 16 * mm, 16 * mm, 18 * mm])
    med_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ccfbf1')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0, 0), (-1, -1), 3),
        ('ALIGN', (3, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(med_table)
    elements.append(Spacer(1, 5))

    # Section 2: Emergency Warning Signs (Red Alert Box)
    warnings = care_plan_data.get("warning_signs", [])
    warning_texts = []
    for w in warnings[:3]:
        s = w.get("sign", "")
        if s:
            warning_texts.append(f"• <b>{s}</b>")

    if not warning_texts:
        warning_texts.append("• Discharge summary specifies no explicit emergency red flags. Confirm with doctor.")

    warn_box_data = [
        [
            Paragraph("<b>EMERGENCY WARNING SIGNS (RED FLAGS) — CALL DOCTOR OR VISIT ER IF SEEN:</b>", warning_style)
        ],
        [
            Paragraph("<br/>".join(warning_texts), warning_style)
        ]
    ]
    warn_table = Table(warn_box_data, colWidths=[185 * mm])
    warn_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fef2f2')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#ef4444')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(warn_table)
    elements.append(Spacer(1, 4))

    # Section 3: Follow-Up Appointment & Diet/Activity Bar
    follow_ups = care_plan_data.get("follow_ups", [])
    fu_text = "As advised by your treating physician"
    if follow_ups:
        fu = follow_ups[0]
        fu_text = f"<b>{fu.get('date', '')}</b> at {fu.get('time', 'Scheduled time')} — {fu.get('clinician_or_department', '')}"

    diet_list = care_plan_data.get("diet_instructions", [])
    diet_text = "; ".join(diet_list[:2]) if diet_list else "Follow regular prescribed diet."

    bottom_data = [
        [
            Paragraph(f"<b>NEXT FOLLOW-UP:</b><br/>{fu_text}", body_style),
            Paragraph(f"<b>DIET & CARE:</b><br/>{diet_text}", body_style)
        ]
    ]
    bottom_table = Table(bottom_data, colWidths=[92 * mm, 93 * mm])
    bottom_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(bottom_table)
    elements.append(Spacer(1, 5))

    # Disclaimer
    disclaimer = (
        "SAFETY NOTICE: This sheet summarizes your hospital discharge instructions for daily convenience. "
        "Original clinician-issued orders always take precedence. If any instruction is unclear, contact your doctor immediately."
    )
    elements.append(Paragraph(disclaimer, disclaimer_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


def generate_fridge_sheet_html(care_plan_data: Dict[str, Any], lang: str = "en") -> str:
    """Generates print-optimized HTML template with dedicated @media print CSS."""
    patient_name = care_plan_data.get("patient_name", "Patient")
    condition = care_plan_data.get("condition", "Medical Discharge Recovery")
    meds = care_plan_data.get("medicines", [])
    warnings = care_plan_data.get("warning_signs", [])
    follow_ups = care_plan_data.get("follow_ups", [])
    diet = care_plan_data.get("diet_instructions", [])
    activity = care_plan_data.get("activity_restrictions", [])

    is_te = (lang == "te")
    title = "CareBridge AI — రోజువారీ రోగి సంరక్షణ ఫ్రిజ్ షీట్" if is_te else "CareBridge AI — Patient Daily Care & Fridge Sheet"
    subtitle = "ఈ షీట్‌ను మీ రిఫ్రిజిరేటర్ లేదా మందుల పెట్టెపై ఉంచండి." if is_te else "Keep this sheet on your refrigerator or medicine cabinet for daily tracking."

    med_rows = ""
    for m in meds:
        m_name = m.get("name", "")
        m_dose = m.get("dose_and_unit", "")
        m_freq = m.get("frequency", "")
        m_timing = m.get("timing", "")
        med_rows += f"""
        <tr>
            <td class="font-bold">{m_name}</td>
            <td><span class="badge">{m_dose}</span></td>
            <td>{m_freq}<br><small class="text-muted">{m_timing}</small></td>
            <td class="center-check"><input type="checkbox"></td>
            <td class="center-check"><input type="checkbox"></td>
            <td class="center-check"><input type="checkbox"></td>
        </tr>
        """

    warn_items = "".join([f"<li><strong>{w.get('sign', '')}</strong></li>" for w in warnings])
    if not warn_items:
        warn_items = "<li>డిశ్చార్జ్ సారాంశంలో ప్రత్యేకమైన అత్యవసర హెచ్చరికలు పేర్కొనబడలేదు.</li>" if is_te else "<li>Discharge summary contains no explicit warning signs. Confirm with doctor.</li>"

    fu_info = "As advised"
    if follow_ups:
        fu = follow_ups[0]
        fu_info = f"{fu.get('date', '')} {fu.get('time', '')} — {fu.get('clinician_or_department', '')}"

    diet_html = "".join([f"<li>{d}</li>" for d in diet[:3]])
    activity_html = "".join([f"<li>{a}</li>" for a in activity[:2]])

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 10mm;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            color: #1e293b;
            margin: 0;
            padding: 10px;
            background: #ffffff;
            font-size: 12px;
            line-height: 1.35;
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #0d9488;
            padding-bottom: 6px;
            margin-bottom: 8px;
        }}
        .header h1 {{
            margin: 0;
            color: #0f766e;
            font-size: 18px;
        }}
        .header p {{
            margin: 2px 0 0 0;
            color: #64748b;
            font-size: 11px;
        }}
        .patient-bar {{
            display: flex;
            justify-content: space-between;
            background: #f0fdfa;
            border: 1px solid #99f6e4;
            padding: 6px 12px;
            border-radius: 6px;
            margin-bottom: 8px;
            font-size: 12px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 8px;
        }}
        th, td {{
            border: 1px solid #cbd5e1;
            padding: 5px 6px;
            text-align: left;
            vertical-align: middle;
        }}
        th {{
            background: #ccfbf1;
            color: #0f766e;
            font-weight: 600;
            font-size: 11px;
        }}
        .center-check {{
            text-align: center;
            width: 45px;
        }}
        .center-check input {{
            width: 15px;
            height: 15px;
            cursor: pointer;
        }}
        .badge {{
            background: #e2e8f0;
            padding: 2px 5px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 11px;
        }}
        .font-bold {{ font-weight: 700; }}
        .text-muted {{ color: #64748b; font-size: 10px; }}
        .warning-box {{
            background: #fef2f2;
            border: 2px solid #ef4444;
            border-radius: 6px;
            padding: 6px 10px;
            margin-bottom: 8px;
        }}
        .warning-box h3 {{
            color: #b91c1c;
            margin: 0 0 4px 0;
            font-size: 12px;
        }}
        .warning-box ul {{
            margin: 0;
            padding-left: 18px;
            color: #991b1b;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-bottom: 8px;
        }}
        .info-card {{
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 6px 8px;
            background: #f8fafc;
        }}
        .info-card h4 {{
            margin: 0 0 3px 0;
            color: #0f766e;
            font-size: 11px;
        }}
        .info-card ul {{
            margin: 0;
            padding-left: 15px;
            font-size: 11px;
        }}
        .disclaimer {{
            text-align: center;
            color: #64748b;
            font-size: 9px;
            margin-top: 6px;
            border-top: 1px solid #e2e8f0;
            padding-top: 4px;
        }}
        @media print {{
            .no-print {{ display: none !important; }}
            body {{ padding: 0; }}
        }}
    </style>
</head>
<body>
    <div class="no-print" style="margin-bottom: 12px; text-align: right;">
        <button onclick="window.print()" style="background:#0d9488;color:#fff;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-weight:600;">🖨️ Print Fridge Sheet</button>
    </div>
    <div class="header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    <div class="patient-bar">
        <div><strong>Patient:</strong> {patient_name}</div>
        <div><strong>Condition:</strong> {condition}</div>
    </div>
    <table>
        <thead>
            <tr>
                <th>Medicine Name</th>
                <th>Dose</th>
                <th>Frequency & Timing</th>
                <th>Morning</th>
                <th>Noon</th>
                <th>Night</th>
            </tr>
        </thead>
        <tbody>
            {med_rows}
        </tbody>
    </table>
    <div class="warning-box">
        <h3>🚨 EMERGENCY WARNING SIGNS (RED FLAGS) — CALL 108 OR GO TO ER:</h3>
        <ul>{warn_items}</ul>
    </div>
    <div class="grid-2">
        <div class="info-card">
            <h4>📅 NEXT FOLLOW-UP APPOINTMENT</h4>
            <p style="margin:2px 0;font-size:11px;"><strong>{fu_info}</strong></p>
        </div>
        <div class="info-card">
            <h4>🥗 DIET & ACTIVITY SUMMARY</h4>
            <ul>{diet_html or "<li>Standard recovery diet.</li>"}{activity_html}</ul>
        </div>
    </div>
    <div class="disclaimer">
        Safety Disclaimer: This sheet summarizes your hospital discharge instructions. Clinician-issued orders take precedence. Confirm any unclear instructions with your treating physician.
    </div>
</body>
</html>"""
    return html
