import React from 'react'
import { createRoot } from 'react-dom/client'
import { RouterProvider, createBrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'
import { ToastProvider } from '@/components/ui/toast'

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
  },
  { path: '/sources', lazy: () => import('./pages/Sources').then(m => ({ Component: m.default })) },
  { path: '/jobs', lazy: () => import('./pages/Jobs').then(m => ({ Component: m.default })) },
  { path: '/applications', lazy: () => import('./pages/Applications').then(m => ({ Component: m.default })) },
  { path: '/documents', lazy: () => import('./pages/Documents').then(m => ({ Component: m.default })) },
])

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ToastProvider>
      <RouterProvider router={router} />
    </ToastProvider>
  </React.StrictMode>,
)
