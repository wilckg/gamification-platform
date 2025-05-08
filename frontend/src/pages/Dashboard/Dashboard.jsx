import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaTrophy, FaCode, FaLayerGroup } from 'react-icons/fa';
import api from '../../services/api';
import ProfileDropdown from '../../components/ProfileDropdown/ProfileDropdown';
import styles from './Dashboard.module.css';

export default function Dashboard() {
  const navigate = useNavigate();
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('challenges');
  const [user, setUser] = useState(null);
  const [tracks, setTracks] = useState([]);
  const [ranking, setRanking] = useState([]);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get('/api/user/profile');
        setUser(res.data);
      } catch (err) {
        console.error('Erro ao buscar usuário:', err);
      }
    };

    const fetchTracks = async () => {
      try {
        const res = await api.get('/api/challenges/user-progress/current/');
        const formatted = res.data.map(item => ({
          id: item.track.id,
          title: item.track.title,
          description: item.track.description,
          icon: <FaCode />,
          challengesCount: item.progress.total,
          completedChallenges: item.progress.completed,
          difficulty: item.track.difficulty ?? 'Desconhecido'
        }));
        setTracks(formatted);
      } catch (err) {
        console.error('Erro ao buscar trilhas:', err);
      }
    };

    const fetchRanking = async () => {
      try {
        const res = await api.get('/ranking/'); // Supondo que você tenha esse endpoint
        const formatted = res.data.map((r, index) => ({
          id: r.id,
          name: r.name,
          points: r.points,
          isCurrentUser: user && r.id === user.id
        }));
        setRanking(formatted);
      } catch (err) {
        console.error('Erro ao buscar ranking:', err);
      }
    };

    fetchUser();
    fetchTracks();
    fetchRanking();
  }, []);

  return (
    <div className={styles.dashboardContainer}>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <h1 className={styles.logo}>CodeChallenge</h1>
          {user && <ProfileDropdown user={user} />}
        </div>
      </header>

      <main className={styles.mainContent}>
        <div className={styles.tabs}>
          <button
            className={`${styles.tabButton} ${activeTab === 'challenges' ? styles.active : ''}`}
            onClick={() => setActiveTab('challenges')}
          >
            <FaLayerGroup /> Trilhas
          </button>
          <button
            className={`${styles.tabButton} ${activeTab === 'ranking' ? styles.active : ''}`}
            onClick={() => setActiveTab('ranking')}
          >
            <FaTrophy /> Ranking
          </button>
        </div>

        {activeTab === 'challenges' ? (
          <div className={styles.tracksList}>
            <h2>Trilhas Disponíveis</h2>
            {tracks.map(track => (
              <div 
                key={track.id} 
                className={styles.trackCard}
                onClick={() => navigate(`/tracks/${track.id}/challenges`)}
              >
                <div className={styles.trackIcon}>
                  {track.icon}
                </div>
                <div className={styles.trackInfo}>
                  <h3>{track.title}</h3>
                  <p className={styles.trackDescription}>{track.description}</p>
                  <div className={styles.trackMeta}>
                    <span className={styles.trackDifficulty}>{track.difficulty}</span>
                    <span>{track.completedChallenges}/{track.challengesCount} desafios</span>
                  </div>
                  <div className={styles.progressBar}>
                    <div 
                      className={styles.progressFill} 
                      style={{ width: `${(track.completedChallenges / (track.challengesCount || 1)) * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className={styles.rankingList}>
            <h2>Ranking de Pontuação</h2>
            <table>
              <thead>
                <tr>
                  <th>Posição</th>
                  <th>Nome</th>
                  <th>Pontos</th>
                </tr>
              </thead>
              <tbody>
                {ranking.map((userRank, index) => (
                  <tr 
                    key={userRank.id} 
                    className={userRank.isCurrentUser ? styles.currentUser : ''}
                  >
                    <td>#{index + 1}</td>
                    <td>{userRank.name}</td>
                    <td>{userRank.points}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}
