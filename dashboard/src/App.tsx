
import { useEffect, useState } from "react"

import DashboardHeader from "./components/dashboard/DashboardHeader"
import KPIGrid from "./components/dashboard/KPIGrid"
import AlertCenter from "./components/dashboard/AlertCenter"
import ForecastPanel from "./components/dashboard/ForecastPanel"
import AIInsightPanel from "./components/dashboard/AIInsightPanel"
import DigitalTwinPanel from "./components/dashboard/DigitalTwinPanel"
import AIRecommendations from "./components/dashboard/AIRecommendations"
import WhatIfAnalysis from "./components/dashboard/WhatIfAnalysis"
import AIDecisionCenter from "./components/dashboard/AIDecisionCenter"

import { getDashboardData } from "./api/dashboardApi"
import type { DashboardData } from "./types/dashboard"

function App() {
  const [dashboardData, setDashboardData] =
    useState<DashboardData | null>(null)

  const [loading, setLoading] = useState(true)
  const [isOptimizing, setIsOptimizing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function loadDashboard(
    showLoading = true,
  ) {
    try {
      if (showLoading) {
        setLoading(true)
      }

      setError(null)

      const data = await getDashboardData()

      console.log(
        "Campus360 dashboard data:",
        data,
      )

      setDashboardData(data)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load dashboard data",
      )
    } finally {
      if (showLoading) {
        setLoading(false)
      }
    }
  }

  async function handleOptimize() {
    try {
      setIsOptimizing(true)
      setError(null)

      await loadDashboard(false)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to optimize campus",
      )
    } finally {
      setIsOptimizing(false)
    }
  }

  useEffect(() => {
    loadDashboard()
  }, [])

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="rounded-2xl border border-blue-100 bg-white px-8 py-6 text-center shadow-sm">
          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-blue-100 border-t-blue-600" />

          <p className="mt-4 text-sm font-medium text-slate-700">
            Loading Campus360 AI dashboard...
          </p>

          <p className="mt-1 text-xs text-slate-400">
            Connecting to the facility intelligence service
          </p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4">
        <div className="max-w-md rounded-2xl border border-red-100 bg-white p-6 text-center shadow-sm">
          <div className="text-3xl">
            ⚠️
          </div>

          <h1 className="mt-3 text-lg font-semibold text-slate-900">
            Unable to load dashboard
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            {error}
          </p>

          <p className="mt-4 text-xs text-slate-400">
            Make sure the FastAPI backend is running on port 8000.
          </p>
        </div>
      </div>
    )
  }

  if (!dashboardData) {
    return null
  }

  /*
   * ------------------------------------------------------------------------
   * Optimization Decision Source of Truth
   * ------------------------------------------------------------------------
   *
   * The existing dashboard status is generated from the original
   * telemetry pipeline. The optimization layer adds context-aware
   * decision information on top of that.
   *
   * When an optimization decision exists, use its top priority to
   * synchronize the facility-facing AI panels.
   *
   * This prevents the dashboard from showing:
   *
   *   Header      -> NORMAL
   *   AI Insight  -> NORMAL / LOW
   *   Decision    -> CRITICAL / P1
   *
   * at the same time.
   */

  const topPriority =
    dashboardData.optimization?.top_priority

  const effectiveCurrentStatus = topPriority
    ? {
        ...dashboardData.current_status,
        overall_status:
          topPriority.status as typeof dashboardData.current_status.overall_status,
        energy_status:
          topPriority.category === "ENERGY"
            ? topPriority.status
            : dashboardData.current_status.energy_status,
      }
    : dashboardData.current_status

  const effectivePriority =
    topPriority?.priority ??
    dashboardData.priority

  const effectiveExplanation =
    dashboardData.context_analysis?.interpretation ??
    dashboardData.explanation

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-[1600px] px-4 py-6 sm:px-6 lg:px-8">
        <DashboardHeader
          facilityName="Parishar360"
          buildingName={
            dashboardData.building.building_name ??
            dashboardData.building.name ??
            "Campus Building"
          }
          location={`${dashboardData.facility.city}, ${dashboardData.facility.state}`}
          status={
            effectiveCurrentStatus.overall_status
          }
          aiOnline={true}
          lastUpdated={
            dashboardData.generated_at
          }
        />

        <main className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-12">
          {/* ---------------------------------------------------------------- */}
          {/* KPI + Forecast                                                    */}
          {/* ---------------------------------------------------------------- */}

          <div className="lg:col-span-5">
            <KPIGrid
              kpis={dashboardData.kpis}
            />
          </div>

          <div className="lg:col-span-7">
            <ForecastPanel
              forecast={dashboardData.forecast}
            />
          </div>

          {/* ---------------------------------------------------------------- */}
          {/* AI Decision Center                                                */}
          {/* ---------------------------------------------------------------- */}

          <div className="lg:col-span-12">
            <AIDecisionCenter
              contextAnalysis={
                dashboardData.context_analysis
              }
              optimization={
                dashboardData.optimization
              }
              onOptimize={handleOptimize}
              isOptimizing={isOptimizing}
            />
          </div>

          {/* ---------------------------------------------------------------- */}
          {/* Existing AI intelligence panels                                  */}
          {/* ---------------------------------------------------------------- */}

          <div className="lg:col-span-4">
            <AlertCenter
              anomalies={
                dashboardData.anomalies
              }
              currentStatus={
                effectiveCurrentStatus
              }
              optimization={
                dashboardData.optimization
              }
            />
          </div>

          <div className="lg:col-span-3">
            <AIInsightPanel
              currentStatus={
                effectiveCurrentStatus
              }
              confidence={
                dashboardData.confidence
              }
              priority={
                effectivePriority
              }
              explanation={
                effectiveExplanation
              }
              forecast={
                dashboardData.forecast
              }
            />
          </div>

          <div className="lg:col-span-5">
            <DigitalTwinPanel
              digitalTwin={
                dashboardData.digital_twin
              }
            />
          </div>

          <div className="lg:col-span-7">
            <AIRecommendations
              recommendation={
                topPriority?.recommended_action ??
                dashboardData.recommendation
              }
              priority={
                effectivePriority
              }
            />
          </div>

          <div className="lg:col-span-5">
            <WhatIfAnalysis
              whatIf={
                dashboardData.what_if
              }
              analysis={
                dashboardData.what_if_analysis
              }
            />
          </div>
        </main>
      </div>
    </div>
  )
}

export default App
