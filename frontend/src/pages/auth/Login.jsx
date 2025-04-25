import { useState } from 'react';
import { Link } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';
import AuthLayout from '../../components/auth/AuthLayout';
import LoginForm from '../../components/auth/LoginForm';
import styles from './Auth.module.css';

const Login = () => {
  const { login } = useAuth();
  const [error, setError] = useState('');

  const handleSubmit = async (formData) => {
    const { success, error } = await login(formData.email, formData.password);
    if (!success) {
      setError(error);
    }
  };

  return (
    <AuthLayout
      icon="sign-in-alt"
      title="Acesse sua conta"
      footer={
        <div className={styles.authFooter}>
          <Link to="/forgot-password" className={styles.authLink}>
            Esqueceu sua senha?
          </Link>
          {/* <p>
            Não tem uma conta?{' '}
            <Link to="/register" className={styles.authLink}>
              Cadastre-se
            </Link>
          </p> */}
        </div>
      }
    >
      <LoginForm onSubmit={handleSubmit} error={error} />
    </AuthLayout>
  );
};

export default Login;