"""
=================================================================
CAMPUS360 - OPTIMIZATION & PRIORITY ENGINE
Optimization & Decision Layer

Purpose:
    Determine which campus issue should be addressed first.

Priority score:
    Severity       -> 50 points
    Deviation      -> 30 points
    Forecast       -> 20 points

Maximum score:
    100

Priority levels:
    80 - 100 -> P1 - IMMEDIATE
    60 - 79  -> P2 - HIGH
    40 - 59  -> P3 - MEDIUM
    < 40     -> P4 - LOW

This module contains decision logic only.
It does NOT replace:
    - Anomaly detection
    - Forecasting
    - RAG
    - Reasoning
    - Recommendations
    - What-If simulation
=================================================================
"""


class OptimizationEngine:

    # ============================================================
    # SCORE WEIGHTS
    # ============================================================

    SEVERITY_WEIGHT = 50

    DEVIATION_WEIGHT = 30

    FORECAST_WEIGHT = 20

    # ============================================================
    # PRIORITY THRESHOLDS
    # ============================================================

    P1_THRESHOLD = 80

    P2_THRESHOLD = 60

    P3_THRESHOLD = 40

    # ============================================================
    # SAFE NUMBER
    # ============================================================

    @staticmethod
    def _number(value, default=0.0):
        """
        Safely convert a value to float.
        """

        try:

            if value is None:
                return default

            return float(value)

        except (TypeError, ValueError):

            return default

    # ============================================================
    # CLAMP
    # ============================================================

    @staticmethod
    def _clamp(value, minimum, maximum):
        """
        Keep a score inside a configured range.
        """

        return max(
            minimum,
            min(
                maximum,
                value
            )
        )

    # ============================================================
    # SEVERITY SCORE
    # ============================================================

    @classmethod
    def calculate_severity_score(
        cls,
        status
    ):
        """
        Convert context/anomaly status into a score.

        The severity component contributes a maximum
        of 50 points.

        Mapping:

            CRITICAL -> 50
            HIGH     -> 40
            MODERATE -> 25
            WARNING  -> 25
            NORMAL   -> 0
        """

        normalized_status = str(
            status or "NORMAL"
        ).upper()

        severity_map = {

            "CRITICAL":
                50,

            "HIGH":
                40,

            "MODERATE":
                25,

            "WARNING":
                25,

            "ATTENTION":
                30,

            "MEDIUM":
                25,

            "NORMAL":
                0
        }

        return severity_map.get(
            normalized_status,
            0
        )

    # ============================================================
    # DEVIATION SCORE
    # ============================================================

    @classmethod
    def calculate_deviation_score(
        cls,
        deviation_percent
    ):
        """
        Convert energy deviation into a score.

        Maximum contribution:
            30 points

        Scaling:

            0% deviation   -> 0
            25% deviation  -> 7.5
            50% deviation  -> 15
            100% deviation -> 30

        Anything above 100% is capped at 30.
        """

        deviation = max(
            0.0,
            cls._number(
                deviation_percent
            )
        )

        score = (
            deviation
            / 100.0
        ) * cls.DEVIATION_WEIGHT

        return round(
            cls._clamp(
                score,
                0.0,
                cls.DEVIATION_WEIGHT
            ),
            2
        )

    # ============================================================
    # FORECAST SCORE
    # ============================================================

    @classmethod
    def calculate_forecast_score(
        cls,
        forecast
    ):
        """
        Calculate forecast contribution.

        Increasing forecast:
            20 points

        Stable forecast:
            10 points

        Decreasing forecast:
            0 points

        Unknown:
            0 points
        """

        if isinstance(
            forecast,
            dict
        ):

            trend = forecast.get(
                "trend",
                "UNKNOWN"
            )

        else:

            trend = forecast

        trend = str(
            trend or "UNKNOWN"
        ).upper()

        if trend == "INCREASING":
            return 20

        if trend == "STABLE":
            return 10

        return 0

    # ============================================================
    # PRIORITY SCORE
    # ============================================================

    @classmethod
    def calculate_priority_score(
        cls,
        severity_status,
        deviation_percent,
        forecast
    ):
        """
        Calculate the complete priority score.

        Formula:

            Priority Score =
                Severity Score
                + Deviation Score
                + Forecast Score
        """

        severity_score = (
            cls.calculate_severity_score(
                severity_status
            )
        )

        deviation_score = (
            cls.calculate_deviation_score(
                deviation_percent
            )
        )

        forecast_score = (
            cls.calculate_forecast_score(
                forecast
            )
        )

        total_score = (
            severity_score
            + deviation_score
            + forecast_score
        )

        total_score = round(
            cls._clamp(
                total_score,
                0.0,
                100.0
            ),
            2
        )

        return {

            "total_score":
                total_score,

            "severity_score":
                severity_score,

            "deviation_score":
                deviation_score,

            "forecast_score":
                forecast_score
        }

    # ============================================================
    # PRIORITY LEVEL
    # ============================================================

    @classmethod
    def determine_priority(
        cls,
        score
    ):
        """
        Convert total score into administrator priority.
        """

        score = cls._number(
            score
        )

        if score >= cls.P1_THRESHOLD:
            return "P1 - IMMEDIATE"

        if score >= cls.P2_THRESHOLD:
            return "P2 - HIGH"

        if score >= cls.P3_THRESHOLD:
            return "P3 - MEDIUM"

        return "P4 - LOW"

    # ============================================================
    # ISSUE ANALYSIS
    # ============================================================

    @classmethod
    def analyze_issue(
        cls,
        category,
        status,
        deviation_percent=0,
        forecast="UNKNOWN"
    ):
        """
        Analyze one campus issue.
        """

        score_breakdown = (
            cls.calculate_priority_score(
                severity_status=status,
                deviation_percent=deviation_percent,
                forecast=forecast
            )
        )

        priority = (
            cls.determine_priority(
                score_breakdown[
                    "total_score"
                ]
            )
        )

        return {

            "category":
                str(
                    category
                ).upper(),

            "status":
                str(
                    status or "NORMAL"
                ).upper(),

            "deviation_percent":
                round(
                    cls._number(
                        deviation_percent
                    ),
                    2
                ),

            "forecast":
                (
                    forecast.get(
                        "trend",
                        "UNKNOWN"
                    )
                    if isinstance(
                        forecast,
                        dict
                    )
                    else str(
                        forecast or "UNKNOWN"
                    ).upper()
                ),

            "priority":
                priority,

            "score":
                score_breakdown[
                    "total_score"
                ],

            "score_breakdown":
                score_breakdown
        }

    # ============================================================
    # RANK ISSUES
    # ============================================================

    @classmethod
    def rank_issues(
        cls,
        issues
    ):
        """
        Rank all active campus issues.

        Highest score appears first.
        """

        if not issues:
            return []

        normalized = []

        for issue in issues:

            if not isinstance(
                issue,
                dict
            ):
                continue

            category = issue.get(
                "category",
                "UNKNOWN"
            )

            status = issue.get(
                "status",
                "NORMAL"
            )

            deviation = issue.get(
                "deviation_percent",
                0
            )

            forecast = issue.get(
                "forecast",
                "UNKNOWN"
            )

            analyzed = cls.analyze_issue(
                category=category,
                status=status,
                deviation_percent=deviation,
                forecast=forecast
            )

            # Preserve additional information supplied
            # by the caller.
            analyzed.update({
                key: value
                for key, value in issue.items()
                if key not in analyzed
            })

            normalized.append(
                analyzed
            )

        normalized.sort(
            key=lambda item: item.get(
                "score",
                0
            ),
            reverse=True
        )

        return normalized

    # ============================================================
    # TOP PRIORITY
    # ============================================================

    @classmethod
    def select_top_priority(
        cls,
        ranked_issues
    ):
        """
        Select the highest-priority active issue.
        """

        if not ranked_issues:
            return None

        return ranked_issues[0]

    # ============================================================
    # FULL OPTIMIZATION ANALYSIS
    # ============================================================

    @classmethod
    def optimize(
        cls,
        issues
    ):
        """
        Complete optimization decision.

        Flow:

            Issues
              ↓
            Analyze
              ↓
            Score
              ↓
            Rank
              ↓
            Select #1
        """

        ranked_issues = cls.rank_issues(
            issues
        )

        top_priority = (
            cls.select_top_priority(
                ranked_issues
            )
        )

        if top_priority is None:

            return {

                "decision":
                    "NO_ACTION_REQUIRED",

                "top_priority":
                    None,

                "ranked_issues":
                    []
            }

        return {

            "decision":
                "ACTION_REQUIRED",

            "top_priority":
                top_priority,

            "ranked_issues":
                ranked_issues
        }


