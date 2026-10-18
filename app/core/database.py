"""
SQLite Persistence Module for CareBridge AI.
Saves and retrieves historical discharge summary processing runs,
patient care plans, faithfulness audit reports, and evaluation metrics.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "carebridge.db")


def get_connection():
    """Returns a SQLite connection with row dictionary factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes SQLite tables if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS care_plans (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                patient_name TEXT,
                condition TEXT,
                source_text TEXT,
                extraction_json TEXT,
                english_plan_json TEXT,
                telugu_plan_json TEXT,
                faithfulness_report_json TEXT,
                readability_json TEXT,
                overall_status TEXT,
                fact_preservation_rate REAL,
                dose_accuracy_rate REAL,
                frequency_accuracy_rate REAL,
                warning_recall_rate REAL,
                hallucination_count INTEGER,
                flesch_grade REAL,
                created_at TEXT
            )
        """)
        # Ensure user_id column exists if table was created previously
        cursor.execute("PRAGMA table_info(care_plans)")
        existing_cols = [c[1] for c in cursor.fetchall()]
        if "user_id" not in existing_cols:
            cursor.execute("ALTER TABLE care_plans ADD COLUMN user_id TEXT")
        conn.commit()


def save_care_plan(plan_dict: Dict[str, Any], user_id: Optional[str] = None) -> str:
    """Inserts a generated care plan and its audit report into SQLite, associating with user."""
    init_db()
    
    plan_id = plan_dict.get("id")
    owner_id = user_id or plan_dict.get("user_id")
    f_rep = plan_dict.get("faithfulness_report", {})
    metrics = f_rep.get("metrics", {})
    readability = plan_dict.get("readability", {})
    eng_read = readability.get("english", {})

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO care_plans (
                id, user_id, patient_name, condition, source_text,
                extraction_json, english_plan_json, telugu_plan_json,
                faithfulness_report_json, readability_json,
                overall_status, fact_preservation_rate, dose_accuracy_rate,
                frequency_accuracy_rate, warning_recall_rate,
                hallucination_count, flesch_grade, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            plan_id,
            owner_id,
            plan_dict.get("patient_name", "Anonymous Patient"),
            plan_dict.get("condition", "Medical Care Plan"),
            plan_dict.get("extraction", {}).get("raw_source_text", ""),
            json.dumps(plan_dict.get("extraction", {})),
            json.dumps(plan_dict.get("english_plan", {})),
            json.dumps(plan_dict.get("telugu_plan", {})),
            json.dumps(f_rep),
            json.dumps(readability),
            f_rep.get("overall_status", "UNKNOWN"),
            metrics.get("fact_preservation_rate", 100.0),
            metrics.get("dose_accuracy_rate", 100.0),
            metrics.get("frequency_accuracy_rate", 100.0),
            metrics.get("warning_recall_rate", 100.0),
            int(metrics.get("hallucination_count", 0)),
            eng_read.get("grade_level", 7.0),
            plan_dict.get("created_at", datetime.now().isoformat())
        ))
        conn.commit()
    
    return plan_id


def get_all_care_plans(user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves care plans sorted by newest first. If user_id provided, filters only for that user."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute("SELECT * FROM care_plans WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        else:
            cursor.execute("SELECT * FROM care_plans ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        results = []
        for r in rows:
            results.append({
                "id": r["id"],
                "user_id": r["user_id"] if "user_id" in r.keys() else None,
                "patient_name": r["patient_name"],
                "condition": r["condition"],
                "overall_status": r["overall_status"],
                "fact_preservation_rate": r["fact_preservation_rate"],
                "dose_accuracy_rate": r["dose_accuracy_rate"],
                "frequency_accuracy_rate": r["frequency_accuracy_rate"],
                "warning_recall_rate": r["warning_recall_rate"],
                "flesch_grade": r["flesch_grade"],
                "created_at": r["created_at"],
                "extraction": json.loads(r["extraction_json"]) if r["extraction_json"] else {},
                "english_plan": json.loads(r["english_plan_json"]) if r["english_plan_json"] else {},
                "telugu_plan": json.loads(r["telugu_plan_json"]) if r["telugu_plan_json"] else {},
                "faithfulness_report": json.loads(r["faithfulness_report_json"]) if r["faithfulness_report_json"] else {},
                "readability": json.loads(r["readability_json"]) if r["readability_json"] else {}
            })
        return results


def get_care_plan_by_id(plan_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Fetches a single care plan by ID, verifying user ownership if user_id is provided."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM care_plans WHERE id = ?", (plan_id,))
        r = cursor.fetchone()
        if not r:
            return None
        
        row_user_id = r["user_id"] if "user_id" in r.keys() else None
        if user_id and row_user_id and row_user_id != user_id:
            return None

        return {
            "id": r["id"],
            "user_id": row_user_id,
            "patient_name": r["patient_name"],
            "condition": r["condition"],
            "overall_status": r["overall_status"],
            "created_at": r["created_at"],
            "extraction": json.loads(r["extraction_json"]) if r["extraction_json"] else {},
            "english_plan": json.loads(r["english_plan_json"]) if r["english_plan_json"] else {},
            "telugu_plan": json.loads(r["telugu_plan_json"]) if r["telugu_plan_json"] else {},
            "faithfulness_report": json.loads(r["faithfulness_report_json"]) if r["faithfulness_report_json"] else {},
            "readability": json.loads(r["readability_json"]) if r["readability_json"] else {}
        }


def get_dashboard_summary() -> Dict[str, Any]:
    """Calculates aggregate metrics for the Evaluation Dashboard."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM care_plans")
        total_count = cursor.fetchone()["cnt"]

        if total_count == 0:
            return {
                "total_processed": 0,
                "verified_count": 0,
                "review_required_count": 0,
                "avg_preservation_rate": 100.0,
                "avg_dose_accuracy": 100.0,
                "avg_frequency_accuracy": 100.0,
                "avg_warning_recall": 100.0,
                "total_hallucinations": 0,
                "avg_flesch_grade": 7.2
            }

        cursor.execute("SELECT COUNT(*) as cnt FROM care_plans WHERE overall_status = 'VERIFIED'")
        verified_count = cursor.fetchone()["cnt"]

        cursor.execute("SELECT COUNT(*) as cnt FROM care_plans WHERE overall_status = 'CLINICIAN_REVIEW_REQUIRED'")
        review_count = cursor.fetchone()["cnt"]

        cursor.execute("""
            SELECT 
                AVG(fact_preservation_rate) as avg_pres,
                AVG(dose_accuracy_rate) as avg_dose,
                AVG(frequency_accuracy_rate) as avg_freq,
                AVG(warning_recall_rate) as avg_warn,
                SUM(hallucination_count) as total_halluc,
                AVG(flesch_grade) as avg_grade
            FROM care_plans
        """)
        row = cursor.fetchone()

        return {
            "total_processed": total_count,
            "verified_count": verified_count,
            "review_required_count": review_count,
            "avg_preservation_rate": round(row["avg_pres"] or 100.0, 1),
            "avg_dose_accuracy": round(row["avg_dose"] or 100.0, 1),
            "avg_frequency_accuracy": round(row["avg_freq"] or 100.0, 1),
            "avg_warning_recall": round(row["avg_warn"] or 100.0, 1),
            "total_hallucinations": int(row["total_halluc"] or 0),
            "avg_flesch_grade": round(row["avg_grade"] or 7.2, 1)
        }
