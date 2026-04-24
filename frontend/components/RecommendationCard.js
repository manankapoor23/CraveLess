export default function RecommendationCard({ recommendation, onRate, onNeverAgain, onAddToCart }) {
  const item = recommendation?.item || {};
  const score = Number(recommendation?.score || 0).toFixed(2);

  return (
    <article className="recommendation-card">
      <div className="recommendation-head">
        <div className="rank-pill">Rank {recommendation.rank}</div>
        <div className="score-pill">Score {score}</div>
      </div>

      <h3>{item.name}</h3>
      <p className="recommendation-description">{item.description}</p>

      <div className="recommendation-why">
        <span>Why this item</span>
        <p>{recommendation.explanation || 'Strong overall match for your intent.'}</p>
      </div>

      <div className="recommendation-meta-grid">
        <div>
          <label>Price</label>
          <strong>Rs {item.price}</strong>
        </div>
        <div>
          <label>Delivery</label>
          <strong>{item.delivery_time_mins || '-'} min</strong>
        </div>
        <div>
          <label>Rating</label>
          <strong>{item.rating || '-'}</strong>
        </div>
        <div>
          <label>Health</label>
          <strong>{item.health_score || '-'} / 10</strong>
        </div>
      </div>

      <div className="recommendation-actions">
        <button className="button button-ghost" onClick={() => onRate(item.id)}>
          Save Preference
        </button>
        <button className="button button-ghost" onClick={() => onNeverAgain(item.id)}>
          Exclude
        </button>
        <button className="button button-primary" onClick={() => onAddToCart(item)}>
          Add to Cart
        </button>
      </div>
    </article>
  );
}
