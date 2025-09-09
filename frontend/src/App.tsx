import { Link, NavLink, Outlet } from 'react-router-dom'
import { useEffect } from 'react'
import { api } from './lib/api'

function App() {
  useEffect(() => {
    api.get('/core/csrf/').catch(() => {})
  }, [])
  return (
    <div className="min-h-screen">
      <header className="border-b">
        <div className="mx-auto max-w-6xl px-6 py-4 flex items-center justify-between">
          <Link to="/" className="font-semibold tracking-tight">Job Scrapper</Link>
          <nav className="flex items-center gap-6 text-sm">
            <NavLink to="/sources" className={({isActive}) => isActive ? 'text-primary font-medium' : 'text-muted-foreground hover:text-foreground'}>Sources</NavLink>
            <NavLink to="/jobs" className={({isActive}) => isActive ? 'text-primary font-medium' : 'text-muted-foreground hover:text-foreground'}>Jobs</NavLink>
            <NavLink to="/applications" className={({isActive}) => isActive ? 'text-primary font-medium' : 'text-muted-foreground hover:text-foreground'}>Applications</NavLink>
            <NavLink to="/documents" className={({isActive}) => isActive ? 'text-primary font-medium' : 'text-muted-foreground hover:text-foreground'}>Documents</NavLink>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-6 py-8">
        <Outlet />
      </main>
    </div>
  )
}

export default App
