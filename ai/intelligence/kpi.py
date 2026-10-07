import pandas as pd


class KPIEngine:

    def energy_kpi(self, df):
        if df is None or df.empty:
            return {
                "total_consumption": 0,
                "average_consumption": 0,
                "latest_consumption": 0
            }

        return {
            "total_consumption": round(df["consumption"].sum(), 2),
            "average_consumption": round(df["consumption"].mean(), 2),
            "latest_consumption": round(
                df.sort_values("recorded_at")
                .iloc[-1]["consumption"], 2
            )
        }

    def water_kpi(self, df):
        if df is None or df.empty:
            return {
                "total_consumption": 0,
                "average_consumption": 0,
                "latest_consumption": 0
            }

        return {
            "total_consumption": round(df["consumption"].sum(), 2),
            "average_consumption": round(df["consumption"].mean(), 2),
            "latest_consumption": round(
                df.sort_values("recorded_at")
                .iloc[-1]["consumption"], 2
            )
        }

    def waste_kpi(self, df):
        if df is None or df.empty:
            return {
                "total_waste": 0,
                "average_waste": 0,
                "latest_waste": 0
            }

        return {
            "total_waste": round(df["quantity"].sum(), 2),
            "average_waste": round(df["quantity"].mean(), 2),
            "latest_waste": round(
                df.sort_values("recorded_at")
                .iloc[-1]["quantity"], 2
            )
        }

    def traffic_kpi(self, df):
        if df is None or df.empty:
            return {
                "vehicle_count": 0,
                "parking_occupancy": 0,
                "average_speed": 0
            }

        latest = df.sort_values("recorded_at").iloc[-1]

        return {
            "vehicle_count": int(latest["vehicle_count"]),
            "parking_occupancy": round(
                latest["parking_occupancy"], 2
            ),
            "average_speed": round(
                latest["average_speed"], 2
            )
        }

    def generate_summary(
        self,
        energy,
        water,
        waste,
        traffic
    ):

        return {
            "energy": self.energy_kpi(energy),
            "water": self.water_kpi(water),
            "waste": self.waste_kpi(waste),
            "traffic": self.traffic_kpi(traffic)
        }