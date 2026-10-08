import { useState } from "react"

import type {
  ContextAnalysis,
  OptimizationData,
  OptimizationPriority,
} from "../../types/dashboard"

type AIDecisionCenterProps = {
  contextAnalysis?: ContextAnalysis
  optimization?: OptimizationData
  onOptimize?: () => void
  isOptimizing?: boolean
}

function getPriorityStyles(priority: string) {
  const value = priority.toUpperCase()

  if (value.startsWith("P1")) {
    return {
      badge: "bg-red-50 text-red-700 border-red-100",
      dot: "bg-red-500",
      accent: "border-red-200",
      background: "bg-red-50/50",
    }
  }

  if (value.startsWith("P2")) {
    return {
      badge: "bg-orange-50 text-orange-700 border-orange-100",
      dot: "bg-orange-500",
      accent: "border-orange-200",
      background: "bg-orange-50/50",
    }
  }

  if (value.startsWith("P3")) {
    return {
      badge: "bg-yellow-50 text-yellow-700 border-yellow-100",
      dot: "bg-yellow-500",
      accent: "border-yellow-200",
      background: "bg-yellow-50/50",
    }
  }

  return {
    badge: "bg-slate-50 text-slate-600 border-slate-200",
    dot: "bg-slate-400",
    accent: "border-slate-200",
    background: "bg-slate-50/50",
  }
}

function getStatusStyles(status: string) {
  const value = status.toUpperCase()

  if (value === "CRITICAL") {
    return "bg-red-50 text-red-700 border-red-100"
  }

  if (value === "HIGH") {
    return "bg-orange-50 text-orange-700 border-orange-100"
  }

  if (value === "MODERATE") {
    return "bg-yellow-50 text-yellow-700 border-yellow-100"
  }

  return "bg-emerald-50 text-emerald-700 border-emerald-100"
}

function formatNumber(value: number) {
  return new Intl.NumberFormat("en-IN", {
    maximumFractionDigits: 1,
  }).format(value)
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat("en-IN", {
    maximumFractionDigits: 0,
  }).format(value)
}

