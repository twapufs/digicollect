import { Loader2, AlertCircle, Package, BookmarkPlus, Trash2 } from 'lucide-react'
import { useCollection, useCollectCard, useRemoveCollectedCard } from '../../hooks/useCollection'
import { useMasterCards } from '../../hooks/useMasterCards'
import Navbar from '../../components/layout/Navbar'
import FlipCard from '../../components/cards/FlipCard'
import type { MasterCardResponse } from '../../api/types'

export default function CollectorDashboard() {
  const { data: collection, isLoading: loadingCollection, error: collectionError } = useCollection()
  const { data: allCards, isLoading: loadingCards } = useMasterCards()
  const collectMutation = useCollectCard()
  const removeMutation = useRemoveCollectedCard()

  const collectedMasterIds = new Set(collection?.map((c) => c.master_card.id) ?? [])
  const availableCards = allCards?.filter((c) => !collectedMasterIds.has(c.id)) ?? []

  const isLoading = loadingCollection || loadingCards

  return (
    <div className="min-h-screen flex flex-col bg-base-200">
      <Navbar />

      <main className="flex-1 container mx-auto px-4 py-8 max-w-6xl space-y-12">

        {/* ── My Collection ── */}
        <section>
          <div className="mb-6">
            <h2 className="text-2xl font-extrabold">My Collection</h2>
            <p className="text-base-content/55 mt-1">
              {collection
                ? `${collection.length} card${collection.length !== 1 ? 's' : ''} owned`
                : 'Loading…'}
            </p>
          </div>

          {collectionError && (
            <div className="alert alert-error mb-4">
              <AlertCircle size={16} /> Failed to load your collection.
            </div>
          )}

          {isLoading && (
            <div className="flex justify-center py-12">
              <Loader2 className="animate-spin text-primary" size={34} />
            </div>
          )}

          {!isLoading && collection?.length === 0 && (
            <div className="flex flex-col items-center gap-3 py-14 text-base-content/35">
              <Package size={48} strokeWidth={1.5} />
              <p className="text-base">No cards yet — start collecting below!</p>
            </div>
          )}

          {collection && collection.length > 0 && (
            <div className="flex flex-wrap gap-6 justify-center">
              {collection.map((collected) => (
                <FlipCard
                  key={collected.id}
                  card={collected.master_card}
                  frontExtra={
                    <span className="text-[10px] text-base-content/45">
                      Collected {new Date(collected.collected_at).toLocaleDateString()}
                    </span>
                  }
                  actions={
                    <button
                      className="btn btn-xs btn-error w-full gap-1"
                      onClick={() => removeMutation.mutate(collected.id)}
                      disabled={removeMutation.isPending}
                    >
                      {removeMutation.isPending
                        ? <Loader2 className="animate-spin" size={11} />
                        : <Trash2 size={11} />}
                      Remove
                    </button>
                  }
                />
              ))}
            </div>
          )}
        </section>

        <div className="divider" />

        {/* ── Available Cards ── */}
        <section>
          <div className="mb-6">
            <h2 className="text-2xl font-extrabold">Available Cards</h2>
            <p className="text-base-content/55 mt-1">Cards you can still add to your collection</p>
          </div>

          {isLoading && (
            <div className="flex justify-center py-12">
              <Loader2 className="animate-spin text-primary" size={34} />
            </div>
          )}

          {!isLoading && availableCards.length === 0 && (
            <div className="flex flex-col items-center gap-3 py-14 text-base-content/35">
              <Package size={48} strokeWidth={1.5} />
              <p className="text-base">You've collected everything — check back later!</p>
            </div>
          )}

          {!isLoading && availableCards.length > 0 && (
            <div className="flex flex-wrap gap-6 justify-center">
              {availableCards.map((card) => (
                <AvailableCardTile
                  key={card.id}
                  card={card}
                  onCollect={() => collectMutation.mutate({ master_card_id: card.id })}
                  isPending={collectMutation.isPending}
                />
              ))}
            </div>
          )}
        </section>

      </main>
    </div>
  )
}

function AvailableCardTile({
  card,
  onCollect,
  isPending,
}: {
  card: MasterCardResponse
  onCollect: () => void
  isPending: boolean
}) {
  const outOfStock = card.available_quantity === 0

  return (
    <FlipCard
      card={card}
      actions={
        <button
          className={`btn btn-xs w-full gap-1 ${outOfStock ? '' : 'btn-success'}`}
          onClick={outOfStock ? undefined : onCollect}
          disabled={isPending || outOfStock}
          title={outOfStock ? 'Out of stock' : 'Add to your collection'}
        >
          {isPending
            ? <Loader2 className="animate-spin" size={11} />
            : <BookmarkPlus size={11} />}
          {outOfStock ? 'Out of stock' : 'Collect'}
        </button>
      }
    />
  )
}
