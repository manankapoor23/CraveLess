import axios from 'axios';
import Link from 'next/link';
import { useCallback, useEffect, useMemo, useState } from 'react';
import CartSummary from '../components/CartSummary';
import RecommendationCard from '../components/RecommendationCard';

export default function Dashboard() {
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const userId = 'demo-user';

  const quickPrompts = [
    'Quick lunch under 300 rupees',
    'High protein dinner for gym day',
    'Comfort food but still healthy',
    'Try something new and bold',
  ];

  const personaHints = {
    balanced: 'balanced across taste, health, price and delivery',
    'health-first': 'prioritize nutrition and protein',
    budget: 'prioritize lower total spend',
    'fast-delivery': 'prioritize shortest delivery times',
    explore: 'prioritize novelty and unseen options',
  };

  const [query, setQuery] = useState('I want something healthy but quick under 350 rupees.');
  const [persona, setPersona] = useState('balanced');
  const [recommendations, setRecommendations] = useState([]);
  const [agentReply, setAgentReply] = useState('');
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [loadingCartSummary, setLoadingCartSummary] = useState(false);
  const [error, setError] = useState(null);
  const [cart, setCart] = useState([]);
  const [cartSummary, setCartSummary] = useState(null);
  const [feedbackText, setFeedbackText] = useState('');

  const cartTotal = useMemo(
    () => cart.reduce((sum, item) => sum + item.price * item.quantity, 0),
    [cart]
  );

  const enrichQueryWithPersona = useCallback(
    (baseQuery) => `${baseQuery} Please optimize for ${personaHints[persona]}.`,
    [persona]
  );

  const fetchRecommendations = useCallback(async (inputQuery) => {
    setLoadingRecommendations(true);
    setError(null);

    try {
      const response = await axios.post(`${API_URL}/agent/chat`, {
        user_id: userId,
        message: enrichQueryWithPersona(inputQuery),
      });

      setAgentReply(response.data.message || 'Recommendations generated successfully.');
      setRecommendations(response.data.recommendations || []);
      setFeedbackText('');
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to get recommendations.');
    } finally {
      setLoadingRecommendations(false);
    }
  }, [API_URL, enrichQueryWithPersona]);

  const fetchCartSummary = useCallback(async (nextCart) => {
    if (!nextCart.length) {
      setCartSummary(null);
      return;
    }

    setLoadingCartSummary(true);
    try {
      const response = await axios.post(`${API_URL}/cart/summary`, {
        items: nextCart.map((item) => ({
          item_id: item.id,
          quantity: item.quantity,
        })),
      });
      setCartSummary(response.data);
    } catch {
      setCartSummary(null);
    } finally {
      setLoadingCartSummary(false);
    }
  }, [API_URL]);

  useEffect(() => {
    fetchRecommendations(query);
  }, []);

  useEffect(() => {
    fetchCartSummary(cart);
  }, [cart, fetchCartSummary]);

  const handlePromptSubmit = async (event) => {
    event.preventDefault();
    await fetchRecommendations(query);
  };

  const handleQuickPrompt = async (prompt) => {
    setQuery(prompt);
    await fetchRecommendations(prompt);
  };

  const handleRate = (itemId) => {
    setFeedbackText(`Saved preference for ${itemId}.`);
  };

  const handleNeverAgain = (itemId) => {
    setRecommendations((prev) => prev.filter((rec) => rec.item.id !== itemId));
    setFeedbackText(`Removed ${itemId} from suggestions.`);
  };

  const addToCart = (item) => {
    const existing = cart.find((i) => i.id === item.id);
    if (existing) {
      setCart(
        cart.map((i) =>
          i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
        )
      );
    } else {
      setCart([...cart, { ...item, quantity: 1 }]);
    }
  };

  const handleCheckout = () => {
    setFeedbackText('Checkout simulation complete. Order pipeline is ready for Swiggy MCP wiring.');
  };

  return (
    <main className="dashboard-shell">
      <header className="dashboard-topbar">
        <div>
          <p className="kicker">CraveLess Agent Console</p>
          <h1>Recommendation Workspace</h1>
        </div>
        <Link href="/" className="button button-ghost">
          Back to Home
        </Link>
      </header>

      <section className="dashboard-layout">
        <div className="dashboard-main-panel">
          <div className="agent-input-card">
            <form onSubmit={handlePromptSubmit} className="agent-prompt-form">
              <label htmlFor="prompt">Describe your craving or constraints</label>
              <textarea
                id="prompt"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                rows={3}
              />

              <div className="persona-row">
                {Object.keys(personaHints).map((p) => (
                  <button
                    key={p}
                    type="button"
                    className={`persona-chip ${persona === p ? 'active' : ''}`}
                    onClick={() => setPersona(p)}
                  >
                    {p}
                  </button>
                ))}
              </div>

              <div className="quick-prompts-row">
                {quickPrompts.map((prompt) => (
                  <button
                    key={prompt}
                    type="button"
                    className="quick-prompt"
                    onClick={() => handleQuickPrompt(prompt)}
                  >
                    {prompt}
                  </button>
                ))}
              </div>

              <div className="agent-actions-row">
                <button className="button button-primary" type="submit" disabled={loadingRecommendations}>
                  {loadingRecommendations ? 'Thinking...' : 'Get Recommendations'}
                </button>
              </div>
            </form>
          </div>

          {error && <p className="inline-error">{error}</p>}
          {feedbackText && <p className="inline-feedback">{feedbackText}</p>}

          <div className="agent-response-card">
            <h2>Agent Explanation</h2>
            <p>{agentReply || 'Run a prompt to generate recommendations.'}</p>
          </div>

          <div className="recommendation-list">
            <h2>Top Recommendations</h2>
            {!loadingRecommendations && recommendations.length === 0 && (
              <p className="empty-state">No recommendations yet. Try a prompt above.</p>
            )}

            {recommendations.map((rec) => (
              <RecommendationCard
                key={rec.item.id}
                recommendation={rec}
                onRate={handleRate}
                onNeverAgain={handleNeverAgain}
                onAddToCart={addToCart}
              />
            ))}
          </div>
        </div>

        <aside className="dashboard-sidebar">
          <div className="mini-cart">
            <div className="mini-cart-head">
              <h3>Cart</h3>
              <strong>Rs {cartTotal.toFixed(0)}</strong>
            </div>
            {!cart.length && <p className="empty-state">Cart is empty.</p>}

            {cart.map((item) => (
              <div className="mini-cart-item" key={item.id}>
                <span>{item.name}</span>
                <span>
                  Rs {item.price} x {item.quantity}
                </span>
              </div>
            ))}
          </div>

          <CartSummary
            cartCount={cart.length}
            summary={cartSummary}
            loading={loadingCartSummary}
            onCheckout={handleCheckout}
          />
        </aside>
      </section>
    </main>
  );
}
