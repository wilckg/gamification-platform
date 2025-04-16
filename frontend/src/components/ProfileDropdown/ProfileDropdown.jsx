import { useState } from 'react';
import { FaUserCircle, FaSignOutAlt, FaChevronDown } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import styles from '../../pages/Dashboard/Dashboard.module.css';

const ProfileDropdown = ({ user }) => {
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);

  const handleLogout = () => {
    // Implemente sua lógica de logout aqui
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    navigate('/login');
  };

  return (
    <div className={styles.profileContainer}>
      <span className={styles.userName}>{user.name}</span>
      <div 
        className={styles.profileDropdownTrigger}
        onClick={() => setIsOpen(!isOpen)}
      >
        <FaUserCircle className={styles.profileIcon} />
        <FaChevronDown className={`${styles.dropdownIcon} ${isOpen ? styles.rotate : ''}`} />
      </div>
      
      {isOpen && (
        <div className={styles.profileDropdown}>
          <div className={styles.profileInfo}>
            <p className={styles.profileEmail}>{user.email}</p>
            <p className={styles.profilePoints}>Pontos: {user.points}</p>
          </div>
          <button 
            className={styles.dropdownLink}
            onClick={() => {
              setIsOpen(false);
              navigate('/profile');
            }}
          >
            <FaUserCircle /> Meu Perfil
          </button>
          <button 
            className={styles.logoutButton}
            onClick={handleLogout}
          >
            <FaSignOutAlt /> Sair
          </button>
        </div>
      )}
    </div>
  );
};

export default ProfileDropdown;