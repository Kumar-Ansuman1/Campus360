from ai.data_loader import CampusDataLoader
from ai.intelligence.kpi import KPIEngine


loader = CampusDataLoader()
kpi = KPIEngine()

building_id = (
    "d040b2f2-9ea8-4336-a9f9-9c72b07e2597"
)

energy = loader.energy_dataframe(building_id)
water = loader.water_dataframe(building_id)
waste = loader.waste_dataframe(building_id)
traffic = loader.traffic_dataframe(building_id)

summary = kpi.generate_summary(
    energy,
    water,
    waste,
    traffic
)

print("\n======================================")
print("CAMPUS360 KPI SUMMARY")
print("======================================")

for category, values in summary.items():

    print(f"\n{category.upper()}")

    for key, value in values.items():
        print(f"{key}: {value}")

print("\n======================================")
print("KPI TEST COMPLETE")
print("======================================")