import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, type PostSummary } from '../api'

export default function Posts() {
  const [posts, setPosts] = useState<PostSummary[]>([])

  useEffect(() => {
    api.posts().then(setPosts).catch(console.error)
  }, [])

  return (
    <>
      <h1>Blog</h1>
      {posts.map((p) => (
        <article key={p.slug}>
          <h2>
            <Link to={`/blog/${p.slug}`}>{p.title}</Link>
          </h2>
          <p className="meta">{p.date}</p>
          <p>{p.summary}</p>
        </article>
      ))}
    </>
  )
}
