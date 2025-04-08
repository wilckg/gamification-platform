import { useState, useEffect } from 'react';
import api from '../../services/api';

export default function ChallengeManager() {
  const [challenges, setChallenges] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    points: 100,
    difficulty: 'E'
  });

  useEffect(() => {
    const fetchChallenges = async () => {
      try {
        const response = await api.get('challenges/');
        setChallenges(response.data);
      } catch (error) {
        console.error('Error fetching challenges:', error);
      }
    };
    fetchChallenges();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('challenges/', formData);
      // Atualiza a lista após criação
      const response = await api.get('challenges/');
      setChallenges(response.data);
    } catch (error) {
      console.error('Error creating challenge:', error);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Manage Challenges</h2>
      
      {/* Formulário de criação */}
      <form onSubmit={handleSubmit} className="mb-8 p-4 border rounded">
        <h3 className="font-bold mb-2">Create New Challenge</h3>
        {/* Campos do formulário... */}
      </form>

      {/* Lista de desafios existentes */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {challenges.map(challenge => (
          <div key={challenge.id} className="border p-4 rounded">
            <h3 className="font-bold">{challenge.title}</h3>
            <p>Points: {challenge.points}</p>
            {/* Mais detalhes... */}
          </div>
        ))}
      </div>
    </div>
  );
}