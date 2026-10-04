import { useEffect, useState } from 'react'
import { api, type Project } from '../api'

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([])

  useEffect(() => {
    api.projects().then(setProjects).catch(console.error)
  }, [])

  return (
    <>
      <h1>Projetos</h1>
      {projects.map((p) => (
        <article key={p.slug}>
          <h2>{p.title}</h2>
          <p className="meta">{p.stack.join(' / ')}</p>
          <p>{p.summary}</p>
        </article>
      ))}
    </>
  )
}
