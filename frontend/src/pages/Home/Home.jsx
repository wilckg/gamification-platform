import styles from './Home.module.css';
import Header from '../../components/Header/Header';
import Footer from '../../components/Footer/Footer';
import MainContent from '../../components/MainContent/MainContent';

export default function Home() {
  return (
    <div className={styles.homeContainer}>
      <Header />
      <MainContent />
      <Footer />
    </div>
  );
}