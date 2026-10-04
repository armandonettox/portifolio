import { useEffect, useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { api, type PostSummary } from '../api'
import TagList from '../components/TagList'
import { formatDate } from '../format'
import './Posts.css'

const MONTHS = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

export default function Posts() {
  // comeca na hora com a ultima versao guardada neste navegador, se houver
  const [posts, setPosts] = useState<PostSummary[]>(() => api.postsCached() ?? [])
  const [failed, setFailed] = useState(false)
  const [params, setParams] = useSearchParams()

  useEffect(() => {
    api
      .posts()
      .then(setPosts)
      .catch(() => setFailed(true))
  }, [])

  const year = params.get('ano') ?? ''
  const month = params.get('mes') ?? ''

  // anos com a quantidade de posts, do mais novo para o mais antigo
  const years = useMemo(() => {
    const count = new Map<string, number>()
    posts.forEach((p) => count.set(p.date.slice(0, 4), (count.get(p.date.slice(0, 4)) ?? 0) + 1))
    return [...count.entries()].sort((a, b) => b[0].localeCompare(a[0]))
  }, [posts])

  // meses do ano escolhido, com a quantidade de posts de cada um
  const months = useMemo(() => {
    const count = new Map<string, number>()
    posts
      .filter((p) => p.date.startsWith(year))
      .forEach((p) => count.set(p.date.slice(5, 7), (count.get(p.date.slice(5, 7)) ?? 0) + 1))
    return [...count.entries()].sort((a, b) => a[0].localeCompare(b[0]))
  }, [posts, year])

  const visible = posts.filter(
    (p) => (!year || p.date.startsWith(year)) && (!month || p.date.slice(5, 7) === month),
  )

  function choose(nextYear: string, nextMonth = '') {
    const next: [string, string][] = []
    if (nextYear) next.push(['ano', nextYear])
    if (nextMonth) next.push(['mes', nextMonth])
    setParams(next, { replace: true })
  }

  return (
    <>
      <h1 className="sr-only">Blog</h1>

      {failed && posts.length === 0 && (
        <p className="meta">Não consegui carregar os posts agora. Tente de novo em instantes.</p>
      )}

      {years.length > 0 && (
        <nav className="timeline" aria-label="Filtrar posts por data">
          <ul className="timeline-row">
            <li>
              <button type="button" className="timeline-chip" aria-pressed={!year} onClick={() => choose('')}>
                Todos <span className="timeline-count">{posts.length}</span>
              </button>
            </li>
            {years.map(([y, n]) => (
              <li key={y}>
                <button
                  type="button"
                  className="timeline-chip"
                  aria-pressed={year === y}
                  onClick={() => choose(year === y ? '' : y)}
                >
                  {y} <span className="timeline-count">{n}</span>
                </button>
              </li>
            ))}
          </ul>

          {year && (
            <ul className="timeline-row timeline-months">
              {months.map(([m, n]) => (
                <li key={m}>
                  <button
                    type="button"
                    className="timeline-chip"
                    aria-pressed={month === m}
                    onClick={() => choose(year, month === m ? '' : m)}
                  >
                    {MONTHS[Number(m) - 1]} <span className="timeline-count">{n}</span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </nav>
      )}

      <ol className="entry-list">
        {visible.map((p) => (
          <li key={p.slug}>
            <Link className="entry" to={`/blog/${p.slug}`}>
              <time className="entry-meta" dateTime={p.date}>
                {formatDate(p.date)}
              </time>
              <div>
                <h2 className="entry-title">
                  {p.title}
                  <span className="entry-arrow" aria-hidden="true">
                    →
                  </span>
                </h2>
                <p className="entry-summary">{p.summary}</p>
                <TagList tags={p.tags ?? []} />
              </div>
            </Link>
          </li>
        ))}
      </ol>
    </>
  )
}
