import { useState, useRef, useEffect } from 'react';
import { FaTrophy, FaAward, FaUserCircle, FaChevronLeft, FaStar, FaMedal, FaCamera, FaTimes } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import ProfileDropdown from '../../components/ProfileDropdown/ProfileDropdown';
import styles from './Dashboard.module.css';

export default function Profile() {
    const [user, setUser] = useState(null);
    const [avatarPreview, setAvatarPreview] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [showPreviewModal, setShowPreviewModal] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [isModalClosing, setIsModalClosing] = useState(false);
    const fileInputRef = useRef(null);

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

    useEffect(() => {
        const loadUserData = async () => {
            try {
                const response = await api.get('/api/user/profile');
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

    useEffect(() => {
        const handleKeyDown = (e) => {
            if (showPreviewModal && e.key === 'Escape') {
                e.preventDefault();
            }
        };

        if (showPreviewModal) {
            window.addEventListener('keydown', handleKeyDown);
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'auto';
        }

        return () => {
            window.removeEventListener('keydown', handleKeyDown);
            document.body.style.overflow = 'auto';
        };
    }, [showPreviewModal]);

    const handleAvatarClick = () => fileInputRef.current.click();

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        setSelectedFile(file);

        const reader = new FileReader();
        reader.onloadend = () => {
            setAvatarPreview(reader.result);
            setShowPreviewModal(true);
        };
        reader.readAsDataURL(file);
    };

    const handleUploadAvatar = async () => {
        if (!selectedFile) return;
        try {
            setIsLoading(true);
            const formData = new FormData();
            formData.append('avatar', selectedFile);

            const response = await api.patch('api/user/avatar', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            setUser(prev => ({ ...prev, avatar: response.data.avatar }));
            setIsModalClosing(true);
            setTimeout(() => {
                setShowPreviewModal(false);
                setIsModalClosing(false);
            }, 300);
        } catch (error) {
            console.error('Erro ao atualizar avatar:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCancel = () => {
        setIsModalClosing(true);
        setTimeout(() => {
            setShowPreviewModal(false);
            setIsModalClosing(false);
            setAvatarPreview(user?.avatar || null);
        }, 300);
    };

    if (!user) return null;

    return (
        <div className={styles.dashboardContainer}>
            <header className={styles.header}>
                <div className={styles.headerContent}>
                    <Link to="/dashboard" className={styles.backButton}>
                        <FaChevronLeft /> Voltar
                    </Link>
                    <h1 className={styles.logo}>Meu Perfil</h1>
                    <ProfileDropdown user={user} />
                </div>
            </header>

            <main className={styles.profileContent}>
                <div className={styles.profileSection}>
                    <div className={styles.profileHeader}>
                        <div className={styles.avatarContainer} onClick={handleAvatarClick}>
                            {isLoading && (
                                <div className={styles.avatarLoading}>
                                    <div className={styles.spinner}></div>
                                </div>
                            )}
                            {avatarPreview ? (
                                <img src={avatarPreview} alt="Avatar" className={styles.avatarImage} />
                            ) : (
                                <div className={styles.avatarPlaceholder}>
                                    {user.first_name.charAt(0).toUpperCase()}
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
                            <h2>{user.first_name} {user.last_name}</h2>
                            <p className={styles.profileEmail}>{user.email}</p>
                        </div>
                    </div>

                    <div className={styles.statsGrid}>
                        <div className={styles.statCard}>
                            <h3>Ranking</h3>
                            <p className={styles.statValue}>#{user.rank ?? '-'}</p>
                        </div>
                        <div className={styles.statCard}>
                            <h3>Pontuação</h3>
                            <p className={styles.statValue}>{user.points ?? 0}</p>
                        </div>
                        <div className={styles.statCard}>
                            <h3>Desafios</h3>
                            <p className={styles.statValue}>{user.challengesCompleted ?? 0}</p>
                        </div>
                        <div className={styles.statCard}>
                            <h3>Precisão</h3>
                            <p className={styles.statValue}>{user.accuracy ?? '0%'}</p>
                        </div>
                    </div>
                </div>

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
                                <div className={styles.achievementIcon}>{achievement.icon}</div>
                                <h3>{achievement.name}</h3>
                                <p>{achievement.description}</p>
                                <div className={styles.achievementStatus}>
                                    {achievement.earned ? 'Conquistado' : 'Em progresso'}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

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

            {showPreviewModal && (
                <div className={`${styles.previewModal} ${isModalClosing ? styles.modalClosing : ''}`}>
                    <div className={styles.previewContent}>
                        <h3>Confirme seu novo avatar</h3>
                        <div className={styles.previewImageContainer}>
                            <img src={avatarPreview} alt="Preview do avatar" className={styles.previewImage} />
                        </div>
                        <p className={styles.previewText}>
                            Esta imagem substituirá seu avatar atual. Você confirma a alteração?
                        </p>
                        <div className={styles.previewActions}>
                            <button onClick={handleCancel} className={styles.cancelButton} disabled={isLoading}>
                                Cancelar
                            </button>
                            <button onClick={handleUploadAvatar} className={styles.confirmButton} disabled={isLoading}>
                                {isLoading ? <div className={styles.spinner}></div> : 'Confirmar Avatar'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
