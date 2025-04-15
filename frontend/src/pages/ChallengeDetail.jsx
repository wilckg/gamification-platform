import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import api from '../services/api';

export default function ChallengeDetail() {
  const { id } = useParams();
  const [challenge, setChallenge] = useState(null);

  useEffect(() => {
    const fetchChallenge = async () => {
      try {
        const response = await api.get(`/challenges/${id}/`);
        setChallenge(response.data);
      } catch (error) {
        console.error('Error fetching challenge:', error);
      }
    };
    fetchChallenge();
  }, [id]);

  if (!challenge) return <div>Loading...</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">{challenge.title}</h1>
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="mb-4">
          <span className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm mr-2">
            {challenge.points} pontos
          </span>
          <span className="text-gray-600">
            Dificuldade: {challenge.get_difficulty_display}
          </span>
        </div>
        <p className="text-gray-700 mb-6">{challenge.description}</p>
        {/* Área para resposta do desafio */}
        <textarea 
          className="w-full p-2 border rounded mb-4" 
          placeholder="Sua resposta aqui..."
        />
        <button className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
          Enviar Resposta
        </button>
      </div>
    </div>
  );
}