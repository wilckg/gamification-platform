import { FaSignInAlt, FaKey, FaEnvelope, FaLock } from 'react-icons/fa';
import styles from '../../pages/auth/Auth.module.css';

const iconComponents = {
  'sign-in-alt': FaSignInAlt,
  'key': FaKey,
  'envelope': FaEnvelope,
  'lock': FaLock
};

const AuthLayout = ({ children, icon, title, footer }) => {
  const IconComponent = iconComponents[icon] || FaSignInAlt;

  return (
    <div className={styles.authContainer}>
      <div className={styles.authCard}>
        <div className={styles.authHeader}>
          <IconComponent className={styles.authIcon} />
          <h2>{title}</h2>
        </div>
        {children}
        {footer}
      </div>
    </div>
  );
};

export default AuthLayout;