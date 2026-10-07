"""
============================================================
CAMPUS360 AI — DATA LOADER
============================================================

Member 1: AI/ML Intelligence Layer

Purpose:
    Connect the AI layer with the Campus360 FastAPI backend.

Flow:

    FastAPI Backend
          ↓
    CampusDataLoader
          ↓
    pandas DataFrames
          ↓
    AI Intelligence Pipeline
          ↓
    Anomaly / Forecast / RAG / Reasoning / What-if
"""

import requests
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000"


class CampusDataLoader:

    def __init__(self, base_url=API_BASE_URL):

        self.base_url = base_url.rstrip("/")


    # ========================================================
    # GENERIC GET REQUEST
    # ========================================================

    def _get(self, endpoint):

        url = f"{self.base_url}{endpoint}"

        try:

            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

            result = response.json()

            # ------------------------------------------------
            # Backend response format:
            #
            # {
            #     "data": [...]
            # }
            # ------------------------------------------------

            if isinstance(result, dict):

                data = result.get(
                    "data",
                    []
                )

                if data is None:
                    return []

                return data

            # ------------------------------------------------
            # Safety fallback
            # ------------------------------------------------

            if isinstance(result, list):

                return result

            return []

        except requests.exceptions.ConnectionError as exc:

            print(
                f"\nAPI connection error: "
                f"{self.base_url}{endpoint}"
            )

            print(
                "Make sure FastAPI is running."
            )

            raise exc

        except requests.exceptions.Timeout as exc:

            print(
                f"\nAPI timeout: "
                f"{self.base_url}{endpoint}"
            )

            raise exc

        except requests.exceptions.HTTPError as exc:

            print(
                f"\nAPI HTTP error: "
                f"{self.base_url}{endpoint}"
            )

            print(
                f"Status code: "
                f"{response.status_code}"
            )

            raise exc


    # ========================================================
    # FACILITIES
    # ========================================================

    def get_facilities(self):

        return self._get(
            "/facilities"
        )


    # ========================================================
    # BUILDINGS
    # ========================================================

    def get_buildings(self):

        return self._get(
            "/buildings"
        )


    # ========================================================
    # ENERGY
    # ========================================================

    def get_energy(
        self,
        building_id
    ):

        return self._get(
            f"/energy/building/{building_id}"
        )


    # ========================================================
    # WATER
    # ========================================================

    def get_water(
        self,
        building_id
    ):

        return self._get(
            f"/water/building/{building_id}"
        )


    # ========================================================
    # WASTE
    # ========================================================

    def get_waste(
        self,
        building_id
    ):

        return self._get(
            f"/waste/building/{building_id}"
        )


    # ========================================================
    # TRAFFIC
    # ========================================================

    def get_traffic(
        self,
        building_id
    ):

        return self._get(
            f"/traffic/building/{building_id}"
        )


    # ========================================================
    # COMPLETE BUILDING DATA
    # ========================================================

    def load_building_data(
        self,
        building_id
    ):

        return {

            "energy":
                self.get_energy(
                    building_id
                ),

            "water":
                self.get_water(
                    building_id
                ),

            "waste":
                self.get_waste(
                    building_id
                ),

            "traffic":
                self.get_traffic(
                    building_id
                )
        }


    # ========================================================
    # DATAFRAME HELPER
    # ========================================================

    @staticmethod
    def _prepare_dataframe(
        data,
        numeric_columns=None
    ):

        if not data:

            return pd.DataFrame()


        df = pd.DataFrame(
            data
        )


        # ----------------------------------------------------
        # Timestamp
        # ----------------------------------------------------

        if "recorded_at" in df.columns:

            df["recorded_at"] = pd.to_datetime(
                df["recorded_at"],
                errors="coerce"
            )


        # ----------------------------------------------------
        # Numeric columns
        # ----------------------------------------------------

        if numeric_columns:

            for column in numeric_columns:

                if column in df.columns:

                    df[column] = pd.to_numeric(
                        df[column],
                        errors="coerce"
                    )


        # ----------------------------------------------------
        # Sort by timestamp
        # ----------------------------------------------------

        if "recorded_at" in df.columns:

            df = df.sort_values(
                "recorded_at"
            )


        return df.reset_index(
            drop=True
        )


    # ========================================================
    # ENERGY DATAFRAME
    # ========================================================

    def energy_dataframe(
        self,
        building_id
    ):

        data = self.get_energy(
            building_id
        )

        return self._prepare_dataframe(
            data,
            numeric_columns=[
                "consumption"
            ]
        )


    # ========================================================
    # WATER DATAFRAME
    # ========================================================

    def water_dataframe(
        self,
        building_id
    ):

        data = self.get_water(
            building_id
        )

        return self._prepare_dataframe(
            data,
            numeric_columns=[
                "consumption"
            ]
        )


    # ========================================================
    # WASTE DATAFRAME
    # ========================================================

    def waste_dataframe(
        self,
        building_id
    ):

        data = self.get_waste(
            building_id
        )

        return self._prepare_dataframe(
            data,
            numeric_columns=[
                "quantity"
            ]
        )


    # ========================================================
    # TRAFFIC DATAFRAME
    # ========================================================

    def traffic_dataframe(
        self,
        building_id
    ):

        data = self.get_traffic(
            building_id
        )

        return self._prepare_dataframe(
            data,
            numeric_columns=[
                "vehicle_count",
                "parking_occupancy",
                "average_speed"
            ]
        )


    # ========================================================
    # COMPLETE BUILDING DATAFRAMES
    # ========================================================

    def load_building_dataframes(
        self,
        building_id
    ):

        return {

            "energy":
                self.energy_dataframe(
                    building_id
                ),

            "water":
                self.water_dataframe(
                    building_id
                ),

            "waste":
                self.waste_dataframe(
                    building_id
                ),

            "traffic":
                self.traffic_dataframe(
                    building_id
                )
        }


