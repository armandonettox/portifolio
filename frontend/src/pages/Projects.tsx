import { useEffect, useState } from 'react'
import { api, type Project } from '../api'
import TagList from '../components/TagList'
import { formatDate } from '../format'

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([])
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    api
      .projects()
      .then(setProjects)
      .catch(() => setFailed(true))
  }, [])

  return (
    <>
      <h1 className="page-title">Projetos</h1>
      {failed && <p className="meta">Não consegui buscar os projetos no GitHub agora. Tente de novo em instantes.</p>}
      <ol className="entry-list">
        {projects.map((p, i) => (
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
