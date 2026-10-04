import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import { NavLink, useLocation } from 'react-router-dom'

type Indicator = { left: number; width: number } | null

// Menu em formato de caminho; o contorno da pagina atual desliza ate o item clicado
export default function SiteNav() {
  const nav = useRef<HTMLElement>(null)
  const { pathname } = useLocation()
  const [indicator, setIndicator] = useState<Indicator>(null)
  const [ready, setReady] = useState(false)

  function measure() {
    const active = nav.current?.querySelector<HTMLElement>('a.active')
    setIndicator(active ? { left: active.offsetLeft, width: active.offsetWidth } : null)
  }

  useLayoutEffect(measure, [pathname])

  useEffect(() => {
    // so liga a transicao depois da primeira medida, para o indicador nao "voar" no carregamento
    const frame = requestAnimationFrame(() => setReady(true))
    document.fonts.ready.then(measure)
    window.addEventListener('resize', measure)
    return () => {
      cancelAnimationFrame(frame)
      window.removeEventListener('resize', measure)
    }
  }, [])

  return (
    <nav className="site-nav" ref={nav}>
      <span
        className={ready ? 'nav-indicator nav-indicator-ready' : 'nav-indicator'}
        style={
          indicator
            ? { transform: `translateX(${indicator.left}px)`, width: indicator.width }
            : { opacity: 0 }
        }
        aria-hidden="true"
      />
      <NavLink to="/" end>
        <span className="nav-prefix">~/</span>início
      </NavLink>
      <NavLink to="/projetos">
        <span className="nav-prefix">~/</span>projetos
      </NavLink>
      <NavLink to="/blog">
        <span className="nav-prefix">~/</span>blog
      </NavLink>
    </nav>
  )
}
