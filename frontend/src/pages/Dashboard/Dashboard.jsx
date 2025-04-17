import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaTrophy, FaCode, FaLayerGroup, FaUserCircle, FaChevronDown, FaSignOutAlt } from 'react-icons/fa';
import ProfileDropdown from '../../components/ProfileDropdown/ProfileDropdown';
import styles from './Dashboard.module.css';

export default function Dashboard() {
  const navigate = useNavigate();
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('challenges');

  // Dados do usuário (exemplo)
  const user = {
    name: 'João Silva',
    email: 'joao@exemplo.com',
    rank: 5,
    points: 1200
  };

  // Dados das trilhas (substitua pela chamada à API)
  const tracks = [
    {
      id: 1,
      title: 'Fundamentos de Programação',
      description: 'Aprenda os conceitos básicos de lógica e algoritmos',
      icon: <FaCode />,
      challengesCount: 8,
      completedChallenges: 3,
      difficulty: 'Iniciante'
    },
    {
      id: 2,
      title: 'Estruturas de Dados',
      description: 'Domine arrays, listas e estruturas complexas',
      icon: <FaLayerGroup />,
      challengesCount: 10,
      completedChallenges: 1,
      difficulty: 'Intermediário'
    },
    {
      id: 3,
      title: 'Algoritmos Avançados',
      description: 'Aprenda algoritmos de busca, ordenação e otimização',
      icon: <FaCode />,
      challengesCount: 12,
      completedChallenges: 0,
      difficulty: 'Avançado'
    }
  ];

  // Dados do ranking (exemplo)
  const ranking = [
    { id: 1, name: 'Maria Souza', points: 2500 },
    { id: 2, name: 'Carlos Oliveira', points: 2100 },
    { id: 3, name: 'Ana Santos', points: 1900 },
    { id: 5, name: user.name, points: user.points, isCurrentUser: true }
  ];

  return (
    <div className={styles.dashboardContainer}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <h1 className={styles.logo}>CodeChallenge</h1>
          <ProfileDropdown user={user} />
        </div>
      </header>

      {/* Conteúdo Principal */}
      <main className={styles.mainContent}>
        {/* Abas */}
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

        {/* Lista de Trilhas (se aba ativa for 'challenges') */}
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
                      style={{ width: `${(track.completedChallenges / track.challengesCount) * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          /* Ranking (se aba ativa for 'ranking') */
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