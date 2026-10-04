export type PostSummary = {
  slug: string
  title: string
  date: string
  summary: string
  tags: string[]
}

export type Post = PostSummary & { body: string }

export type Project = {
  name: string
  description: string | null
  url: string
  homepage: string | null
  language: string | null
  stars: number
  pushed_at: string | null
  topics: string[]
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(path)
  if (!res.ok) throw new Error(`erro ${res.status} em ${path}`)
  return res.json()
}

export const api = {
  posts: () => get<PostSummary[]>('/api/posts'),
  post: (slug: string) => get<Post>(`/api/posts/${slug}`),
  projects: () => get<Project[]>('/api/projects'),
}
