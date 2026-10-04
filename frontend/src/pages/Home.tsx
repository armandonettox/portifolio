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
            <a href="mailto:contato@armandonetto.com">contato@armandonetto.com</a>
          </li>
          <li>
            <a href="https://www.linkedin.com/in/armandonettox/" target="_blank" rel="noopener">
              linkedin.com/in/armandonettox
            </a>
          </li>
          <li>
            <a href="https://github.com/armandonettox" target="_blank" rel="noopener">
              github.com/armandonettox
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
