import { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { api, type Project } from '../api'
import TagList from '../components/TagList'
import { formatDate } from '../format'
import './Projects.css'

type Sort = 'updated' | 'name' | 'stars'
type Period = 'any' | 'month' | 'half' | 'year'

const SORT_LABELS: Record<Sort, string> = {
  updated: 'Atualização',
  name: 'Nome',
  stars: 'Estrelas',
}

const PERIOD_LABELS: Record<Period, string> = {
  any: 'Data',
  month: 'Último mês',
  half: 'Últimos 6 meses',
  year: 'Último ano',
}

const PERIOD_DAYS: Record<Exclude<Period, 'any'>, number> = { month: 30, half: 183, year: 365 }

// busca sem diferenciar maiusculas nem acentos
function normalize(text: string): string {
  return text
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
}

function isSort(value: string | null): value is Sort {
  return value === 'updated' || value === 'name' || value === 'stars'
}

function isPeriod(value: string | null): value is Period {
  return value === 'any' || value === 'month' || value === 'half' || value === 'year'
}

export default function Projects() {
  // comeca na hora com a ultima versao guardada neste navegador, se houver
  const [projects, setProjects] = useState<Project[]>(() => api.projectsCached() ?? [])
  const [failed, setFailed] = useState(false)
  const [loaded, setLoaded] = useState(() => api.projectsCached() !== null)
  const [params, setParams] = useSearchParams()
  // guarda o instante da abertura da pagina para o filtro de periodo nao mudar a cada render
  const [now] = useState(() => Date.now())

  const query = params.get('q') ?? ''
  const language = params.get('lang') ?? ''
  const sortParam = params.get('sort')
  const periodParam = params.get('periodo')
  const sort: Sort = isSort(sortParam) ? sortParam : 'updated'
  const period: Period = isPeriod(periodParam) ? periodParam : 'any'

  useEffect(() => {
    api
      .projects()
      .then((list) => {
        setProjects(list)
        setLoaded(true)
      })
      .catch(() => setFailed(true))
  }, [])

  // os filtros vao para a URL, entao a busca pode ser compartilhada e sobrevive ao recarregar
  function setParam(key: string, value: string, fallback = '') {
    setParams(
      (current) => {
        const kept = [...current].filter(([name]) => name !== key)
        return value === fallback ? kept : [...kept, [key, value]]
      },
      { replace: true },
    )
  }

  const languages = useMemo(
    () => [...new Set(projects.map((p) => p.language).filter((l): l is string => !!l))].sort(),
    [projects],
  )

  const visible = useMemo(() => {
    // cada palavra digitada precisa aparecer no nome ou na descricao, em qualquer ordem
    const terms = normalize(query).split(/\s+/).filter(Boolean)
    const limit = period === 'any' ? 0 : now - PERIOD_DAYS[period] * 86_400_000

    const filtered = projects.filter((p) => {
      if (language && p.language !== language) return false
      if (limit && (!p.pushed_at || new Date(p.pushed_at).getTime() < limit)) return false
      const text = normalize(`${p.name} ${p.description ?? ''}`)
      return terms.every((term) => text.includes(term))
    })

    return filtered.sort((a, b) => {
      if (sort === 'name') return a.name.localeCompare(b.name, 'pt-BR')
      if (sort === 'stars') return b.stars - a.stars || a.name.localeCompare(b.name, 'pt-BR')
      return (b.pushed_at ?? '').localeCompare(a.pushed_at ?? '')
    })
  }, [projects, query, language, period, sort, now])

  const hasFilter = query !== '' || language !== '' || period !== 'any' || sort !== 'updated'

  return (
    <>
      <h1 className="sr-only">Projetos</h1>

      <form className="finder" role="search" onSubmit={(e) => e.preventDefault()}>
        <label className="finder-search">
          <span className="sr-only">Buscar projeto</span>
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            aria-hidden="true"
          >
            <circle cx="11" cy="11" r="7" />
            <path d="m20 20-3.5-3.5" />
          </svg>
          <input
            type="search"
            value={query}
            onChange={(e) => setParam('q', e.target.value)}
            placeholder="Buscar projeto..."
            autoComplete="off"
          />
        </label>

        <label className="finder-select">
          <span className="sr-only">Linguagem</span>
          <select value={language} onChange={(e) => setParam('lang', e.target.value)}>
            <option value="">Linguagem</option>
            {languages.map((l) => (
              <option key={l} value={l}>
                {l}
              </option>
            ))}
          </select>
        </label>

        <label className="finder-select">
          <span className="sr-only">Período da última atualização</span>
          <select value={period} onChange={(e) => setParam('periodo', e.target.value, 'any')}>
            {Object.entries(PERIOD_LABELS).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>

        <label className="finder-select">
          <span className="sr-only">Ordenar por</span>
          <select value={sort} onChange={(e) => setParam('sort', e.target.value, 'updated')}>
            {Object.entries(SORT_LABELS).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>
      </form>

      <p className="finder-status" aria-live="polite">
        <span>
          {loaded ? `${visible.length} ${visible.length === 1 ? 'projeto' : 'projetos'}` : null}
        </span>
        {hasFilter && (
          <button type="button" className="finder-clear" onClick={() => setParams([], { replace: true })}>
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.2"
              strokeLinecap="round"
              aria-hidden="true"
            >
              <path d="M6 6l12 12M18 6 6 18" />
            </svg>
            limpar filtros
          </button>
        )}
      </p>

      {failed && projects.length === 0 && (
        <p className="meta">Não consegui buscar os projetos no GitHub agora. Tente de novo em instantes.</p>
      )}

      {!failed && projects.length > 0 && visible.length === 0 && (
        <p className="meta">Nenhum projeto encontrado com esses filtros.</p>
      )}

      <ol className="entry-list">
        {visible.map((p, i) => (
          <li key={p.name}>
            <a
              className="entry"
              href={p.url}
              target="_blank"
              rel="noopener"
              aria-label={`${p.name} (abre o repositório em nova aba)`}
            >
              <span className="entry-meta">{String(i + 1).padStart(2, '0')}</span>
              <div>
                <h2 className="entry-title">
                  {p.name}
                  <span className="entry-arrow" aria-hidden="true">
                    ↗
                  </span>
                </h2>
                {p.description && <p className="entry-summary">{p.description}</p>}
                <TagList tags={p.language ? [p.language] : []} />
                <p className="entry-footer">
                  <span title="Estrelas no GitHub">★ {p.stars}</span>
                  {p.pushed_at && <span>atualizado em {formatDate(p.pushed_at)}</span>}
                </p>
              </div>
            </a>
          </li>
        ))}
      </ol>
    </>
  )
}
