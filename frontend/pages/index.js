import Link from 'next/link';

export default function Home() {
  return (
    <main className="landing-shell">
      <div className="landing-backdrop" />

      <header className="top-nav">
        <div className="brand-lockup">
          <span className="brand-dot" />
          <span className="brand-wordmark">CraveLess</span>
        </div>
        <Link href="/dashboard" className="button button-ghost">
          Open Demo
        </Link>
      </header>

      <section className="hero-grid">
        <div className="hero-copy">
          <p className="kicker">AI Decision Agent for Food Ordering</p>
          <h1>Stop browsing. Start deciding in one prompt.</h1>
          <p>
            CraveLess converts messy cravings into a clear top-3 shortlist with
            reasoning, nutrition context, and persona-aware trade-offs.
          </p>

          <div className="hero-actions">
            <Link href="/dashboard" className="button button-primary">
              Launch Agent Console
            </Link>
            <a href="http://localhost:8000/docs" className="button button-ghost">
              API Docs
            </a>
          </div>
        </div>

        <div className="hero-card">
          <h3>Example Prompt</h3>
          <p className="prompt-preview">
            I need dinner under 350 rupees, high protein, and delivered fast.
          </p>

          <div className="hero-metrics">
            <div>
              <span className="metric-label">Output</span>
              <strong>Top 3 ranked items</strong>
            </div>
            <div>
              <span className="metric-label">Latency</span>
              <strong>1 API call</strong>
            </div>
            <div>
              <span className="metric-label">Strategy</span>
              <strong>Multi-objective ranking</strong>
            </div>
          </div>
        </div>
      </section>

      <section className="feature-section">
        <div className="section-head">
          <p className="kicker">Built for Real Decisions</p>
          <h2>From intent to action in a single loop</h2>
        </div>

        <div className="feature-grid">
          <article className="feature-card">
            <h3>Intent Parsing</h3>
            <p>
              Understands phrases like healthy and quick, low budget, or try
              something new.
            </p>
          </article>
          <article className="feature-card">
            <h3>Persona Switching</h3>
            <p>
              Moves between Balanced, Health-First, Budget, Fast-Delivery, and
              Explore automatically.
            </p>
          </article>
          <article className="feature-card">
            <h3>Taste Memory</h3>
            <p>
              Preserves user preference signals and reuses them for future
              recommendations.
            </p>
          </article>
          <article className="feature-card">
            <h3>Nutrition-Aware Cart</h3>
            <p>
              Live cart summary reports calories, macros, and health gaps before
              checkout.
            </p>
          </article>
          <article className="feature-card">
            <h3>Agentic Flow</h3>
            <p>
              Conversation endpoint orchestrates recommendation tools behind a
              single UX.
            </p>
          </article>
          <article className="feature-card">
            <h3>Future-Ready Tooling</h3>
            <p>
              Mock data now, direct Swiggy MCP tool integration when you move to
              production APIs.
            </p>
          </article>
        </div>
      </section>

      <section className="stack-section">
        <div className="section-head">
          <p className="kicker">Modern Stack</p>
          <h2>Engineered for speed, clarity, and extension</h2>
        </div>
        <div className="stack-grid">
          <div>
            <span>Frontend</span>
            <strong>Next.js 14 + React 18</strong>
          </div>
          <div>
            <span>Backend</span>
            <strong>FastAPI + Pydantic</strong>
          </div>
          <div>
            <span>Decision Layer</span>
            <strong>Ranking + Memory + Taste Graph</strong>
          </div>
          <div>
            <span>Data Mode</span>
            <strong>Mock now, MCP tools next</strong>
          </div>
        </div>
      </section>

      <footer className="landing-footer">
        <p>CraveLess 2026. Decision intelligence for food ordering.</p>
      </footer>
    </main>
  );
}
