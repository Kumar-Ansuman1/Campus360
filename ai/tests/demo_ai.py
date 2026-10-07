from ai.intelligence.advanced_rag import AdvancedRAG
from ai.intelligence.reasoning import DecisionReasoningEngine
from ai.intelligence.what_if import WhatIfEngine


print("=" * 70)
print("              CAMPUS360 AI DEMO SCENARIO")
print("=" * 70)


# =========================================================
# 1. SIMULATED LIVE CAMPUS TELEMETRY
# =========================================================

energy = 75.0
water = 180.0
waste = 30.0
vehicles = 65
parking = 85.0

print("\nLIVE CAMPUS TELEMETRY")
print("-" * 40)

print(f"Energy consumption : {energy} kWh")
print(f"Water consumption  : {water} L")
print(f"Waste generation   : {waste} kg")
print(f"Vehicles           : {vehicles}")
print(f"Parking occupancy  : {parking}%")


# =========================================================
# 2. ANOMALY DETECTION
# =========================================================

anomaly_status = "ANOMALY"
anomaly_score = -0.72

print("\nANOMALY DETECTION")
print("-" * 40)

print("Energy status : ANOMALY")
print(f"Anomaly score : {anomaly_score}")


# =========================================================
# 3. FORECAST
# =========================================================

forecast = {
    "trend": "INCREASING"
}

print("\nSHORT-TERM FORECAST")
print("-" * 40)

print("Energy demand : INCREASING")


# =========================================================
# 4. ADVANCED SEMANTIC RAG
# =========================================================

print("\nADVANCED SEMANTIC RAG")
print("-" * 40)

rag = AdvancedRAG()

query = (
    "high energy consumption HVAC efficiency inspection "
    "increasing energy demand office campus"
)

context, rag_results = rag.build_context(
    query=query,
    top_k=3
)

print(f"\nRetrieved evidence: {len(rag_results)}")

for item in rag_results:
    print(f"\nSource: {item['source']}")
    print(f"Semantic similarity: {item['score']}")


# =========================================================
# 5. DECISION REASONING
# =========================================================

recommendation = (
    "Inspect HVAC operating schedules, cooling demand, "
    "HVAC efficiency, lighting operation, and high-load equipment."
)

reasoning = DecisionReasoningEngine(
    rag_engine=rag
)

result = reasoning.analyze(
    category="ENERGY",
    metric="HVAC consumption",
    current_value=energy,
    anomaly_status=anomaly_status,
    anomaly_score=anomaly_score,
    recommendation=recommendation,
    forecast=forecast,
    context={
        "facility": "EcoFacility Smart Campus",
        "building": "Administration Building",
        "occupancy": 78
    }
)


print("\nAI DECISION")
print("-" * 40)

print("Priority :", result["priority"])
print("Forecast :", result["forecast_signal"])

print("\nExplanation:")
print(result["explanation"])

print("\nRecommendation:")
print(result["recommendation"])

print("\nEvidence:")

for item in result["evidence"]:
    print(
        f"  {item['source']} -> "
        f"{item['relevance']:.4f}"
    )


# =========================================================
# 6. WHAT-IF SIMULATION
# =========================================================

print("\nWHAT-IF IMPACT ANALYSIS")
print("-" * 40)

what_if = WhatIfEngine()

# Use the method already supported by your WhatIfEngine.
scenario = what_if.simulate_energy_reduction(
    current_consumption=energy,
    reduction_percent=15,
    hours=24
)

print(
    f"Current consumption : "
    f"{scenario['current_consumption']} kWh"
)

print(
    f"Reduction           : "
    f"{scenario['reduction_percent']}%"
)

print(
    f"Projected           : "
    f"{scenario['projected_consumption']} kWh"
)

print(
    f"Energy saved        : "
    f"{scenario['energy_saved']} kWh"
)

print(
    f"Cost saving         : "
    f"{scenario['estimated_cost_saving_inr']} INR/day"
)

print(
    f"CO2 reduction       : "
    f"{scenario['estimated_co2_reduction_kg']} kg"
)


# =========================================================
# 7. FINAL EXECUTIVE AI INSIGHT
# =========================================================

print("\n" + "=" * 70)
print("                 CAMPUS360 AI DECISION")
print("=" * 70)

print("\nHIGH PRIORITY ENERGY ISSUE")

print(
    "\nThe campus is experiencing unusually high "
    "HVAC-related energy consumption."
)

print(
    "\nThe AI detected an anomalous operating pattern "
    "and the forecast indicates increasing demand."
)

print(
    "\nAdvanced semantic RAG retrieved operational "
    "evidence related to HVAC schedules, cooling "
    "demand, HVAC efficiency, lighting and "
    "high-load equipment."
)

print("\nRECOMMENDED ACTION:")

print(
    "Inspect HVAC systems and high-load "
    "electrical equipment."
)

print("\nPOTENTIAL IMPACT:")

print(
    f"A 15% energy reduction could save approximately "
    f"₹{scenario['estimated_cost_saving_inr']} per day."
)

print(
    f"Potential CO2 reduction: "
    f"{scenario['estimated_co2_reduction_kg']} kg/day."
)

print("\n" + "=" * 70)
print("              DEMO SCENARIO COMPLETE")
print("=" * 70)