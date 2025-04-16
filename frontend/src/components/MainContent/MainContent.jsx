import styles from './MainContent.module.css';
import HighlightCard from '../HighlightCard/HighlightCard';

export default function MainContent() {
  return (
    <div className={styles.mainContainer}>
      {/* Seção de Introdução */}
      <section className={styles.introSection}>
        <div className={styles.introContent}>
          <h1 className={styles.introTitle}>Plataforma de Gamificação Educacional</h1>
          <div className={styles.introText}>
            <p>
              Nossa plataforma transforma o aprendizado de programação em uma experiência envolvente, 
              combinando educação de qualidade com elementos de jogos para maximizar o engajamento e 
              a retenção de conhecimento.
            </p>
            <p>
              Desenvolvida em parceria pelo SENAI Santana de Parnaíba e a Fábrica de Programadores, 
              oferecemos um ambiente onde cada conquista acadêmica se traduz em progresso visível.
            </p>
          </div>
        </div>
      </section>

      {/* Seção de Benefícios */}
      <section className={styles.benefitsSection}>
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Benefícios da Plataforma</h2>
          <p className={styles.sectionSubtitle}>Uma experiência de aprendizado completa e engajadora</p>
        </div>

        <div className={styles.cardsContainer}>
          <HighlightCard 
            title="Aprendizado Interativo" 
            description="Conquiste pontos, medalhas e suba de nível enquanto adquire novos conhecimentos em programação." 
            icon="📚"
            color="#4CAF50"
          />
          <HighlightCard 
            title="Desafios Reais" 
            description="Resolva problemas práticos do mercado de trabalho e mostre suas habilidades." 
            icon="💻"
            color="#2196F3"
          />
          <HighlightCard 
            title="Ranking Competitivo" 
            description="Compare seu desempenho com outros alunos e incentive-se a melhorar." 
            icon="🏆"
            color="#FF9800"
          />
        </div>
      </section>

      {/* Seção de Chamada para Ação */}
      <section className={styles.ctaSection}>
        <h2 className={styles.ctaTitle}>Pronto para transformar seu aprendizado?</h2>
        <a href="/register" className={styles.ctaButton}>Comece Agora</a>
      </section>
    </div>
  );
}