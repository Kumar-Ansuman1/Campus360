"""
Campus360 AI - Recommendation Engine

Generates operational recommendations from:
- KPIs
- anomaly summaries
- current facility status
- forecast information

Supports both:
1. Explicit KPI/anomaly arguments
2. A single `data=` dictionary from the unified pipeline
"""

from datetime import datetime


class RecommendationEngine:

    def __init__(self):

        self.recommendations = []

    # =========================================================
    # ADD
    # =========================================================

    def _add_recommendation(
        self,
        category,
        severity,
        title,
        message,
        action
    ):

        recommendation = {

            "category":
                category,

            "severity":
                severity,

            "title":
                title,

            "message":
                message,

            "action":
                action,

            "created_at":
                datetime.now().isoformat()
        }

        self.recommendations.append(
            recommendation
        )

        return recommendation

    # =========================================================
    # ENERGY
    # =========================================================

    def analyze_energy(
        self,
        kpi,
        anomaly_summary
    ):

        kpi = kpi or {}
        anomaly_summary = (
            anomaly_summary or {}
        )

        latest = float(
            kpi.get(
                "latest_consumption",
                0
            ) or 0
        )

        anomalies = int(
            anomaly_summary.get(
                "anomalies",
                anomaly_summary.get(
                    "count",
                    0
                )
            ) or 0
        )

        if anomalies > 0:

            return self._add_recommendation(

                "ENERGY",

                "HIGH",

                "Unusual energy consumption detected",

                (
                    "An unusual energy reading "
                    f"was detected. Latest "
                    f"consumption: {latest:.2f} kWh."
                ),

                (
                    "Inspect HVAC systems, "
                    "lighting, and high-load "
                    "equipment."
                )
            )

        if latest > 50:

            return self._add_recommendation(

                "ENERGY",

                "MEDIUM",

                "Energy consumption is elevated",

                (
                    f"Current energy consumption "
                    f"is {latest:.2f} kWh."
                ),

                (
                    "Review peak-hour equipment "
                    "usage and HVAC schedules."
                )
            )

        return None

    # =========================================================
    # WATER
    # =========================================================

    def analyze_water(
        self,
        kpi,
        anomaly_summary
    ):

        kpi = kpi or {}
        anomaly_summary = (
            anomaly_summary or {}
        )

        latest = float(
            kpi.get(
                "latest_consumption",
                0
            ) or 0
        )

        anomalies = int(
            anomaly_summary.get(
                "anomalies",
                anomaly_summary.get(
                    "count",
                    0
                )
            ) or 0
        )

        if anomalies > 0:

            return self._add_recommendation(

                "WATER",

                "HIGH",

                "Unusual water consumption detected",

                (
                    "An unusual water reading "
                    f"was detected. Latest "
                    f"consumption: {latest:.2f} L."
                ),

                (
                    "Inspect pipelines, tanks, "
                    "washrooms, and leakage points."
                )
            )

        if latest > 150:

            return self._add_recommendation(

                "WATER",

                "MEDIUM",

                "Water consumption is elevated",

                (
                    f"Current water consumption "
                    f"is {latest:.2f} L."
                ),

                (
                    "Check high-consumption areas "
                    "and review water usage."
                )
            )

        return None

    # =========================================================
    # WASTE
    # =========================================================

    def analyze_waste(
        self,
        kpi,
        anomaly_summary
    ):

        kpi = kpi or {}
        anomaly_summary = (
            anomaly_summary or {}
        )

        latest = float(
            kpi.get(
                "latest_waste",
                0
            ) or 0
        )

        anomalies = int(
            anomaly_summary.get(
                "anomalies",
                anomaly_summary.get(
                    "count",
                    0
                )
            ) or 0
        )

        if anomalies > 0:

            return self._add_recommendation(

                "WASTE",

                "HIGH",

                "Unusual waste generation detected",

                (
                    "An unusual waste reading "
                    f"was detected. Latest "
                    f"quantity: {latest:.2f} kg."
                ),

                (
                    "Inspect waste collection "
                    "points and collection frequency."
                )
            )

        if latest > 25:

            return self._add_recommendation(

                "WASTE",

                "MEDIUM",

                "Waste generation is elevated",

                (
                    f"Latest waste quantity "
                    f"is {latest:.2f} kg."
                ),

                (
                    "Review waste sources and "
                    "improve segregation."
                )
            )

        return None

    # =========================================================
    # TRAFFIC
    # =========================================================

    def analyze_traffic(
        self,
        kpi,
        anomaly_summary
    ):

        kpi = kpi or {}
        anomaly_summary = (
            anomaly_summary or {}
        )

        vehicles = float(
            kpi.get(
                "vehicle_count",
                0
            ) or 0
        )

        parking = float(
            kpi.get(
                "parking_occupancy",
                0
            ) or 0
        )

        anomalies = int(
            anomaly_summary.get(
                "anomalies",
                anomaly_summary.get(
                    "count",
                    0
                )
            ) or 0
        )

        if anomalies > 0:

            return self._add_recommendation(

                "TRAFFIC",

                "HIGH",

                "Unusual traffic activity detected",

                (
                    "Unusual vehicle activity "
                    f"detected. Current vehicles: "
                    f"{vehicles:.0f}."
                ),

                (
                    "Review traffic flow and "
                    "parking conditions."
                )
            )

        if parking > 80:

            return self._add_recommendation(

                "TRAFFIC",

                "MEDIUM",

                "Parking occupancy is high",

                (
                    f"Current parking occupancy "
                    f"is {parking:.1f}%."
                ),

                (
                    "Optimize parking allocation "
                    "and entry/exit flow."
                )
            )

        return None

    # =========================================================
    # NORMALIZE PIPELINE DATA
    # =========================================================

    @staticmethod
    def _extract_kpi(
        data,
        category
    ):

        data = data or {}

        kpis = data.get(
            "kpis",
            {}
        )

        category_data = kpis.get(
            category,
            {}
        )

        if isinstance(
            category_data,
            dict
        ):
            return category_data

        return {}

    @staticmethod
    def _extract_anomaly(
        data,
        category
    ):

        data = data or {}

        anomalies = data.get(
            "anomalies",
            {}
        )

        category_data = anomalies.get(
            category,
            {}
        )

        if isinstance(
            category_data,
            dict
        ):
            return category_data

        return {}

    # =========================================================
    # COMPLETE ANALYSIS
    # =========================================================

    def generate_recommendations(
        self,
        energy_kpi=None,
        water_kpi=None,
        waste_kpi=None,
        traffic_kpi=None,
        energy_anomaly=None,
        water_anomaly=None,
        waste_anomaly=None,
        traffic_anomaly=None,
        data=None,
        **kwargs
    ):

        self.recommendations = []

        # -----------------------------------------------------
        # Support pipeline `data=...`
        # -----------------------------------------------------

        if data is not None:

            if energy_kpi is None:
                energy_kpi = self._extract_kpi(
                    data,
                    "energy"
                )

            if water_kpi is None:
                water_kpi = self._extract_kpi(
                    data,
                    "water"
                )

            if waste_kpi is None:
                waste_kpi = self._extract_kpi(
                    data,
                    "waste"
                )

            if traffic_kpi is None:
                traffic_kpi = self._extract_kpi(
                    data,
                    "traffic"
                )

            if energy_anomaly is None:
                energy_anomaly = self._extract_anomaly(
                    data,
                    "energy"
                )

            if water_anomaly is None:
                water_anomaly = self._extract_anomaly(
                    data,
                    "water"
                )

            if waste_anomaly is None:
                waste_anomaly = self._extract_anomaly(
                    data,
                    "waste"
                )

            if traffic_anomaly is None:
                traffic_anomaly = self._extract_anomaly(
                    data,
                    "traffic"
                )

        # -----------------------------------------------------
        # Analyze all domains
        # -----------------------------------------------------

        self.analyze_energy(
            energy_kpi or {},
            energy_anomaly or {}
        )

        self.analyze_water(
            water_kpi or {},
            water_anomaly or {}
        )

        self.analyze_waste(
            waste_kpi or {},
            waste_anomaly or {}
        )

        self.analyze_traffic(
            traffic_kpi or {},
            traffic_anomaly or {}
        )

        return self.recommendations

    # =========================================================
    # SUMMARY
    # =========================================================

    def get_summary(self):

        total = len(
            self.recommendations
        )

        high = sum(
            1
            for recommendation
            in self.recommendations
            if recommendation.get(
                "severity"
            ) == "HIGH"
        )

        medium = sum(
            1
            for recommendation
            in self.recommendations
            if recommendation.get(
                "severity"
            ) == "MEDIUM"
        )

        low = sum(
            1
            for recommendation
            in self.recommendations
            if recommendation.get(
                "severity"
            ) == "LOW"
        )

        return {

            "total_recommendations":
                total,

            "high_priority":
                high,

            "medium_priority":
                medium,

            "low_priority":
                low,

            "recommendations":
                self.recommendations
        }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("CAMPUS360 RECOMMENDATION ENGINE")
    print("=" * 60)

    engine = RecommendationEngine()

    recommendations = (
        engine.generate_recommendations(

            energy_kpi={
                "latest_consumption": 75
            },

            water_kpi={
                "latest_consumption": 180
            },

            waste_kpi={
                "latest_waste": 30
            },

            traffic_kpi={
                "vehicle_count": 60,
                "parking_occupancy": 85
            },

            energy_anomaly={
                "anomalies": 1
            },

            water_anomaly={
                "anomalies": 0
            },

            waste_anomaly={
                "anomalies": 0
            },

            traffic_anomaly={
                "anomalies": 0
            }
        )
    )

    for item in recommendations:

        print(
            f"\n[{item['severity']}] "
            f"{item['title']}"
        )

        print(
            "Message:",
            item["message"]
        )

        print(
            "Action:",
            item["action"]
        )

    print("\nSUMMARY")
    print(
        engine.get_summary()
    )

    print("=" * 60)