# ================================================================
# DEMO / QUICK TEST
# ================================================================

if __name__ == "__main__":

    print(
        "=" * 65
    )

    print(
        "        CAMPUS360 OPTIMIZATION ENGINE"
    )

    print(
        "=" * 65
    )

    # ------------------------------------------------------------
    # Example campus issues
    # ------------------------------------------------------------

    issues = [

        {
            "category":
                "ENERGY",

            "status":
                "CRITICAL",

            "deviation_percent":
                270,

            "forecast":
                "INCREASING"
        },

        {
            "category":
                "WATER",

            "status":
                "MODERATE",

            "deviation_percent":
                35,

            "forecast":
                "STABLE"
        },

        {
            "category":
                "WASTE",

            "status":
                "MODERATE",

            "deviation_percent":
                20,

            "forecast":
                "STABLE"
        },

        {
            "category":
                "TRAFFIC",

            "status":
                "NORMAL",

            "deviation_percent":
                0,

            "forecast":
                "DECREASING"
        }
    ]

    result = OptimizationEngine.optimize(
        issues
    )

    print()

    print(
        "DECISION:"
    )

    print(
        result[
            "decision"
        ]
    )

    print()

    print(
        "RANKING:"
    )

    for index, issue in enumerate(
        result[
            "ranked_issues"
        ],
        start=1
    ):

        print(
            f"{index}. "
            f"{issue['category']} | "
            f"{issue['priority']} | "
            f"Score: {issue['score']}"
        )

        print(
            f"   Severity: "
            f"{issue['score_breakdown']['severity_score']}"
        )

        print(
            f"   Deviation: "
            f"{issue['score_breakdown']['deviation_score']}"
        )

        print(
            f"   Forecast: "
            f"{issue['score_breakdown']['forecast_score']}"
        )

    print()

    print(
        "TOP PRIORITY:"
    )

    print(
        result[
            "top_priority"
        ]
    )

    print()

    print(
        "=" * 65
    )

    print(
        "        OPTIMIZATION ENGINE COMPLETE"
    )

    print(
        "=" * 65
    )