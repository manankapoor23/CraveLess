export default function CartSummary({ cartCount, summary, loading, onCheckout }) {
  if (loading) {
    return (
      <section className="cart-summary-card">
        <h3>Cart Intelligence</h3>
        <p className="muted-copy">Analyzing cart nutrition...</p>
      </section>
    );
  }

  if (!summary) {
    return (
      <section className="cart-summary-card">
        <h3>Cart Intelligence</h3>
        <p className="muted-copy">Add items to see macros, health score, and gap detection.</p>
      </section>
    );
  }

  return (
    <section className="cart-summary-card">
      <div className="cart-summary-head">
        <h3>Cart Intelligence</h3>
        <strong>{cartCount} items</strong>
      </div>

      <div className="macro-grid">
        <div>
          <label>Calories</label>
          <strong>{summary.nutrition?.calories || 0}</strong>
        </div>
        <div>
          <label>Protein</label>
          <strong>{summary.nutrition?.protein || 0} g</strong>
        </div>
        <div>
          <label>Carbs</label>
          <strong>{summary.nutrition?.carbs || 0} g</strong>
        </div>
        <div>
          <label>Fat</label>
          <strong>{summary.nutrition?.fat || 0} g</strong>
        </div>
      </div>

      <div className="health-score-row">
        <span>Health score</span>
        <strong>{summary.health_score || 0} / 10</strong>
      </div>

      {!!summary.nutrition_gaps?.length && (
        <div className="gap-box">
          <span>Detected gaps</span>
          <ul>
            {summary.nutrition_gaps.map((gap) => (
              <li key={gap}>{gap}</li>
            ))}
          </ul>
        </div>
      )}

      <button className="button button-primary" onClick={onCheckout}>
        Proceed to Checkout
      </button>
    </section>
  );
}
