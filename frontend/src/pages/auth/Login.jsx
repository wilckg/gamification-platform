import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { FaSignInAlt, FaLock, FaEnvelope } from 'react-icons/fa';
import styles from './Auth.module.css';

export default function Login() {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/auth/login/', formData);
      localStorage.setItem('access', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);
      navigate('/dashboard');
    } catch (err) {
      setError('Credenciais inválidas');
    }
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authCard}>
        <div className={styles.authHeader}>
          <FaSignInAlt className={styles.authIcon} />
          <h2>Acesse sua conta</h2>
        </div>

        {error && <div className={styles.authError}>{error}</div>}

        <form onSubmit={handleSubmit} className={styles.authForm}>
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
              onChange={(e) => setFormData({...formData, email: e.target.value})}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="password">
              <FaLock className={styles.inputIcon} />
              Senha
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
            />
          </div>

          <div className={styles.formFooter}>
            <Link to="/forgot-password" className={styles.forgotLink}>
              Esqueceu sua senha?
            </Link>
          </div>

          <button type="submit" className={styles.submitButton}>
            Entrar
          </button>
        </form>

        {/* <div className={s tyles.authFooter}>
          <p>Não tem uma conta? <Link to="/register" className={styles.authLink}>Cadastre-se</Link></p>
        </div> */}
      </div>
    </div>
  );
}