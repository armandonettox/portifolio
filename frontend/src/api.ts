export type PostSummary = {
  slug: string
  title: string
  date: string
  summary: string
  tags: string[]
  // os campos abaixo so existem em posts que vem das discussoes do GitHub
  number?: number
  url?: string
  comments?: number
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

export type BlogConfig = {
  repo: string
  repo_id: string
  category: string
  category_id: string
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
  blogConfig: () => get<BlogConfig>('/api/blog-config'),
}
