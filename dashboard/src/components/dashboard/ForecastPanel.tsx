import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"
import type { ForecastData } from "../../types/dashboard"

type ForecastPanelProps = {
  forecast: ForecastData
}

function ForecastPanel({
  forecast,
}: ForecastPanelProps) {
  const chartData = forecast.forecast.map(
    (point) => ({
      time: new Date(point.timestamp).toLocaleTimeString(
        [],
        {
          hour: "2-digit",
          minute: "2-digit",
        },
      ),
      predicted: point.predicted_consumption,
      lower: point.lower_bound,
      upper: point.upper_bound,
    }),
  )

  const latestPoint =
    forecast.forecast[
      forecast.forecast.length - 1
    ]

  return (
    <section className="h-full rounded-2xl border border-blue-100 bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Energy Forecast
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            AI-powered consumption prediction
          </p>
        </div>

        <div className="rounded-lg bg-blue-50 px-3 py-2 text-right">
          <p className="text-[10px] font-medium uppercase tracking-wide text-blue-500">
            Trend
          </p>

          <p
            className={`mt-0.5 text-sm font-semibold ${
              forecast.trend === "INCREASING"
                ? "text-amber-600"
                : forecast.trend === "DECREASING"
                  ? "text-emerald-600"
                  : "text-blue-600"
            }`}
          >
            {forecast.trend}
          </p>
        </div>
      </div>

      {/* Model information */}
      <div className="mt-4 flex flex-wrap items-center gap-2">
        <span className="rounded-md border border-blue-100 bg-blue-50 px-2.5 py-1 text-xs font-medium text-blue-600">
          {forecast.model}
        </span>

        <span className="rounded-md border border-slate-200 bg-slate-50 px-2.5 py-1 text-xs text-slate-500">
          {forecast.periods} forecast periods
        </span>

        <span
          className={`rounded-md px-2.5 py-1 text-xs font-medium ${
            forecast.status === "SUCCESS"
              ? "bg-emerald-50 text-emerald-600"
              : "bg-amber-50 text-amber-600"
          }`}
        >
          {forecast.status}
        </span>
      </div>

      {/* Chart */}
      <div className="mt-5 h-64">
        {chartData.length > 0 ? (
          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <LineChart
              data={chartData}
              margin={{
                top: 10,
                right: 10,
                left: -15,
                bottom: 0,
              }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="time"
                tick={{
                  fontSize: 10,
                }}
                tickLine={false}
                axisLine={false}
                minTickGap={30}
              />

              <YAxis
                tick={{
                  fontSize: 10,
                }}
                tickLine={false}
                axisLine={false}
                width={45}
              />

              <Tooltip
                contentStyle={{
                  borderRadius: "10px",
                  border: "1px solid #dbeafe",
                  boxShadow:
                    "0 4px 12px rgba(15, 23, 42, 0.08)",
                }}
                formatter={(
                  value,
                  name,
                ) => {
                  const labels: Record<
                    string,
                    string
                  > = {
                    predicted:
                      "Predicted",
                    lower:
                      "Lower Bound",
                    upper:
                      "Upper Bound",
                  }

                  return [
                    `${Number(value).toLocaleString()} kWh`,
                    labels[String(name)] ??
                      String(name),
                  ]
                }}
              />

              {/* Main prediction */}
              <Line
                type="monotone"
                dataKey="predicted"
                strokeWidth={2.5}
                dot={false}
                activeDot={{
                  r: 4,
                }}
              />

              {/* Confidence range */}
              <Line
                type="monotone"
                dataKey="upper"
                strokeWidth={1}
                strokeDasharray="4 4"
                dot={false}
              />

              <Line
                type="monotone"
                dataKey="lower"
                strokeWidth={1}
                strokeDasharray="4 4"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="flex h-full items-center justify-center rounded-xl border border-dashed border-slate-200 bg-slate-50">
            <p className="text-sm text-slate-400">
              No forecast data available
            </p>
          </div>
        )}
      </div>

      {/* Footer statistics */}
      <div className="mt-4 grid grid-cols-2 gap-3">
        <div className="rounded-xl border border-blue-100 bg-blue-50/50 p-3">
          <p className="text-[11px] text-slate-400">
            Latest prediction
          </p>

          <p className="mt-1 text-lg font-bold text-slate-900">
            {latestPoint
              ? `${latestPoint.predicted_consumption.toLocaleString()} kWh`
              : "—"}
          </p>
        </div>

        <div className="rounded-xl border border-slate-100 bg-slate-50 p-3">
          <p className="text-[11px] text-slate-400">
            Forecast range
          </p>

          <p className="mt-1 text-sm font-semibold text-slate-700">
            {latestPoint
              ? `${latestPoint.lower_bound.toLocaleString()} – ${latestPoint.upper_bound.toLocaleString()} kWh`
              : "—"}
          </p>
        </div>
      </div>
    </section>
  )
}

export default ForecastPanel