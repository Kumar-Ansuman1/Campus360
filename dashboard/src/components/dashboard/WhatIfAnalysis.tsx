import type {
  WhatIfAnalysis as WhatIfAnalysisData,
  WhatIfData,
} from "../../types/dashboard"

type WhatIfAnalysisProps = {
  whatIf: WhatIfData
  analysis: WhatIfAnalysisData
}

function formatNumber(value: number, decimals = 1) {
  return value.toLocaleString(undefined, {
    maximumFractionDigits: decimals,
  })
}

function formatCurrency(value: number) {
  return `₹${value.toLocaleString(undefined, {
    maximumFractionDigits: 0,
  })}`
}

function WhatIfAnalysis({
  whatIf,
  analysis,
}: WhatIfAnalysisProps) {
  if (!analysis.available) {
    return (
      <section className="h-full rounded-2xl border border-blue-100 bg-white p-5 shadow-sm">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            What-If Analysis
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            AI-powered sustainability scenario
          </p>
        </div>

        <div className="mt-6 flex min-h-60 items-center justify-center rounded-xl bg-slate-50">
          <p className="text-sm text-slate-400">
            No What-If scenario is currently available.
          </p>
        </div>
      </section>
    )
  }

  return (
    <section className="h-full rounded-2xl border border-blue-100 bg-white p-5 shadow-sm">
      <div className="mb-5 flex items-start justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            What-If Analysis
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            AI-powered sustainability scenario
          </p>
        </div>

        <span className="rounded-full border border-blue-100 bg-blue-50 px-3 py-1 text-[10px] font-semibold text-blue-600">
          {whatIf.reduction_percent}% reduction
        </span>
      </div>

      <div className="rounded-xl border border-blue-100 bg-blue-50 p-4">
        <p className="text-[10px] font-semibold uppercase tracking-wide text-blue-600">
          Scenario
        </p>

        <p className="mt-1 text-sm font-semibold text-slate-800">
          {whatIf.scenario.replaceAll("_", " ")}
        </p>

        <p className="mt-2 text-xs leading-5 text-slate-500">
          {analysis.interpretation}
        </p>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-3">
        <div className="rounded-xl border border-slate-100 bg-slate-50 p-3">
          <p className="text-[10px] font-medium uppercase tracking-wide text-slate-400">
            Baseline
          </p>

          <p className="mt-1 text-sm font-semibold text-slate-700">
            {formatNumber(analysis.baseline_daily_kwh)} kWh/day
          </p>
        </div>

        <div className="rounded-xl border border-slate-100 bg-slate-50 p-3">
          <p className="text-[10px] font-medium uppercase tracking-wide text-slate-400">
            Projected
          </p>

          <p className="mt-1 text-sm font-semibold text-blue-700">
            {formatNumber(analysis.projected_daily_kwh)} kWh/day
          </p>
        </div>

        <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-3">
          <p className="text-[10px] font-medium uppercase tracking-wide text-emerald-600">
            Energy Saved
          </p>

          <p className="mt-1 text-sm font-semibold text-emerald-700">
            {formatNumber(analysis.energy_saved_kwh_per_day)} kWh/day
          </p>
        </div>

        <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-3">
          <p className="text-[10px] font-medium uppercase tracking-wide text-emerald-600">
            Cost Saving
          </p>

          <p className="mt-1 text-sm font-semibold text-emerald-700">
            {formatCurrency(
              analysis.estimated_cost_saving_inr_per_day,
            )}
            /day
          </p>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-3">
        <div className="rounded-xl border border-slate-100 bg-white p-3">
          <p className="text-[10px] font-medium uppercase tracking-wide text-slate-400">
            CO₂ Reduction
          </p>

          <p className="mt-1 text-sm font-semibold text-slate-700">
            {formatNumber(
              analysis.estimated_co2_reduction_kg_per_day,
            )}{" "}
            kg/day
          </p>
        </div>

        <div className="rounded-xl border border-slate-100 bg-white p-3">
          <p className="text-[10px] font-medium uppercase tracking-wide text-slate-400">
            Saving
          </p>

          <p className="mt-1 text-sm font-semibold text-slate-700">
            {analysis.saving_percent}%
          </p>
        </div>
      </div>

      <p className="mt-4 text-[10px] text-slate-400">
        Values are supplied by the Campus360 AI backend.
      </p>
    </section>
  )
}

export default WhatIfAnalysis