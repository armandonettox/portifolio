import { useEffect, useState } from 'react'
import Markdown from 'react-markdown'
import { Link, useParams } from 'react-router-dom'
import { api, type Post } from '../api'
import Comments from '../components/Comments'
import TagList from '../components/TagList'
import { formatDate } from '../format'
import './PostPage.css'

export default function PostPage() {
  const { slug = '' } = useParams()
  // guarda o resultado junto do slug; se o slug mudou, o resultado antigo ainda nao vale
  const [result, setResult] = useState<{ slug: string; post: Post | null } | null>(null)

  useEffect(() => {
    let cancelled = false
    api
      .post(slug)
      .then((post) => !cancelled && setResult({ slug, post }))
      .catch(() => !cancelled && setResult({ slug, post: null }))
    return () => {
      cancelled = true
    }
  }, [slug])

  const current = result?.slug === slug ? result : null
  const post = current?.post ?? null
  const failed = current !== null && current.post === null

  if (failed) {
    return (
      <article className="post">
        <p className="meta">Não encontrei este post.</p>
        <Link className="post-back" to="/blog">
          <span aria-hidden="true">←</span> voltar ao blog
        </Link>
      </article>
    )
  }

  if (!post) return <p className="meta">Carregando...</p>

  return (
    <article className="post">
      <Link className="post-back" to="/blog">
        <span aria-hidden="true">←</span> blog
      </Link>

      <header className="post-header">
        <h1 className="post-title">{post.title}</h1>
        <p className="post-meta">
          <time dateTime={post.date}>{formatDate(post.date)}</time>
          {post.url && (
            <a href={post.url} target="_blank" rel="noopener">
              ver no GitHub ↗
            </a>
          )}
        </p>
        <TagList tags={post.tags ?? []} />
      </header>

      <div className="prose">
        <Markdown>{post.body}</Markdown>
      </div>

      {post.number !== undefined && <Comments number={post.number} />}
    </article>
  )
}
