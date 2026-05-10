import { useRef, useState } from 'react'
import { Link } from 'react-router'
import { Plus, Loader2, AlertCircle, Package } from 'lucide-react'
import { useMasterCards, useDeleteMasterCard } from '../../hooks/useMasterCards'
import Navbar from '../../components/layout/Navbar'
import AdminCardTile from '../../components/cards/AdminCardTile'

export default function AdminDashboard() {
  const { data: cards, isLoading, error } = useMasterCards()
  const deleteMutation = useDeleteMasterCard()
  const deleteModal = useRef<HTMLDialogElement>(null)
  const [pendingDeleteId, setPendingDeleteId] = useState<string | null>(null)

  const handleDeleteClick = (id: string) => {
    setPendingDeleteId(id)
    deleteModal.current?.showModal()
  }

  const handleConfirmDelete = async () => {
    if (!pendingDeleteId) return
    await deleteMutation.mutateAsync(pendingDeleteId)
    deleteModal.current?.close()
    setPendingDeleteId(null)
  }

  return (
    <div className="min-h-screen flex flex-col bg-base-200">
      <Navbar />

      <main className="flex-1 container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-extrabold">Master Cards</h1>
            <p className="text-base-content/55 mt-1">
              {cards ? `${cards.length} card${cards.length !== 1 ? 's' : ''} in catalog` : 'Loading catalog…'}
            </p>
          </div>
          <Link to="/admin/cards/new" className="btn btn-primary gap-2">
            <Plus size={18} /> New Card
          </Link>
        </div>

        {/* Loading */}
        {isLoading && (
          <div className="flex justify-center py-24">
            <Loader2 className="animate-spin text-primary" size={38} />
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="alert alert-error">
            <AlertCircle size={18} />
            Failed to load the card catalog. Please refresh.
          </div>
        )}

        {/* Empty */}
        {!isLoading && !error && cards?.length === 0 && (
          <div className="flex flex-col items-center gap-4 py-24 text-base-content/35">
            <Package size={52} strokeWidth={1.5} />
            <p className="text-lg">No cards yet. Create your first one!</p>
            <Link to="/admin/cards/new" className="btn btn-primary btn-sm gap-1">
              <Plus size={15} /> Create Card
            </Link>
          </div>
        )}

        {/* Grid */}
        {cards && cards.length > 0 && (
          <div className="flex flex-wrap gap-6 justify-center">
            {cards.map((card) => (
              <AdminCardTile
                key={card.id}
                card={card}
                onDelete={() => handleDeleteClick(card.id)}
              />
            ))}
          </div>
        )}
      </main>

      {/* Delete confirmation modal */}
      <dialog ref={deleteModal} className="modal">
        <div className="modal-box">
          <h3 className="font-bold text-lg">Delete Card</h3>
          <p className="py-4 text-base-content/65">
            This will permanently remove the card from the catalog.
          </p>
          <div className="modal-action">
            <button
              className="btn btn-error"
              onClick={handleConfirmDelete}
              disabled={deleteMutation.isPending}
            >
              {deleteMutation.isPending ? <Loader2 className="animate-spin" size={16} /> : 'Delete'}
            </button>
            <button className="btn btn-ghost" onClick={() => deleteModal.current?.close()}>
              Cancel
            </button>
          </div>
        </div>
        <form method="dialog" className="modal-backdrop">
          <button>close</button>
        </form>
      </dialog>
    </div>
  )
}
