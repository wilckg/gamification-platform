import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { FaLock, FaCheck } from 'react-icons/fa';
import styles from './Auth.module.css';

export default function ResetPassword() {
  const { uidb64, token } = useParams();
  const [formData, setFormData] = useState({ 
    new_password: '', 
    confirm_password: '' 
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.new_password !== formData.confirm_password) {
      setError('As senhas não coincidem');
      return;
    }
    
    try {
      await api.post(`/auth/password-reset-confirm/${uidb64}/${token}/`, {
        new_password: formData.new_password
      });
      setMessage('Senha redefinida com sucesso! Redirecionando...');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError('Link inválido ou expirado');
    }
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authCard}>
        <div className={styles.authHeader}>
          <FaLock className={styles.authIcon} />
          <h2>Redefinir senha</h2>
        </div>

        {message && <div className={styles.authSuccess}>{message}</div>}
        {error && <div className={styles.authError}>{error}</div>}

        <form onSubmit={handleSubmit} className={styles.authForm}>
          <div className={styles.formGroup}>
            <label htmlFor="new_password">
              <FaLock className={styles.inputIcon} />
              Nova senha
            </label>
            <input
              id="new_password"
              name="new_password"
              type="password"
              required
              value={formData.new_password}
              onChange={(e) => setFormData({...formData, new_password: e.target.value})}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="confirm_password">
              <FaCheck className={styles.inputIcon} />
              Confirmar nova senha
            </label>
            <input
              id="confirm_password"
              name="confirm_password"
              type="password"
              required
              value={formData.confirm_password}
              onChange={(e) => setFormData({...formData, confirm_password: e.target.value})}
            />
          </div>

          <button type="submit" className={styles.submitButton}>
            Redefinir senha
          </button>
        </form>
      </div>
    </div>
  );
}