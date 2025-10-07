// src/components/Dashboard.js
import React, { useState, useEffect } from 'react';
import { authAPI, authStorage } from '../api';
import './Dashboard.css';

const Dashboard = ({ user, onLogout }) => {
  const [projects, setProjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('projects');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const token = authStorage.getToken();
    
    try {
      const [projectsData, tasksData] = await Promise.all([
        authAPI.getProjects(token),
        authAPI.getTasks(token)
      ]);
      
      setProjects(projectsData);
      setTasks(tasksData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getDashboardContent = () => {
    switch (user.role) {
      case 1: // Инженер
        return (
          <div className="engineer-dashboard">
            <h3>Мои задачи</h3>
            {tasks.filter(task => task.assigned_to === user.id).map(task => (
              <div key={task.id} className="task-card">
                <h4>{task.title}</h4>
                <p>{task.description}</p>
                <span className={`status ${task.status}`}>{task.status}</span>
                <span className={`priority ${task.priority}`}>{task.priority}</span>
              </div>
            ))}
          </div>
        );
      
      case 2: // Менеджер
        return (
          <div className="manager-dashboard">
            <h3>Проекты под управлением</h3>
            <div className="dashboard-cards">
              {projects.map(project => (
                <div key={project.id} className="card">
                  <h4>{project.name}</h4>
                  <p>{project.description}</p>
                  <span className={`status ${project.status}`}>{project.status}</span>
                </div>
              ))}
            </div>
          </div>
        );
      
      case 3: // Руководитель
        return (
          <div className="director-dashboard">
            <h3>Обзор системы</h3>
            <div className="stats-grid">
              <div className="stat-card">
                <h4>Всего проектов</h4>
                <div className="stat-number">{projects.length}</div>
              </div>
              <div className="stat-card">
                <h4>Всего задач</h4>
                <div className="stat-number">{tasks.length}</div>
              </div>
              <div className="stat-card">
                <h4>Активных пользователей</h4>
                <div className="stat-number">-</div>
              </div>
            </div>
          </div>
        );
      
      default:
        return <div>Неизвестная роль</div>;
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <header className="dashboard-header">
          <div className="user-info">
            <h2>Загрузка...</h2>
          </div>
        </header>
        <div className="loading">Загрузка данных...</div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="user-info">
          <h2>Добро пожаловать, {user.full_name || user.username}!</h2>
          <span className="user-role">Роль: {user.role_name}</span>
          <span className="user-email">Email: {user.email}</span>
        </div>
        <button onClick={onLogout} className="logout-button">
          Выйти
        </button>
      </header>
      
      <nav className="dashboard-nav">
        <button 
          className={activeTab === 'projects' ? 'nav-button active' : 'nav-button'}
          onClick={() => setActiveTab('projects')}
        >
          Проекты
        </button>
        <button 
          className={activeTab === 'tasks' ? 'nav-button active' : 'nav-button'}
          onClick={() => setActiveTab('tasks')}
        >
          Задачи
        </button>
        <button 
          className={activeTab === 'overview' ? 'nav-button active' : 'nav-button'}
          onClick={() => setActiveTab('overview')}
        >
          Обзор
        </button>
      </nav>
      
      <main className="dashboard-content">
        {getDashboardContent()}
      </main>
    </div>
  );
};

export default Dashboard;