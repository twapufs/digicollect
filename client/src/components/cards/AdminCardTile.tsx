import { Link } from 'react-router'
import { Pencil, Trash2 } from 'lucide-react'
import type { MasterCardResponse } from '../../api/types'
import FlipCard from './FlipCard'

interface Props {
  card: MasterCardResponse
  onDelete: () => void
}

export default function AdminCardTile({ card, onDelete }: Props) {
  return (
    <FlipCard
      card={card}
      actions={
        <>
          <Link
            to={`/admin/cards/${card.id}`}
            className="btn btn-xs btn-info flex-1 gap-1"
          >
            <Pencil size={11} /> Edit
          </Link>
          <button
            className="btn btn-xs btn-error flex-1 gap-1"
            onClick={onDelete}
          >
            <Trash2 size={11} /> Delete
          </button>
        </>
      }
    />
  )
}
