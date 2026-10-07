"""
Campus360 AI - Forecasting Engine

Uses the trained Prophet model exported from Google Colab.
Falls back to TrendFallback if the trained model cannot be loaded.
"""

from datetime import timedelta
from pathlib import Path

import joblib
import pandas as pd


class ForecastEngine:

    def __init__(self):
        self.model = None
        self.model_path = (
            Path(__file__).resolve().parents[2]
            / "models"
            / "prophet_model.pkl"
        )

        self._load_model()

    # =========================================================
    # LOAD TRAINED PROPHET MODEL
    # =========================================================

    def _load_model(self):
        try:
            if self.model_path.exists():
                self.model = joblib.load(self.model_path)
                print(
                    f"✅ Loaded trained Prophet model: "
                    f"{self.model_path}"
                )
            else:
                print(
                    f"⚠️ Prophet model not found: "
                    f"{self.model_path}"
                )

        except Exception as exc:
            print(
                f"⚠️ Could not load trained Prophet model: {exc}"
            )
            self.model = None

    # =========================================================
    # NORMALIZE INPUT
    # =========================================================

    @staticmethod
    def _normalize_records(records):

        if records is None:
            return pd.DataFrame()

        if isinstance(records, pd.DataFrame):
            return records.copy()

        if isinstance(records, list):

            if not records:
                return pd.DataFrame()

            return pd.DataFrame(records)

        if isinstance(records, dict):

            return pd.DataFrame([records])

        return pd.DataFrame()

    # =========================================================
    # TREND
    # =========================================================

    @staticmethod
    def _calculate_trend(
        first_prediction,
        last_prediction
    ):

        try:

            first_prediction = float(
                first_prediction
            )

            last_prediction = float(
                last_prediction
            )

        except Exception:

            return "UNKNOWN"

        if first_prediction == 0:

            if last_prediction > 0:
                return "INCREASING"

            return "STABLE"

        if (
            last_prediction
            >
            first_prediction * 1.05
        ):

            return "INCREASING"

        if (
            last_prediction
            <
            first_prediction * 0.95
        ):

            return "DECREASING"

        return "STABLE"

    # =========================================================
    # ENERGY FORECAST
    # =========================================================

    def forecast_energy(
        self,
        records,
        periods=24,
        freq="h"
    ):

        df = self._normalize_records(records)

        if df.empty:

            return {
                "status": "ERROR",
                "model": "None",
                "message": "No energy records available",
                "periods": periods,
                "trend": "UNKNOWN",
                "forecast": []
            }

        required = [
            "consumption",
            "recorded_at"
        ]

        missing = [
            column
            for column in required
            if column not in df.columns
        ]

        if missing:

            return {
                "status": "ERROR",
                "model": "None",
                "message":
                    "Missing required fields: "
                    + ", ".join(missing),
                "periods": periods,
                "trend": "UNKNOWN",
                "forecast": []
            }

        # -----------------------------------------------------
        # CLEAN DATA
        # -----------------------------------------------------

        df = df[
            [
                "recorded_at",
                "consumption"
            ]
        ].copy()

        df["recorded_at"] = pd.to_datetime(
            df["recorded_at"],
            errors="coerce"
        )

        df["consumption"] = pd.to_numeric(
            df["consumption"],
            errors="coerce"
        )

        df = (
            df
            .dropna(
                subset=[
                    "recorded_at",
                    "consumption"
                ]
            )
            .sort_values(
                "recorded_at"
            )
            .reset_index(
                drop=True
            )
        )

        if len(df) < 2:

            return {
                "status": "INSUFFICIENT_DATA",
                "model": "None",
                "message":
                    "At least 2 energy records are required",
                "periods": periods,
                "trend": "UNKNOWN",
                "forecast": []
            }

        # =====================================================
        # USE TRAINED COLAB PROPHET MODEL
        # =====================================================

        if self.model is not None:

            try:

                # Latest telemetry timestamp
                last_time = pd.to_datetime(
                    df["recorded_at"].iloc[-1]
                )

                # Prophet models generally use timezone-naive
                # timestamps.
                if getattr(
                    last_time,
                    "tzinfo",
                    None
                ) is not None:

                    last_time = (
                        last_time
                        .tz_localize(None)
                    )

                # Create exactly the future timestamps needed
                future = pd.DataFrame(
                    {
                        "ds": pd.date_range(
                            start=last_time + pd.Timedelta(
                                hours=1
                            ),
                            periods=int(periods),
                            freq=freq
                        )
                    }
                )

                prediction = self.model.predict(
                    future
                )

                forecast = []

                for _, row in prediction.iterrows():

                    predicted = max(
                        0.0,
                        float(row["yhat"])
                    )

                    lower = max(
                        0.0,
                        float(row["yhat_lower"])
                    )

                    upper = max(
                        0.0,
                        float(row["yhat_upper"])
                    )

                    forecast.append(
                        {
                            "timestamp":
                                pd.to_datetime(
                                    row["ds"]
                                ).isoformat(),

                            "predicted_consumption":
                                round(
                                    predicted,
                                    2
                                ),

                            "lower_bound":
                                round(
                                    lower,
                                    2
                                ),

                            "upper_bound":
                                round(
                                    upper,
                                    2
                                )
                        }
                    )

                if forecast:

                    trend = self._calculate_trend(
                        forecast[0][
                            "predicted_consumption"
                        ],
                        forecast[-1][
                            "predicted_consumption"
                        ]
                    )

                    return {
                        "status": "SUCCESS",

                        "model":
                            "Prophet-Colab-Trained",

                        "periods":
                            int(periods),

                        "trend":
                            trend,

                        "forecast":
                            forecast
                    }

            except Exception as exc:

                print(
                    "⚠️ Trained Prophet prediction warning:",
                    exc
                )

        # =====================================================
        # FALLBACK
        # =====================================================

        return self._fallback_forecast(
            df,
            periods
        )

    # =========================================================
    # FALLBACK
    # =========================================================

    def _fallback_forecast(
        self,
        df,
        periods
    ):

        if (
            df is None
            or df.empty
        ):

            return {
                "status": "ERROR",
                "model": "TrendFallback",
                "periods": periods,
                "trend": "UNKNOWN",
                "forecast": []
            }

        values = (
            pd.to_numeric(
                df["consumption"],
                errors="coerce"
            )
            .dropna()
            .tolist()
        )

        if len(values) < 2:

            return {
                "status": "INSUFFICIENT_DATA",
                "model": "TrendFallback",
                "periods": periods,
                "trend": "UNKNOWN",
                "forecast": []
            }

        last_value = float(
            values[-1]
        )

        previous_value = float(
            values[-2]
        )

        change = (
            last_value
            -
            previous_value
        )

        last_time = pd.to_datetime(
            df["recorded_at"].iloc[-1]
        )

        forecast = []

        for i in range(
            1,
            int(periods) + 1
        ):

            predicted = max(
                0.0,
                last_value
                +
                (change * i)
            )

            timestamp = (
                last_time
                +
                timedelta(
                    hours=i
                )
            )

            forecast.append(
                {
                    "timestamp":
                        timestamp.isoformat(),

                    "predicted_consumption":
                        round(
                            predicted,
                            2
                        ),

                    "lower_bound":
                        round(
                            max(
                                0.0,
                                predicted * 0.90
                            ),
                            2
                        ),

                    "upper_bound":
                        round(
                            predicted * 1.10,
                            2
                        )
                }
            )

        trend = self._calculate_trend(
            forecast[0][
                "predicted_consumption"
            ],
            forecast[-1][
                "predicted_consumption"
            ]
        )

        return {
            "status": "SUCCESS",
            "model": "TrendFallback",
            "periods": int(periods),
            "trend": trend,
            "forecast": forecast
        }

    # =========================================================
    # GENERIC COMPATIBILITY METHOD
    # =========================================================

    def forecast(
        self,
        records,
        periods=24,
        freq="h"
    ):

        return self.forecast_energy(
            records,
            periods=periods,
            freq=freq
        )


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("CAMPUS360 FORECASTING ENGINE TEST")
    print("=" * 60)

    sample_data = [

        {
            "consumption": 42.7,
            "recorded_at":
                "2026-09-29T14:30:00"
        },

        {
            "consumption": 45.8,
            "recorded_at":
                "2026-09-29T16:00:00"
        },

        {
            "consumption": 44.1,
            "recorded_at":
                "2026-09-29T17:00:00"
        },

        {
            "consumption": 47.2,
            "recorded_at":
                "2026-09-29T18:00:00"
        }
    ]

    engine = ForecastEngine()

    result = engine.forecast_energy(
        sample_data,
        periods=6
    )

    print(
        "\nStatus:",
        result.get("status")
    )

    print(
        "Model:",
        result.get("model")
    )

    print(
        "Trend:",
        result.get("trend")
    )

    print("\nForecast:")

    for item in result.get(
        "forecast",
        []
    ):

        print(
            item["timestamp"],
            "->",
            item[
                "predicted_consumption"
            ],
            "kWh"
        )

    print("=" * 60)
    print("FORECASTING TEST COMPLETE")
    print("=" * 60)
