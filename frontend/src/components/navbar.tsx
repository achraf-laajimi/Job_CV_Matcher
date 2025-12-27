import { useState } from 'react'

const navigation = [
  { name: 'Product', href: '#' },
  { name: 'How it Works', href: '#guide' },
  { name: 'Try Matching', href: '#matching' },
  { name: 'Company', href: '#' },
]

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="absolute inset-x-0 top-0 z-50">
      <nav
        aria-label="Global"
        className="flex items-center justify-between p-6 lg:px-8"
      >
        <div className="flex lg:flex-1">
          <a href="#" className="-m-1.5 p-1.5">
            <span className="sr-only">MatchaCV</span>
            <span className="text-xl font-bold text-purple-400">
              MatchaCV
            </span>
          </a>
        </div>

        {/* Mobile menu button */}
        <div className="flex lg:hidden">
          <button
            type="button"
            onClick={() => setMobileMenuOpen(true)}
            className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-300"
            aria-label="Open main menu"
          >
            ☰
          </button>
        </div>

        {/* Desktop navigation */}
        <div className="hidden lg:flex lg:gap-x-12">
          {navigation.map((item) => (
            <a
              key={item.name}
              href={item.href}
              className="text-sm font-semibold text-gray-200 hover:text-purple-400 transition-colors"
            >
              {item.name}
            </a>
          ))}
        </div>

        <div className="hidden lg:flex lg:flex-1 lg:justify-end">
          <a
            href="#"
            className="text-sm font-semibold text-gray-200 hover:text-purple-400 transition-colors"
          >
            Log in →
          </a>
        </div>
      </nav>

      {/* MOBILE MENU */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 bg-gray-900 p-6 lg:hidden">
          <div className="flex items-center justify-between">
            <span className="text-lg font-bold text-purple-400">
              MatchaCV
            </span>
            <button
              type="button"
              onClick={() => setMobileMenuOpen(false)}
              className="rounded-md p-2 text-gray-300"
              aria-label="Close menu"
            >
              ✕
            </button>
          </div>

          <div className="mt-6">
            <div className="space-y-4">
              {navigation.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="block text-base font-semibold text-gray-200 hover:bg-gray-800 rounded-md px-3 py-2"
                >
                  {item.name}
                </a>
              ))}
            </div>

            <div className="mt-6">
              <a
                href="#"
                className="block text-base font-semibold text-gray-200 hover:bg-gray-800 rounded-md px-3 py-2"
              >
                Log in
              </a>
            </div>
          </div>
        </div>
      )}
    </header>
  )
}