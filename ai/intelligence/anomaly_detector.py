import pandas as pd
import numpy as np


# ============================================================
# CAMPUS360 AI — ANOMALY DETECTION ENGINE
# Member 1 — AI/ML Intelligence Layer
# ============================================================


class AnomalyDetector:

    def __init__(self, z_threshold=2.0):
        self.z_threshold = z_threshold

    # --------------------------------------------------------
    # Generic Z-score anomaly detection
    # --------------------------------------------------------

    def detect_zscore(self, df, value_column):

        if df.empty:
            return df.copy()

        result = df.copy()

        values = pd.to_numeric(
            result[value_column],
            errors="coerce"
        )

        mean = values.mean()
        std = values.std()

        # Avoid division by zero
        if pd.isna(std) or std == 0:

            result["z_score"] = 0.0
            result["is_anomaly"] = False

            return result

        result["z_score"] = (
            (values - mean) / std
        )

        result["is_anomaly"] = (
            result["z_score"].abs()
            >= self.z_threshold
        )

        return result

    # --------------------------------------------------------
    # Percentage-change anomaly detection
    # --------------------------------------------------------

    def detect_change(self, df, value_column, threshold=0.20):

        if df.empty:
            return df.copy()

        result = df.copy()

        values = pd.to_numeric(
            result[value_column],
            errors="coerce"
        )

        result["previous_value"] = values.shift(1)

        result["percentage_change"] = (
            (values - result["previous_value"])
            / result["previous_value"]
        )

        result["is_change_anomaly"] = (
            result["percentage_change"].abs()
            >= threshold
        )

        return result

    # --------------------------------------------------------
    # ENERGY
    # --------------------------------------------------------

    def analyze_energy(self, df):

        if df.empty:
            return {
                "data": df,
                "anomalies": [],
                "summary": "No energy data available."
            }

        result = self.detect_zscore(
            df,
            "consumption"
        )

        result = self.detect_change(
            result,
            "consumption"
        )

        anomalies = result[
            result["is_anomaly"]
            | result["is_change_anomaly"]
        ]

        return {
            "data": result,
            "anomalies": anomalies.to_dict(
                orient="records"
            ),
            "summary": self._generate_summary(
                "energy",
                anomalies
            )
        }

    # --------------------------------------------------------
    # WATER
    # --------------------------------------------------------

    def analyze_water(self, df):

        if df.empty:
            return {
                "data": df,
                "anomalies": [],
                "summary": "No water data available."
            }

        result = self.detect_zscore(
            df,
            "consumption"
        )

        result = self.detect_change(
            result,
            "consumption"
        )

        anomalies = result[
            result["is_anomaly"]
            | result["is_change_anomaly"]
        ]

        return {
            "data": result,
            "anomalies": anomalies.to_dict(
                orient="records"
            ),
            "summary": self._generate_summary(
                "water",
                anomalies
            )
        }

    # --------------------------------------------------------
    # WASTE
    # --------------------------------------------------------

    def analyze_waste(self, df):

        if df.empty:
            return {
                "data": df,
                "anomalies": [],
                "summary": "No waste data available."
            }

        result = self.detect_zscore(
            df,
            "quantity"
        )

        result = self.detect_change(
            result,
            "quantity"
        )

        anomalies = result[
            result["is_anomaly"]
            | result["is_change_anomaly"]
        ]

        return {
            "data": result,
            "anomalies": anomalies.to_dict(
                orient="records"
            ),
            "summary": self._generate_summary(
                "waste",
                anomalies
            )
        }

    # --------------------------------------------------------
    # TRAFFIC
    # --------------------------------------------------------

    def analyze_traffic(self, df):

        if df.empty:
            return {
                "data": df,
                "anomalies": [],
                "summary": "No traffic data available."
            }

        result = self.detect_zscore(
            df,
            "vehicle_count"
        )

        result = self.detect_change(
            result,
            "vehicle_count"
        )

        anomalies = result[
            result["is_anomaly"]
            | result["is_change_anomaly"]
        ]

        return {
            "data": result,
            "anomalies": anomalies.to_dict(
                orient="records"
            ),
            "summary": self._generate_summary(
                "traffic",
                anomalies
            )
        }

    # --------------------------------------------------------
    # Summary generator
    # --------------------------------------------------------

    def _generate_summary(
        self,
        metric,
        anomalies
    ):

        if len(anomalies) == 0:

            return (
                f"No significant {metric} "
                f"anomalies detected."
            )

        return (
            f"{len(anomalies)} unusual "
            f"{metric} record(s) detected."
        )