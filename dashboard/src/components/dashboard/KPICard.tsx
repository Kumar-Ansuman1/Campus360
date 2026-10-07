type KPICardProps = {
  title: string
  value: string | number
  unit: string
  icon: string
}

function KPICard({
  title,
  value,
  unit,
  icon,
}: KPICardProps) {
  return (
    <div className="rounded-xl border border-blue-100 bg-white p-4 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">

      <div className="flex items-center justify-between">
        <p className="text-xs font-medium text-slate-500">
          {title}
        </p>

        <span className="text-lg">
          {icon}
        </span>
      </div>

      <div className="mt-3">
        <span className="text-2xl font-bold text-slate-900">
          {value.toLocaleString()}
        </span>

        <span className="ml-1.5 text-xs text-slate-500">
          {unit}
        </span>
      </div>

    </div>
  )
}

export default KPICard