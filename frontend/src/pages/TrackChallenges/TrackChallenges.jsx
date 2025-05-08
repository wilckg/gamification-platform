import { useParams, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { FaArrowLeft, FaFlag, FaCheck } from 'react-icons/fa';
import ProfileDropdown from '../../components/ProfileDropdown/ProfileDropdown';
import api from '../../services/api';
import styles from './TrackChallenges.module.css';

const TrackChallenges = () => {
  const { trackId } = useParams();
  const navigate = useNavigate();

  const [track, setTrack] = useState(null);
  const [user, setUser] = useState(null);

  const [difficulty, setDifficulty] = useState({
    "EASY": "Fácil",
    "MEDIUM": "Médio",
    "HARD": "Difícil"
  });

  useEffect(() => {
    const fetchUserAndTrack = async () => {
      try {
        const userRes = await api.get('/api/user/profile');
        setUser(userRes.data);

        const trackRes = await api.get(`/api/challenges/tracks/${trackId}/`);
        const challengesRes = await api.get('/api/challenges/user-challenges/');

        const userChallenges = challengesRes.data.filter(c => c.track === parseInt(trackId));

        const formattedChallenges = trackRes.data.challenges.map(challenge => {
          const userChallenge = userChallenges.find(uc => uc.challenge === challenge.id);
          return {
            id: challenge.id,
            title: challenge.title,
            difficulty: difficulty[challenge.difficulty],
            completed: userChallenge?.completed || false,
          };
        });

        const completedCount = formattedChallenges.filter(c => c.completed).length;
        const total = formattedChallenges.length;
        const progress = total > 0 ? Math.round((completedCount / total) * 100) : 0;

        setTrack({
          id: trackRes.data.id,
          title: trackRes.data.title,
          description: trackRes.data.description,
          progress,
          challenges: formattedChallenges
        });
      } catch (error) {
        console.error('Erro ao carregar trilha ou desafios:', error);
      }
    };

    fetchUserAndTrack();
  }, [trackId]);

  if (!track || !user) return null;

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <button onClick={() => navigate('/dashboard')} className={styles.backButton}>
            <FaArrowLeft /> Voltar
          </button>
          <h1 className={styles.logo}>Trilha: {track.title}</h1>
          <ProfileDropdown user={user} />
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
