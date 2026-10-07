"""
Campus360 AI Intelligence API
"""

import math
from datetime import date, datetime
from decimal import Decimal

import numpy as np
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ai.intelligence.pipeline import CampusIntelligencePipeline


router = APIRouter(
    prefix="/api/ai",
    tags=["AI Intelligence"],
)


# ============================================================
# SINGLE PIPELINE INSTANCE
# ============================================================

_pipeline = None


def get_pipeline():
    global _pipeline

    if _pipeline is None:
        _pipeline = CampusIntelligencePipeline()

    return _pipeline


# ============================================================
# UNIVERSAL JSON SANITIZER
# ============================================================

def clean_for_json(value):

    # -----------------------------
    # None / basic Python types
    # -----------------------------

    if value is None:
        return None

    if isinstance(value, (str, int, bool)):
        return value

    # -----------------------------
    # NumPy scalar types
    # -----------------------------

    if isinstance(value, np.generic):
        return clean_for_json(value.item())

    # -----------------------------
    # NumPy arrays
    # -----------------------------

    if isinstance(value, np.ndarray):
        return [
            clean_for_json(x)
            for x in value.tolist()
        ]

    # -----------------------------
    # Float handling
    # -----------------------------

    if isinstance(value, float):

        if math.isnan(value):
            return None

        if math.isinf(value):
            return None

        return value

    # -----------------------------
    # Decimal
    # -----------------------------

    if isinstance(value, Decimal):
        return float(value)

    # -----------------------------
    # Date / datetime
    # -----------------------------

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    # -----------------------------
    # Dictionary
    # -----------------------------

    if isinstance(value, dict):

        cleaned = {}

        for key, val in value.items():

            # Convert unusual keys to strings
            if isinstance(key, np.generic):
                key = key.item()

            key = str(key)

            cleaned[key] = clean_for_json(val)

        return cleaned

    # -----------------------------
    # List
    # -----------------------------

    if isinstance(value, list):

        return [
            clean_for_json(x)
            for x in value
        ]

    # -----------------------------
    # Tuple
    # -----------------------------

    if isinstance(value, tuple):

        return [
            clean_for_json(x)
            for x in value
        ]

    # -----------------------------
    # Set
    # -----------------------------

    if isinstance(value, set):

        return [
            clean_for_json(x)
            for x in value
        ]

    # -----------------------------
    # Objects with to_dict()
    # -----------------------------

    if hasattr(value, "to_dict"):

        try:
            return clean_for_json(
                value.to_dict()
            )
        except Exception:
            pass

    # -----------------------------
    # Fallback
    # -----------------------------

    return str(value)


# ============================================================
# HEALTH
# ============================================================

@router.get("/health")
def ai_health():

    return {
        "status": "UP",
        "service": "Campus360 AI Intelligence",

        "modules": {
            "backend_telemetry": True,
            "data_normalization": True,
            "anomaly_detection": True,
            "kpi_extraction": True,
            "forecasting": True,
            "advanced_semantic_rag": True,
            "decision_reasoning": True,
            "recommendation_engine": True,
            "what_if_simulation": True,
            "current_status_analysis": True,
            "what_if_impact_analysis": True,
            "digital_twin_visualization_data": True,
        },
    }


# ============================================================
# DASHBOARD
# ============================================================

@router.get("/dashboard")
def ai_dashboard():

    try:

        print("\n======================================")
        print("      CAMPUS360 AI API REQUEST")
        print("======================================")

        pipeline = get_pipeline()

        print("Running AI pipeline...")

        result = pipeline.run()

        print("AI pipeline finished.")

        # ----------------------------------------
        # Convert EVERYTHING to native Python
        # ----------------------------------------

        cleaned_result = clean_for_json(result)

        print("JSON sanitization complete.")

        # ----------------------------------------
        # Return JSONResponse directly.
        #
        # This bypasses FastAPI's jsonable_encoder.
        # ----------------------------------------

        return JSONResponse(
            content={
                "status": "success",
                "service": "Campus360 AI Intelligence",
                "pipeline_status": "COMPLETE",
                "data": cleaned_result,
            }
        )

    except Exception as exc:

        print("\nAI API ERROR:")
        print(repr(exc))

        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "service": "Campus360 AI Intelligence",
                "message": str(exc),
            },
        )


# ============================================================
# RUN PIPELINE
# ============================================================

@router.post("/run")
def run_ai_pipeline():

    try:

        pipeline = get_pipeline()

        result = pipeline.run()

        cleaned_result = clean_for_json(result)

        return JSONResponse(
            content={
                "status": "success",
                "pipeline_status": "COMPLETE",
                "data": cleaned_result,
            }
        )

    except Exception as exc:

        print("\nAI API ERROR:")
        print(repr(exc))

        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": str(exc),
            },
        )