import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { FaKey, FaEnvelope, FaArrowLeft } from 'react-icons/fa';
import styles from './Auth.module.css';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/auth/password-reset/', { email });
      setMessage('Se o e-mail existir, um link de redefinição foi enviado');
      setError('');
    } catch (err) {
      setError('Ocorreu um erro ao processar sua solicitação');
      setMessage('');
    }
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authCard}>
        <div className={styles.authHeader}>
          <FaKey className={styles.authIcon} />
          <h2>Recuperação de senha</h2>
        </div>

        {message && <div className={styles.authSuccess}>{message}</div>}
        {error && <div className={styles.authError}>{error}</div>}

        <form onSubmit={handleSubmit} className={styles.authForm}>
          <div className={styles.formGroup}>
            <label htmlFor="email">
              <FaEnvelope className={styles.inputIcon} />
              E-mail cadastrado
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <button type="submit" className={styles.submitButton}>
            Enviar link de recuperação
          </button>
        </form>

        <div className={styles.authFooter}>
          <Link to="/login" className={styles.authLink}>
            <FaArrowLeft className={styles.linkIcon} />
            Voltar para login
          </Link>
        </div>
      </div>
    </div>
  );
}