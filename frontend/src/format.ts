// aceita 2026-07-19 ou 2026-07-19T12:00:00Z e devolve algo como "19 jul 2026"
export function formatDate(iso: string): string {
  const [year, month, day] = iso.slice(0, 10).split('-').map(Number)
  // montar pelo dia local evita voltar um dia por causa do fuso
  return new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' })
    .format(new Date(year, month - 1, day))
    .replace(/\./g, '')
    .replace(/ de /g, ' ')
}
