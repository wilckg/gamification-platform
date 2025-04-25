import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem('access_token');
      const userData = localStorage.getItem('user_data');
      
      if (token && userData) {
        try {
          await api.get('/api/auth/verify/');
          setUser(JSON.parse(userData));
        } catch (err) {
          logout();
        }
      }
      setLoading(false);
    };
    
    loadUser();
  }, []);

  const login = async (email, password) => {
    try {
      const response = await api.post('/api/auth/aluno/login/', { email, password });
      
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      localStorage.setItem('user_data', JSON.stringify({
        email: response.data.email,
        firstName: response.data.first_name,
        lastName: response.data.last_name
      }));
      
      setUser({
        email: response.data.email,
        firstName: response.data.first_name,
        lastName: response.data.last_name
      });
      
      navigate('/dashboard');
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Erro ao fazer login' 
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
    setUser(null);
    navigate('/login');
  };

  return { user, loading, login, logout };
};

export default useAuth;