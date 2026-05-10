import { useState, type ReactNode } from 'react'
import type { MasterCardResponse } from '../../api/types'

const RARITY = {
  common: {
    border: 'border-base-300',
    bg: 'bg-base-200',
    badge: 'badge-neutral',
    symbol: 'text-base-content/70',
    heading: 'text-base-content',
    shadow: 'shadow-md',
  },
  uncommon: {
    border: 'border-success/50',
    bg: 'bg-success/10',
    badge: 'badge-success',
    symbol: 'text-success',
    heading: 'text-success',
    shadow: 'shadow-[0_0_20px_2px_color-mix(in_srgb,oklch(var(--color-success))_20%,transparent)]',
  },
  rare: {
    border: 'border-info/50',
    bg: 'bg-info/10',
    badge: 'badge-info',
    symbol: 'text-info',
    heading: 'text-info',
    shadow: 'shadow-[0_0_20px_2px_color-mix(in_srgb,oklch(var(--color-info))_20%,transparent)]',
  },
  epic: {
    border: 'border-secondary/50',
    bg: 'bg-secondary/10',
    badge: 'badge-secondary',
    symbol: 'text-secondary',
    heading: 'text-secondary',
    shadow: 'shadow-[0_0_20px_2px_color-mix(in_srgb,oklch(var(--color-secondary))_20%,transparent)]',
  },
  legendary: {
    border: 'border-warning/50',
    bg: 'bg-warning/10',
    badge: 'badge-warning',
    symbol: 'text-warning',
    heading: 'text-warning',
    shadow: 'shadow-[0_0_24px_4px_color-mix(in_srgb,oklch(var(--color-warning))_25%,transparent)]',
  },
} as const

interface FlipCardProps {
  card: MasterCardResponse
  actions?: ReactNode
  frontExtra?: ReactNode
}

export default function FlipCard({ card, actions, frontExtra }: FlipCardProps) {
  const [flipped, setFlipped] = useState(false)
  const s = RARITY[card.rarity]

  return (
    <div
      className="flip-card w-48 h-72 cursor-pointer select-none shrink-0"
      onClick={() => setFlipped((f) => !f)}
      title="Click to flip"
    >
      <div className={`flip-card-inner ${flipped ? 'flipped' : ''}`}>

        {/* Front */}
        <div className={`flip-card-front rounded-2xl overflow-hidden border-2 ${s.border} ${s.bg} ${s.shadow} flex flex-col items-center p-3`}>
          <div className="flex w-full justify-between items-center mb-1">
            <span className={`badge badge-xs ${s.badge} capitalize`}>{card.rarity}</span>
            <span className="text-[10px] text-base-content/40 font-mono tabular-nums">
              {card.available_quantity}/{card.quantity}
            </span>
          </div>
          <div className={`text-7xl leading-none my-auto py-3 ${s.symbol}`}>
            {card.symbol}
          </div>
          <div className="w-full mt-auto space-y-1">
            <div className={`font-bold text-sm text-center leading-tight line-clamp-2 ${s.heading}`}>
              {card.title}
            </div>
            {frontExtra && (
              <div className="text-center">{frontExtra}</div>
            )}
          </div>
        </div>

        {/* Back */}
        <div className={`flip-card-back rounded-2xl overflow-hidden border-2 ${s.border} ${s.bg} ${s.shadow} flex flex-col p-3 gap-2`}>
          <div className={`font-bold text-sm line-clamp-1 ${s.heading}`}>{card.title}</div>
          <p className="text-xs text-base-content/75 leading-relaxed line-clamp-5 flex-1">
            {card.description}
          </p>
          <div className="flex justify-between text-[10px] text-base-content/50 border-t border-base-300 pt-1.5">
            <span>Total: {card.quantity}</span>
            <span>Available: {card.available_quantity}</span>
          </div>
          {actions && (
            <div
              className="flex gap-1.5 flex-wrap"
              onClick={(e) => e.stopPropagation()}
            >
              {actions}
            </div>
          )}
        </div>

      </div>
    </div>
  )
}
