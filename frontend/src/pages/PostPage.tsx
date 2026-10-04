import { useEffect, useState } from 'react'
import Markdown from 'react-markdown'
import { useParams } from 'react-router-dom'
import { api, type Post } from '../api'
import Comments from '../components/Comments'
import { formatDate } from '../format'

export default function PostPage() {
  const { slug = '' } = useParams()
  const [post, setPost] = useState<Post | null>(null)

  useEffect(() => {
    api.post(slug).then(setPost).catch(console.error)
  }, [slug])

  if (!post) return <p>Carregando...</p>

  return (
    <>
      <h1>{post.title}</h1>
      <p className="meta">{formatDate(post.date)}</p>
      <Markdown>{post.body}</Markdown>
      {post.number !== undefined && <Comments number={post.number} />}
    </>
  )
}
