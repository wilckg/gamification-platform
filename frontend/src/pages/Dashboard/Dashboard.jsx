import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaTrophy, FaFlag, FaUserCircle, FaChevronDown, FaSignOutAlt } from 'react-icons/fa';
import ProfileDropdown from '../../components/ProfileDropdown/ProfileDropdown';
import styles from './Dashboard.module.css';

export default function Dashboard() {
    const navigate = useNavigate();
    const [isProfileOpen, setIsProfileOpen] = useState(false);
    const [activeTab, setActiveTab] = useState('challenges');

    // Dados de exemplo
    const user = {
        name: 'João Silva',
        email: 'joao@exemplo.com',
        rank: 5,
        points: 1200
    };

    const challenges = [
        { id: 1, title: 'Desafio de Lógica Básica', difficulty: 'Fácil', completed: true },
        { id: 2, title: 'Algoritmos de Ordenação', difficulty: 'Médio', completed: false },
        { id: 3, title: 'Estruturas de Dados Avançadas', difficulty: 'Difícil', completed: false }
    ];

    const ranking = [
        { id: 1, name: 'Maria Souza', points: 2500 },
        { id: 2, name: 'Carlos Oliveira', points: 2100 },
        { id: 3, name: 'Ana Santos', points: 1900 },
        { id: 4, name: 'Pedro Costa', points: 1500 },
        { id: 5, name: user.name, points: user.points }
    ];

    const handleProfileClick = () => {
        setIsProfileOpen(false); // Fecha o dropdown
        setTimeout(() => navigate('/profile'), 100); // Pequeno delay para garantir
    };

    const handleLogout = () => {
        // Implemente a lógica de logout aqui
        console.log('Usuário deslogado');
    };

    return (
        <div className={styles.dashboardContainer}>
            {/* Header com menu de usuário */}
            <header className={styles.header}>
                <div className={styles.headerContent}>
                    <h1 className={styles.logo}>CodeChallenge</h1>

                    <ProfileDropdown user={user} />
                </div>
            </header>

            <main className={styles.mainContent}>
                <div className={styles.tabs}>
                    <button
                        className={`${styles.tabButton} ${activeTab === 'challenges' ? styles.active : ''}`}
                        onClick={() => setActiveTab('challenges')}
                    >
                        <FaFlag /> Desafios
                    </button>
                    <button
                        className={`${styles.tabButton} ${activeTab === 'ranking' ? styles.active : ''}`}
                        onClick={() => setActiveTab('ranking')}
                    >
                        <FaTrophy /> Ranking
                    </button>
                </div>

                {activeTab === 'challenges' ? (
                    <div className={styles.challengesList}>
                        <h2>Desafios Disponíveis</h2>
                        {challenges.map(challenge => (
                            <div key={challenge.id} className={styles.challengeCard}>
                                <h3>{challenge.title}</h3>
                                <p>Dificuldade: <span className={styles[challenge.difficulty.toLowerCase()]}>{challenge.difficulty}</span></p>
                                <button
                                    className={`${styles.challengeButton} ${challenge.completed ? styles.completed : ''}`}
                                >
                                    {challenge.completed ? 'Concluído' : 'Iniciar Desafio'}
                                </button>
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
                                    <tr key={userRank.id} className={userRank.name === user.name ? styles.currentUser : ''}>
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