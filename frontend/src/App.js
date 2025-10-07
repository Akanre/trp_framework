// src/App.js
import React, { useState, useEffect } from 'react';
import LoginPage from './components/LoginPage';
import Dashboard from './components/Dashboard';
import { authStorage } from './api';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Проверяем сохраненную сессию при загрузке
  useEffect(() => {
    const checkAuth = async () => {
      const token = authStorage.getToken();
      const storedUser = authStorage.getStoredUser();
      
      if (token && storedUser) {
        try {
          // Можно добавить проверку токена через API
          setUser(storedUser);
        } catch (error) {
          console.error('Auth check failed:', error);
          authStorage.clear();
        }
      }
      
      setLoading(false);
    };

    checkAuth();
  }, []);

  const handleLogin = (userData, token) => {
    setUser(userData);
    authStorage.setToken(token);
    authStorage.setStoredUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
    authStorage.clear();
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner">Загрузка...</div>
      </div>
    );
  }

  return (
    <div className="App">
      {!user ? (
        <LoginPage onLogin={handleLogin} />
      ) : (
        <Dashboard user={user} onLogout={handleLogout} />
      )}
    </div>
  );
}

export default App;