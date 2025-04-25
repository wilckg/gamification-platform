import { useState } from 'react';
import { FaEye, FaEyeSlash, FaLock } from 'react-icons/fa';
import styles from '../../pages/auth/Auth.module.css';

const PasswordInput = ({ value, onChange, placeholder, id, name, error }) => {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className={`${styles.formGroup} ${error ? styles.invalid : ''}`}>
      <label htmlFor={id}>
        <FaLock className={styles.inputIcon} />
        Senha
      </label>
      <div className={styles.passwordInput}>
        <input
          id={id}
          name={name}
          type={showPassword ? 'text' : 'password'}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
        />
        <button
          type="button"
          className={styles.passwordToggle}
          onClick={() => setShowPassword(!showPassword)}
        >
          {showPassword ? <FaEyeSlash /> : <FaEye />}
        </button>
      </div>
      {error && <span className={styles.errorMessage}>{error}</span>}
    </div>
  );
};

export default PasswordInput;