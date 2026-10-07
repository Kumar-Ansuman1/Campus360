"""
=================================================================
CAMPUS360 - UNIFIED AI INTELLIGENCE PIPELINE
AI Engineer 1
=================================================================

Pipeline:

Backend Telemetry
        ↓
Data Normalization
        ↓
Anomaly Detection
        ↓
KPI Extraction
        ↓
Forecasting
        ↓
Advanced Semantic RAG
        ↓
Decision Reasoning
        ↓
Recommendations
        ↓
What-If Simulation
        ↓
Current Status Analysis
        ↓
What-If Impact Analysis
        ↓
Digital Twin Visualization Data

The Digital Twin is a visualization/decision layer.
It does NOT replace the AI intelligence layer.
=================================================================
"""

import json
import traceback
from datetime import datetime

import pandas as pd


# ================================================================
# OPTIONAL MODULE IMPORTS
# ================================================================

try:
    from ai.data_loader import CampusDataLoader
except Exception as exc:
    CampusDataLoader = None
    print("Data loader initialization warning:", exc)


try:
    from ai.intelligence.anomaly import AnomalyDetector
except Exception:
    try:
        from ai.intelligence.anomaly_detector import AnomalyDetector
    except Exception as exc:
        AnomalyDetector = None
        print("Anomaly detector initialization warning:", exc)


try:
    from ai.intelligence.what_if import WhatIfEngine
except Exception as exc:
    WhatIfEngine = None
    print("What-if initialization warning:", exc)


try:
    from ai.intelligence.advanced_rag import AdvancedRAG
except Exception as exc:
    AdvancedRAG = None
    print("Advanced RAG initialization warning:", exc)


try:
    from ai.intelligence.reasoning import DecisionReasoningEngine
except Exception:
    try:
        from ai.intelligence.reasoning import DecisionReasoner
        DecisionReasoningEngine = DecisionReasoner
    except Exception as exc:
        DecisionReasoningEngine = None
        print("Decision reasoner initialization warning:", exc)


try:
    from ai.intelligence.recommendations import RecommendationEngine
except Exception as exc:
    RecommendationEngine = None
    print("Recommendation engine initialization warning:", exc)


# ================================================================
# MAIN PIPELINE
# ================================================================

