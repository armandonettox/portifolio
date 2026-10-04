import { useEffect, useRef } from 'react'
import { api } from '../api'

const GISCUS_ORIGIN = 'https://giscus.app'

function currentTheme(): 'light' | 'dark' {
  return document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light'
}

// Comentarios do post: o giscus mostra e grava na propria discussao do GitHub, entao
// quem comenta aqui aparece no GitHub e vice-versa
export default function Comments({ number }: { number: number }) {
  const box = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const container = box.current
    if (!container) return
    let cancelled = false

    api
      .blogConfig()
      .then((cfg) => {
        if (cancelled) return
        const script = document.createElement('script')
        script.src = `${GISCUS_ORIGIN}/client.js`
        script.async = true
        script.crossOrigin = 'anonymous'
        const attrs: Record<string, string> = {
          'data-repo': cfg.repo,
          'data-repo-id': cfg.repo_id,
          'data-category': cfg.category,
          'data-category-id': cfg.category_id,
          'data-mapping': 'number',
          'data-term': String(number),
          'data-strict': '0',
          'data-reactions-enabled': '1',
          'data-emit-metadata': '0',
          'data-input-position': 'top',
          'data-theme': currentTheme(),
          'data-lang': 'pt',
          'data-loading': 'lazy',
        }
        Object.entries(attrs).forEach(([key, value]) => script.setAttribute(key, value))
        container.replaceChildren(script)
      })
      .catch(console.error)

    // quando o visitante troca o tema do site, o widget acompanha
    const observer = new MutationObserver(() => {
      const frame = container.querySelector<HTMLIFrameElement>('iframe.giscus-frame')
      frame?.contentWindow?.postMessage(
        { giscus: { setConfig: { theme: currentTheme() } } },
        GISCUS_ORIGIN,
      )
    })
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] })

    return () => {
      cancelled = true
      observer.disconnect()
      container.replaceChildren()
    }
  }, [number])

  return (
    <section className="comments" aria-label="Comentários">
      <h2 className="comments-title">Comentários</h2>
      <p className="meta">Para comentar, entre com a sua conta do GitHub.</p>
      <div ref={box} />
    </section>
  )
}
