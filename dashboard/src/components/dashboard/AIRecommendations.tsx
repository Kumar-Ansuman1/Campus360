type AIRecommendationsProps = {
  recommendation: string
  priority: string
}

function getPriorityStyle(priority: string) {
  switch (priority.toUpperCase()) {
    case "CRITICAL":
      return {
        badge:
          "border-red-100 bg-red-50 text-red-700",
        dot: "bg-red-500",
      }

    case "HIGH":
      return {
        badge:
          "border-orange-100 bg-orange-50 text-orange-700",
        dot: "bg-orange-500",
      }

    case "MEDIUM":
      return {
        badge:
          "border-yellow-100 bg-yellow-50 text-yellow-700",
        dot: "bg-yellow-500",
      }

    case "LOW":
    default:
      return {
        badge:
          "border-emerald-100 bg-emerald-50 text-emerald-700",
        dot: "bg-emerald-500",
      }
  }
}

function AIRecommendations({
  recommendation,
  priority,
}: AIRecommendationsProps) {
  const priorityStyle =
    getPriorityStyle(priority)

  return (
    <section className="h-full rounded-2xl border border-blue-100 bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            AI Recommendation
          </h2>

          <p className="text-sm text-slate-500">
            Recommended action based on current facility conditions
          </p>
        </div>

        <span
          className={`rounded-full border px-3 py-1 text-[10px] font-semibold ${priorityStyle.badge}`}
        >
          {priority.toUpperCase()}
        </span>
      </div>

      {/* Recommendation */}
      <div className="mt-5 rounded-xl border border-blue-100 bg-blue-50/60 p-5">
        <div className="flex items-start gap-3">
          {/* Icon */}
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-blue-100 bg-white text-lg shadow-sm">
            💡
          </div>

          <div className="min-w-0">
            <p className="text-[10px] font-semibold uppercase tracking-wide text-blue-600">
              AI Suggested Action
            </p>

            <p className="mt-2 text-sm leading-6 text-slate-700">
              {recommendation}
            </p>
          </div>
        </div>
      </div>

      {/* Details */}
      <div className="mt-4 grid grid-cols-2 gap-3">
        <div className="rounded-xl border border-slate-100 bg-slate-50 p-3">
          <p className="text-[10px] uppercase tracking-wide text-slate-400">
            Priority
          </p>

          <div className="mt-1 flex items-center gap-2">
            <span
              className={`h-2 w-2 rounded-full ${priorityStyle.dot}`}
            />

            <p className="text-sm font-semibold text-slate-800">
              {priority.toUpperCase()}
            </p>
          </div>
        </div>

        <div className="rounded-xl border border-slate-100 bg-slate-50 p-3">
          <p className="text-[10px] uppercase tracking-wide text-slate-400">
            Source
          </p>

          <p className="mt-1 text-sm font-semibold text-slate-800">
            AI Analysis
          </p>
        </div>
      </div>
    </section>
  )
}

export default AIRecommendations