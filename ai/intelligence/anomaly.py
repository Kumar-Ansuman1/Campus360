import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    """
    Campus360 anomaly detection engine.

    Detects unusual values in:
    - Energy consumption
    - Water consumption
    - Waste quantity
    - Traffic / parking data
    """

    def __init__(self, contamination=0.15, random_state=42):
        self.contamination = contamination
        self.random_state = random_state

    def detect(self, df, value_column):
        """
        Detect anomalies in a single metric column.

        Returns the original dataframe with:
        - anomaly_score
        - is_anomaly
        - anomaly_status
        """

        if df is None or df.empty:
            return pd.DataFrame()

        if value_column not in df.columns:
            raise ValueError(
                f"Column '{value_column}' not found in dataframe"
            )

        result = df.copy()

        # Remove rows where the metric is missing
        result = result.dropna(
            subset=[value_column]
        ).reset_index(drop=True)

        # Not enough data for meaningful anomaly detection
        if len(result) < 2:
            result["anomaly_score"] = 0.0
            result["is_anomaly"] = False
            result["anomaly_status"] = "INSUFFICIENT_DATA"
            return result

        X = result[[value_column]].astype(float)

        model = IsolationForest(
            contamination=min(
                self.contamination,
                max(1 / len(result), 0.49)
            ),
            random_state=self.random_state
        )

        predictions = model.fit_predict(X)

        scores = model.decision_function(X)

        result["anomaly_score"] = scores

        result["is_anomaly"] = (
            predictions == -1
        )

        result["anomaly_status"] = np.where(
            result["is_anomaly"],
            "ANOMALY",
            "NORMAL"
        )

        return result

    def energy_anomalies(self, df):
        return self.detect(
            df,
            "consumption"
        )

    def water_anomalies(self, df):
        return self.detect(
            df,
            "consumption"
        )

    def waste_anomalies(self, df):
        return self.detect(
            df,
            "quantity"
        )

    def traffic_anomalies(self, df):
        """
        Detect anomalies using vehicle count.
        """

        return self.detect(
            df,
            "vehicle_count"
        )

    def get_anomaly_summary(
        self,
        df,
        value_column
    ):
        """
        Generate a simple summary for the dashboard.
        """

        result = self.detect(
            df,
            value_column
        )

        if result.empty:
            return {
                "total_records": 0,
                "anomalies": 0,
                "normal_records": 0,
                "anomaly_percentage": 0
            }

        total = len(result)

        anomalies = int(
            result["is_anomaly"].sum()
        )

        normal = total - anomalies

        percentage = (
            anomalies / total
        ) * 100

        return {
            "total_records": total,
            "anomalies": anomalies,
            "normal_records": normal,
            "anomaly_percentage": round(
                percentage,
                2
            )
        }


if __name__ == "__main__":

    print("======================================")
    print("CAMPUS360 ANOMALY DETECTOR")
    print("======================================")

    # Small standalone test
    sample_data = pd.DataFrame({
        "consumption": [
            42.7,
            45.8,
            44.1,
            43.9,
            46.2,
            150.0
        ]
    })

    detector = AnomalyDetector()

    result = detector.energy_anomalies(
        sample_data
    )

    print("\nDetection Results:")
    print(result)

    print("\nSummary:")
    print(
        detector.get_anomaly_summary(
            sample_data,
            "consumption"
        )
    )

    print("\n======================================")
    print("ANOMALY DETECTOR TEST COMPLETE")
    print("======================================")