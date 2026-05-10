import { useState, useEffect, type FormEvent, type ChangeEvent } from 'react'
import { useParams, useNavigate, Link } from 'react-router'
import { ChevronLeft, Loader2, AlertCircle } from 'lucide-react'
import { useMasterCard, useCreateMasterCard, useUpdateMasterCard } from '../../hooks/useMasterCards'
import Navbar from '../../components/layout/Navbar'
import FlipCard from '../../components/cards/FlipCard'
import type { Rarity, MasterCardResponse } from '../../api/types'

const RARITIES: Rarity[] = ['common', 'uncommon', 'rare', 'epic', 'legendary']

interface FormState {
  title: string
  symbol: string
  rarity: Rarity
  description: string
  quantity: string
}

const EMPTY_FORM: FormState = {
  title: '',
  symbol: '★',
  rarity: 'common',
  description: '',
  quantity: '1',
}

export default function MasterCardEditorPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const isEditMode = !!id

  const { data: existing, isLoading: loadingCard } = useMasterCard(id ?? '')
  const createMutation = useCreateMasterCard()
  const updateMutation = useUpdateMasterCard(id ?? '')

  const [form, setForm] = useState<FormState>(EMPTY_FORM)
  const [submitError, setSubmitError] = useState<string | null>(null)

  useEffect(() => {
    if (existing) {
      setForm({
        title: existing.title,
        symbol: existing.symbol,
        rarity: existing.rarity,
        description: existing.description,
        quantity: String(existing.quantity),
      })
    }
  }, [existing])

  const field =
    (key: keyof FormState) =>
    (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) =>
      setForm((f) => ({ ...f, [key]: e.target.value }))

  const isPending = createMutation.isPending || updateMutation.isPending

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setSubmitError(null)
    const payload = {
      title: form.title.trim(),
      symbol: form.symbol.trim() || '★',
      rarity: form.rarity,
      description: form.description.trim(),
      quantity: Math.max(1, parseInt(form.quantity, 10) || 1),
    }
    try {
      if (isEditMode) {
        await updateMutation.mutateAsync(payload)
      } else {
        await createMutation.mutateAsync(payload)
      }
      navigate('/admin')
    } catch {
      setSubmitError('Failed to save card. Please try again.')
    }
  }

  if (isEditMode && loadingCard) {
    return (
      <div className="min-h-screen flex flex-col bg-base-200">
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <Loader2 className="animate-spin text-primary" size={40} />
        </div>
      </div>
    )
  }

  const previewCard: MasterCardResponse = {
    id: 'preview',
    title: form.title || 'Card Title',
    symbol: form.symbol || '★',
    rarity: form.rarity,
    description: form.description || 'Description will appear here.',
    quantity: parseInt(form.quantity, 10) || 1,
    available_quantity: parseInt(form.quantity, 10) || 1,
  }

  return (
    <div className="min-h-screen flex flex-col bg-base-200">
      <Navbar />

      <main className="flex-1 container mx-auto px-4 py-8 max-w-3xl">
        <div className="mb-6">
          <Link to="/admin" className="btn btn-ghost btn-sm gap-1 -ml-2 mb-3">
            <ChevronLeft size={16} /> Back
          </Link>
          <h1 className="text-3xl font-extrabold">
            {isEditMode ? 'Edit Card' : 'New Card'}
          </h1>
        </div>

        <div className="flex gap-10 items-start flex-wrap">
          {/* Live preview */}
          <div className="flex flex-col items-center gap-3">
            <p className="text-xs text-base-content/45 uppercase tracking-widest">Preview</p>
            <FlipCard card={previewCard} />
            <p className="text-xs text-base-content/40">Click to flip</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="flex-1 min-w-[260px] flex flex-col gap-4">
            {submitError && (
              <div className="alert alert-error text-sm py-2.5">
                <AlertCircle size={16} /> {submitError}
              </div>
            )}

            <fieldset className="fieldset">
              <legend className="fieldset-legend">Title</legend>
              <input
                className="input input-bordered w-full"
                value={form.title}
                onChange={field('title')}
                placeholder="Card name"
                maxLength={80}
                required
              />
            </fieldset>

            <fieldset className="fieldset">
              <legend className="fieldset-legend">Symbol</legend>
              <input
                className="input input-bordered w-full"
                value={form.symbol}
                onChange={field('symbol')}
                placeholder="★"
                maxLength={4}
                required
              />
              <p className="fieldset-label">Unicode character or emoji</p>
            </fieldset>

            <fieldset className="fieldset">
              <legend className="fieldset-legend">Rarity</legend>
              <select className="select select-bordered w-full capitalize" value={form.rarity} onChange={field('rarity')}>
                {RARITIES.map((r) => (
                  <option key={r} value={r} className="capitalize">{r}</option>
                ))}
              </select>
            </fieldset>

            <fieldset className="fieldset">
              <legend className="fieldset-legend">Description</legend>
              <textarea
                className="textarea textarea-bordered resize-none w-full"
                rows={4}
                value={form.description}
                onChange={field('description')}
                placeholder="Describe this card…"
                required
              />
            </fieldset>

            <fieldset className="fieldset">
              <legend className="fieldset-legend">Quantity</legend>
              <input
                type="number"
                className="input input-bordered w-full"
                value={form.quantity}
                onChange={field('quantity')}
                min={1}
                required
              />
            </fieldset>

            <div className="flex gap-3 mt-2">
              <button type="submit" className="btn btn-primary flex-1" disabled={isPending}>
                {isPending
                  ? <Loader2 className="animate-spin" size={18} />
                  : isEditMode ? 'Save Changes' : 'Create Card'}
              </button>
              <Link to="/admin" className="btn btn-ghost">Cancel</Link>
            </div>
          </form>
        </div>
      </main>
    </div>
  )
}
