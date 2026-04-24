export default function CartSummary({ cartCount, summary, loading, onCheckout }) {
  if (loading) {
    return (
      <section className="cart-panel">
        <div className="cart-header">
          <h2>🛒 Order</h2>
          <span className="cart-badge">{cartCount}</span>
        </div>
        <div className="cart-loading">
          <div className="pulse-dot"></div>
          <p>Analyzing nutrition...</p>
        </div>
      </section>
    );
  }

  if (!summary) {
    return (
      <section className="cart-panel">
        <div className="cart-header">
          <h2>🛒 Order</h2>
          <span className="cart-badge">0</span>
        </div>
        <div className="cart-empty">
          <p className="empty-text">Add items to build your order</p>
        </div>
      </section>
    );
  }

  const calorieGoal = 2000;
  const caloriePercent = Math.min(100, (summary.nutrition?.calories / calorieGoal) * 100);
  const proteinGoal = 50;
  const proteinPercent = Math.min(100, ((summary.nutrition?.protein || 0) / proteinGoal) * 100);

  return (
    <section className="cart-panel">
      <div className="cart-header">
        <h2>🛒 Order</h2>
        <span className="cart-badge">{cartCount}</span>
      </div>

      <div className="nutrition-summary">
        <div className="calorie-box">
          <div className="calorie-circle">
            <div className="calorie-value">{summary.nutrition?.calories || 0}</div>
            <div className="calorie-label">kcal</div>
          </div>
          <p className="calorie-note">of {calorieGoal} daily</p>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${caloriePercent}%` }}></div>
          </div>
        </div>

        <div className="macros-compact">
          <div className="macro-item">
            <span className="macro-label">Protein</span>
            <strong>{summary.nutrition?.protein || 0}g</strong>
            <div className="macro-bar">
              <div className="macro-bar-fill protein-fill" style={{ width: `${proteinPercent}%` }}></div>
            </div>
          </div>
          <div className="macro-item">
            <span className="macro-label">Carbs</span>
            <strong>{summary.nutrition?.carbs || 0}g</strong>
          </div>
          <div className="macro-item">
            <span className="macro-label">Fat</span>
            <strong>{summary.nutrition?.fat || 0}g</strong>
          </div>
        </div>
      </div>

      <div className="health-indicator">
        <div className="health-score-big">
          <div className="health-circle">
            <span className="health-value">{summary.health_score || 0}</span>
            <span className="health-max">/10</span>
          </div>
          <span className="health-text">Health Score</span>
        </div>
      </div>

      {!!summary.nutrition_gaps?.length && (
        <div className="gaps-alert">
          <p className="gaps-label">💡 Suggested additions:</p>
          <ul className="gaps-list">
            {summary.nutrition_gaps.slice(0, 2).map((gap) => (
              <li key={gap}>{gap}</li>
            ))}
          </ul>
        </div>
      )}

      <button className="btn-checkout" onClick={onCheckout}>
        Proceed to Checkout
        <span className="checkout-arrow">→</span>
      </button>
    </section>
  );
}
