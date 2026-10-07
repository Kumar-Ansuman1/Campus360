import type {
  DashboardStatus,
  ForecastData,
  OverallStatus,
} from "../../types/dashboard"

type AIInsightPanelProps = {
  currentStatus: OverallStatus
  confidence: string
  priority: string
  explanation: string
  forecast: ForecastData
}

function getStatusStyle(status: DashboardStatus) {
  switch (status) {
    case "CRITICAL":
      return "bg-red-50 text-red-600 border-red-100"

    case "ATTENTION":
      return "bg-amber-50 text-amber-700 border-amber-100"

    case "WARNING":
      return "bg-yellow-50 text-yellow-700 border-yellow-100"

    case "NORMAL":
      return "bg-emerald-50 text-emerald-600 border-emerald-100"

    default:
      return "bg-slate-50 text-slate-600 border-slate-100"
  }
}

function getPriorityStyle(priority: string) {
  const normalized = priority.toUpperCase()

  if (normalized === "CRITICAL") {
    return "text-red-600"
  }

  if (normalized === "HIGH") {
    return "text-amber-600"
  }

  if (normalized === "MEDIUM") {
    return "text-blue-600"
  }

  return "text-emerald-600"
}

function formatConfidence(confidence: string | null | undefined) {
  if (!confidence) {
    return "N/A"
  }

  return confidence
}

function AIInsightPanel({
  currentStatus,
  confidence,
  priority,
  explanation,
  forecast,
}: AIInsightPanelProps) {
  const status = currentStatus.overall_status

  return (
    <section className="h-full rounded-2xl border border-blue-100 bg-white p-5 shadow-sm">
      <div className="mb-5 flex items-start justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            AI Insight
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Current facility intelligence
          </p>
        </div>

        <span
          className={`rounded-full border px-3 py-1 text-[10px] font-semibold ${getStatusStyle(
            status,
          )}`}
        >
          {status}
        </span>
      </div>

      <div className="rounded-xl border border-blue-100 bg-blue-50 p-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-wide text-blue-600">
              AI Confidence
            </p>

            <p className="mt-1 text-2xl font-bold text-slate-900">
              {formatConfidence(confidence)}
            </p>
          </div>

          <div className="text-right">
            <p className="text-[10px] font-semibold uppercase tracking-wide text-slate-400">
              Priority
            </p>

            <p
              className={`mt-1 text-sm font-bold ${getPriorityStyle(
                priority,
              )}`}
            >
              {priority}
            </p>
          </div>
        </div>
      </div>

      <div className="mt-4">
        <p className="text-[10px] font-semibold uppercase tracking-wide text-slate-400">
          AI Explanation
        </p>

        <p className="mt-2 text-sm leading-6 text-slate-600">
          {explanation || "No AI explanation is currently available."}
        </p>
      </div>

      <div className="mt-5 grid grid-cols-2 gap-3">
        <div className="rounded-xl border border-slate-100 bg-slate-50 p-3">
          <p className="text-[10px] font-medium uppercase tracking-wide text-slate-400">
            Energy
          </p>

          <p className="mt-1 text-sm font-semibold text-slate-700">
            {currentStatus.energy_status}
          </p>
        </div>

        <div className="rounded-xl border border-slate-100 bg-slate-50 p-3">
          <p className="text-[10px] font-medium uppercase tracking-wide text-slate-400">
            Trend
          </p>

          <p className="mt-1 text-sm font-semibold text-slate-700">
            {forecast.trend}
          </p>
        </div>

        <div className="rounded-xl border border-slate-100 bg-slate-50 p-3">
          <p className="text-[10px] font-medium uppercase tracking-wide text-slate-400">
            Water
          </p>

          <p className="mt-1 text-sm font-semibold text-slate-700">
            {currentStatus.water_status}
          </p>
        </div>

        <div className="rounded-xl border border-slate-100 bg-slate-50 p-3">
          <p className="text-[10px] font-medium uppercase tracking-wide text-slate-400">
            Traffic
          </p>

          <p className="mt-1 text-sm font-semibold text-slate-700">
            {currentStatus.traffic_status}
          </p>
        </div>
      </div>

      <div className="mt-4 rounded-xl border border-slate-100 bg-white p-3">
        <p className="text-[10px] font-semibold uppercase tracking-wide text-slate-400">
          AI Assessment
        </p>

        <p className="mt-1 text-xs leading-5 text-slate-500">
          The current facility state is{" "}
          <span className="font-semibold text-slate-700">
            {status.toLowerCase()}
          </span>{" "}
          with an{" "}
          <span className="font-semibold text-slate-700">
            {forecast.trend.toLowerCase()}
          </span>{" "}
          energy forecast.
        </p>
      </div>
    </section>
  )
}

export default AIInsightPanel