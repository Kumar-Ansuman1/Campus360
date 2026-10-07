from ai.data_loader import CampusDataLoader
from ai.intelligence.anomaly import AnomalyDetector
from ai.intelligence.recommendations import RecommendationEngine


BUILDING_ID = "d040b2f2-9ea8-4336-a9f9-9c72b07e2597"


def get_latest(df, column):
    if df.empty:
        return 0

    return float(
        df.sort_values("recorded_at")
        .iloc[-1][column]
    )


def get_anomaly_summary(result):
    if result.empty:
        return {
            "total_records": 0,
            "anomalies": 0
        }

    return {
        "total_records": len(result),
        "anomalies": int(result["is_anomaly"].sum())
    }


def main():

    print("\n==============================================")
    print("       CAMPUS360 AI INTELLIGENCE")
    print("==============================================")

    # ------------------------------------------
    # 1. LOAD DATA
    # ------------------------------------------

    print("\n[1/4] Loading backend data...")

    loader = CampusDataLoader()

    energy = loader.energy_dataframe(BUILDING_ID)
    water = loader.water_dataframe(BUILDING_ID)
    waste = loader.waste_dataframe(BUILDING_ID)
    traffic = loader.traffic_dataframe(BUILDING_ID)

    print(f"Energy records : {len(energy)}")
    print(f"Water records  : {len(water)}")
    print(f"Waste records  : {len(waste)}")
    print(f"Traffic records: {len(traffic)}")

    # ------------------------------------------
    # 2. ANOMALY DETECTION
    # ------------------------------------------

    print("\n[2/4] Running anomaly detection...")

    detector = AnomalyDetector()

    energy_anomaly = detector.energy_anomalies(energy)
    water_anomaly = detector.water_anomalies(water)
    waste_anomaly = detector.waste_anomalies(waste)
    traffic_anomaly = detector.traffic_anomalies(traffic)

    energy_summary = get_anomaly_summary(
        energy_anomaly
    )

    water_summary = get_anomaly_summary(
        water_anomaly
    )

    waste_summary = get_anomaly_summary(
        waste_anomaly
    )

    traffic_summary = get_anomaly_summary(
        traffic_anomaly
    )

    print(
        f"Energy anomalies : "
        f"{energy_summary['anomalies']}"
    )

    print(
        f"Water anomalies  : "
        f"{water_summary['anomalies']}"
    )

    print(
        f"Waste anomalies  : "
        f"{waste_summary['anomalies']}"
    )

    print(
        f"Traffic anomalies: "
        f"{traffic_summary['anomalies']}"
    )

    # ------------------------------------------
    # 3. BUILD KPI DATA
    # ------------------------------------------

    print("\n[3/4] Preparing KPI values...")

    energy_kpi = {
        "latest_consumption": get_latest(
            energy,
            "consumption"
        )
    }

    water_kpi = {
        "latest_consumption": get_latest(
            water,
            "consumption"
        )
    }

    waste_kpi = {
        "latest_waste": get_latest(
            waste,
            "quantity"
        )
    }

    traffic_kpi = {
        "vehicle_count": get_latest(
            traffic,
            "vehicle_count"
        ),
        "parking_occupancy": get_latest(
            traffic,
            "parking_occupancy"
        )
    }

    print(
        f"Latest energy : "
        f"{energy_kpi['latest_consumption']} kWh"
    )

    print(
        f"Latest water  : "
        f"{water_kpi['latest_consumption']} L"
    )

    print(
        f"Latest waste  : "
        f"{waste_kpi['latest_waste']} kg"
    )

    print(
        f"Vehicles      : "
        f"{traffic_kpi['vehicle_count']}"
    )

    print(
        f"Parking       : "
        f"{traffic_kpi['parking_occupancy']}%"
    )

    # ------------------------------------------
    # 4. GENERATE RECOMMENDATIONS
    # ------------------------------------------

    print("\n[4/4] Generating recommendations...")

    engine = RecommendationEngine()

    recommendations = engine.generate_recommendations(

        energy_kpi,
        water_kpi,
        waste_kpi,
        traffic_kpi,

        energy_summary,
        water_summary,
        waste_summary,
        traffic_summary
    )

    # ------------------------------------------
    # FINAL OUTPUT
    # ------------------------------------------

    print("\n==============================================")
    print("           CAMPUS360 AI INSIGHTS")
    print("==============================================")

    if not recommendations:

        print("\nNo actionable issues detected.")

    else:

        for i, recommendation in enumerate(
            recommendations,
            start=1
        ):

            print(
                f"\n{i}. "
                f"[{recommendation['severity']}] "
                f"{recommendation['title']}"
            )

            print(
                f"   Category : "
                f"{recommendation['category']}"
            )

            print(
                f"   Message  : "
                f"{recommendation['message']}"
            )

            print(
                f"   Action   : "
                f"{recommendation['action']}"
            )

    # ------------------------------------------
    # SUMMARY
    # ------------------------------------------

    summary = engine.get_summary()

    print("\n==============================================")
    print("               SUMMARY")
    print("==============================================")

    print(
        f"Total recommendations : "
        f"{summary['total_recommendations']}"
    )

    print(
        f"High priority         : "
        f"{summary['high_priority']}"
    )

    print(
        f"Medium priority       : "
        f"{summary['medium_priority']}"
    )

    print("\n==============================================")
    print("       FULL INTELLIGENCE TEST COMPLETE")
    print("==============================================")


if __name__ == "__main__":
    main()