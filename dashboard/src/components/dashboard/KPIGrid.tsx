import KPICard from "./KPICard"
import type { KPIData } from "../../types/dashboard"

type KPIGridProps = {
  kpis: KPIData
}

function KPIGrid({ kpis }: KPIGridProps) {
  return (
    <section className="h-full rounded-2xl border border-blue-100 bg-white p-5 shadow-sm">
      <div className="mb-5">
        <h2 className="text-lg font-semibold text-slate-900">
          Facility Overview
        </h2>

        <p className="text-sm text-slate-500">
          Current facility performance
        </p>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <KPICard
          title="Energy"
          value={kpis.energy_kwh}
          unit="kWh"
          icon="⚡"
        />

        <KPICard
          title="Water"
          value={kpis.water_liters}
          unit="L"
          icon="💧"
        />

        <KPICard
          title="Waste"
          value={kpis.waste_kg}
          unit="kg"
          icon="🗑️"
        />

        <KPICard
          title="Vehicles"
          value={kpis.vehicles}
          unit="vehicles"
          icon="🚗"
        />

        <KPICard
          title="Parking"
          value={kpis.parking_percent}
          unit="% occupied"
          icon="🅿️"
        />

        <KPICard
          title="Average Speed"
          value={kpis.average_speed}
          unit="km/h"
          icon="🛣️"
        />
      </div>
    </section>
  )
}

export default KPIGrid