export default function TagList({ tags }: { tags: string[] }) {
  if (tags.length === 0) return null
  return (
    <ul className="tags">
      {tags.map((tag) => (
        <li key={tag} className="tag">
          {tag}
        </li>
      ))}
    </ul>
  )
}
