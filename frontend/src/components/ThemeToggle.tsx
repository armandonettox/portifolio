import { useState } from 'react'

type Theme = 'light' | 'dark'

const TRANSITION_MS = 500

function currentTheme(): Theme {
  return document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light'
}

// Botao que alterna entre tema claro e escuro e lembra a escolha
export default function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>(currentTheme)

  function toggle() {
    const next: Theme = theme === 'dark' ? 'light' : 'dark'
    const root = document.documentElement

    // a classe liga a transicao de cores so durante a troca, para nao afetar o resto do site
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      root.classList.add('theme-changing')
      window.setTimeout(() => root.classList.remove('theme-changing'), TRANSITION_MS + 100)
    }
    root.dataset.theme = next
    try {
      localStorage.setItem('theme', next)
    } catch {
      // sem localStorage o tema vale so ate recarregar a pagina
    }
    setTheme(next)
  }

  const label = theme === 'dark' ? 'Ativar tema claro' : 'Ativar tema escuro'

  return (
    <button
      type="button"
      className="theme-toggle"
      data-theme-atual={theme}
      onClick={toggle}
      aria-label={label}
      title={label}
    >
      <svg className="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" aria-hidden="true">
        <circle cx="12" cy="12" r="4" />
        <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
      </svg>
      <svg className="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" />
      </svg>
    </button>
  )
}
