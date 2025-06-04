import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FaArrowLeft, FaPython, FaCheck } from 'react-icons/fa';
import ProfileDropdown from '../../components/ProfileDropdown/ProfileDropdown';
import api from '../../services/api';
import styles from './ChallengeDetail.module.css';

const ChallengeDetail = () => {
  const { challengeId } = useParams();
  const navigate = useNavigate();

  const [challenge, setChallenge] = useState(null);
  const [user, setUser] = useState(null);
  const [code, setCode] = useState('');
  const [answer, setAnswer] = useState('');
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [submitted, setSubmitted] = useState(false);

  const [difficulty, setDifficulty] = useState({
    "EASY": "Fácil",
    "MEDIUM": "Médio",
    "HARD": "Difícil"
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [userRes, challengeRes, userChallengesRes] = await Promise.all([
          api.get('/api/user/profile'),
          api.get(`/api/challenges/challenges/${challengeId}/`),
          api.get('/api/challenges/user-challenges/')
        ]);

        setUser(userRes.data);
        setChallenge(challengeRes.data);

        const existing = userChallengesRes.data.find(sub => sub.challenge.id === parseInt(challengeId));
        if (existing) {
          setSubmitted(true);
          if (existing.code) setCode(existing.code);
          if (existing.answer) setAnswer(existing.answer);
          if (Array.isArray(existing.selected_options)) {
            const optionIds = existing.selected_options.map(opt => opt.id);
            setSelectedOptions(optionIds);
          }
        }
      } catch (err) {
        console.error('Erro ao carregar desafio:', err);
      }
    };

    fetchData();
  }, [challengeId]);

  const handleOptionSelect = (optionId, isMultiple) => {
    setSelectedOptions(prev =>
      isMultiple
        ? prev.includes(optionId) ? prev.filter(id => id !== optionId) : [...prev, optionId]
        : [optionId]
    );
  };

  const handleSubmit = async () => {
    const payload = { challenge: challenge.id };

    if (challenge.challenge_type === 'DESCRIPTION' && answer.trim()) {
      payload.answer = answer.trim();
    }

    if (challenge.challenge_type === 'CODE' && code.trim()) {
      payload.code = code.trim();
    }

    if (['SINGLE_CHOICE', 'MULTIPLE_CHOICE'].includes(challenge.challenge_type)) {
      payload.selected_options = selectedOptions.map(Number);
    }

    try {
      await api.post('/api/challenges/user-challenges/', payload);
      setSubmitted(true);
    } catch (err) {
      console.error('Erro ao submeter desafio:', err);
      alert('Erro ao enviar o desafio. Verifique suas respostas e tente novamente.');
    }
  };

  if (!challenge || !user) return null;

  const renderContent = () => {
    switch (challenge.challenge_type) {
      case 'DESCRIPTION':
        return (
          <textarea
            className={styles.textAnswer}
            value={answer}
            onChange={e => setAnswer(e.target.value)}
            placeholder="Digite sua resposta aqui..."
            rows={8}
            disabled={submitted}
          />
        );

      case 'CODE':
        return (
          <div className={styles.codeEditorContainer}>
            <div className={styles.codeLanguage}><FaPython /> Python</div>
            <textarea
              className={styles.codeEditor}
              value={code || challenge.starter_code}
              onChange={e => setCode(e.target.value)}
              spellCheck="false"
              disabled={submitted}
            />
          </div>
        );

      case 'SINGLE_CHOICE':
      case 'MULTIPLE_CHOICE':
        return (
          <div className={styles.choiceChallenge}>
            <h3>Questões</h3>
            {Array.isArray(challenge.questions) && challenge.questions.length > 0 ? (
              challenge.questions.map(question => (
                <div key={question.id} className={styles.questionContainer}>
                  <p className={styles.questionText}>{question.text}</p>
                  <div className={styles.optionsContainer}>
                    {question.options.map(option => (
                      <div
                        key={option.id}
                        className={`${styles.option} ${selectedOptions.includes(option.id) ? styles.selected : ''}`}
                        onClick={() => !submitted && handleOptionSelect(option.id, challenge.challenge_type === 'MULTIPLE_CHOICE')}
                      >
                        <div className={styles.optionSelector}>
                          {challenge.challenge_type === 'MULTIPLE_CHOICE'
                            ? <div className={styles.checkbox}>{selectedOptions.includes(option.id) && <FaCheck />}</div>
                            : <div className={styles.radio} />}
                        </div>
                        <div className={styles.optionText}>{option.text}</div>
                      </div>
                    ))}
                  </div>
                </div>
              ))
            ) : (
              <p>Nenhuma pergunta disponível.</p>
            )}
          </div>
        );

      default:
        return <p>Tipo de desafio não reconhecido</p>;
    }
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <button onClick={() => navigate(-1)} className={styles.backButton}>
            <FaArrowLeft /> Voltar
          </button>
          <h1 className={styles.logo}>{challenge.title}</h1>
          <ProfileDropdown user={user} />
        </div>
      </header>

      <main className={styles.mainContent}>
        <div className={styles.difficultyBadge}>
          Dificuldade: <span className={styles[difficulty[challenge.difficulty.toLowerCase()]]}>{difficulty[challenge.difficulty]}</span>
          <span className={styles.typeBadge}>
            {({
              DESCRIPTION: 'Descritivo',
              CODE: 'Código',
              SINGLE_CHOICE: 'Escolha Única',
              MULTIPLE_CHOICE: 'Múltipla Escolha'
            })[challenge.challenge_type]}
          </span>
        </div>

        <div className={styles.contentSection}>
          <h3>Descrição</h3>
          <p className={styles.description}>{challenge.description}</p>

          <h3>Instruções</h3>
          <pre className={styles.instructions}>{challenge.instructions || 'Siga as instruções do desafio.'}</pre>

          {challenge.challenge_type === 'CODE' && challenge.starter_code && (
            <>
              <h3>Código Inicial</h3>
              <pre className={styles.codeBlock}>{challenge.starter_code}</pre>
            </>
          )}

          {renderContent()}

          <div className={styles.actions}>
            {submitted ? (
              <div className={styles.submissionStatus}>
                <FaCheck /> Desafio enviado
              </div>
            ) : (
              <button
                className={styles.submitButton}
                onClick={handleSubmit}
                disabled={
                  (challenge.challenge_type === 'DESCRIPTION' && !answer.trim()) ||
                  (challenge.challenge_type === 'CODE' && !code.trim()) ||
                  (['SINGLE_CHOICE', 'MULTIPLE_CHOICE'].includes(challenge.challenge_type) && selectedOptions.length === 0)
                }
              >
                <FaCheck /> Submeter
              </button>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default ChallengeDetail;
