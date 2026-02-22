<template>
  <div class="container">
    <header class="header">
      <div class="header-content">
        <div class="title-row">
          <h1>Dev Orbit 🪐</h1>
          <button class="button" @click="handleCreateProject">Launch Project</button>
        </div>
      </div>
    </header>

    <div v-if="loading" class="loading">Syncing with the orbit...</div>
    
    <div v-else class="project-grid">
      <div
        v-for="project in projects"
        :key="project.id"
        class="project-card"
        @click="handleProject(project.id)"
      >
        <h2>{{ project.name }}</h2>
        <p><b>Description:</b> {{ project.description || 'No description provided.' }}</p>
        <p><b>Created at:</b> {{ project.created_at ? new Date(project.created_at * 1000).toLocaleString() : 'No creation date' }}</p>
        <button class="delete-button" @click.stop="handleDeleteProject(project.id)">Delete</button>
      </div>

      <div v-if="projects.length === 0" class="empty-state">
        No projects yet. Ready to launch your first project into orbit? 🚀
      </div>
    </div>

    <div v-if="showCreateProjectModal" class="modal-overlay">
      <div class="modal-content">
        <h2 class="modal-title">Launch New Project</h2>
        
        <div class="form-group">
          <label>Name</label>
          <input v-model="newProject.name" placeholder="e.g. Portfolio Site" autofocus />
        </div>
        
        <div class="form-group">
          <label>Description</label>
          <textarea v-model="newProject.description" placeholder="What are we building?"></textarea>
        </div>
        
        <div class="modal-actions">
          <button class="button" @click="showCreateProjectModal = false">Cancel</button>
          <button class="button" @click="handleSaveProject" :disabled="isSaving">{{ isSaving ? 'Launching...' : 'Launch Project' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const projects = ref([])
const loading = ref(true)
const showCreateProjectModal = ref(false)
const isSaving = ref(false)
const newProject = ref({ name: '', description: '' })

const fetchProjects = async () => {
  try {
    const response = await api.getProjects()
    projects.value = response.data
  } catch (error) {
    console.error('Error fetching projects:', error)
    alert('Failed to load projects. Please try again.')
  } finally {
    loading.value = false
  }
}

const handleProject = (projectId) => {
  router.push({ name: 'project', params: { id: projectId } })
}

const handleCreateProject = () => {
  newProject.value = {
    name: '',
    description: '',
  }
  showCreateProjectModal.value = true
}

const handleSaveProject = async () => {
  if (!newProject.value.name.trim()) {
    alert('Project name is required.')
    return
  }

  isSaving.value = true

  try {
    await api.createProject(newProject.value)
    showCreateProjectModal.value = false
    await fetchProjects()
  } catch (error) {
    console.error('Error creating project:', error)
    alert('Failed to create project. Please try again.')
  } finally {
    isSaving.value = false
  }
}

const handleDeleteProject = async (projectId) => {
  if (!confirm("Are you sure you want to delete this project? This will remove the project and all its tasks permanently.")) {
    return
  }

  try {
    await api.deleteProject(projectId)
    projects.value = projects.value.filter(p => p.id !== projectId)
  } catch (error) {
    console.error('Error deleting project:', error)
    alert('Failed to delete project. Please try again.')
  }
}

onMounted(() => {
  fetchProjects()
})
</script>
