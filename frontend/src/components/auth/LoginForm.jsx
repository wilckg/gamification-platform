import { useState } from 'react';
import PasswordInput from './PasswordInput';
import LoadingSpinner from '../ui/LoadingSpinner';
import { FaEnvelope } from 'react-icons/fa';
import styles from '../../pages/auth/Auth.module.css';

const LoginForm = ({ onSubmit, error }) => {
  const [formData, setFormData] = useState({ 
    email: '', 
    password: '' 
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    await onSubmit(formData);
    setLoading(false);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <form onSubmit={handleSubmit} className={styles.authForm}>
      {error && <div className={styles.authError}>{error}</div>}

      <div className={styles.formGroup}>
        <label htmlFor="email">
          <FaEnvelope className={styles.inputIcon} />
          E-mail
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          value={formData.email}
          onChange={handleChange}
          placeholder="Digite seu e-mail"
        />
      </div>

      <PasswordInput
        id="password"
        name="password"
        value={formData.password}
        onChange={handleChange}
        placeholder="Digite sua senha"
      />

      <button 
        type="submit" 
        className={`${styles.submitButton} ${loading ? styles.loading : ''}`}
        disabled={loading}
      >
        {loading ? <LoadingSpinner size={20} /> : 'Entrar'}
      </button>
    </form>
  );
};

export default LoginForm;