import { useState, useRef, useEffect } from 'react';
import { FaTrophy, FaAward, FaUserCircle, FaChevronLeft, FaStar, FaMedal, FaCamera } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import styles from './Dashboard.module.css';

export default function Profile() {
    // Dados de exemplo - substitua pelos dados reais da sua API
    const [user, setUser] = useState({
        name: 'João Silva',
        email: 'joao@exemplo.com',
        rank: 5,
        points: 1200,
        joined: '15/03/2023',
        challengesCompleted: 24,
        accuracy: '87%',
        avatar: null
    });

    const achievements = [
        { id: 1, name: 'Iniciante', description: 'Completou 5 desafios', icon: <FaStar />, earned: true },
        { id: 2, name: 'Intermediário', description: 'Completou 15 desafios', icon: <FaMedal />, earned: true },
        { id: 3, name: 'Avançado', description: 'Completou 30 desafios', icon: <FaTrophy />, earned: false },
        { id: 4, name: 'Precisão', description: '90% de acertos', icon: <FaAward />, earned: false }
    ];

    const badges = [
        { id: 1, name: 'Lógica', level: 'Ouro', earned: true },
        { id: 2, name: 'Algoritmos', level: 'Prata', earned: true },
        { id: 3, name: 'Estruturas', level: 'Bronze', earned: true },
        { id: 4, name: 'Otimização', level: 'Ouro', earned: false }
    ];

    const [avatarPreview, setAvatarPreview] = useState(null);
    const fileInputRef = useRef(null);
    const [isLoading, setIsLoading] = useState(false);

    // Carrega os dados do usuário e avatar
    useEffect(() => {
        const loadUserData = async () => {
            try {
                const response = await api.get('/user/profile');
                setUser(response.data);
                if (response.data.avatar) {
                    setAvatarPreview(`${process.env.REACT_APP_API_URL}${response.data.avatar}`);
                }
            } catch (error) {
                console.error('Erro ao carregar perfil:', error);
            }
        };
        loadUserData();
    }, []);

    const handleAvatarClick = () => {
        fileInputRef.current.click();
    };

    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        try {
            setIsLoading(true);
            const formData = new FormData();
            formData.append('avatar', file);

            const response = await api.patch('/user/avatar', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            // Atualiza a visualização
            const reader = new FileReader();
            reader.onloadend = () => {
                setAvatarPreview(reader.result);
            };
            reader.readAsDataURL(file);

            setUser(prev => ({ ...prev, avatar: response.data.avatar }));
        } catch (error) {
            console.error('Erro ao atualizar avatar:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={styles.dashboardContainer}>
            <header className={styles.header}>
                <div className={styles.headerContent}>
                    <Link to="/dashboard" className={styles.backButton}>
                        <FaChevronLeft /> Voltar
                    </Link>
                    <h1 className={styles.logo}>Meu Perfil</h1>
                    <div className={styles.profileContainer}>
                        <span className={styles.userName}>{user.name}</span>
                        <FaUserCircle className={styles.profileIcon} />
                    </div>
                </div>
            </header>

            <main className={styles.profileContent}>
                {/* Seção de Informações do Usuário */}
                <div className={styles.profileSection}>
                    <div className={styles.profileHeader}>
                        <div className={styles.avatarContainer} onClick={handleAvatarClick}>
                            {avatarPreview ? (
                                <img
                                    src={avatarPreview}
                                    alt="Avatar"
                                    className={styles.avatarImage}
                                />
                            ) : (
                                <div className={styles.avatarPlaceholder}>
                                    {user.name.charAt(0).toUpperCase()}
                                </div>
                            )}
                            <div className={styles.avatarOverlay}>
                                <FaCamera className={styles.cameraIcon} />
                            </div>
                            <input
                                type="file"
                                ref={fileInputRef}
                                onChange={handleFileChange}
                                accept="image/*"
                                style={{ display: 'none' }}
                            />
                        </div>
                        <div>
                            <h2>{user.name}</h2>
                            <p className={styles.profileEmail}>{user.email}</p>
                        </div>
                    </div>

                    <div className={styles.statsGrid}>
                        <div className={styles.statCard}>
                            <h3>Ranking</h3>
                            <p className={styles.statValue}>#{user.rank}</p>
                        </div>
                        <div className={styles.statCard}>
                            <h3>Pontuação</h3>
                            <p className={styles.statValue}>{user.points}</p>
                        </div>
                        <div className={styles.statCard}>
                            <h3>Desafios</h3>
                            <p className={styles.statValue}>{user.challengesCompleted}</p>
                        </div>
                        <div className={styles.statCard}>
                            <h3>Precisão</h3>
                            <p className={styles.statValue}>{user.accuracy}</p>
                        </div>
                    </div>
                </div>

                {/* Seção de Conquistas */}
                <div className={styles.profileSection}>
                    <h2 className={styles.sectionTitle}>
                        <FaAward className={styles.sectionIcon} /> Conquistas
                    </h2>
                    <div className={styles.achievementsGrid}>
                        {achievements.map(achievement => (
                            <div
                                key={achievement.id}
                                className={`${styles.achievementCard} ${achievement.earned ? styles.earned : ''}`}
                            >
                                <div className={styles.achievementIcon}>
                                    {achievement.icon}
                                </div>
                                <h3>{achievement.name}</h3>
                                <p>{achievement.description}</p>
                                <div className={styles.achievementStatus}>
                                    {achievement.earned ? 'Conquistado' : 'Em progresso'}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Seção de Badges */}
                <div className={styles.profileSection}>
                    <h2 className={styles.sectionTitle}>
                        <FaMedal className={styles.sectionIcon} /> Badges
                    </h2>
                    <div className={styles.badgesGrid}>
                        {badges.map(badge => (
                            <div
                                key={badge.id}
                                className={`${styles.badgeCard} ${badge.earned ? styles.earned : ''}`}
                            >
                                <div className={`${styles.badgeIcon} ${styles[badge.level.toLowerCase()]}`}>
                                    <FaMedal />
                                </div>
                                <h3>{badge.name}</h3>
                                <p>{badge.level}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </main>
        </div>
    );
}