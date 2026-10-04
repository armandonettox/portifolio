import { useEffect, useRef, useState } from 'react'

const GLYPHS = '01{}[]<>/=+*#$%&'
const TICK_MS = 45
const SCRAMBLE_MS = 600
const RESOLVE_STEP_MS = 80
const FIRST_RUN_MS = 500
const REPEAT_MS = 3000

// palavras escondidas: aparecem raramente, por um instante, no meio dos simbolos
const SECRET_WORDS = ['surf', 'bruna', 'dados', 'vitoria']
const SECRET_CHANCE = 0.08

function randomGlyph(): string {
  return GLYPHS[Math.floor(Math.random() * GLYPHS.length)]
}

function buildFrame(chars: string[], done: boolean[]): string[] {
  const free = (i: number) => !done[i] && chars[i] !== ' '
  const frame = chars.map((c, i) => (free(i) ? randomGlyph() : c))
  if (Math.random() >= SECRET_CHANCE) return frame

  // as vezes a palavra aparece de tras para frente, o que dificulta ainda mais
  let word = SECRET_WORDS[Math.floor(Math.random() * SECRET_WORDS.length)]
  if (Math.random() < 0.5) word = [...word].reverse().join('')

  const starts: number[] = []
  for (let s = 0; s + word.length <= chars.length; s++) {
    if ([...word].every((_, k) => free(s + k))) starts.push(s)
  }
  if (starts.length === 0) return frame

  const start = starts[Math.floor(Math.random() * starts.length)]
  ;[...word].forEach((letter, k) => {
    frame[start + k] = letter
  })
  return frame
}

// Nome que de tempos em tempos vira simbolos e volta ao texto, letra por letra
export default function AnimatedName({ name }: { name: string }) {
  const letters = [...name]
  const [shown, setShown] = useState<string[]>(letters)
  const [resolved, setResolved] = useState<boolean[]>(() => letters.map(() => true))
  const [widths, setWidths] = useState<number[]>([])
  const spans = useRef<(HTMLSpanElement | null)[]>([])

  // trava a largura de cada letra para o titulo nao pular enquanto os simbolos mudam
  useEffect(() => {
    document.fonts.ready.then(() => {
      setWidths(
        spans.current.map((el) => {
          if (!el) return 0
          const size = parseFloat(getComputedStyle(el).fontSize)
          return el.getBoundingClientRect().width / size
        }),
      )
    })
  }, [])

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

    const chars = [...name]
    let tick: number | undefined
    let next: number | undefined

    function run() {
      const start = performance.now()
      tick = window.setInterval(() => {
        const elapsed = performance.now() - start
        const done = chars.map((_, i) => elapsed >= SCRAMBLE_MS + i * RESOLVE_STEP_MS)
        setResolved(done)
        setShown(buildFrame(chars, done))
        if (done.every(Boolean)) {
          window.clearInterval(tick)
          next = window.setTimeout(run, REPEAT_MS)
        }
      }, TICK_MS)
    }

    next = window.setTimeout(run, FIRST_RUN_MS)
    return () => {
      window.clearInterval(tick)
      window.clearTimeout(next)
    }
  }, [name])

  return (
    <h1 aria-label={name}>
      {shown.map((char, i) => (
        <span
          key={i}
          ref={(el) => {
            spans.current[i] = el
          }}
          aria-hidden="true"
          className={resolved[i] ? 'glyph' : 'glyph glyph-scrambling'}
          style={widths[i] ? { width: `${widths[i]}em` } : undefined}
        >
          {char === ' ' ? ' ' : char}
        </span>
      ))}
    </h1>
  )
}
