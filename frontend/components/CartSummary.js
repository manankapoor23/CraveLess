import React from 'react';

/**
 * CartSummary - Display cart intelligence with nutrition and suggestions.
 */
export default function CartSummary({ cart, nutrition, health_score, gaps }) {
  return (
    <div style={styles.summary}>
      <div style={styles.header}>
        <h2> Cart Summary</h2>
        <span style={styles.total}>₹{cart.total_price}</span>
      </div>

      {nutrition && (
        <>
          <div style={styles.section}>
            <h3> Nutrition</h3>
            <div style={styles.nutrition_grid}>
              <div style={styles.nutrition_item}>
                <span style={styles.label}>Calories</span>
                <span style={styles.value}>{nutrition.calories} kcal</span>
              </div>
              <div style={styles.nutrition_item}>
                <span style={styles.label}>Protein</span>
                <span style={styles.value}>{nutrition.protein}g</span>
              </div>
              <div style={styles.nutrition_item}>
                <span style={styles.label}>Carbs</span>
                <span style={styles.value}>{nutrition.carbs}g</span>
              </div>
              <div style={styles.nutrition_item}>
                <span style={styles.label}>Fat</span>
                <span style={styles.value}>{nutrition.fat}g</span>
              </div>
            </div>
          </div>

          <div style={styles.section}>
            <h3> Health Score: {health_score}/10</h3>
            <div style={styles.health_bar}>
              <div
                style={{
                  ...styles.health_fill,
                  width: `${health_score * 10}%`,
                  background: health_score > 7 ? '#4CAF50' : health_score > 5 ? '#FF9800' : '#f44336',
                }}
              />
            </div>
          </div>

          {gaps.length > 0 && (
            <div style={styles.section}>
              <h3> Nutrition Gaps</h3>
              <ul style={styles.gaps_list}>
                {gaps.map((gap, idx) => (
                  <li key={idx} style={styles.gap_item}>
                    {gap}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}

      <div style={styles.action}>
        <button style={styles.checkout_button}>
           Proceed to Checkout
        </button>
      </div>
    </div>
  );
}

const styles = {
  summary: {
    background: '#fff',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    padding: '16px',
    maxWidth: '400px',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '16px',
    borderBottom: '2px solid #f0f0f0',
    paddingBottom: '12px',
  },
  total: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  section: {
    marginBottom: '16px',
  },
  nutrition_grid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '12px',
  },
  nutrition_item: {
    background: '#f9f9f9',
    padding: '12px',
    borderRadius: '6px',
    textAlign: 'center',
  },
  label: {
    display: 'block',
    fontSize: '12px',
    color: '#666',
    marginBottom: '4px',
  },
  value: {
    display: 'block',
    fontSize: '16px',
    fontWeight: 'bold',
  },
  health_bar: {
    background: '#f0f0f0',
    height: '12px',
    borderRadius: '6px',
    overflow: 'hidden',
  },
  health_fill: {
    height: '100%',
    transition: 'width 0.3s ease',
  },
  gaps_list: {
    margin: 0,
    paddingLeft: '20px',
  },
  gap_item: {
    marginBottom: '6px',
    fontSize: '13px',
    color: '#f44336',
  },
  action: {
    marginTop: '16px',
  },
  checkout_button: {
    width: '100%',
    padding: '12px',
    background: '#4CAF50',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'background 0.2s',
  },
};
