// frontend/src/pages/Challenges.js
import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import ChallengeCard from '../components/ChallengeCard';
import ChallengeModal from '../components/ChallengeModal';

const Challenges = () => {
  const { user } = useAuth();
  const [challenges, setChallenges] = useState([]);
  const [selectedChallenge, setSelectedChallenge] = useState(null);
  const [userChallenges, setUserChallenges] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [challengesRes, userChallengesRes] = await Promise.all([
          api.get('challenges/'),
          user ? api.get('user-challenges/') : Promise.resolve({ data: [] }),
        ]);
        setChallenges(challengesRes.data);
        setUserChallenges(userChallengesRes.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [user]);

  const handleChallengeSubmit = async (answer) => {
    try {
      const response = await api.post('user-challenges/', {
        challenge: selectedChallenge.id,
        answer,
      });
      setUserChallenges([...userChallenges, response.data]);
      setSelectedChallenge(null);
    } catch (error) {
      console.error('Error submitting challenge:', error);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Desafios Disponíveis</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {challenges.map((challenge) => {
          const isCompleted = userChallenges.some(
            (uc) => uc.challenge.id === challenge.id && uc.is_correct
          );
          return (
            <ChallengeCard
              key={challenge.id}
              challenge={challenge}
              isCompleted={isCompleted}
              onClick={() => setSelectedChallenge(challenge)}
            />
          );
        })}
      </div>

      {selectedChallenge && (
        <ChallengeModal
          challenge={selectedChallenge}
          onSubmit={handleChallengeSubmit}
          onClose={() => setSelectedChallenge(null)}
        />
      )}
    </div>
  );
};

export default Challenges;