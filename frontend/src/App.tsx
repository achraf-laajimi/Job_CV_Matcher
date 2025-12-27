import { useState } from 'react'

import './App.css'
import MatchaCVLanding from './components/launding_page'
import GuidePage from './components/GuidePage'
import MatchingPage from './components/MatchingPage'

function App() {
  const [currentPage, setCurrentPage] = useState<'landing' | 'guide' | 'matching'>('landing')

  // Simple routing based on hash
  window.addEventListener('hashchange', () => {
    const hash = window.location.hash
    if (hash === '#guide') {
      setCurrentPage('guide')
    } else if (hash === '#matching') {
      setCurrentPage('matching')
    } else {
      setCurrentPage('landing')
    }
  })

  // Check initial hash
  const hash = window.location.hash
  if (hash === '#guide' && currentPage === 'landing') {
    setCurrentPage('guide')
  } else if (hash === '#matching' && currentPage === 'landing') {
    setCurrentPage('matching')
  }

  return (
    <>
      {currentPage === 'landing' ? (
        <MatchaCVLanding onNavigateToGuide={() => setCurrentPage('guide')} />
      ) : currentPage === 'guide' ? (
        <GuidePage />
      ) : (
        <MatchingPage />
      )}
    </>
  )
}

export default App
