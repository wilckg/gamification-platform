import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FaArrowLeft, FaCode, FaQuestionCircle, FaCheck, FaChevronRight, FaPython } from 'react-icons/fa';
import ProfileDropdown from '../../components/ProfileDropdown/ProfileDropdown';
import styles from './ChallengeDetail.module.css';

const ChallengeDetail = () => {
  const { challengeId } = useParams();
  const navigate = useNavigate();
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [codeSolution, setCodeSolution] = useState('');
  const [textAnswer, setTextAnswer] = useState('');

  // Dados mockados - Exemplo com Python
  const [challenge, setChallenge] = useState({
    id: challengeId,
    title: 'Manipulação de Listas em Python',
    description: 'Exercícios práticos com listas em Python',
    difficulty: 'Médio',
    type: 'description', // Pode ser: 'description', 'code', 'single_choice', 'multiple_choice'
    language: 'python',
    instructions: 'Complete as funções abaixo conforme solicitado',
    starterCode: 'def dobrar_numeros(lista):\n    """Retorna uma nova lista com cada número multiplicado por 2"""\n    # Implemente sua solução aqui\n    pass\n\ndef filtrar_pares(lista):\n    """Retorna apenas os números pares da lista"""\n    # Implemente sua solução aqui\n    pass',
    questions: [
      {
        id: 1,
        text: 'Qual método Python é usado para adicionar um item ao final de uma lista?',
        options: [
          { id: 1, text: 'lista.insert()', isCorrect: false },
          { id: 2, text: 'lista.append()', isCorrect: true },
          { id: 3, text: 'lista.add()', isCorrect: false }
        ]
      }
    ],
    submission: null
  });

  // Simula carregamento da API
  useEffect(() => {
    // Aqui você faria a chamada à API:
    // const loadChallenge = async () => {
    //   const response = await api.get(`/challenges/${challengeId}`);
    //   setChallenge(response.data);
    // };
    // loadChallenge();
  }, [challengeId]);

  const handleOptionSelect = (optionId, isMultiple) => {
    if (isMultiple) {
      setSelectedOptions(prev => 
        prev.includes(optionId) 
          ? prev.filter(id => id !== optionId) 
          : [...prev, optionId]
      );
    } else {
      setSelectedOptions([optionId]);
    }
  };

  const handleSubmit = () => {
    // Lógica de submissão para a API
    console.log('Submetendo:', {
      challengeId,
      code: codeSolution,
      textAnswer,
      selectedOptions
    });
    
    // Simula sucesso na submissão
    setChallenge(prev => ({
      ...prev,
      submission: { status: 'submitted' }
    }));
  };

  const renderChallengeContent = () => {
    switch (challenge.type) {
      case 'description':
        return (
          <div className={styles.descriptionChallenge}>
            <h3>Sua Resposta</h3>
            <textarea
              className={styles.textAnswer}
              value={textAnswer}
              onChange={(e) => setTextAnswer(e.target.value)}
              placeholder="Digite sua resposta aqui..."
              rows={8}
            />
          </div>
        );

      case 'code':
        return (
          <div className={styles.codeChallenge}>
            <h3>Sua Solução</h3>
            <div className={styles.codeEditorContainer}>
              <div className={styles.codeLanguage}>
                <FaPython /> Python
              </div>
              <textarea
                className={styles.codeEditor}
                value={codeSolution || challenge.starterCode}
                onChange={(e) => setCodeSolution(e.target.value)}
                spellCheck="false"
              />
            </div>
          </div>
        );

      case 'single_choice':
      case 'multiple_choice':
        return (
          <div className={styles.choiceChallenge}>
            <h3>Questões</h3>
            {challenge.questions.map((question) => (
              <div key={question.id} className={styles.questionContainer}>
                <p className={styles.questionText}>{question.text}</p>
                <div className={styles.optionsContainer}>
                  {question.options.map((option) => (
                    <div
                      key={option.id}
                      className={`${styles.option} ${
                        selectedOptions.includes(option.id) ? styles.selected : ''
                      }`}
                      onClick={() => handleOptionSelect(option.id, challenge.type === 'multiple_choice')}
                    >
                      <div className={styles.optionSelector}>
                        {challenge.type === 'multiple_choice' ? (
                          <div className={styles.checkbox}>
                            {selectedOptions.includes(option.id) && <FaCheck />}
                          </div>
                        ) : (
                          <div className={styles.radio} />
                        )}
                      </div>
                      <div className={styles.optionText}>{option.text}</div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        );

      default:
        return <p>Tipo de desafio não reconhecido</p>;
    }
  };

  return (
    <div className={styles.container}>
      {/* Header consistente */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <button onClick={() => navigate(-1)} className={styles.backButton}>
            <FaArrowLeft /> Voltar
          </button>
          <h1 className={styles.logo}>{challenge.title}</h1>
          <ProfileDropdown user={{ name: 'Usuário', points: 1200 }} />
        </div>
      </header>

      <main className={styles.mainContent}>
        <div className={styles.difficultyBadge}>
          Dificuldade: <span className={styles[challenge.difficulty.toLowerCase()]}>{challenge.difficulty}</span>
          <span className={styles.typeBadge}>
            {{
              'description': 'Descritivo',
              'code': 'Código Python',
              'single_choice': 'Escolha Única',
              'multiple_choice': 'Múltipla Escolha'
            }[challenge.type]}
          </span>
        </div>

        <div className={styles.contentSection}>
          <h3>Descrição</h3>
          <p className={styles.description}>{challenge.description}</p>

          <h3>Instruções</h3>
          <pre className={styles.instructions}>{challenge.instructions}</pre>

          {challenge.type === 'code' && (
            <>
              <h3>Código Inicial</h3>
              <pre className={styles.codeBlock}>
                {challenge.starterCode}
              </pre>
            </>
          )}

          {renderChallengeContent()}

          <div className={styles.actions}>
            {challenge.submission ? (
              <div className={styles.submissionStatus}>
                <FaCheck /> Desafio enviado para correção
              </div>
            ) : (
              <button 
                className={styles.submitButton}
                onClick={handleSubmit}
                disabled={
                  (challenge.type === 'description' && !textAnswer.trim()) ||
                  (challenge.type === 'code' && !codeSolution.trim()) ||
                  ((challenge.type === 'single_choice' || challenge.type === 'multiple_choice') && selectedOptions.length === 0)
                }
              >
                <FaCheck /> Submeter Solução
              </button>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default ChallengeDetail;