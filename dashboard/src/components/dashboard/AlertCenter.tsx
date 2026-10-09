import type {
  DashboardAnomalies,
  DashboardStatus,
  OptimizationData,
} from "../../types/dashboard"

type AlertCenterProps = {
  anomalies: DashboardAnomalies
  currentStatus: {
    overall_status?: DashboardStatus
    energy_status: string
    water_status: string
    waste_status: string
    traffic_status: string
  }
  optimization?: OptimizationData
}

type AlertItem = {
  category: string
  status: DashboardStatus
  message: string
}

function normalizeStatus(
  status: string,
): DashboardStatus {
  const normalized =
    status.toUpperCase()

  if (
    normalized === "CRITICAL" ||
    normalized === "ATTENTION" ||
    normalized === "WARNING" ||
    normalized === "NORMAL"
  ) {
    return normalized
  }

  if (normalized === "HIGH") {
    return "ATTENTION"
  }

  return "NORMAL"
}

function getStatusStyle(
  status: DashboardStatus,
) {
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

function getTotalAnomalyCount(
  anomalies: DashboardAnomalies,
) {
  return (
    (anomalies?.energy?.count ?? 0) +
    (anomalies?.water?.count ?? 0) +
    (anomalies?.waste?.count ?? 0) +
    (anomalies?.traffic?.count ?? 0)
  )
}

function getTotalRecordsAnalyzed(
  anomalies: DashboardAnomalies,
) {
  const getLength = (
    data:
      | unknown
      | unknown[],
  ) => {
    if (Array.isArray(data)) {
      return data.length
    }

    return data ? 1 : 0
  }

  return (
    getLength(anomalies?.energy?.data) +
    getLength(anomalies?.water?.data) +
    getLength(anomalies?.waste?.data) +
    getLength(anomalies?.traffic?.data)
  )
}

function getLatestAnomalyScore(
  anomalies: DashboardAnomalies,
) {
  const scores = [
    anomalies?.energy?.latest_score,
    anomalies?.water?.latest_score,
    anomalies?.waste?.latest_score,
    anomalies?.traffic?.latest_score,
  ].filter(
    (score): score is number =>
      typeof score === "number" &&
      Number.isFinite(score),
  )

  if (scores.length === 0) {
    return "N/A"
  }

  return scores[0].toFixed(2)
}

function getLatestAnomalyStatus(
  anomalies: DashboardAnomalies,
) {
  const statuses = [
    anomalies?.energy?.latest_status,
    anomalies?.water?.latest_status,
    anomalies?.waste?.latest_status,
    anomalies?.traffic?.latest_status,
  ].filter(Boolean)

  if (statuses.length === 0) {
    return null
  }

  const priority = [
    "CRITICAL",
    "ATTENTION",
    "WARNING",
    "ANOMALY",
    "NORMAL",
  ]

  for (const status of priority) {
    const found = statuses.find(
      (item) =>
        item.toUpperCase() === status,
    )

    if (found) {
      return found
    }
  }

  return statuses[0]
}

function getAnomalyMessage(
  anomalies: DashboardAnomalies,
) {
  const count =
    getTotalAnomalyCount(anomalies)

  const latestStatus =
    getLatestAnomalyStatus(anomalies)

  if (count === 0) {
    return "No anomalies detected by the AI pipeline."
  }

  if (latestStatus) {
    return `Latest AI anomaly status: ${latestStatus}.`
  }

  return `${count} anomal${
    count === 1 ? "y" : "ies"
  } detected by the AI pipeline.`
}

function getActiveIssueCount(
  currentStatus: AlertCenterProps["currentStatus"],
) {
  const statuses = [
    currentStatus.energy_status,
    currentStatus.water_status,
    currentStatus.waste_status,
    currentStatus.traffic_status,
  ]

  return statuses.filter(
    (status) =>
      normalizeStatus(status) !==
      "NORMAL",
  ).length
}

function AlertCenter({
  anomalies,
  currentStatus,
  optimization,
}: AlertCenterProps) {
  const topPriority =
    optimization?.top_priority

  const alerts: AlertItem[] = [
    {
      category: "Energy",
      status: normalizeStatus(
        currentStatus.energy_status,
      ),
      message:
        currentStatus.energy_status.toUpperCase() ===
        "NORMAL"
          ? "Energy consumption is within the normal operating range."
          : `Energy consumption is currently ${currentStatus.energy_status.toUpperCase()} and requires attention.`,
    },

    {
      category: "Water",
      status: normalizeStatus(
        currentStatus.water_status,
      ),
      message:
        currentStatus.water_status.toUpperCase() ===
        "NORMAL"
          ? "Water consumption is within the normal operating range."
          : `Water status reported as ${currentStatus.water_status}.`,
    },

    {
      category: "Waste",
      status: normalizeStatus(
        currentStatus.waste_status,
      ),
      message:
        currentStatus.waste_status.toUpperCase() ===
        "NORMAL"
          ? "Waste generation is within expected levels."
          : `Waste status reported as ${currentStatus.waste_status}.`,
    },

    {
      category: "Traffic",
      status: normalizeStatus(
        currentStatus.traffic_status,
      ),
      message:
        currentStatus.traffic_status.toUpperCase() ===
        "NORMAL"
          ? "Traffic conditions are stable."
          : `Traffic status reported as ${currentStatus.traffic_status}.`,
    },
  ]

  const totalAnomalies =
    getTotalAnomalyCount(anomalies)

  const recordsAnalyzed =
    getTotalRecordsAnalyzed(anomalies)

  const activeIssues =
    getActiveIssueCount(
      currentStatus,
    )

  return (
    <section className="h-full rounded-2xl border border-blue-100 bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="mb-5 flex items-start justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Facility Alerts
          </h2>

          <p className="text-sm text-slate-500">
            AI-detected operational conditions
          </p>
        </div>

        <span className="rounded-lg bg-blue-50 px-2.5 py-1 text-[10px] font-semibold text-blue-600">
          {activeIssues} active{" "}
          {activeIssues === 1
            ? "issue"
            : "issues"}
        </span>
      </div>

      {/* Status alerts */}
      <div className="space-y-3">
        {alerts.map((alert) => (
          <div
            key={alert.category}
            className="rounded-xl border border-slate-100 bg-slate-50 p-3"
          >
            <div className="flex items-center justify-between gap-3">
              <p className="text-sm font-medium text-slate-700">
                {alert.category}
              </p>

              <span
                className={`rounded-full border px-2.5 py-1 text-[10px] font-semibold ${getStatusStyle(
                  alert.status,
                )}`}
              >
                {alert.status}
              </span>
            </div>

            <p className="mt-2 text-xs leading-5 text-slate-500">
              {alert.message}
            </p>

            {topPriority?.category ===
              alert.category &&
              alert.status !==
                "NORMAL" && (
                <p className="mt-1 text-[10px] font-semibold text-red-600">
                  Priority:{" "}
                  {topPriority.priority}
                </p>
              )}
          </div>
        ))}
      </div>

      {/* AI anomaly summary */}
      <div className="mt-4 rounded-xl border border-blue-100 bg-blue-50 p-3">
        <p className="text-[10px] font-semibold uppercase tracking-wide text-blue-600">
          AI Anomaly Detection
        </p>

        <p className="mt-1 text-xs leading-5 text-slate-600">
          {getAnomalyMessage(anomalies)}
        </p>

        <div className="mt-2 flex items-center justify-between text-[10px] text-slate-400">
          <span>
            Latest score:{" "}
            {getLatestAnomalyScore(
              anomalies,
            )}
          </span>

          <span>
            {recordsAnalyzed} records analyzed
          </span>
        </div>
      </div>
    </section>
  )
}

export default AlertCenter