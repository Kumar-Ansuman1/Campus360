"""
Campus360 AI - Decision Reasoning Engine

Converts:
    telemetry
    + anomalies
    + forecast
    + recommendations
    + RAG evidence

into an explainable operational decision.
"""

from datetime import datetime

from ai.intelligence.advanced_rag import AdvancedRAG


class DecisionReasoningEngine:

    def __init__(
        self,
        rag_engine=None
    ):

        self.rag = (
            rag_engine
            if rag_engine is not None
            else AdvancedRAG()
        )

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        category,
        metric,
        current_value,
        anomaly_status="NORMAL",
        anomaly_score=0.0,
        recommendation=None,
        forecast=None,
        context=None
    ):

        context = context or {}

        category = str(
            category or "FACILITY"
        )

        metric = str(
            metric or "metric"
        )

        # -----------------------------------------------------
        # BUILD SEMANTIC QUERY
        # -----------------------------------------------------

        query_parts = [
            category,
            metric,
            "facility operations",
            "efficiency",
            "anomaly",
            "inspection",
            "operational response"
        ]

        if context.get("building_type"):
            query_parts.append(
                str(
                    context["building_type"]
                )
            )

        if context.get("building"):
            query_parts.append(
                str(
                    context["building"]
                )
            )

        if forecast:

            trend = forecast.get(
                "trend",
                forecast.get(
                    "forecast_trend",
                    ""
                )
            )

            if trend:
                query_parts.append(
                    str(trend)
                )

        query = " ".join(
            query_parts
        )

        # -----------------------------------------------------
        # RAG
        # -----------------------------------------------------

        context_text = ""
        retrieved = []

        try:

            context_text, retrieved = (
                self.rag.build_context(
                    query=query,
                    top_k=3
                )
            )

        except Exception as exc:

            print(
                "RAG retrieval warning:",
                exc
            )

        # -----------------------------------------------------
        # NORMALIZE ANOMALY STATUS
        # -----------------------------------------------------

        normalized_status = str(
            anomaly_status or "NORMAL"
        ).upper()

        # -----------------------------------------------------
        # PRIORITY + EXPLANATION
        # -----------------------------------------------------

        if normalized_status in {
            "CRITICAL",
            "HIGH",
            "ANOMALY"
        }:

            priority = "HIGH"

            explanation = (
                f"{category} shows an abnormal "
                f"{metric} value of "
                f"{current_value}. "
                f"The AI anomaly layer detected "
                f"a deviation from the expected "
                f"operating pattern."
            )

        elif recommendation:

            priority = "MEDIUM"

            explanation = (
                f"{category} requires attention "
                f"because {metric} may be outside "
                f"the preferred operational range "
                f"or requires preventive review."
            )

        else:

            priority = "LOW"

            explanation = (
                f"{category} is currently operating "
                f"without a significant detected issue."
            )

        # -----------------------------------------------------
        # FORECAST
        # -----------------------------------------------------

        forecast_signal = "UNKNOWN"

        if isinstance(
            forecast,
            dict
        ):

            forecast_signal = (
                forecast.get(
                    "trend",
                    forecast.get(
                        "forecast_trend",
                        "UNKNOWN"
                    )
                )
            )

        # -----------------------------------------------------
        # EVIDENCE
        # -----------------------------------------------------

        evidence = []

        for item in retrieved:

            evidence.append(
                {
                    "source":
                        item.get(
                            "source",
                            "unknown"
                        ),

                    "relevance":
                        float(
                            item.get(
                                "score",
                                0.0
                            )
                        ),

                    "evidence":
                        item.get(
                            "text",
                            ""
                        )
                }
            )

        # -----------------------------------------------------
        # DEFAULT GROUNDED RECOMMENDATION
        # -----------------------------------------------------

        grounded_recommendation = (
            recommendation
        )

        if not grounded_recommendation:

            if category.upper() == "ENERGY":

                grounded_recommendation = (
                    "Investigate HVAC operating "
                    "schedules, cooling or heating "
                    "demand, lighting operation, "
                    "and high-load equipment."
                )

            elif category.upper() == "WATER":

                grounded_recommendation = (
                    "Verify sensor readings and "
                    "investigate possible leaks, "
                    "occupancy changes, irrigation "
                    "demand, and abnormal equipment "
                    "consumption."
                )

            elif category.upper() == "WASTE":

                grounded_recommendation = (
                    "Investigate sources of increased "
                    "waste generation and review "
                    "segregation and collection "
                    "practices."
                )

            elif category.upper() == "TRAFFIC":

                grounded_recommendation = (
                    "Review vehicle flow, parking "
                    "occupancy, and entry/exit "
                    "operations."
                )

            else:

                grounded_recommendation = (
                    "Continue monitoring facility "
                    "operations and investigate "
                    "persistent deviations."
                )

        # -----------------------------------------------------
        # CONFIDENCE
        # -----------------------------------------------------

        if len(evidence) >= 2:

            confidence = "HIGH"

        elif len(evidence) == 1:

            confidence = "MEDIUM"

        else:

            confidence = "LOW"

        # -----------------------------------------------------
        # RESULT
        # -----------------------------------------------------

        return {

            "category":
                category,

            "metric":
                metric,

            "current_value":
                current_value,

            "priority":
                priority,

            "confidence":
                confidence,

            "anomaly":
                {
                    "status":
                        normalized_status,

                    "score":
                        anomaly_score
                },

            "explanation":
                explanation,

            "recommendation":
                grounded_recommendation,

            "forecast_signal":
                forecast_signal,

            "context":
                context,

            "rag_query":
                query,

            "evidence":
                evidence,

            "evidence_count":
                len(evidence),

            "retrieved_context":
                context_text,

            "generated_at":
                datetime.now().isoformat()
        }


# =========================================================
# PIPELINE COMPATIBILITY ALIAS
# =========================================================

DecisionReasoner = DecisionReasoningEngine


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("CAMPUS360 DECISION REASONING TEST")
    print("=" * 60)

    engine = DecisionReasoningEngine()

    result = engine.analyze(

        category="ENERGY",

        metric="HVAC consumption",

        current_value=75,

        anomaly_status="ANOMALY",

        anomaly_score=-0.72,

        recommendation=(
            "Inspect HVAC systems, "
            "lighting, and high-load equipment."
        ),

        forecast={
            "trend": "INCREASING"
        },

        context={
            "building":
                "Administration Building",

            "building_type":
                "OFFICE",

            "occupancy":
                78
        }
    )

    print(
        "\nPriority:",
        result["priority"]
    )

    print(
        "Confidence:",
        result["confidence"]
    )

    print(
        "Explanation:",
        result["explanation"]
    )

    print(
        "Recommendation:",
        result["recommendation"]
    )

    print(
        "Forecast:",
        result["forecast_signal"]
    )

    print(
        "Evidence count:",
        result["evidence_count"]
    )

    print("=" * 60)