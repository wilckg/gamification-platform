import { FaSpinner } from 'react-icons/fa';
import styles from '../../pages/auth/Auth.module.css';

const LoadingSpinner = ({ size = 20 }) => {
  return (
    <div className={styles.spinnerContainer}>
      <FaSpinner 
        className={styles.spinner} 
        style={{ fontSize: size }} 
      />
    </div>
  );
};

export default LoadingSpinner;