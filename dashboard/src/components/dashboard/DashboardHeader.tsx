type DashboardHeaderProps = {
  facilityName: string
  buildingName: string
  location: string
  status: string
  aiOnline: boolean
  lastUpdated: string
}

function getStatusStyle(status: string) {
  switch (status.toUpperCase()) {
    case "CRITICAL":
      return "bg-red-100 text-red-700"

    case "ATTENTION":
      return "bg-amber-100 text-amber-700"

    case "WARNING":
      return "bg-yellow-100 text-yellow-700"

    case "NORMAL":
    default:
      return "bg-emerald-100 text-emerald-700"
  }
}

function DashboardHeader({
  facilityName,
  buildingName,
  location,
  status,
  aiOnline,
  lastUpdated,
}: DashboardHeaderProps) {
  return (
    <header className="flex flex-col gap-5 border-b border-blue-100 pb-5 sm:flex-row sm:items-center sm:justify-between">
      {/* Facility information */}
      <div>
        <p className="text-sm font-medium text-blue-600">
          {facilityName}
        </p>

        <h1 className="mt-1 text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
          {buildingName}
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          {location}
        </p>
      </div>

      {/* Status */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span
            className={`h-2.5 w-2.5 rounded-full ${
              aiOnline
                ? "bg-emerald-500"
                : "bg-red-500"
            }`}
          />

          <span className="text-sm font-medium text-slate-700">
            AI {aiOnline ? "Online" : "Offline"}
          </span>
        </div>

        <span
          className={`rounded-lg px-3 py-1.5 text-xs font-semibold ${getStatusStyle(
            status,
          )}`}
        >
          {status}
        </span>

        <span className="hidden text-xs text-slate-400 sm:block">
          Updated {lastUpdated}
        </span>
      </div>
    </header>
  )
}

export default DashboardHeader