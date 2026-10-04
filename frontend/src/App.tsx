import { BrowserRouter, Route, Routes } from 'react-router-dom'
import SiteNav from './components/SiteNav'
import ThemeToggle from './components/ThemeToggle'
import Home from './pages/Home'
import PostPage from './pages/PostPage'
import Posts from './pages/Posts'
import Projects from './pages/Projects'

export default function App() {
  return (
    <BrowserRouter>
      <header className="topbar">
        <div className="topbar-inner">
          <SiteNav />
          <span className="topbar-divider" aria-hidden="true" />
          <ThemeToggle />
        </div>
      </header>
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/projetos" element={<Projects />} />
          <Route path="/blog" element={<Posts />} />
          <Route path="/blog/:slug" element={<PostPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
