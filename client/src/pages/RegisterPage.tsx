import { useState, type FormEvent } from 'react'
import { Link } from 'react-router'
import { Layers, Loader2 } from 'lucide-react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'
import type { Role } from '../api/types'

export default function RegisterPage() {
  const { register, login } = useAuth()
  const [form, setForm] = useState({
    username: '',
    password: '',
    role: 'collector' as Role,
    admin_key: '',
  })
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await register({
        username: form.username,
        password: form.password,
        role: form.role,
        admin_key: form.role === 'admin' && form.admin_key ? form.admin_key : undefined,
      })
      await login({ username: form.username, password: form.password })
    } catch (err) {
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail
        setError(
          typeof detail === 'string'
            ? detail
            : 'Registration failed. Username may be taken or admin key is invalid.',
        )
      } else {
        setError('Registration failed. Please try again.')
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
            <h2 className="text-xl font-bold">Create account</h2>
            <p className="text-sm text-base-content/55">Start building your collection</p>
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

            <label className="form-control">
              <div className="label py-1"><span className="label-text">Role</span></div>
              <select
                className="select select-bordered"
                value={form.role}
                onChange={(e) => setForm((f) => ({ ...f, role: e.target.value as Role }))}
              >
                <option value="collector">Collector</option>
                <option value="admin">Admin</option>
              </select>
            </label>

            {form.role === 'admin' && (
              <label className="form-control">
                <div className="label py-1">
                  <span className="label-text">Admin Key</span>
                </div>
                <input
                  type="password"
                  className="input input-bordered"
                  value={form.admin_key}
                  onChange={(e) => setForm((f) => ({ ...f, admin_key: e.target.value }))}
                  placeholder="Required to create admin account"
                  required
                />
              </label>
            )}

            <button type="submit" className="btn btn-primary mt-1" disabled={loading}>
              {loading ? <Loader2 className="animate-spin" size={18} /> : 'Create Account'}
            </button>
          </form>

          <p className="text-sm text-center text-base-content/55">
            Already have an account?{' '}
            <Link to="/login" className="link link-primary font-medium">Login</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
