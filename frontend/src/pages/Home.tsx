import AnimatedName from '../components/AnimatedName'
import TechFloat from '../components/TechFloat'

const NOME = 'Armando Netto'

function saudacao(): string {
  const hora = new Date().getHours()
  const periodo = hora < 12 ? 'bom dia' : hora < 18 ? 'boa tarde' : 'boa noite'
  return `Olá, ${periodo}!`
}

export default function Home() {
  return (
    <section className="home">
      <div className="home-text">
        <AnimatedName name={NOME} />
        <p className="home-lead">
          <span className="home-greeting">{saudacao()}</span> Sou programador e misturo técnica, criatividade e análise de dados
          para resolver problemas reais. Acredito que dados e tecnologia mudam como um negócio
          funciona, e que o que faz isso dar certo é partir de um problema real e das pessoas que
          vão viver com a solução.
        </p>
        <ul className="home-links">
          <li>
            <a href="mailto:contato@armandonetto.com" aria-label="E-mail: contato@armandonetto.com">
              <span className="nav-prefix">~/</span>email<span className="link-arrow">↗</span>
              <span className="link-reveal" aria-hidden="true">
                contato@armandonetto.com
              </span>
            </a>
          </li>
          <li>
            <a
              href="https://www.linkedin.com/in/armandonettox/"
              target="_blank"
              rel="noopener"
              aria-label="LinkedIn (abre em nova aba)"
            >
              <span className="nav-prefix">~/</span>linkedin<span className="link-arrow">↗</span>
              <span className="link-reveal" aria-hidden="true">
                armandonettox
              </span>
            </a>
          </li>
          <li>
            <a
              href="https://github.com/armandonettox"
              target="_blank"
              rel="noopener"
              aria-label="GitHub (abre em nova aba)"
            >
              <span className="nav-prefix">~/</span>github<span className="link-arrow">↗</span>
              <span className="link-reveal" aria-hidden="true">
                armandonettox
              </span>
            </a>
          </li>
        </ul>
      </div>
      <div className="home-visual">
        <img className="home-photo" src="/profile.webp" alt="Armando Netto" />
        <TechFloat />
      </div>
    </section>
  )
}
