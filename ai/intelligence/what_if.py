"""
Campus360 AI - What-If Simulation Engine

Simulates the operational impact of changing facility parameters.
"""

from datetime import datetime


class WhatIfEngine:

    def simulate_energy_reduction(
        self,
        current_consumption,
        reduction_percent,
        hours=24,
        electricity_rate=8.0,
        emission_factor=0.82
    ):
        """
        Simulate reducing energy consumption.

        electricity_rate:
            ₹ per kWh

        emission_factor:
            kg CO2 per kWh
        """

        current_consumption = float(current_consumption)
        reduction_percent = float(reduction_percent)

        reduction_fraction = reduction_percent / 100

        projected_consumption = (
            current_consumption * (1 - reduction_fraction)
        )

        energy_saved_per_period = (
            current_consumption - projected_consumption
        )

        total_energy_saved = (
            energy_saved_per_period * hours
        )

        cost_saving = (
            total_energy_saved * electricity_rate
        )

        co2_reduction = (
            total_energy_saved * emission_factor
        )

        return {
            "scenario": "ENERGY_REDUCTION",
            "current_consumption": round(
                current_consumption, 2
            ),
            "reduction_percent": round(
                reduction_percent, 2
            ),
            "projected_consumption": round(
                projected_consumption, 2
            ),
            "energy_saved": round(
                total_energy_saved, 2
            ),
            "estimated_cost_saving_inr": round(
                cost_saving, 2
            ),
            "estimated_co2_reduction_kg": round(
                co2_reduction, 2
            ),
            "hours": hours,
            "created_at": datetime.now().isoformat()
        }

    def simulate_water_reduction(
        self,
        current_consumption,
        reduction_percent,
        hours=24,
        water_cost=0.05
    ):
        """
        Simulate reducing water consumption.

        water_cost:
            ₹ per litre
        """

        current_consumption = float(current_consumption)
        reduction_percent = float(reduction_percent)

        reduction_fraction = reduction_percent / 100

        projected_consumption = (
            current_consumption * (1 - reduction_fraction)
        )

        water_saved = (
            current_consumption -
            projected_consumption
        )

        total_water_saved = (
            water_saved * hours
        )

        cost_saving = (
            total_water_saved * water_cost
        )

        return {
            "scenario": "WATER_REDUCTION",
            "current_consumption": round(
                current_consumption, 2
            ),
            "reduction_percent": round(
                reduction_percent, 2
            ),
            "projected_consumption": round(
                projected_consumption, 2
            ),
            "water_saved_litres": round(
                total_water_saved, 2
            ),
            "estimated_cost_saving_inr": round(
                cost_saving, 2
            ),
            "hours": hours,
            "created_at": datetime.now().isoformat()
        }

    def simulate_hvac(
        self,
        current_energy,
        hvac_efficiency_improvement
    ):
        """
        Simulate HVAC efficiency improvement.
        """

        return self.simulate_energy_reduction(
            current_consumption=current_energy,
            reduction_percent=hvac_efficiency_improvement
        )

    def compare_scenarios(
        self,
        current_energy,
        scenarios
    ):
        """
        Compare multiple energy scenarios.

        Example:

        scenarios = [
            {"name": "HVAC Optimization", "reduction": 10},
            {"name": "Lighting Optimization", "reduction": 15},
            {"name": "Combined Optimization", "reduction": 25}
        ]
        """

        results = []

        for scenario in scenarios:

            result = self.simulate_energy_reduction(
                current_consumption=current_energy,
                reduction_percent=scenario["reduction"]
            )

            result["scenario_name"] = scenario["name"]

            results.append(result)

        best = None

        if results:
            best = max(
                results,
                key=lambda x: x["estimated_cost_saving_inr"]
            )

        return {
            "scenario_count": len(results),
            "scenarios": results,
            "best_scenario": best
        }


if __name__ == "__main__":

    print("=" * 55)
    print("CAMPUS360 WHAT-IF SIMULATION ENGINE")
    print("=" * 55)

    engine = WhatIfEngine()

    print("\n[1] ENERGY REDUCTION SCENARIO")

    result = engine.simulate_energy_reduction(
        current_consumption=45.8,
        reduction_percent=15,
        hours=24
    )

    print(result)

    print("\n[2] HVAC SCENARIO")

    hvac = engine.simulate_hvac(
        current_energy=45.8,
        hvac_efficiency_improvement=20
    )

    print(hvac)

    print("\n[3] SCENARIO COMPARISON")

    scenarios = [
        {
            "name": "HVAC Optimization",
            "reduction": 10
        },
        {
            "name": "Lighting Optimization",
            "reduction": 15
        },
        {
            "name": "Combined Optimization",
            "reduction": 25
        }
    ]

    comparison = engine.compare_scenarios(
        current_energy=45.8,
        scenarios=scenarios
    )

    for scenario in comparison["scenarios"]:
        print(
            scenario["scenario_name"],
            "->",
            scenario["estimated_cost_saving_inr"],
            "INR/day"
        )

    print("\nBEST SCENARIO:")

    print(
        comparison["best_scenario"]["scenario_name"]
    )

    print("\n" + "=" * 55)
    print("WHAT-IF TEST COMPLETE")
    print("=" * 55)