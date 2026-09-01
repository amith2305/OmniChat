export function formatTime(date) {
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

export function formatNumber(value) {
  return Number(value).toLocaleString()
}
