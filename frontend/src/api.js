import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default {
  getProjects() {
    return apiClient.get('/projects')
  },

  createProject(project) {
    return apiClient.post('/projects', project)
  },

  deleteProject(projectId) {
    return apiClient.delete(`/projects/${projectId}`)
  },

  getProjectTasks(projectId) {
    return apiClient.get(`/projects/${projectId}/tasks`)
  },

  createTask(task) {
    return apiClient.post('/tasks', task)
  },

  updateTask(taskId, updates) {
    return apiClient.patch(`/tasks/${taskId}`, updates)
  },

  deleteTask(taskId) {
    return apiClient.delete(`/tasks/${taskId}`)
  }
}
