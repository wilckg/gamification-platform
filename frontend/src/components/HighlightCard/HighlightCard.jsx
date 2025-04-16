import styles from './HighlightCard.module.css';

export default function HighlightCard({ title, description, icon, color }) {
  return (
    <div className={styles.card}>
      <div className={styles.iconContainer} style={{ backgroundColor: `${color}20`, borderColor: color }}>
        <span className={styles.icon} style={{ color }}>{icon}</span>
      </div>
      <h3 className={styles.title}>{title}</h3>
      <p className={styles.description}>{description}</p>
    </div>
  );
}