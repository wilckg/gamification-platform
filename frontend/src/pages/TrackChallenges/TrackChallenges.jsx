import { useParams, useNavigate } from 'react-router-dom';
import { FaArrowLeft, FaFlag, FaCheck } from 'react-icons/fa';
import ProfileDropdown from '../../components/ProfileDropdown/ProfileDropdown';
import styles from './TrackChallenges.module.css'; // Arquivo CSS que vamos criar

const TrackChallenges = () => {
  const { trackId } = useParams();
  const navigate = useNavigate();

  // Dados mockados (substitua pela API)
  const track = {
    id: trackId,
    title: 'Fundamentos de Programação',
    description: 'Trilha introdutória para iniciantes em lógica de programação',
    progress: 35,
    challenges: [
      { id: 1, title: 'Variáveis e Tipos', difficulty: 'Fácil', completed: true },
      { id: 2, title: 'Estruturas Condicionais', difficulty: 'Fácil', completed: false },
      { id: 3, title: 'Loops e Iterações', difficulty: 'Médio', completed: false }
    ]
  };

  return (
    <div className={styles.container}>
      {/* Header consistente com o Dashboard */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <button onClick={() => navigate('/dashboard')} className={styles.backButton}>
            <FaArrowLeft /> Voltar
          </button>
          <h1 className={styles.logo}>Trilha: {track.title}</h1>
          <ProfileDropdown user={{ name: 'Usuário', points: 1200 }} />
        </div>
      </header>

      <main className={styles.mainContent}>
        <div className={styles.trackInfo}>
          <p className={styles.trackDescription}>{track.description}</p>
          <div className={styles.progressContainer}>
            <div className={styles.progressBar}>
              <div 
                className={styles.progressFill} 
                style={{ width: `${track.progress}%` }}
              ></div>
            </div>
            <span>{track.progress}% concluído</span>
          </div>
        </div>

        <div className={styles.challengesSection}>
          <h2 className={styles.sectionTitle}>
            <FaFlag /> Desafios
          </h2>
          
          <div className={styles.challengesList}>
            {track.challenges.map(challenge => (
              <div 
                key={challenge.id} 
                className={`${styles.challengeCard} ${challenge.completed ? styles.completed : ''}`}
                onClick={() => navigate(`/challenges/${challenge.id}`)}
              >
                <h3>{challenge.title}</h3>
                <div className={styles.challengeMeta}>
                  <span className={`${styles.difficulty} ${styles[challenge.difficulty.toLowerCase()]}`}>
                    {challenge.difficulty}
                  </span>
                  {challenge.completed && (
                    <span className={styles.completedBadge}>
                      <FaCheck /> Concluído
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default TrackChallenges;