# ============================================================
# QUICK TEST
# ============================================================

if __name__ == "__main__":

    loader = CampusDataLoader()

    print(
        "\n============================================================"
    )

    print(
        "        CAMPUS360 AI DATA LOADER TEST"
    )

    print(
        "============================================================"
    )


    # ========================================================
    # BACKEND CONNECTION
    # ========================================================

    print(
        "\nBackend:"
    )

    print(
        loader.base_url
    )


    # ========================================================
    # FACILITIES
    # ========================================================

    try:

        facilities = (
            loader.get_facilities()
        )

        print(
            "\nFacilities:"
        )

        print(
            facilities
        )

    except Exception as exc:

        print(
            "\nFailed to load facilities:"
        )

        print(
            exc
        )

        raise


    # ========================================================
    # BUILDINGS
    # ========================================================

    try:

        buildings = (
            loader.get_buildings()
        )

        print(
            "\nBuildings:"
        )

        print(
            buildings
        )

    except Exception as exc:

        print(
            "\nFailed to load buildings:"
        )

        print(
            exc
        )

        raise


    # ========================================================
    # BUILDING TELEMETRY
    # ========================================================

    if buildings:

        building_id = (
            buildings[0].get(
                "id"
            )
        )

        print(
            "\nSelected Building ID:"
        )

        print(
            building_id
        )


        # ----------------------------------------------------
        # Raw data
        # ----------------------------------------------------

        data = (
            loader.load_building_data(
                building_id
            )
        )


        print(
            "\nENERGY:"
        )

        print(
            data["energy"]
        )


        print(
            "\nWATER:"
        )

        print(
            data["water"]
        )


        print(
            "\nWASTE:"
        )

        print(
            data["waste"]
        )


        print(
            "\nTRAFFIC:"
        )

        print(
            data["traffic"]
        )


        # ----------------------------------------------------
        # DataFrames
        # ----------------------------------------------------

        dataframes = (
            loader.load_building_dataframes(
                building_id
            )
        )


        print(
            "\n============================================================"
        )

        print(
            "DATAFRAME SUMMARY"
        )

        print(
            "============================================================"
        )


        for name, dataframe in dataframes.items():

            print(
                f"\n{name.upper()}:"
            )

            print(
                "Rows:",
                len(dataframe)
            )

            print(
                "Columns:",
                list(
                    dataframe.columns
                )
            )


    else:

        print(
            "\nWARNING:"
        )

        print(
            "No buildings were returned by the backend."
        )


    print(
        "\n============================================================"
    )

    print(
        "        DATA LOADER TEST COMPLETE"
    )

    print(
        "============================================================"
    )