function PriorityBadge({
  priority,
}: {
  priority: string
}) {
  const styles = getPriorityStyles(priority)

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] font-bold ${styles.badge}`}
    >
      <span
        className={`h-1.5 w-1.5 rounded-full ${styles.dot}`}
      />

      {priority}
    </span>
  )
}

function ImpactCard({
  label,
  value,
  unit,
}: {
  label: string
  value: string
  unit: string
}) {
  return (
    <div className="rounded-xl border border-blue-100 bg-white p-3">
      <p className="text-[10px] font-medium uppercase tracking-wide text-slate-400">
        {label}
      </p>

      <p className="mt-1 text-lg font-bold text-slate-900">
        {value}
      </p>

      <p className="text-[10px] text-slate-400">
        {unit}
      </p>
    </div>
  )
}

function ContextMetric({
  label,
  value,
  highlighted = false,
}: {
  label: string
  value: string
  highlighted?: boolean
}) {
  return (
    <div
      className={`rounded-xl border p-3 ${
        highlighted
          ? "border-orange-100 bg-orange-50/60"
          : "border-slate-100 bg-slate-50"
      }`}
    >
      <p className="text-[10px] font-medium text-slate-400">
        {label}
      </p>

      <p
        className={`mt-1 text-sm font-bold ${
          highlighted
            ? "text-orange-700"
            : "text-slate-800"
        }`}
      >
        {value}
      </p>
    </div>
  )
}

function PriorityRow({
  issue,
  active,
}: {
  issue: OptimizationData["ranked_issues"][number]
  active: boolean
}) {
  const styles = getPriorityStyles(issue.priority)

  return (
    <div
      className={`flex items-center justify-between rounded-xl border px-3 py-2.5 ${
        active
          ? `${styles.accent} ${styles.background}`
          : "border-slate-100 bg-white"
      }`}
    >
      <div className="flex min-w-0 items-center gap-2.5">
        <span
          className={`h-2 w-2 shrink-0 rounded-full ${styles.dot}`}
        />

        <div className="min-w-0">
          <p className="text-xs font-semibold text-slate-800">
            {issue.category}
          </p>

          <p className="text-[10px] text-slate-400">
            {issue.status} • {issue.deviation_percent}% deviation
          </p>
        </div>
      </div>

      <PriorityBadge priority={issue.priority} />
    </div>
  )
}

function DecisionDetails({
  priority,
  showRecommendation,
}: {
  priority: OptimizationPriority
  showRecommendation: boolean
}) {
  const styles = getPriorityStyles(
    priority.priority,
  )

  return (
    <div
      className={`mt-4 rounded-2xl border p-4 ${styles.accent} ${styles.background}`}
    >
      <div className="flex flex-col gap-4">
        <div>
          <p className="text-[10px] font-bold uppercase tracking-[0.12em] text-slate-400">
            Top Priority
          </p>

          <div className="mt-1 flex items-center gap-2">
            <h3 className="text-xl font-bold text-slate-900">
              {priority.category}
            </h3>

            <PriorityBadge
              priority={priority.priority}
            />
          </div>
        </div>

        <div className="grid gap-3 md:grid-cols-2">
          <div className="rounded-xl border border-white bg-white/80 p-3">
            <p className="text-[10px] font-bold uppercase tracking-wide text-slate-400">
              Why this needs attention
            </p>

            <p className="mt-2 text-sm leading-6 text-slate-700">
              {priority.category} is currently{" "}
              <span className="font-semibold">
                {priority.status}
              </span>{" "}
              with a{" "}
              <span className="font-semibold">
                {formatNumber(
                  priority.deviation_percent,
                )}
                %
              </span>{" "}
              deviation from the expected state.
            </p>

            <p className="mt-1 text-xs text-slate-500">
              Forecast trend:{" "}
              <span className="font-semibold text-slate-700">
                {priority.forecast}
              </span>
            </p>
          </div>

          {showRecommendation && (
            <div className="rounded-xl border border-blue-200 bg-white p-3">
              <p className="text-[10px] font-bold uppercase tracking-wide text-blue-600">
                Recommended action
              </p>

              <p className="mt-2 text-sm font-semibold leading-6 text-slate-800">
                {priority.recommended_action}
              </p>
            </div>
          )}
        </div>

        {showRecommendation && (
          <div className="rounded-xl border border-blue-200 bg-white p-3">
            <div className="mb-3">
              <p className="text-xs font-bold text-blue-700">
                Expected impact
              </p>

              <p className="mt-0.5 text-[10px] text-slate-400">
                Based on the existing What-If simulation
              </p>
            </div>

            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              <ImpactCard
                label="Energy saved"
                value={formatNumber(
                  priority.impact
                    .energy_saved_kwh_per_day,
                )}
                unit="kWh / day"
              />

              <ImpactCard
                label="Cost saving"
                value={`₹${formatCurrency(
                  priority.impact
                    .cost_saving_inr_per_day,
                )}`}
                unit="per day"
              />

              <ImpactCard
                label="CO₂ reduction"
                value={formatNumber(
                  priority.impact
                    .co2_reduction_kg_per_day,
                )}
                unit="kg / day"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

function ContextPanel({
  context,
}: {
  context: ContextAnalysis
}) {
  const enabledFlags = Object.entries(
    context.flags,
  ).filter(([, enabled]) => enabled)

  return (
    <div className="rounded-2xl border border-blue-100 bg-white p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-[10px] font-bold uppercase tracking-[0.12em] text-blue-500">
            Context Analysis
          </p>

          <h3 className="mt-1 text-sm font-semibold text-slate-900">
            Why the AI considers this critical
          </h3>
        </div>

        <span
          className={`rounded-full border px-2.5 py-1 text-[10px] font-bold ${getStatusStyles(
            context.status,
          )}`}
        >
          {context.status}
        </span>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-2">
        <ContextMetric
          label="Actual energy"
          value={`${formatNumber(
            context.actual_energy,
          )} kWh`}
          highlighted
        />

        <ContextMetric
          label="Expected energy"
          value={`${formatNumber(
            context.expected_energy,
          )} kWh`}
        />

        <ContextMetric
          label="Deviation"
          value={`+${formatNumber(
            context.deviation_percent,
          )}%`}
          highlighted
        />

        <ContextMetric
          label="Occupancy"
          value={`${formatNumber(
            context.occupancy,
          )}%`}
          highlighted={
            context.occupancy < 30
          }
        />

        <ContextMetric
          label="Temperature"
          value={`${formatNumber(
            context.temperature,
          )}°C`}
          highlighted={
            context.temperature >= 30
          }
        />

        <ContextMetric
          label="HVAC load"
          value={`${formatNumber(
            context.hvac_load,
          )}%`}
          highlighted={
            context.hvac_load >= 80
          }
        />
      </div>

      <div className="mt-3 rounded-xl bg-blue-50 p-3">
        <p className="text-[10px] font-bold uppercase tracking-wide text-blue-500">
          AI interpretation
        </p>

        <p className="mt-1 text-xs leading-5 text-slate-600">
          {context.interpretation}
        </p>
      </div>

      {enabledFlags.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {enabledFlags.map(([flag]) => (
            <span
              key={flag}
              className="rounded-full border border-orange-100 bg-orange-50 px-2 py-1 text-[10px] font-medium capitalize text-orange-700"
            >
              {flag.replaceAll("_", " ")}
            </span>
          ))}
        </div>
      )}
    </div>
  )
}

function EmptyDecisionState({
  onOptimize,
  isOptimizing,
}: {
  onOptimize?: () => void
  isOptimizing?: boolean
}) {
  return (
    <section className="rounded-2xl border border-blue-100 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-lg">
            🤖
          </div>

          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              AI Decision Center
            </h2>

            <p className="text-sm text-slate-500">
              Ready to analyze campus priorities
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={onOptimize}
          disabled={isOptimizing}
          className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-xs font-bold text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isOptimizing ? (
            <>
              <span className="h-3 w-3 animate-spin rounded-full border-2 border-white/40 border-t-white" />
              Optimizing...
            </>
          ) : (
            <>
              <span>⚡</span>
              Optimize Campus
            </>
          )}
        </button>
      </div>

      <div className="mt-5 rounded-xl border border-slate-100 bg-slate-50 p-4">
        <p className="text-sm text-slate-500">
          Click Optimize Campus to analyze the current campus state and identify the recommended action.
        </p>
      </div>
    </section>
  )
}

function AIDecisionCenter({
  contextAnalysis,
  optimization,
  onOptimize,
  isOptimizing = false,
}: AIDecisionCenterProps) {
  const [showRecommendation, setShowRecommendation] =
    useState(false)

  if (
    !optimization ||
    !optimization.top_priority
  ) {
    return (
      <EmptyDecisionState
        onOptimize={onOptimize}
        isOptimizing={isOptimizing}
      />
    )
  }

  const topPriority =
    optimization.top_priority

  function handleOptimize() {
    setShowRecommendation(true)
    onOptimize?.()
  }

  return (
    <section className="rounded-2xl border border-blue-100 bg-white p-5 shadow-sm">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-50 text-base">
              🤖
            </div>

            <div>
              <h2 className="text-lg font-semibold text-slate-900">
                AI Decision Center
              </h2>

              <p className="text-xs text-slate-500">
                Campus optimization & priority engine
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleOptimize}
            disabled={isOptimizing}
            className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2 text-xs font-bold text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isOptimizing ? (
              <>
                <span className="h-3 w-3 animate-spin rounded-full border-2 border-white/40 border-t-white" />
                Optimizing...
              </>
            ) : (
              <>
                <span>⚡</span>
                Optimize Campus
              </>
            )}
          </button>

          <div className="rounded-xl border border-orange-100 bg-orange-50 px-3 py-2">
            <p className="text-[10px] font-bold uppercase tracking-wide text-orange-600">
              Attention
            </p>

            <p className="mt-0.5 text-xs font-bold text-orange-700">
              {topPriority.priority}
            </p>
          </div>
        </div>
      </div>

      <DecisionDetails
        priority={topPriority}
        showRecommendation={showRecommendation}
      />

      <div className="mt-4 grid gap-4 lg:grid-cols-2">
        {contextAnalysis ? (
          <ContextPanel
            context={contextAnalysis}
          />
        ) : (
          <div className="rounded-2xl border border-blue-100 bg-slate-50 p-4">
            <p className="text-xs text-slate-500">
              Context analysis is not available.
            </p>
          </div>
        )}

        <div className="rounded-2xl border border-blue-100 bg-white p-4">
          <div>
            <p className="text-[10px] font-bold uppercase tracking-[0.12em] text-blue-500">
              Priority Queue
            </p>

            <h3 className="mt-1 text-sm font-semibold text-slate-900">
              Other active campus issues
            </h3>
          </div>

          <div className="mt-4 space-y-2">
            {optimization.ranked_issues
              .filter(
                (issue) =>
                  issue.category !==
                  topPriority.category,
              )
              .map((issue) => (
                <PriorityRow
                  key={issue.category}
                  issue={issue}
                  active={false}
                />
              ))}

            {optimization.ranked_issues.filter(
              (issue) =>
                issue.category !==
                topPriority.category,
            ).length === 0 && (
              <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-4">
                <p className="text-xs font-medium text-emerald-700">
                  No other significant issues detected.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  )
}

export default AIDecisionCenter