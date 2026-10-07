const API_BASE_URL = "http://127.0.0.1:8000"

export async function getDashboardData() {
  const response = await fetch(`${API_BASE_URL}/api/ai/dashboard`)

  if (!response.ok) {
    throw new Error(`Dashboard API failed: ${response.status}`)
  }

  const result = await response.json()

  if (result.status !== "success") {
    throw new Error(result.message || "Failed to load dashboard data")
  }

  return result.data
}