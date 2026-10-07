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