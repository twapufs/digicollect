import { useState, type FormEvent } from 'react'
import { Link } from 'react-router'
import { Layers, Loader2 } from 'lucide-react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
  const { login } = useAuth()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await login(form)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        setError('Invalid username or password.')
      } else {
        setError('Login failed. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 bg-base-200">
      <div className="card bg-base-100 shadow-xl w-full max-w-sm">
        <div className="card-body gap-5">
          <Link to="/" className="flex items-center gap-2 text-primary w-fit">
            <Layers size={26} />
            <span className="text-xl font-extrabold">DigiCollect</span>
          </Link>

          <div>
            <h2 className="text-xl font-bold">Welcome back</h2>
            <p className="text-sm text-base-content/55">Sign in to your account</p>
          </div>

          {error && (
            <div className="alert alert-error text-sm py-2.5">{error}</div>
          )}

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <label className="form-control">
              <div className="label py-1"><span className="label-text">Username</span></div>
              <input
                type="text"
                className="input input-bordered"
                value={form.username}
                onChange={(e) => setForm((f) => ({ ...f, username: e.target.value }))}
                autoFocus
                required
              />
            </label>

            <label className="form-control">
              <div className="label py-1"><span className="label-text">Password</span></div>
              <input
                type="password"
                className="input input-bordered"
                value={form.password}
                onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
                required
              />
            </label>

            <button type="submit" className="btn btn-primary mt-1" disabled={loading}>
              {loading ? <Loader2 className="animate-spin" size={18} /> : 'Login'}
            </button>
          </form>

          <p className="text-sm text-center text-base-content/55">
            Don't have an account?{' '}
            <Link to="/register" className="link link-primary font-medium">Register</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
