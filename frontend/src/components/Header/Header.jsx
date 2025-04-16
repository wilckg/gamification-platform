import styles from './Header.module.css';
import senaiLogo from '../../../public/images/SENAI_São_Paulo_logo.png';
import santanaLogo from '../../../public/images/logo-santana.jpg';
import fabricaLogo from '../../../public/images/logo-fabrica.jpg';
import platformLogo from '../../../public/images/logo-plataforma.jpg';
import { FaSignInAlt } from 'react-icons/fa';

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.headerContainer}>
        {/* Logo da Plataforma (Esquerda) */}
        <div className={styles.platformLogo}>
          <img src={platformLogo} alt="Plataforma de Gamificação" className={styles.mainLogo} />
        </div>
        
        {/* Logos dos Parceiros (Centro) */}
        <div className={styles.partnerLogos}>
          <img src={senaiLogo} alt="Logo SENAI" className={styles.partnerLogo} />
          <img src={santanaLogo} alt="Santana de Parnaíba" className={styles.partnerLogo} />
          <img src={fabricaLogo} alt="Fábrica de Programadores" className={styles.partnerLogo} />
        </div>
        
        {/* Botão de Login (Direita) */}
        <div className={styles.loginContainer}>
          <a href="/login" className={styles.loginButton} title="Acessar sua conta">
            <FaSignInAlt className={styles.loginIcon} />
            <span>Entrar</span>
          </a>
        </div>
      </div>
    </header>
  );
}