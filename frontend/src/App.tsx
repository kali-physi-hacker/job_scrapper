import { useEffect, useState } from 'react'

type Health = { ok: boolean } | null

function App() {
  const [health, setHealth] = useState<Health>(null)

  useEffect(() => {
    // Placeholder ping; replace with backend health endpoint when available
    setHealth({ ok: true })
  }, [])

  return (
    <div style={{ padding: 24, fontFamily: 'system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif' }}>
      <h1>Job Scrapper</h1>
      <p>Deep job search and auto-application platform.</p>
      <div>
        <strong>Backend:</strong> {health ? (health.ok ? 'OK' : 'Down') : '…'}
      </div>
      <ul>
        <li>View sources and configure adapters</li>
        <li>Review matched jobs and tailored docs</li>
        <li>Queue and monitor applications</li>
      </ul>
    </div>
  )
}

export default App

