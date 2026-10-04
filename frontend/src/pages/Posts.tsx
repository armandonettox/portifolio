import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, type PostSummary } from '../api'
import TagList from '../components/TagList'
import { formatDate } from '../format'

export default function Posts() {
  const [posts, setPosts] = useState<PostSummary[]>([])

  useEffect(() => {
    api.posts().then(setPosts).catch(console.error)
  }, [])

  return (
    <>
      <h1 className="page-title">Blog</h1>
      <ol className="entry-list">
        {posts.map((p) => (
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
