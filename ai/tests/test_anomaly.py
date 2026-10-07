from ai.data_loader import CampusDataLoader
from ai.intelligence.anomaly import AnomalyDetector


BUILDING_ID = "d040b2f2-9ea8-4336-a9f9-9c72b07e2597"


def print_results(name, result, value_column):
    print(f"\n{'=' * 50}")
    print(f"{name.upper()} ANOMALY DETECTION")
    print(f"{'=' * 50}")

    if result.empty:
        print("No data available.")
        return

    print(
        result[
            [
                "recorded_at",
                value_column,
                "anomaly_score",
                "is_anomaly",
                "anomaly_status",
            ]
        ].to_string(index=False)
    )

    anomaly_count = int(
        result["is_anomaly"].sum()
    )

    print(f"\nTotal records: {len(result)}")
    print(f"Anomalies detected: {anomaly_count}")


def main():

    print("\n======================================")
    print("CAMPUS360 REAL DATA ANOMALY TEST")
    print("======================================")

    # ----------------------------------
    # LOAD BACKEND DATA
    # ----------------------------------

    loader = CampusDataLoader()
    detector = AnomalyDetector()

    print("\nLoading Campus360 data...")

    energy = loader.energy_dataframe(
        BUILDING_ID
    )

    water = loader.water_dataframe(
        BUILDING_ID
    )

    waste = loader.waste_dataframe(
        BUILDING_ID
    )

    traffic = loader.traffic_dataframe(
        BUILDING_ID
    )

    # ----------------------------------
    # ENERGY
    # ----------------------------------

    energy_result = detector.energy_anomalies(
        energy
    )

    print_results(
        "Energy",
        energy_result,
        "consumption"
    )

    # ----------------------------------
    # WATER
    # ----------------------------------

    water_result = detector.water_anomalies(
        water
    )

    print_results(
        "Water",
        water_result,
        "consumption"
    )

    # ----------------------------------
    # WASTE
    # ----------------------------------

    waste_result = detector.waste_anomalies(
        waste
    )

    print_results(
        "Waste",
        waste_result,
        "quantity"
    )

    # ----------------------------------
    # TRAFFIC
    # ----------------------------------

    traffic_result = detector.traffic_anomalies(
        traffic
    )

    print_results(
        "Traffic",
        traffic_result,
        "vehicle_count"
    )

    print("\n======================================")
    print("REAL DATA ANOMALY TEST COMPLETE")
    print("======================================")


if __name__ == "__main__":
    main()