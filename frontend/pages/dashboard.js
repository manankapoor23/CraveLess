import { useEffect, useState } from 'react';
import RecommendationCard from '../components/RecommendationCard';
import axios from 'axios';

/**
 * Dashboard - Main user interface for recommendations and ordering.
 */
export default function Dashboard() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [persona, setPersona] = useState('balanced');
  const [cart, setCart] = useState([]);

  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    fetchRecommendations();
  }, [persona]);

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(
        `${API_URL}/recommendations/get-top-3`,
        {
          persona: persona,
          intent: null,
          filters: null,
        }
      );
      setRecommendations(response.data.recommendations);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRate = (itemId) => {
    alert(`Rated ${itemId} 5/5!`);
    // In production: Send to backend
  };

  const handleNeverAgain = (itemId) => {
    alert(`Removed ${itemId} from recommendations`);
    // In production: Send to backend
  };

  const addToCart = (item) => {
    const existing = cart.find(i => i.id === item.id);
    if (existing) {
      setCart(cart.map(i => i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i));
    } else {
      setCart([...cart, { ...item, quantity: 1 }]);
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1>🍽️ CraveLess</h1>
        <p>AI Food Decision Engine</p>
      </header>

      <div style={styles.controls}>
        <label style={styles.label}>Choose your persona:</label>
        <div style={styles.persona_buttons}>
          {['balanced', 'health-first', 'budget', 'fast_delivery', 'explore'].map(p => (
            <button
              key={p}
              style={{
                ...styles.persona_button,
                ...(persona === p ? styles.persona_button_active : {}),
              }}
              onClick={() => setPersona(p)}
            >
              {p === 'balanced' && '⚖️'}
              {p === 'health-first' && '💪'}
              {p === 'budget' && '💰'}
              {p === 'fast_delivery' && '⚡'}
              {p === 'explore' && '🔍'}
              {' ' + p.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      <div style={styles.content}>
        <div style={styles.recommendations}>
          <h2>🎯 Top 3 Recommendations</h2>
          {loading && <p>Loading...</p>}
          {error && <p style={styles.error}>Error: {error}</p>}
          {!loading && recommendations.length === 0 && <p>No recommendations yet</p>}
          {recommendations.map(rec => (
            <div key={rec.item.id}>
              <RecommendationCard
                recommendation={rec}
                onRate={handleRate}
                onNeverAgain={handleNeverAgain}
              />
              <button
                style={styles.add_to_cart_button}
                onClick={() => addToCart(rec.item)}
              >
                ➕ Add to Cart
              </button>
            </div>
          ))}
        </div>

        <div style={styles.sidebar}>
          <h2>🛒 Cart ({cart.length})</h2>
          {cart.length === 0 ? (
            <p style={styles.empty_cart}>Your cart is empty</p>
          ) : (
            <>
              <div style={styles.cart_items}>
                {cart.map(item => (
                  <div key={item.id} style={styles.cart_item}>
                    <span>{item.name}</span>
                    <span>₹{item.price} x {item.quantity}</span>
                  </div>
                ))}
              </div>
              <div style={styles.cart_total}>
                Total: ₹{cart.reduce((sum, item) => sum + item.price * item.quantity, 0)}
              </div>
              <button style={styles.checkout_button}>
                Checkout
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    background: '#f9f9f9',
    padding: '20px',
  },
  header: {
    textAlign: 'center',
    marginBottom: '32px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: '#fff',
    padding: '32px',
    borderRadius: '8px',
  },
  controls: {
    marginBottom: '24px',
  },
  label: {
    display: 'block',
    marginBottom: '12px',
    fontWeight: '600',
  },
  persona_buttons: {
    display: 'flex',
    gap: '8px',
    flexWrap: 'wrap',
  },
  persona_button: {
    padding: '8px 16px',
    background: '#fff',
    border: '1px solid #ddd',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '13px',
    transition: 'all 0.2s',
  },
  persona_button_active: {
    background: '#667eea',
    color: '#fff',
    borderColor: '#667eea',
  },
  content: {
    display: 'grid',
    gridTemplateColumns: '1fr 320px',
    gap: '24px',
  },
  recommendations: {
    flex: 1,
  },
  sidebar: {
    background: '#fff',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    padding: '16px',
    height: 'fit-content',
    position: 'sticky',
    top: '20px',
  },
  cart_items: {
    marginBottom: '12px',
  },
  cart_item: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '8px',
    borderBottom: '1px solid #eee',
    fontSize: '13px',
  },
  cart_total: {
    fontWeight: 'bold',
    fontSize: '16px',
    marginBottom: '12px',
    padding: '8px 0',
    borderTop: '2px solid #eee',
  },
  empty_cart: {
    color: '#999',
    textAlign: 'center',
    padding: '20px',
  },
  checkout_button: {
    width: '100%',
    padding: '10px',
    background: '#4CAF50',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontWeight: '600',
  },
  add_to_cart_button: {
    width: '100%',
    padding: '8px',
    background: '#667eea',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    marginBottom: '12px',
  },
  error: {
    color: '#f44336',
  },
};
