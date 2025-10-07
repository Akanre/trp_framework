// src/api.js
const API_BASE_URL = 'http://localhost:8000';

// Вспомогательная функция для запросов
async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    method: options.method || 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  if (config.body && typeof config.body === 'object') {
    config.body = JSON.stringify(config.body);
  }

  console.log('Making request to:', url, config);

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch (e) {
        // Не удалось распарсить JSON ошибку
      }
      throw new Error(errorMessage);
    }

    const data = await response.json();
    console.log('Response data:', data);
    return data;

  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

// Функция для запросов с авторизацией
function authRequest(token) {
  return (endpoint, options = {}) => {
    return request(endpoint, {
      ...options,
      headers: {
        'Authorization': `Bearer ${token}`,
        ...options.headers,
      },
    });
  };
}

export const authAPI = {
  // Вход в систему
  async login(username, password) {
    return request('/auth/login', {
      method: 'POST',
      body: { username, password },
    });
  },

  // Регистрация
  async register(userData) {
    return request('/auth/register', {
      method: 'POST',
      body: userData,
    });
  },

  // Получение профиля
  async getProfile(token) {
    const req = authRequest(token);
    return req('/users/me');
  },

  // Получение проектов
  async getProjects(token) {
    const req = authRequest(token);
    return req('/projects/');
  },

  // Создание проекта
  async createProject(token, projectData) {
    const req = authRequest(token);
    return req('/projects/', {
      method: 'POST',
      body: projectData,
    });
  },

  // Получение задач
  async getTasks(token) {
    const req = authRequest(token);
    return req('/tasks/');
  },

  // Создание задачи
  async createTask(token, taskData) {
    const req = authRequest(token);
    return req('/tasks/', {
      method: 'POST',
      body: taskData,
    });
  },
};

// Сохранение токена в localStorage
export const authStorage = {
  getToken() {
    return localStorage.getItem('authToken');
  },
  
  setToken(token) {
    localStorage.setItem('authToken', token);
  },
  
  removeToken() {
    localStorage.removeItem('authToken');
  },
  
  getStoredUser() {
    const user = localStorage.getItem('userData');
    return user ? JSON.parse(user) : null;
  },
  
  setStoredUser(user) {
    localStorage.setItem('userData', JSON.stringify(user));
  },
  
  removeStoredUser() {
    localStorage.removeItem('userData');
  },
  
  clear() {
    this.removeToken();
    this.removeStoredUser();
  }
};