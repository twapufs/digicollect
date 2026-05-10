import { Link } from 'react-router'
import { Layers } from 'lucide-react'
import Navbar from '../components/layout/Navbar'
import FlipCard from '../components/cards/FlipCard'
import type { MasterCardResponse } from '../api/types'

const SAMPLE_CARDS: MasterCardResponse[] = [
  {
    id: '1',
    title: 'Shadow Dragon',
    symbol: '🐉',
    rarity: 'legendary',
    description: 'An ancient dragon woven from pure shadow. Said to eclipse entire kingdoms.',
    quantity: 5,
    available_quantity: 2,
  },
  {
    id: '2',
    title: 'Storm Phoenix',
    symbol: '🦅',
    rarity: 'epic',
    description: 'A phoenix that commands lightning and rides the eye of every storm.',
    quantity: 15,
    available_quantity: 7,
  },
  {
    id: '3',
    title: 'Crystal Golem',
    symbol: '💎',
    rarity: 'rare',
    description: 'Forged from enchanted crystal deep underground. Nearly unbreakable.',
    quantity: 40,
    available_quantity: 22,
  },
]

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-base-200">
      <Navbar />

      <main className="flex-1 flex flex-col items-center justify-center gap-20 px-4 py-16">
        {/* Hero */}
        <section className="text-center max-w-2xl">
          <div className="flex items-center justify-center gap-3 mb-6">
            <Layers size={52} className="text-primary" />
            <h1 className="text-6xl font-extrabold tracking-tight text-primary">DigiCollect</h1>
          </div>
          <p className="text-lg text-base-content/65 mb-10 leading-relaxed">
            Discover, collect, and trade digital cards spanning five tiers of rarity.
            <br />
            Every card tells a story — flip one to find out.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link to="/register" className="btn btn-primary btn-lg px-8">Start Collecting</Link>
            <Link to="/login" className="btn btn-outline btn-lg px-8">Login</Link>
          </div>
        </section>

        {/* Sample Cards (interactive preview) */}
        <section className="flex flex-wrap gap-8 justify-center items-center">
          {SAMPLE_CARDS.map((card) => (
            <FlipCard key={card.id} card={card} />
          ))}
        </section>

        {/* Feature tiles */}
        <section className="grid grid-cols-1 sm:grid-cols-3 gap-5 max-w-3xl w-full text-center">
          {[
            { title: 'Five Rarities', desc: 'Common, Uncommon, Rare, Epic, and Legendary — each with unique glows and colors.' },
            { title: 'Live Collection', desc: 'Track every card you own and browse what\'s still available to grab.' },
            { title: 'Admin Catalog', desc: 'Create and manage the master catalog with a full card editor.' },
          ].map(({ title, desc }) => (
            <div key={title} className="card bg-base-100 p-5 shadow">
              <h3 className="font-bold mb-2">{title}</h3>
              <p className="text-sm text-base-content/60">{desc}</p>
            </div>
          ))}
        </section>
      </main>

      <footer className="text-center py-6 text-xs text-base-content/40">
        © {new Date().getFullYear()} DigiCollect
      </footer>
    </div>
  )
}
