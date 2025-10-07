// src/components/LoginPage.js
import React, { useState } from 'react';
import { authAPI } from '../api';
import './LoginPage.css';

const LoginPage = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    role: 1
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'role' ? parseInt(value) : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      console.log('Form data:', formData);

      if (!formData.username || !formData.password) {
        setError('Заполните все обязательные поля');
        return;
      }

      if (!isLogin) {
        // Валидация для регистрации
        if (!formData.email) {
          setError('Email обязателен для регистрации');
          return;
        }
        if (formData.password !== formData.confirmPassword) {
          setError('Пароли не совпадают');
          return;
        }
        if (formData.password.length < 6) {
          setError('Пароль должен быть не менее 6 символов');
          return;
        }
      }

      let response;
      
      if (isLogin) {
        // Вход
        console.log('Attempting login...');
        response = await authAPI.login(formData.username, formData.password);
        console.log('Login response:', response);
      } else {
        // Регистрация
        console.log('Attempting registration...');
        const { confirmPassword, ...registerData } = formData;
        response = await authAPI.register(registerData);
        console.log('Registration response:', response);
        
        // После успешной регистрации автоматически входим
        if (response.id) {
          console.log('Auto-login after registration...');
          const loginResponse = await authAPI.login(formData.username, formData.password);
          response = loginResponse;
        }
      }

      // Вызываем колбэк с данными пользователя и токеном
      console.log('Final response for onLogin:', response);
      onLogin(response.user, response.access_token);

    } catch (err) {
      console.error('Auth error:', err);
      setError(err.message || 'Произошла ошибка. Попробуйте снова.');
    } finally {
      setLoading(false);
    }
  };

  const switchMode = () => {
    setIsLogin(!isLogin);
    setError('');
    setFormData({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      full_name: '',
      role: 1
    });
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h2>{isLogin ? 'Вход в систему' : 'Регистрация'}</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Логин *</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Введите логин"
              disabled={loading}
              required
            />
          </div>

          {!isLogin && (
            <>
              <div className="form-group">
                <label htmlFor="email">Email *</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Введите email"
                  disabled={loading}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="full_name">Полное имя</label>
                <input
                  type="text"
                  id="full_name"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  placeholder="Введите ваше имя"
                  disabled={loading}
                />
              </div>
            </>
          )}

          <div className="form-group">
            <label htmlFor="password">Пароль *</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Введите пароль"
              disabled={loading}
              required
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="confirmPassword">Подтвердите пароль *</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="Повторите пароль"
                disabled={loading}
                required
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="role">Роль</label>
            <select
              id="role"
              name="role"
              value={formData.role}
              onChange={handleChange}
              disabled={loading}
            >
              <option value="1">Инженер</option>
              <option value="2">Менеджер</option>
              <option value="3">Руководитель</option>
            </select>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button 
            type="submit" 
            className="login-button"
            disabled={loading}
          >
            {loading ? 'Загрузка...' : (isLogin ? 'Войти' : 'Зарегистрироваться')}
          </button>
        </form>

        <div className="switch-mode">
          <p>
            {isLogin ? 'Нет аккаунта?' : 'Уже есть аккаунт?'}
            <button 
              type="button" 
              className="switch-button"
              onClick={switchMode}
              disabled={loading}
            >
              {isLogin ? 'Зарегистрироваться' : 'Войти'}
            </button>
          </p>
        </div>

        <div className="debug-info">
          <h4>Отладочная информация:</h4>
          <p>Бэкенд: http://localhost:8000</p>
          <p>Фронтенд: http://localhost:4001</p>
          <p>Статус: {loading ? 'Загрузка...' : 'Готов'}</p>
        </div>

        <div className="role-info">
          <h4>Описание ролей:</h4>
          <ul>
            <li><strong>Инженер:</strong> Работа с задачами, техническая реализация</li>
            <li><strong>Менеджер:</strong> Управление проектами, координация команды</li>
            <li><strong>Руководитель:</strong> Контроль, отчетность, принятие решений</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;