export type DashboardStatus =
  | "NORMAL"
  | "WARNING"
  | "ATTENTION"
  | "CRITICAL"

export type KPIData = {
  energy_kwh: number
  water_liters: number
  waste_kg: number
  vehicles: number
  parking_percent: number
  average_speed: number
}

export type OverallStatus = {
  overall_status: DashboardStatus
  energy_status: string
  water_status: string
  waste_status: string
  traffic_status: string
  energy_trend: string
}

export type AnomalyItem = {
  anomaly_score: number
  is_anomaly: boolean
  anomaly_status: string
  [key: string]: unknown
}

export type AnomalyData = {
  data: AnomalyItem | AnomalyItem[]
  count: number
  latest_status: string
  latest_score: number
}

export type AnomalyCategory = {
  data: AnomalyItem | AnomalyItem[]
  count: number
  latest_status: string
  latest_score: number
}

export type ForecastPoint = {
  timestamp: string
  predicted_consumption: number
  lower_bound: number
  upper_bound: number
}

export type ForecastData = {
  status: string
  model: string
  periods: number
  trend: string
  forecast: ForecastPoint[]
}

export type WhatIfData = {
  scenario: string
  current_consumption: number
  reduction_percent: number
  projected_consumption: number
  energy_saved: number
  estimated_cost_saving_inr: number
  estimated_co2_reduction_kg: number
  hours: number
  created_at: string
}

export type WhatIfAnalysis = {
  available: boolean
  scenario: string
  baseline_daily_kwh: number
  projected_daily_kwh: number
  energy_saved_kwh_per_day: number
  saving_percent: number
  estimated_cost_saving_inr_per_day: number
  estimated_co2_reduction_kg_per_day: number
  interpretation: string
}

export type ContextAnalysis = {
  actual_energy: number
  expected_energy: number
  deviation_percent: number
  status: string
  occupancy: number
  working_day: boolean
  temperature: number
  hvac_load: number
  hour: number
  flags: string[]
  interpretation: string
}

export type OptimizationImpact = {
  energy_saved_kwh_per_day: number
  cost_saving_inr_per_day: number
  co2_reduction_kg_per_day: number
}

export type OptimizationIssue = {
  category: string
  status: string
  deviation_percent: number
  forecast_trend: string
  priority_score: number
  priority: string
}

export type OptimizationPriority = {
  category: string
  status: string
  deviation_percent: number
  forecast_trend: string
  priority_score: number
  priority: string
  recommended_action: string
  impact: OptimizationImpact
}

export type OptimizationData = {
  decision: string
  issues: OptimizationIssue[]
  ranked_issues: OptimizationIssue[]
  top_priority: OptimizationPriority | null
}

export type DigitalTwinVisualization = {
  energy_state: string
  water_state: string
  waste_state: string
  traffic_state: string
  forecast_state: string
}

export type DigitalTwinState = {
  facility: string
  building: string
  building_id: string
  building_type: string
  status: DashboardStatus
  energy: number
  water: number
  waste: number
  vehicles: number
  parking: number
  average_speed: number
  forecast: string
  priority: string
  what_if: WhatIfData
  visualization: DigitalTwinVisualization
  optimization?: OptimizationData
}

export type FacilityData = {
  id: string
  name?: string
  facility_name?: string
  location: string
  city: string
  state: string
  country: string
  created_at: string
  updated_at: string
}

export type BuildingData = {
  id: string
  building_name?: string
  name?: string
  building_type?: string
  area_sq_m?: number
  building_code?: string
  floor_count?: number
  facility_id?: string
  created_at?: string
  updated_at?: string
  [key: string]: unknown
}

export type DashboardAnomalies = {
  energy: AnomalyCategory
  water: AnomalyCategory
  waste: AnomalyCategory
  traffic: AnomalyCategory
}

export type DashboardData = {
  status: string
  generated_at: string

  facility: FacilityData

  building: BuildingData

  building_id: string

  priority: string

  confidence: string

  current_status: OverallStatus

  kpis: KPIData

  anomalies: DashboardAnomalies

  forecast: ForecastData

  explanation: string

  /*
   * Backend returns this as a plain string.
   */
  recommendation: string

  rag: unknown

  reasoning: unknown

  recommendation_details: unknown

  what_if: WhatIfData

  what_if_analysis: WhatIfAnalysis

  context_analysis?: ContextAnalysis

  optimization?: OptimizationData

  digital_twin: DigitalTwinState
}