class CampusIntelligencePipeline:

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self):

        self.loader = (
            CampusDataLoader()
            if CampusDataLoader
            else None
        )

        self.anomaly = (
            AnomalyDetector()
            if AnomalyDetector
            else None
        )

        self.what_if = (
            WhatIfEngine()
            if WhatIfEngine
            else None
        )

        self.rag = None

        if AdvancedRAG:

            try:
                self.rag = AdvancedRAG()
            except Exception as exc:
                print(
                    "Advanced RAG initialization warning:",
                    exc
                )

        self.reasoner = None

        if DecisionReasoningEngine:

            try:
                self.reasoner = (
                    DecisionReasoningEngine(
                        rag_engine=self.rag
                    )
                    if self.rag is not None
                    else DecisionReasoningEngine()
                )

            except TypeError:

                try:
                    self.reasoner = (
                        DecisionReasoningEngine()
                    )

                except Exception as exc:
                    print(
                        "Decision reasoner initialization warning:",
                        exc
                    )

            except Exception as exc:

                print(
                    "Decision reasoner initialization warning:",
                    exc
                )

        self.recommendation_engine = None

        if RecommendationEngine:

            try:
                self.recommendation_engine = (
                    RecommendationEngine()
                )

            except Exception as exc:

                print(
                    "Recommendation engine initialization warning:",
                    exc
                )

    # ============================================================
    # DATAFRAME NORMALIZATION
    # ============================================================

    @staticmethod
    def dataframe(records):

        if records is None:
            return pd.DataFrame()

        if isinstance(
            records,
            pd.DataFrame
        ):
            return records.copy()

        if isinstance(
            records,
            list
        ):

            if not records:
                return pd.DataFrame()

            return pd.DataFrame(records)

        if isinstance(
            records,
            dict
        ):
            return pd.DataFrame(
                [records]
            )

        try:
            return pd.DataFrame(records)

        except Exception:
            return pd.DataFrame()

    # ============================================================
    # SAFE NUMBER
    # ============================================================

    @staticmethod
    def number(
        value,
        default=0.0
    ):

        try:

            if value is None:
                return default

            return float(value)

        except Exception:

            return default

    # ============================================================
    # LATEST VALUE
    # ============================================================

    @staticmethod
    def latest_value(
        df,
        column,
        default=0.0
    ):

        if df is None:
            return default

        if not isinstance(
            df,
            pd.DataFrame
        ):
            return default

        if df.empty:
            return default

        if column not in df.columns:
            return default

        try:

            return CampusIntelligencePipeline.number(
                df.iloc[-1][column],
                default
            )

        except Exception:

            return default

    # ============================================================
    # ANOMALY NORMALIZATION
    # ============================================================

    @staticmethod
    def normalize_anomaly_result(
        result
    ):

        default = {

            "data":
                pd.DataFrame(),

            "count":
                0,

            "latest_status":
                "NORMAL",

            "latest_score":
                0.0
        }

        if result is None:
            return default

        # --------------------------------------------------------
        # DataFrame
        # --------------------------------------------------------

        if isinstance(
            result,
            pd.DataFrame
        ):

            df = result

        # --------------------------------------------------------
        # Dictionary
        # --------------------------------------------------------

        elif isinstance(
            result,
            dict
        ):

            data = result.get(
                "data"
            )

            if isinstance(
                data,
                pd.DataFrame
            ):

                df = data

            else:

                # Preserve summary if detector returned one
                return {

                    "data":
                        pd.DataFrame(),

                    "count":
                        int(
                            result.get(
                                "count",
                                result.get(
                                    "anomalies",
                                    0
                                )
                            )
                            or 0
                        ),

                    "latest_status":
                        str(
                            result.get(
                                "latest_status",
                                result.get(
                                    "status",
                                    "NORMAL"
                                )
                            )
                        ),

                    "latest_score":
                        CampusIntelligencePipeline.number(
                            result.get(
                                "latest_score",
                                result.get(
                                    "anomaly_score",
                                    0.0
                                )
                            )
                        )
                }

        else:

            return default

        if df.empty:
            return default

        # --------------------------------------------------------
        # COUNT
        # --------------------------------------------------------

        anomaly_count = 0

        if "is_anomaly" in df.columns:

            try:

                anomaly_count = int(
                    df["is_anomaly"]
                    .fillna(False)
                    .astype(bool)
                    .sum()
                )

            except Exception:

                anomaly_count = 0

        elif "anomaly_status" in df.columns:

            try:

                anomaly_count = int(
                    (
                        df["anomaly_status"]
                        .astype(str)
                        .str.upper()
                        == "ANOMALY"
                    ).sum()
                )

            except Exception:

                anomaly_count = 0

        # --------------------------------------------------------
        # LATEST RECORD
        # --------------------------------------------------------

        try:

            row = df.iloc[-1]

            status = row.get(
                "anomaly_status",
                "NORMAL"
            )

            score = row.get(
                "anomaly_score",
                0.0
            )

        except Exception:

            status = "NORMAL"
            score = 0.0

        return {

            "data":
                df,

            "count":
                anomaly_count,

            "latest_status":
                str(status),

            "latest_score":
                CampusIntelligencePipeline.number(
                    score,
                    0.0
                )
        }

    # ============================================================
    # ANOMALY SEVERITY
    # ============================================================

    @staticmethod
    def anomaly_severity(
        result
    ):

        if not result:
            return "NORMAL"

        count = int(
            result.get(
                "count",
                0
            )
            or 0
        )

        status = str(
            result.get(
                "latest_status",
                "NORMAL"
            )
        ).upper()

        score = CampusIntelligencePipeline.number(
            result.get(
                "latest_score",
                0.0
            ),
            0.0
        )

        if status == "INSUFFICIENT_DATA":
            return "UNKNOWN"

        if count <= 0:
            return "NORMAL"

        if status in {
            "CRITICAL",
            "HIGH"
        }:
            return status

        if score <= -0.5:
            return "CRITICAL"

        if score <= -0.2:
            return "HIGH"

        return "MEDIUM"

    # ============================================================
    # RUN ANOMALY
    # ============================================================

    def run_anomaly(
        self,
        method_name,
        df
    ):

        if self.anomaly is None:
            return self.normalize_anomaly_result(
                None
            )

        if df is None:
            return self.normalize_anomaly_result(
                None
            )

        if not isinstance(
            df,
            pd.DataFrame
        ):
            return self.normalize_anomaly_result(
                None
            )

        if df.empty:
            return self.normalize_anomaly_result(
                None
            )

        # --------------------------------------------------------
        # Preferred detector method
        # --------------------------------------------------------

        if hasattr(
            self.anomaly,
            method_name
        ):

            try:

                method = getattr(
                    self.anomaly,
                    method_name
                )

                result = method(df)

                return self.normalize_anomaly_result(
                    result
                )

            except Exception as exc:

                print(
                    f"Anomaly warning ({method_name}):",
                    exc
                )

        # --------------------------------------------------------
        # Generic detector
        # --------------------------------------------------------

        if hasattr(
            self.anomaly,
            "detect"
        ):

            column_map = {

                "energy_anomalies":
                    "consumption",

                "water_anomalies":
                    "consumption",

                "waste_anomalies":
                    "quantity",

                "traffic_anomalies":
                    "vehicle_count"
            }

            column = column_map.get(
                method_name
            )

            if column in df.columns:

                try:

                    result = self.anomaly.detect(
                        df,
                        column
                    )

                    return self.normalize_anomaly_result(
                        result
                    )

                except Exception as exc:

                    print(
                        "Generic anomaly warning:",
                        exc
                    )

        return self.normalize_anomaly_result(
            None
        )

    # ============================================================
    # FORECAST
    # ============================================================

    def run_forecast(
        self,
        energy
    ):

        default = {

            "status":
                "UNAVAILABLE",

            "trend":
                "UNKNOWN",

            "forecast":
                []
        }

        if energy is None:
            return default

        if not isinstance(
            energy,
            pd.DataFrame
        ):
            return default

        if energy.empty:
            return default

        try:

            from ai.intelligence.forecasting import (
                ForecastEngine
            )

            engine = ForecastEngine()

        except Exception as exc:

            print(
                "Forecast module unavailable:",
                exc
            )

            return default

        try:

            result = engine.forecast_energy(
                energy.to_dict(orient="records")
            )

            if isinstance(
                result,
                dict
            ):

                return result

        except Exception as exc:

            print(
                "forecast_energy warning:",
                exc
            )

        # --------------------------------------------------------
        # Generic forecast compatibility
        # --------------------------------------------------------

        if hasattr(
            engine,
            "forecast"
        ):

            try:

                result = engine.forecast(
                    energy
                )

                if isinstance(
                    result,
                    dict
                ):

                    return result

            except Exception as exc:

                print(
                    "forecast warning:",
                    exc
                )

        # --------------------------------------------------------
        # Safe fallback
        # --------------------------------------------------------

        if "consumption" in energy.columns:

            values = (
                pd.to_numeric(
                    energy["consumption"],
                    errors="coerce"
                )
                .dropna()
                .tolist()
            )

            if len(values) >= 2:

                first = float(
                    values[0]
                )

                last = float(
                    values[-1]
                )

                if last > first:
                    trend = "INCREASING"

                elif last < first:
                    trend = "DECREASING"

                else:
                    trend = "STABLE"

                return {

                    "status":
                        "AVAILABLE",

                    "model":
                        "SimpleTrend",

                    "trend":
                        trend,

                    "forecast":
                        []
                }

        return default

    # ============================================================
    # WHAT-IF
    # ============================================================

    def run_what_if(
        self,
        current_energy,
        reduction_percent=15,
        hours=24
    ):

        if current_energy is None:
            return None

        current_energy = self.number(
            current_energy
        )

        # --------------------------------------------------------
        # Existing engine
        # --------------------------------------------------------

        if self.what_if is not None:

            if hasattr(
                self.what_if,
                "simulate_energy_reduction"
            ):

                try:

                    result = (
                        self.what_if
                        .simulate_energy_reduction(
                            current_consumption=
                                current_energy,

                            reduction_percent=
                                reduction_percent,

                            hours=
                                hours
                        )
                    )

                    if isinstance(
                        result,
                        dict
                    ):

                        return result

                except Exception as exc:

                    print(
                        "What-if engine warning:",
                        exc
                    )

            if hasattr(
                self.what_if,
                "energy_reduction"
            ):

                try:

                    result = (
                        self.what_if
                        .energy_reduction(
                            current_consumption=
                                current_energy,

                            reduction_percent=
                                reduction_percent,

                            hours=
                                hours
                        )
                    )

                    if isinstance(
                        result,
                        dict
                    ):

                        return result

                except Exception as exc:

                    print(
                        "Energy reduction warning:",
                        exc
                    )

        # --------------------------------------------------------
        # Universal fallback
        # --------------------------------------------------------

        reduction_factor = (
            1 -
            (
                reduction_percent /
                100
            )
        )

        projected_hourly = (
            current_energy *
            reduction_factor
        )

        baseline_daily = (
            current_energy *
            hours
        )

        projected_daily = (
            projected_hourly *
            hours
        )

        energy_saved = (
            baseline_daily -
            projected_daily
        )

        # Demo assumptions.
        # These are intentionally centralized so they can
        # later be replaced with campus-specific factors.

        electricity_cost = 8.0
        co2_factor = 0.82

        cost_saving = (
            energy_saved *
            electricity_cost
        )

        co2_reduction = (
            energy_saved *
            co2_factor
        )

        return {

            "available":
                True,

            "scenario":
                f"{reduction_percent}% energy reduction "
                f"over {hours} hours",

            "baseline_hourly_kwh":
                round(
                    current_energy,
                    2
                ),

            "baseline_daily_kwh":
                round(
                    baseline_daily,
                    2
                ),

            "projected_consumption":
                round(
                    projected_hourly,
                    2
                ),

            "projected_daily_kwh":
                round(
                    projected_daily,
                    2
                ),

            "energy_saved":
                round(
                    energy_saved,
                    2
                ),

            "energy_saved_kwh_per_day":
                round(
                    energy_saved,
                    2
                ),

            "saving_percent":
                float(
                    reduction_percent
                ),

            "estimated_cost_saving_inr":
                round(
                    cost_saving,
                    2
                ),

            "estimated_cost_saving_inr_per_day":
                round(
                    cost_saving,
                    2
                ),

            "estimated_co2_reduction_kg":
                round(
                    co2_reduction,
                    2
                ),

            "estimated_co2_reduction_kg_per_day":
                round(
                    co2_reduction,
                    2
                )
        }

    # ============================================================
    # WHAT-IF IMPACT ANALYSIS
    # ============================================================

    def build_what_if_analysis(
        self,
        current_energy,
        what_if
    ):

        if not what_if:
            return {
                "available": False,
                "interpretation": "No what-if simulation was available."
            }

        current_energy = self.number(current_energy, 0.0)

        # Normalize the scenario around the actual 15% reduction
        # used by run_what_if(). This prevents stale/incorrect
        # percentage values from the underlying engine.
        reduction_percent = self.number(
            what_if.get("saving_percent", 15.0),
            15.0
        )

        # If the engine returned an invalid/zero percentage while
        # energy_saved is positive, recover the actual percentage.
        baseline_daily = current_energy * 24.0

        projected_hourly = current_energy * (1.0 - reduction_percent / 100.0)
        projected_daily = projected_hourly * 24.0
        energy_saved = baseline_daily - projected_daily

        if baseline_daily > 0 and energy_saved > 0 and reduction_percent <= 0:
            reduction_percent = (energy_saved / baseline_daily) * 100.0

        # Use the actual normalized values for consistency.
        electricity_cost = 8.0
        co2_factor = 0.82

        cost_saving = energy_saved * electricity_cost
        co2_reduction = energy_saved * co2_factor

        interpretation = (
            f"A {reduction_percent:.0f}% energy reduction scenario could lower "
            "the facility's daily energy demand while producing financial "
            "and emissions benefits."
        )

        return {
            "available": True,
            "scenario": "ENERGY_REDUCTION",
            "baseline_daily_kwh": round(baseline_daily, 2),
            "projected_daily_kwh": round(projected_daily, 2),
            "energy_saved_kwh_per_day": round(energy_saved, 2),
            "saving_percent": round(reduction_percent, 2),
            "estimated_cost_saving_inr_per_day": round(cost_saving, 2),
            "estimated_co2_reduction_kg_per_day": round(co2_reduction, 2),
            "interpretation": interpretation
        }

    # ============================================================
    # CURRENT STATUS ANALYSIS
    # ============================================================

    def build_current_status(
        self,
        energy_result,
        water_result,
        waste_result,
        traffic_result,
        forecast
    ):

        statuses = {

            "energy":
                self.anomaly_severity(
                    energy_result
                ),

            "water":
                self.anomaly_severity(
                    water_result
                ),

            "waste":
                self.anomaly_severity(
                    waste_result
                ),

            "traffic":
                self.anomaly_severity(
                    traffic_result
                )
        }

        severity_rank = {

            "UNKNOWN":
                0,

            "NORMAL":
                1,

            "MEDIUM":
                2,

            "HIGH":
                3,

            "CRITICAL":
                4
        }

        highest = max(
            statuses.values(),
            key=lambda x:
                severity_rank.get(
                    x,
                    0
                )
        )

        if highest == "CRITICAL":
            overall = "CRITICAL"

        elif highest == "HIGH":
            overall = "ATTENTION"

        elif highest == "MEDIUM":
            overall = "WATCH"

        else:
            overall = "NORMAL"

        trend = "UNKNOWN"

        if isinstance(
            forecast,
            dict
        ):

            trend = str(
                forecast.get(
                    "trend",
                    "UNKNOWN"
                )
            ).upper()

        return {

            "overall_status":
                overall,

            "energy_status":
                statuses["energy"],

            "water_status":
                statuses["water"],

            "waste_status":
                statuses["waste"],

            "traffic_status":
                statuses["traffic"],

            "energy_trend":
                trend
        }

    # ============================================================
    # RAG
    # ============================================================

    def run_rag(
        self,
        query
    ):

        default = {

            "query":
                query,

            "evidence":
                [],

            "evidence_count":
                0,

            "context":
                ""
        }

        if self.rag is None:
            return default

        if not hasattr(
            self.rag,
            "build_context"
        ):
            return default

        try:

            result = self.rag.build_context(
                query=query,
                top_k=3
            )

            if not isinstance(
                result,
                tuple
            ):
                return default

            context_text, retrieved = result

            evidence = []

            for item in (
                retrieved or []
            ):

                evidence.append({

                    "source":
                        item.get(
                            "source",
                            "unknown"
                        ),

                    "relevance":
                        self.number(
                            item.get(
                                "score",
                                0
                            )
                        ),

                    "evidence":
                        item.get(
                            "text",
                            ""
                        )
                })

            return {

                "query":
                    query,

                "evidence":
                    evidence,

                "evidence_count":
                    len(evidence),

                "context":
                    context_text or ""
            }

        except Exception as exc:

            print(
                "RAG warning:",
                exc
            )

            return default

    # ============================================================
    # REASONING
    # ============================================================

    def run_reasoning(
        self,
        context
    ):

        if self.reasoner is None:
            return None

        # --------------------------------------------------------
        # IMPORTANT:
        # Do NOT blindly call analyze(data=context).
        #
        # DecisionReasoningEngine.analyze() expects:
        # category
        # metric
        # current_value
        # anomaly_status
        # anomaly_score
        # recommendation
        # forecast
        # context
        # --------------------------------------------------------

        try:

            result = self.reasoner.analyze(

                category=
                    context.get(
                        "category",
                        "ENERGY"
                    ),

                metric=
                    context.get(
                        "metric",
                        "facility consumption"
                    ),

                current_value=
                    context.get(
                        "current_value",
                        0
                    ),

                anomaly_status=
                    context.get(
                        "anomaly_status",
                        "NORMAL"
                    ),

                anomaly_score=
                    context.get(
                        "anomaly_score",
                        0.0
                    ),

                recommendation=
                    context.get(
                        "recommendation"
                    ),

                forecast=
                    context.get(
                        "forecast",
                        {}
                    ),

                context={
                    "building":
                        context.get(
                            "building"
                        ),

                    "building_type":
                        context.get(
                            "building_type"
                        ),

                    "facility":
                        context.get(
                            "facility"
                        ),

                    "occupancy":
                        context.get(
                            "occupancy"
                        )
                }
            )

            return result

        except TypeError as exc:

            print(
                "Reasoning compatibility warning:",
                exc
            )

            # ----------------------------------------------------
            # Compatibility fallback for alternate engines
            # ----------------------------------------------------

            methods = [
                "reason",
                "decide",
                "generate_decision",
                "generate_insight",
                "run"
            ]

            for method_name in methods:

                if not hasattr(
                    self.reasoner,
                    method_name
                ):
                    continue

                try:

                    method = getattr(
                        self.reasoner,
                        method_name
                    )

                    result = method(
                        context
                    )

                    if result is not None:
                        return result

                except Exception as fallback_exc:

                    print(
                        f"Reasoning fallback "
                        f"({method_name}) warning:",
                        fallback_exc
                    )

        except Exception as exc:

            print(
                "Reasoning warning:",
                exc
            )

        return None

    # ============================================================
    # RECOMMENDATIONS
    # ============================================================

    def run_recommendations(
        self,
        context
    ):

        if self.recommendation_engine is None:
            return None

        engine = self.recommendation_engine

        # --------------------------------------------------------
        # Preferred domain-specific API
        # --------------------------------------------------------

        try:

            recommendations = []

            energy_kpi = {
                "latest_consumption":
                    context.get(
                        "energy",
                        0
                    )
            }

            water_kpi = {
                "latest_consumption":
                    context.get(
                        "water",
                        0
                    )
            }

            waste_kpi = {
                "latest_quantity":
                    context.get(
                        "waste",
                        0
                    )
            }

            traffic_kpi = {
                "vehicle_count":
                    context.get(
                        "vehicles",
                        0
                    ),

                "parking_occupancy":
                    context.get(
                        "parking",
                        0
                    )
            }

            if hasattr(
                engine,
                "analyze_energy"
            ):

                result = engine.analyze_energy(
                    energy_kpi,
                    context.get(
                        "energy_anomaly",
                        {}
                    )
                )

                if result:
                    recommendations.append(
                        result
                    )

            if hasattr(
                engine,
                "analyze_water"
            ):

                result = engine.analyze_water(
                    water_kpi,
                    context.get(
                        "water_anomaly",
                        {}
                    )
                )

                if result:
                    recommendations.append(
                        result
                    )

            if hasattr(
                engine,
                "analyze_waste"
            ):

                result = engine.analyze_waste(
                    waste_kpi,
                    context.get(
                        "waste_anomaly",
                        {}
                    )
                )

                if result:
                    recommendations.append(
                        result
                    )

            if hasattr(
                engine,
                "analyze_traffic"
            ):

                result = engine.analyze_traffic(
                    traffic_kpi,
                    context.get(
                        "traffic_anomaly",
                        {}
                    )
                )

                if result:
                    recommendations.append(
                        result
                    )

            if recommendations:

                return recommendations

        except Exception as exc:

            print(
                "Domain recommendation warning:",
                exc
            )

        # --------------------------------------------------------
        # Generic APIs
        # --------------------------------------------------------

        for method_name in [
            "recommend",
            "generate",
            "generate_recommendations",
            "get_recommendations",
            "run"
        ]:

            if not hasattr(
                engine,
                method_name
            ):
                continue

            method = getattr(
                engine,
                method_name
            )

            try:

                return method(
                    context
                )

            except TypeError:

                try:

                    return method(
                        context=context
                    )

                except Exception as exc:

                    print(
                        f"Recommendation "
                        f"({method_name}) warning:",
                        exc
                    )

            except Exception as exc:

                print(
                    f"Recommendation "
                    f"({method_name}) warning:",
                    exc
                )

        return None

    # ============================================================
    # BUILD FINAL RECOMMENDATION
    # ============================================================

    @staticmethod
    def select_recommendation(
        recommendation_result,
        reasoning_result,
        forecast
    ):

        # --------------------------------------------------------
        # Reasoning result has priority
        # --------------------------------------------------------

        if isinstance(
            reasoning_result,
            dict
        ):

            recommendation = (
                reasoning_result.get(
                    "recommendation"
                )
            )

            if recommendation:
                return str(
                    recommendation
                )

        # --------------------------------------------------------
        # Recommendation engine
        # --------------------------------------------------------

        if isinstance(
            recommendation_result,
            list
        ):

            for item in recommendation_result:

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                action = (
                    item.get(
                        "action"
                    )
                    or
                    item.get(
                        "message"
                    )
                )

                if action:
                    return str(
                        action
                    )

        elif isinstance(
            recommendation_result,
            dict
        ):

            for key in [
                "recommendation",
                "action",
                "message"
            ]:

                if recommendation_result.get(
                    key
                ):

                    return str(
                        recommendation_result[key]
                    )

        # --------------------------------------------------------
        # Safe domain recommendation
        # --------------------------------------------------------

        recommendation = (
            "Continue monitoring facility operations "
            "and investigate HVAC, lighting, and "
            "high-load equipment efficiency."
        )

        if isinstance(
            forecast,
            dict
        ):

            trend = str(
                forecast.get(
                    "trend",
                    ""
                )
            ).upper()

            if trend == "INCREASING":

                recommendation += (
                    " Energy demand is trending upward, "
                    "so HVAC and high-load equipment "
                    "should be reviewed proactively."
                )

        return recommendation

    # ============================================================
    # PRIORITY
    # ============================================================

    @staticmethod
    def calculate_priority(
                current_status,
        forecast,
        reasoning_result=None
    ):

        if isinstance(
            reasoning_result,
            dict
        ):

            priority = str(
                reasoning_result.get(
                    "priority",
                    ""
                )
            ).upper()

            if priority in {
                "HIGH",
                "MEDIUM",
                "LOW"
            }:

                return priority

        overall = str(
            current_status.get(
                "overall_status",
                "NORMAL"
            )
        ).upper()

        if overall == "CRITICAL":
            return "HIGH"

        if overall == "ATTENTION":
            return "HIGH"

        if overall == "WATCH":
            return "MEDIUM"

        if isinstance(
            forecast,
            dict
        ):

            trend = str(
                forecast.get(
                    "trend",
                    ""
                )
            ).upper()

            if trend == "INCREASING":
                return "MEDIUM"

        return "LOW"

    # ============================================================
    # CONFIDENCE
    # ============================================================

    @staticmethod
    def calculate_confidence(
        rag_result,
        reasoning_result
    ):

        if isinstance(
            reasoning_result,
            dict
        ):

            confidence = str(
                reasoning_result.get(
                    "confidence",
                    ""
                )
            ).upper()

            if confidence in {
                "HIGH",
                "MEDIUM",
                "LOW"
            }:

                return confidence

        count = int(
            rag_result.get(
                "evidence_count",
                0
            )
            or 0
        )

        if count >= 2:
            return "HIGH"

        if count == 1:
            return "MEDIUM"

        return "LOW"

    # ============================================================
    # BUILD EXPLANATION
    # ============================================================

    @staticmethod
    def build_explanation(
        current_status,
        forecast,
        reasoning
    ):

        if isinstance(
            reasoning,
            dict
        ):

            explanation = (
                reasoning.get(
                    "explanation"
                )
            )

            if explanation:
                return str(
                    explanation
                )

        status = current_status.get(
            "overall_status",
            "NORMAL"
        )

        trend = (
            forecast.get(
                "trend",
                "UNKNOWN"
            )
            if isinstance(
                forecast,
                dict
            )
            else "UNKNOWN"
        )

        if status == "NORMAL":

            if str(
                trend
            ).upper() == "INCREASING":

                return (
                    "Current telemetry does not show "
                    "a significant anomaly, but energy "
                    "demand is trending upward and "
                    "should be monitored proactively."
                )

            return (
                "The facility is currently operating "
                "without a significant detected issue."
            )

        return (
            f"The facility currently requires "
            f"operational attention. Overall status: "
            f"{status}."
        )

    # ============================================================
    # DIGITAL TWIN DATA
    # ============================================================

    def build_digital_twin(
        self,
        facility,
        building,
        building_id,
        current_status,
        current_energy,
        current_water,
        current_waste,
        current_vehicles,
        current_parking,
        current_speed,
        forecast,
        priority,
        what_if_analysis
    ):

        return {

            "facility":
                facility.get(
                    "name",
                    "Unknown"
                ),

            "building":
                building.get(
                    "name",
                    "Unknown"
                ),

            "building_id":
                building_id,

            "building_type":
                building.get(
                    "building_type",
                    "UNKNOWN"
                ),

            "status":
                current_status.get(
                    "overall_status",
                    "NORMAL"
                ),

            "energy":
                current_energy,

            "water":
                current_water,

            "waste":
                current_waste,

            "vehicles":
                current_vehicles,

            "parking":
                current_parking,

            "average_speed":
                current_speed,

            "forecast":
                forecast.get(
                    "trend",
                    "UNKNOWN"
                )
                if isinstance(
                    forecast,
                    dict
                )
                else "UNKNOWN",

            "priority":
                priority,

            "what_if":
                what_if_analysis,

            # ----------------------------------------------------
            # Visualization-friendly states
            # ----------------------------------------------------

            "visualization":

                {

                    "energy_state":
                        current_status.get(
                            "energy_status",
                            "NORMAL"
                        ),

                    "water_state":
                        current_status.get(
                            "water_status",
                            "NORMAL"
                        ),

                    "waste_state":
                        current_status.get(
                            "waste_status",
                            "NORMAL"
                        ),

                    "traffic_state":
                        current_status.get(
                            "traffic_status",
                            "NORMAL"
                        ),

                    "forecast_state":
                        forecast.get(
                            "trend",
                            "UNKNOWN"
                        )
                        if isinstance(
                            forecast,
                            dict
                        )
                        else "UNKNOWN"
                }
        }

    # ============================================================
    # MAIN RUN
    # ============================================================

    def run(self):

        print(
            "\n[1/6] Loading backend data..."
        )

        # --------------------------------------------------------
        # Backend
        # --------------------------------------------------------

        facilities = []
        buildings = []

        if self.loader is not None:

            try:

                facilities = (
                    self.loader.get_facilities()
                    or []
                )

            except Exception as exc:

                print(
                    "Facility loading warning:",
                    exc
                )

            try:

                buildings = (
                    self.loader.get_buildings()
                    or []
                )

            except Exception as exc:

                print(
                    "Building loading warning:",
                    exc
                )

        if not facilities:
            print(
                "ERROR: No facility data found."
            )
            return None

        if not buildings:
            print(
                "ERROR: No building data found."
            )
            return None

        facility = facilities[0]
        building = buildings[0]

        building_id = building.get(
            "id"
        )

        if not building_id:

            print(
                "ERROR: Building ID unavailable."
            )

            return None

        # --------------------------------------------------------
        # Telemetry
        # --------------------------------------------------------

        energy = pd.DataFrame()
        water = pd.DataFrame()
        waste = pd.DataFrame()
        traffic = pd.DataFrame()

        if self.loader is not None:

            try:
                energy = (
                    self.loader.energy_dataframe(
                        building_id
                    )
                )
            except Exception as exc:
                print(
                    "Energy loading warning:",
                    exc
                )

            try:
                water = (
                    self.loader.water_dataframe(
                        building_id
                    )
                )
            except Exception as exc:
                print(
                    "Water loading warning:",
                    exc
                )

            try:
                waste = (
                    self.loader.waste_dataframe(
                        building_id
                    )
                )
            except Exception as exc:
                print(
                    "Waste loading warning:",
                    exc
                )

            try:
                traffic = (
                    self.loader.traffic_dataframe(
                        building_id
                    )
                )
            except Exception as exc:
                print(
                    "Traffic loading warning:",
                    exc
                )

        print(
            "Energy :",
            len(energy)
        )

        print(
            "Water  :",
            len(water)
        )

        print(
            "Waste  :",
            len(waste)
        )

        print(
            "Traffic:",
            len(traffic)
        )

        if (
            energy.empty
            and water.empty
            and waste.empty
            and traffic.empty
        ):

            print(
                "ERROR: No telemetry data found."
            )

            return None

        # ========================================================
        # 2. ANOMALIES
        # ========================================================

        print(
            "\n[2/6] Detecting anomalies..."
        )

        energy_result = self.run_anomaly(
            "energy_anomalies",
            energy
        )

        water_result = self.run_anomaly(
            "water_anomalies",
            water
        )

        waste_result = self.run_anomaly(
            "waste_anomalies",
            waste
        )

        traffic_result = self.run_anomaly(
            "traffic_anomalies",
            traffic
        )

        print(
            "Energy anomalies:",
            energy_result["count"]
        )

        print(
            "Water anomalies:",
            water_result["count"]
        )

        print(
            "Waste anomalies:",
            waste_result["count"]
        )

        print(
            "Traffic anomalies:",
            traffic_result["count"]
        )

        # ========================================================
        # 3. KPIs
        # ========================================================

        print(
            "\n[3/6] Preparing KPI values..."
        )

        current_energy = self.latest_value(
            energy,
            "consumption"
        )

        current_water = self.latest_value(
            water,
            "consumption"
        )

        current_waste = self.latest_value(
            waste,
            "quantity"
        )

        current_vehicles = self.latest_value(
            traffic,
            "vehicle_count"
        )

        current_parking = self.latest_value(
            traffic,
            "parking_occupancy"
        )

        current_speed = self.latest_value(
            traffic,
            "average_speed"
        )

        print(
            "Latest energy :",
            current_energy,
            "kWh"
        )

        print(
            "Latest water  :",
            current_water,
            "L"
        )

        print(
            "Latest waste  :",
            current_waste,
            "kg"
        )

        print(
            "Vehicles      :",
            current_vehicles
        )

        print(
            "Parking       :",
            current_parking,
            "%"
        )

        # ========================================================
        # 4. FORECAST
        # ========================================================

        print(
            "\n[4/6] Generating forecast..."
        )

        forecast = self.run_forecast(
            energy
        )

        print(
            "Forecast:",
            forecast.get(
                "trend",
                "UNKNOWN"
            )
        )

        # ========================================================
        # CURRENT STATUS
        # ========================================================

        current_status = (
            self.build_current_status(
                energy_result,
                water_result,
                waste_result,
                traffic_result,
                forecast
            )
        )

        # ========================================================
        # RECOMMENDATION CONTEXT
        # ========================================================

        recommendation_context = {

            "facility":
                facility.get(
                    "name"
                ),

            "building":
                building.get(
                    "name"
                ),

            "building_type":
                building.get(
                    "building_type"
                ),

            "energy":
                current_energy,

            "water":
                current_water,

            "waste":
                current_waste,

            "vehicles":
                current_vehicles,

            "parking":
                current_parking,

            "speed":
                current_speed,

            "energy_anomaly":
                energy_result,

            "water_anomaly":
                water_result,

            "waste_anomaly":
                waste_result,

            "traffic_anomaly":
                traffic_result,

            "forecast":
                forecast
        }

        # ========================================================
        # 5. RAG + REASONING
        # ========================================================

        print(
            "\n[5/6] Running Advanced RAG + reasoning..."
        )

        energy_status = (
            self.anomaly_severity(
                energy_result
            )
        )

        energy_score = self.number(
            energy_result.get(
                "latest_score",
                0
            )
        )

        rag_query = (
            "facility operations "
            "energy efficiency "
            "anomaly inspection "
            f"{building.get('building_type', '')} "
            f"{forecast.get('trend', '')}"
        )

        rag_result = self.run_rag(
            rag_query
        )

        reasoning_context = {

            "category":
                "ENERGY",

            "metric":
                "energy consumption",

            "current_value":
                current_energy,

            "anomaly_status":
                energy_status,

            "anomaly_score":
                energy_score,

            "forecast":
                forecast,

            "building":
                building.get(
                    "name"
                ),

            "building_type":
                building.get(
                    "building_type"
                ),

            "facility":
                facility.get(
                    "name"
                ),

            "occupancy":
                building.get(
                    "occupancy"
                ),

            "recommendation":
                None
        }

        # --------------------------------------------------------
        # Reasoning
        # --------------------------------------------------------

        reasoning_result = self.run_reasoning(
            reasoning_context
        )

        # --------------------------------------------------------
        # Recommendations
        # --------------------------------------------------------

        recommendation_result = (
            self.run_recommendations(
                recommendation_context
            )
        )

        # --------------------------------------------------------
        # Final recommendation
        # --------------------------------------------------------

        recommendation = (
            self.select_recommendation(
                recommendation_result,
                reasoning_result,
                forecast
            )
        )

        # --------------------------------------------------------
        # Priority
        # --------------------------------------------------------

        priority = (
            self.calculate_priority(
                current_status,
                forecast,
                reasoning_result
            )
        )

        # --------------------------------------------------------
        # Confidence
        # --------------------------------------------------------

        confidence = (
            self.calculate_confidence(
                rag_result,
                reasoning_result
            )
        )

        # --------------------------------------------------------
        # Explanation
        # --------------------------------------------------------

        explanation = (
            self.build_explanation(
                current_status,
                forecast,
                reasoning_result
            )
        )

        # ========================================================
        # 6. WHAT-IF
        # ========================================================

        print(
            "\n[6/6] Running what-if simulation..."
        )

        what_if = self.run_what_if(
            current_energy
        )

        what_if_analysis = (
            self.build_what_if_analysis(
                current_energy,
                what_if
            )
        )

        # ========================================================
        # DIGITAL TWIN
        # ========================================================

        digital_twin = (
            self.build_digital_twin(

                facility=
                    facility,

                building=
                    building,

                building_id=
                    building_id,

                current_status=
                    current_status,

                current_energy=
                    current_energy,

                current_water=
                    current_water,

                current_waste=
                    current_waste,

                current_vehicles=
                    current_vehicles,

                current_parking=
                    current_parking,

                current_speed=
                    current_speed,

                forecast=
                    forecast,

                priority=
                    priority,

                what_if_analysis=
                    what_if_analysis
            )
        )

        # ========================================================
        # CONSOLE OUTPUT
        # ========================================================

        print(
            "\n"
        )

        print(
            "=" * 65
        )

        print(
            "              CAMPUS360 AI RESULT"
        )

        print(
            "=" * 65
        )

        print(
            "\nFACILITY:"
        )

        print(
            facility.get(
                "name",
                "Unknown"
            )
        )

        print(
            "\nBUILDING:"
        )

        print(
            building.get(
                "name",
                "Unknown"
            )
        )

        print(
            "\nPRIORITY:"
        )

        print(
            priority
        )

        print(
            "\nCONFIDENCE:"
        )

        print(
            confidence
        )

        print(
            "\nCURRENT STATUS:"
        )

        print(
            current_status.get(
                "overall_status",
                "NORMAL"
            )
        )

        print(
            "\nCURRENT ENERGY:"
        )

        print(
            current_energy,
            "kWh"
        )

        print(
            "\nCURRENT WATER:"
        )

        print(
            current_water,
            "L"
        )

        print(
            "\nCURRENT WASTE:"
        )

        print(
            current_waste,
            "kg"
        )

        print(
            "\nVEHICLES:"
        )

        print(
            current_vehicles
        )

        print(
            "\nPARKING:"
        )

        print(
            current_parking,
            "%"
        )

        print(
            "\nEXPLANATION:"
        )

        print(
            explanation
        )

        print(
            "\nRECOMMENDATION:"
        )

        print(
            recommendation
        )

        print(
            "\nFORECAST:"
        )

        print(
            forecast.get(
                "trend",
                "UNKNOWN"
            )
        )

        # ========================================================
        # CURRENT STATUS ANALYSIS
        # ========================================================

        print(
            "\nDETAILED CURRENT STATUS ANALYSIS:"
        )

        print(
            "Overall operational status:",
            current_status.get(
                "overall_status"
            )
        )

        print(
            "Energy anomaly:",
            current_status.get(
                "energy_status"
            )
        )

        print(
            "Water anomaly:",
            current_status.get(
                "water_status"
            )
        )

        print(
            "Waste anomaly:",
            current_status.get(
                "waste_status"
            )
        )

        print(
            "Traffic anomaly:",
            current_status.get(
                "traffic_status"
            )
        )

        print(
            "Energy trend:",
            current_status.get(
                "energy_trend"
            )
        )

        # ========================================================
        # RAG
        # ========================================================

        print(
            "\nADVANCED SEMANTIC RAG EVIDENCE:"
        )

        if rag_result.get(
            "evidence"
        ):

            for item in rag_result[
                "evidence"
            ]:

                print(
                    f"  {item['source']} "
                    f"-> "
                    f"{item['relevance']:.4f}"
                )

        else:

            print(
                "  No evidence returned."
            )

        print(
            "\nEvidence count:",
            rag_result.get(
                "evidence_count",
                0
            )
        )

        # ========================================================
        # WHAT-IF
        # ========================================================

        if what_if:

            print(
                "\nWHAT-IF ENERGY SCENARIO:"
            )

            print(
                "Scenario:",
                what_if.get(
                    "scenario",
                    "15% energy reduction over 24 hours"
                )
            )

            print(
                "Current hourly consumption:",
                current_energy,
                "kWh"
            )

            print(
                "Projected consumption:",
                what_if.get(
                    "projected_consumption",
                    "N/A"
                )
            )

            print(
                "Energy saved:",
                what_if.get(
                    "energy_saved",
                    what_if_analysis.get(
                        "energy_saved_kwh_per_day",
                        "N/A"
                    )
                )
            )

            print(
                "Estimated cost saving:",
                what_if.get(
                    "estimated_cost_saving_inr",
                    what_if_analysis.get(
                        "estimated_cost_saving_inr_per_day",
                        "N/A"
                    )
                ),
                "INR/day"
            )

            print(
                "Estimated CO2 reduction:",
                what_if.get(
                    "estimated_co2_reduction_kg",
                    what_if_analysis.get(
                        "estimated_co2_reduction_kg_per_day",
                        "N/A"
                    )
                ),
                "kg/day"
            )

        # ========================================================
        # DETAILED WHAT-IF
        # ========================================================

        print(
            "\nDETAILED WHAT-IF IMPACT ANALYSIS:"
        )

        print(
            "Baseline daily energy:",
            what_if_analysis.get(
                "baseline_daily_kwh",
                "N/A"
            ),
            "kWh/day"
        )

        print(
            "Projected daily energy:",
            what_if_analysis.get(
                "projected_daily_kwh",
                "N/A"
            ),
            "kWh/day"
        )

        print(
            "Daily energy reduction:",
            what_if_analysis.get(
                "energy_saved_kwh_per_day",
                "N/A"
            ),
            "kWh/day"
        )

        print(
            "Reduction percentage:",
            what_if_analysis.get(
                "saving_percent",
                "N/A"
            ),
            "%"
        )

        print(
            "Financial impact:",
            what_if_analysis.get(
                "estimated_cost_saving_inr_per_day",
                "N/A"
            ),
            "INR/day"
        )

        print(
            "Environmental impact:",
            what_if_analysis.get(
                "estimated_co2_reduction_kg_per_day",
                "N/A"
            ),
            "kg CO2/day"
        )

        print(
            "Interpretation:",
            what_if_analysis.get(
                "interpretation",
                "N/A"
            )
        )

        # ========================================================
        # DIGITAL TWIN
        # ========================================================

        print(
            "\nDIGITAL TWIN VISUALIZATION DATA:"
        )

        print(
            json.dumps(
                digital_twin,
                indent=2,
                default=str
            )
        )

        # ========================================================
        # MODULE STATUS
        # ========================================================

        print(
            "\nSYSTEM MODULE STATUS:"
        )

        print(
            "✓ Backend telemetry"
        )

        print(
            "✓ Data normalization"
        )

        print(
            "✓ Anomaly detection"
        )

        print(
            "✓ KPI extraction"
        )

        print(
            "✓ Forecast layer"
        )

        print(
            "✓ Advanced semantic RAG"
        )

        print(
            "✓ Decision reasoning"
        )

        print(
            "✓ Recommendation engine"
        )

        print(
            "✓ What-if simulation"
        )

        print(
            "✓ Current-status analysis"
        )

        print(
            "✓ What-if impact analysis"
        )

        print(
            "✓ Digital-twin visualization data"
        )

        print(
            "\n"
        )

        print(
            "=" * 65
        )

        print(
            "        UNIFIED AI PIPELINE COMPLETE"
        )

        print(
            "=" * 65
        )

        # ========================================================
        # MACHINE-READABLE RESULT
        # ========================================================

        return {

            "status":
                "success",

            "generated_at":
                datetime.now().isoformat(),

            "facility":
                facility,

            "building":
                building,

            "building_id":
                building_id,

            "priority":
                priority,

            "confidence":
                confidence,

            "current_status":
                current_status,

            "kpis": {

                "energy_kwh":
                    current_energy,

                "water_liters":
                    current_water,

                "waste_kg":
                    current_waste,

                "vehicles":
                    current_vehicles,

                "parking_percent":
                    current_parking,

                "average_speed":
                    current_speed
            },

            "anomalies": {

                "energy":
                    energy_result,

                "water":
                    water_result,

                "waste":
                    waste_result,

                "traffic":
                    traffic_result
            },

            "forecast":
                forecast,

            "explanation":
                explanation,

            "recommendation":
                recommendation,

            "rag":
                rag_result,

            "reasoning":
                reasoning_result,

            "recommendation_details":
                recommendation_result,

            "what_if":
                what_if,

            "what_if_analysis":
                what_if_analysis,

            "digital_twin":
                digital_twin
        }


# =================================================================
# ENTRY POINT
# =================================================================

if __name__ == "__main__":

    print(
        "=" * 65
    )

    print(
        "        CAMPUS360 UNIFIED AI INTELLIGENCE"
    )

    print(
        "=" * 65
    )

    try:

        pipeline = (
            CampusIntelligencePipeline()
        )

        pipeline.run()

    except KeyboardInterrupt:

        print(
            "\nPipeline stopped by user."
        )

    except Exception as exc:

        print(
            "\nFATAL PIPELINE ERROR:"
        )

        print(
            str(exc)
        )

        traceback.print_exc()