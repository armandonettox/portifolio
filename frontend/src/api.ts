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

class HttpError extends Error {
  status: number

  constructor(status: number, path: string) {
    super(`erro ${status} em ${path}`)
    this.status = status
  }
}

// a ultima resposta boa de cada rota fica guardada no navegador; se a API falhar, ela continua valendo
const STORAGE_PREFIX = 'cache:'

function readStored<T>(path: string): T | null {
  try {
    const raw = localStorage.getItem(STORAGE_PREFIX + path)
    return raw ? (JSON.parse(raw) as T) : null
  } catch {
    // sem localStorage (modo privado, bloqueado): segue sem a copia
    return null
  }
}

function writeStored(path: string, data: unknown) {
  try {
    localStorage.setItem(STORAGE_PREFIX + path, JSON.stringify(data))
  } catch {
    // cheio ou bloqueado: nao e motivo para quebrar a pagina
  }
}

// pausas entre as tentativas: cobrem uma falha passageira de rede ou os segundos de uma atualizacao
const RETRY_DELAYS_MS = [700, 2000, 4000]

async function fetchWithRetry<T>(path: string): Promise<T> {
  for (let attempt = 0; ; attempt++) {
    try {
      const res = await fetch(path)
      if (!res.ok) throw new HttpError(res.status, path)
      return (await res.json()) as T
    } catch (err) {
      // erro 4xx (ex: 404) nao melhora tentando de novo; rede e 5xx sim
      const retryable = !(err instanceof HttpError) || err.status >= 500
      if (!retryable || attempt >= RETRY_DELAYS_MS.length) throw err
      await new Promise((resolve) => setTimeout(resolve, RETRY_DELAYS_MS[attempt]))
    }
  }
}

async function get<T>(path: string): Promise<T> {
  const stored = readStored<T>(path)
  try {
    const data = await fetchWithRetry<T>(path)
    // lista vazia nunca substitui uma lista boa guardada
    if (Array.isArray(data) && data.length === 0 && Array.isArray(stored) && stored.length > 0) {
      return stored
    }
    writeStored(path, data)
    return data
  } catch (err) {
    // API fora do ar: mostra a versao guardada. So falha se nunca houve uma
    if (stored !== null && !(err instanceof HttpError && err.status < 500)) return stored
    throw err
  }
}

export const api = {
  posts: () => get<PostSummary[]>('/api/posts'),
  post: (slug: string) => get<Post>(`/api/posts/${slug}`),
  projects: () => get<Project[]>('/api/projects'),
  blogConfig: () => get<BlogConfig>('/api/blog-config'),
  // ultima versao guardada, para mostrar na hora enquanto a atualizada chega
  postsCached: () => readStored<PostSummary[]>('/api/posts'),
  postCached: (slug: string) => readStored<Post>(`/api/posts/${slug}`),
  projectsCached: () => readStored<Project[]>('/api/projects'),
}
