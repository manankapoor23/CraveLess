import { useState } from 'react';
import Link from 'next/link';

/**
 * Index - Landing page with login and feature overview.
 */
export default function Home() {
  const [email, setEmail] = useState('');
  const [loggingIn, setLoggingIn] = useState(false);

  const handleLogin = async (provider) => {
    setLoggingIn(true);
    try {
      // In production: Call /auth/login endpoint
      window.location.href = '/dashboard';
    } catch (err) {
      console.error('Login error:', err);
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <div style={styles.hero}>
          <h1 style={styles.title}> CraveLess</h1>
          <p style={styles.subtitle}>AI Food Decision Engine</p>
          <p style={styles.tagline}>
            Stop scrolling. Start deciding.
          </p>
        </div>
      </header>

      <section style={styles.problem}>
        <div style={styles.content_width}>
          <h2>The Problem</h2>
          <div style={styles.problem_grid}>
            <div style={styles.problem_item}>
              <span style={styles.problem_icon}></span>
              <h3>Endless Scrolling</h3>
              <p>Users waste time browsing endless options</p>
            </div>
            <div style={styles.problem_item}>
              <span style={styles.problem_icon}></span>
              <h3>Decision Fatigue</h3>
              <p>Too many choices lead to indecision</p>
            </div>
            <div style={styles.problem_item}>
              <span style={styles.problem_icon}>⏱</span>
              <h3>Time Waste</h3>
              <p>Ordering should be fast and effortless</p>
            </div>
          </div>
        </div>
      </section>

      <section style={styles.solution}>
        <div style={styles.content_width}>
          <h2>The Solution</h2>
          <p style={styles.solution_text}>
            CraveLess is an AI agent that understands your intent,
            remembers your preferences, and recommends your top 3 options instantly.
          </p>

          <div style={styles.features}>
            <div style={styles.feature}>
              <h3> Intent-Driven</h3>
              <p>Tell us what you want: "cheap", "high protein", "fast" - we understand.</p>
            </div>
            <div style={styles.feature}>
              <h3> Smart Memory</h3>
              <p>We remember what you loved, what you hated, and learn over time.</p>
            </div>
            <div style={styles.feature}>
              <h3> Multi-Objective Ranking</h3>
              <p>Optimizes for preference, price, health, delivery time, and novelty.</p>
            </div>
            <div style={styles.feature}>
              <h3> Taste Graph</h3>
              <p>Models relationships between ingredients and cuisines intelligently.</p>
            </div>
            <div style={styles.feature}>
              <h3> Nutrition Tracking</h3>
              <p>Track calories, protein, macros. Get personalized health insights.</p>
            </div>
            <div style={styles.feature}>
              <h3> Personas</h3>
              <p>Switch between health-first, budget, fast-delivery, explore modes.</p>
            </div>
          </div>
        </div>
      </section>

      <section style={styles.cta}>
        <div style={styles.content_width}>
          <h2>Get Started</h2>
          <div style={styles.login_options}>
            <button
              style={{ ...styles.login_button, background: '#4285F4' }}
              onClick={() => handleLogin('google')}
              disabled={loggingIn}
            >
               Login with Google
            </button>
            <button
              style={{ ...styles.login_button, background: '#FF5733' }}
              onClick={() => handleLogin('swiggy')}
              disabled={loggingIn}
            >
               Login with Swiggy
            </button>
          </div>
          <p style={styles.cta_text}>
            or{' '}
            <Link href="/dashboard" style={styles.demo_link}>
              try demo
            </Link>
          </p>
        </div>
      </section>

      <section style={styles.tech_stack}>
        <div style={styles.content_width}>
          <h2>Built With</h2>
          <div style={styles.tech_grid}>
            <div style={styles.tech_item}>
              <h4>Backend</h4>
              <p>FastAPI + Python</p>
            </div>
            <div style={styles.tech_item}>
              <h4>Frontend</h4>
              <p>Next.js + React</p>
            </div>
            <div style={styles.tech_item}>
              <h4>Database</h4>
              <p>PostgreSQL</p>
            </div>
            <div style={styles.tech_item}>
              <h4>AI</h4>
              <p>Graph-based + Multi-objective optimization</p>
            </div>
          </div>
        </div>
      </section>

      <footer style={styles.footer}>
        <p>CraveLess © 2025. Making food ordering decisions effortless.</p>
      </footer>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    background: '#fff',
  },
  header: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: '#fff',
    padding: '80px 20px',
    textAlign: 'center',
  },
  hero: {},
  title: {
    fontSize: '48px',
    marginBottom: '8px',
  },
  subtitle: {
    fontSize: '24px',
    marginBottom: '16px',
    opacity: 0.9,
  },
  tagline: {
    fontSize: '20px',
    fontWeight: 'bold',
  },
  content_width: {
    maxWidth: '1200px',
    margin: '0 auto',
  },
  problem: {
    padding: '60px 20px',
    background: '#f9f9f9',
  },
  problem_grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '24px',
    marginTop: '32px',
  },
  problem_item: {
    textAlign: 'center',
    padding: '24px',
    background: '#fff',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  },
  problem_icon: {
    fontSize: '40px',
    display: 'block',
    marginBottom: '12px',
  },
  solution: {
    padding: '60px 20px',
  },
  solution_text: {
    fontSize: '18px',
    textAlign: 'center',
    maxWidth: '600px',
    margin: '24px auto',
  },
  features: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '24px',
    marginTop: '32px',
  },
  feature: {
    padding: '24px',
    background: '#f9f9f9',
    borderRadius: '8px',
    borderLeft: '4px solid #667eea',
  },
  cta: {
    padding: '60px 20px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: '#fff',
    textAlign: 'center',
  },
  login_options: {
    display: 'flex',
    gap: '16px',
    justifyContent: 'center',
    marginTop: '24px',
    flexWrap: 'wrap',
  },
  login_button: {
    padding: '14px 32px',
    border: 'none',
    borderRadius: '4px',
    color: '#fff',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: '600',
  },
  cta_text: {
    marginTop: '16px',
  },
  demo_link: {
    color: '#fff',
    textDecoration: 'underline',
    cursor: 'pointer',
  },
  tech_stack: {
    padding: '60px 20px',
    background: '#f9f9f9',
  },
  tech_grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
    gap: '24px',
    marginTop: '32px',
  },
  tech_item: {
    padding: '24px',
    background: '#fff',
    borderRadius: '8px',
    textAlign: 'center',
  },
  footer: {
    padding: '24px 20px',
    textAlign: 'center',
    borderTop: '1px solid #e0e0e0',
  },
};
