import styles from './Footer.module.css';
import senaiLogo from '../../../public/images/SENAI_São_Paulo_logo.png';
import santanaLogo from '../../../public/images/logo-santana.jpg';
import fabricaLogo from '../../../public/images/logo-fabrica.jpg';

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.footerLogos}>
        <img src={senaiLogo} alt="Logo SENAI" className={styles.logo} />
        <img src={santanaLogo} alt="Santana de Parnaíba" className={styles.logo} />
        <img src={fabricaLogo} alt="Fábrica de Programadores" className={styles.logo} />
      </div>
      <p>© 2023 Gamification Platform - SENAI Santana de Parnaíba | Fábrica de Programadores</p>
    </footer>
  );
}