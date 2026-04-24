import React from 'react';

/**
 * RecommendationCard - Display a single recommendation with explanation and nutrition.
 */
export default function RecommendationCard({ recommendation, onRate, onNeverAgain }) {
  return (
    <div style={styles.card}>
      <div style={styles.header}>
        <span style={styles.rank}>#{recommendation.rank}</span>
        <h3 style={styles.title}>{recommendation.item.name}</h3>
        <span style={styles.score}>{recommendation.score}/10</span>
      </div>

      <p style={styles.description}>{recommendation.item.description}</p>

      {recommendation.memory_signal?.seen && (
        <div style={styles.memory_signal}>
           You {recommendation.memory_signal.signal === 'liked' ? ' loved' : ' disliked'} this before
        </div>
      )}

      <div style={styles.explanation}>
        <span style={styles.badge}>Why recommended:</span>
        <p>{recommendation.explanation}</p>
      </div>

      {recommendation.nutrition && (
        <div style={styles.nutrition}>
          <div style={styles.nutrition_item}>
             {recommendation.nutrition.calories} cal
          </div>
          <div style={styles.nutrition_item}>
             {recommendation.nutrition.protein}g protein
          </div>
          <div style={styles.nutrition_item}>
             Health: {Math.round(recommendation.item.health_score * 10) / 10}/10
          </div>
        </div>
      )}

      <div style={styles.meta}>
        <span> ₹{recommendation.item.price}</span>
        <span>⏱ {recommendation.item.delivery_time_mins} mins</span>
        <span> {recommendation.item.rating}</span>
      </div>

      <div style={styles.actions}>
        <button
          style={{ ...styles.button, ...styles.buttonRate }}
          onClick={() => onRate(recommendation.item.id)}
        >
           I like this
        </button>
        <button
          style={{ ...styles.button, ...styles.buttonNever }}
          onClick={() => onNeverAgain(recommendation.item.id)}
        >
           Never again
        </button>
      </div>
    </div>
  );
}

const styles = {
  card: {
    background: '#fff',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    padding: '16px',
    marginBottom: '16px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: '12px',
  },
  rank: {
    background: '#ff6b6b',
    color: '#fff',
    borderRadius: '50%',
    width: '32px',
    height: '32px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '14px',
    fontWeight: 'bold',
  },
  title: {
    margin: 0,
    flex: 1,
    marginLeft: '12px',
    fontSize: '18px',
    fontWeight: '600',
  },
  score: {
    background: '#4CAF50',
    color: '#fff',
    padding: '4px 8px',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: 'bold',
  },
  description: {
    color: '#666',
    margin: '8px 0',
    fontSize: '14px',
  },
  memory_signal: {
    background: '#fff3cd',
    border: '1px solid #ffc107',
    borderRadius: '4px',
    padding: '8px',
    marginBottom: '8px',
    fontSize: '13px',
  },
  explanation: {
    background: '#f5f5f5',
    borderLeft: '3px solid #2196F3',
    padding: '8px 12px',
    marginBottom: '12px',
    borderRadius: '2px',
  },
  badge: {
    fontSize: '12px',
    fontWeight: 'bold',
    color: '#2196F3',
  },
  nutrition: {
    display: 'flex',
    gap: '12px',
    marginBottom: '12px',
    fontSize: '13px',
  },
  nutrition_item: {
    background: '#e8f5e9',
    padding: '6px 10px',
    borderRadius: '4px',
  },
  meta: {
    display: 'flex',
    gap: '16px',
    marginBottom: '12px',
    fontSize: '13px',
    color: '#666',
  },
  actions: {
    display: 'flex',
    gap: '8px',
  },
  button: {
    flex: 1,
    padding: '10px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '13px',
    fontWeight: '600',
    transition: 'all 0.2s',
  },
  buttonRate: {
    background: '#4CAF50',
    color: '#fff',
  },
  buttonNever: {
    background: '#f44336',
    color: '#fff',
  },
};
