import { Link, useNavigate } from 'react-router'
import { Layers, LogOut } from 'lucide-react'
import { useAuth } from '../../context/AuthContext'

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const homeHref = isAuthenticated
    ? user?.role === 'admin' ? '/admin' : '/collector'
    : '/'

  return (
    <nav className="navbar bg-base-100 border-b border-base-300 sticky top-0 z-50 px-4">
      <div className="flex-1">
        <Link to={homeHref} className="flex items-center gap-2 text-xl font-extrabold text-primary select-none">
          <Layers size={22} />
          DigiCollect
        </Link>
      </div>

      <div className="flex-none flex items-center gap-3">
        {isAuthenticated ? (
          <>
            <span className="hidden sm:inline text-sm text-base-content/60">{user?.username}</span>
            <div className={`badge badge-sm ${user?.role === 'admin' ? 'badge-error' : 'badge-info'} capitalize`}>
              {user?.role}
            </div>
            <button className="btn btn-ghost btn-sm gap-1.5" onClick={handleLogout}>
              <LogOut size={14} />
              <span className="hidden sm:inline">Logout</span>
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="btn btn-ghost btn-sm">Login</Link>
            <Link to="/register" className="btn btn-primary btn-sm">Register</Link>
          </>
        )}
      </div>
    </nav>
  )
}
