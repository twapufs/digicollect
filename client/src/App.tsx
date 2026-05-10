import { Routes, Route, Navigate } from 'react-router'
import { Loader2 } from 'lucide-react'
import { useAuth } from './context/AuthContext'
import ProtectedRoute from './components/layout/ProtectedRoute'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import AdminDashboard from './pages/admin/AdminDashboard'
import MasterCardEditorPage from './pages/admin/MasterCardEditorPage'
import CollectorDashboard from './pages/collector/CollectorDashboard'

export default function App() {
  const { isAuthenticated, user, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-base-200">
        <Loader2 className="animate-spin text-primary" size={40} />
      </div>
    )
  }

  const dashboardPath = user?.role === 'admin' ? '/admin' : '/collector'

  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route
        path="/login"
        element={isAuthenticated ? <Navigate to={dashboardPath} replace /> : <LoginPage />}
      />
      <Route
        path="/register"
        element={isAuthenticated ? <Navigate to={dashboardPath} replace /> : <RegisterPage />}
      />
      <Route element={<ProtectedRoute role="admin" />}>
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/cards/new" element={<MasterCardEditorPage />} />
        <Route path="/admin/cards/:id" element={<MasterCardEditorPage />} />
      </Route>
      <Route element={<ProtectedRoute role="collector" />}>
        <Route path="/collector" element={<CollectorDashboard />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
