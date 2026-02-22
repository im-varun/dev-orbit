<template>
  <div class="container has-back-nav" v-if="project">
    <router-link to="/" class="back-link">Back to Dashboard</router-link>

    <header class="header">
      <div class="header-content">
        <div class="title-row">
          <h1>{{ project.name }}</h1>
          <button class="button" @click="handleCreateTask">Launch Task</button>
        </div>
      </div>
    </header>

    <div class="description-container" v-if="project.description">
      <div class="description-container-header">
        <h2>Description</h2>
      </div>
      <p class="description-container-content">{{ project.description }}</p>
    </div>

    <div class="task-list">
      <div class="task-list-header">
        <h2>Tasks</h2>
        <span class="task-count">{{ tasks.length }} total</span>
      </div>

      <div 
        v-for="task in tasks" 
        :key="task.id" 
        class="task-card"
      >
        <div class="task-content">
          <input 
            type="checkbox"
            :checked="task.status === 'done'"
            @change="handleToggleTask(task)" 
          />
          <span :class="{ 'completed': task.status === 'done' }">{{ task.title }}</span>
        </div>
        <button class="delete-button" @click="handleDeleteTask(task.id)">Delete</button>
      </div>

      <div v-if="tasks.length === 0" class="empty-state">
        No tasks yet. Ready to launch your first task into orbit? 🚀
      </div>
    </div>

    <div v-if="showCreateTaskModal" class="modal-overlay" @click.self="showCreateTaskModal = false">
      <div class="modal-content">
        <h2 class="modal-title">Launch New Task</h2>
        
        <div class="form-group">
          <label>What needs to be done?</label>
          <input v-model="newTask" placeholder="e.g. Design system audit" @keyup.enter="handleSaveTask" autofocus />
        </div>
        
        <div class="modal-actions">
          <button class="button" @click="showCreateTaskModal = false">Cancel</button>
          <button class="button" @click="handleSaveTask" :disabled="!newTask.trim()">Launch Task</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'

const route = useRoute()
const project = ref(null)
const tasks = ref([])
const showCreateTaskModal = ref(false)
const newTask = ref('')

const fetchProjectAndTasks = async () => {
  const projectId = route.params.id
  try {
    const [projRes, taskRes] = await Promise.all([
      api.getProjects().then(res => res.data.find(p => p.id === projectId)),
      api.getProjectTasks(projectId)
    ])
    project.value = projRes
    tasks.value = taskRes.data
  } catch (error) {
    console.error('Error fetching project or tasks:', error)
    alert('Failed to load project details. Please try again.')
  }
}

const handleCreateTask = async () => {
  newTask.value = ''
  showCreateTaskModal.value = true
}

const handleSaveTask = async () => {
  if (!newTask.value.trim()) {
    alert('Task title is required.')
    return
  }

  try {
    await api.createTask({ title: newTask.value, project_id: route.params.id })
    showCreateTaskModal.value = false
    await fetchProjectAndTasks()
  } catch (error) {
    console.error('Error creating task:', error)
    alert('Failed to create task. Please try again.')
  }
}

const handleToggleTask = async (task) => {
  const newStatus = task.status === 'done' ? 'todo' : 'done'
  try {
    await api.updateTask(task.id, { status: newStatus })
    task.status = newStatus
  } catch (error) {
    console.error('Error updating task:', error)
    alert('Failed to update task. Please try again.')
  }
}

const handleDeleteTask = async (taskId) => {
  if (!confirm("Are you sure you want to delete this task?")) {
    return
  }
  
  try {
    await api.deleteTask(taskId)
    tasks.value = tasks.value.filter(t => t.id !== taskId)
  } catch (error) {
    console.error('Error deleting task:', error)
    alert('Failed to delete task. Please try again.')
  }
}

onMounted(() => {
  fetchProjectAndTasks()
})
</script>
