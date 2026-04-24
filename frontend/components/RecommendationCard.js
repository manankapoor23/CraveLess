export default function RecommendationCard({ recommendation, onRate, onNeverAgain, onAddToCart }) {
  const item = recommendation?.item || {};
  const score = Number(recommendation?.score || 0).toFixed(2);
  
  // Create a predictable gradient based on item id
  const hue = (item.id.length * 37) % 360;
  const gradient = `linear-gradient(135deg, hsl(${hue}, 80%, 90%), hsl(${hue + 30}, 80%, 75%))`;

  return (
    <article className="food-card">
      <div className="food-card-image" style={{ background: gradient }}>
        <div className="food-badge">
          ✨ {Math.round((score / 10) * 100)}% Match
        </div>
        <div className="food-time-badge">
          {item.delivery_time_mins || '20'} min
        </div>
      </div>
      
      <div className="food-card-content">
        <div className="food-card-header">
          <h3 className="food-title">{item.name}</h3>
          <span className="food-price">₹{item.price}</span>
        </div>
        
        <p className="food-desc">{item.description}</p>
        
        <div className="food-stats">
          <span className="stat"><span className="stat-icon">⭐</span> {item.rating || '4.5'}</span>
          <span className="stat"><span className="stat-icon">🔥</span> {item.health_score || '-'} / 10 Health</span>
          {item.nutrition && <span className="stat"><span className="stat-icon">💪</span> {item.nutrition.protein}g Protein</span>}
        </div>

        {recommendation.explanation && (
          <div className="food-insight">
            <span className="insight-icon">💡</span>
            <p>{recommendation.explanation}</p>
          </div>
        )}

        <div className="food-actions">
          <button className="btn-secondary" onClick={() => onRate(item.id)}>
             Heart
          </button>
          <button className="btn-secondary" onClick={() => onNeverAgain(item.id)}>
             Hide
          </button>
          <button className="btn-primary" onClick={() => onAddToCart(item)}>
            Add
          </button>
        </div>
      </div>
    </article>
  );
}
