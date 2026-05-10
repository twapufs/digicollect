import { Navigate, Outlet } from 'react-router'
import { useAuth } from '../../context/AuthContext'
import type { Role } from '../../api/types'

interface Props {
  role?: Role
}

export default function ProtectedRoute({ role }: Props) {
  const { isAuthenticated, user } = useAuth()

  if (!isAuthenticated) return <Navigate to="/login" replace />
  if (role && user?.role !== role) {
    return <Navigate to={user?.role === 'admin' ? '/admin' : '/collector'} replace />
  }
  return <Outlet />
}
