import { useState, useEffect } from 'react'
import {
  Typography,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  Chip,
  Alert,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TablePagination,
  InputAdornment
} from '@mui/material'
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  Code as CodeIcon,
  GitHub as GitHubIcon
} from '@mui/icons-material'
import { useNavigate } from 'react-router-dom'

interface Project {
  id: number
  name: string
  description: string
  repository_url: string
  language: string
  status: string
  created_at: string
  updated_at: string
}

interface ProjectFormData {
  name: string
  description: string
  repository_url: string
  language: string
}

const LANGUAGES = [
  'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 'Go', 'Rust',
  'PHP', 'Ruby', 'Swift', 'Kotlin', 'Scala', 'Clojure', 'Elixir'
]

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [openDialog, setOpenDialog] = useState(false)
  const [editingProject, setEditingProject] = useState<Project | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [languageFilter, setLanguageFilter] = useState('')
  const [page, setPage] = useState(0)
  const [rowsPerPage, setRowsPerPage] = useState(10)
  const navigate = useNavigate()

  const [formData, setFormData] = useState<ProjectFormData>({
    name: '',
    description: '',
    repository_url: '',
    language: ''
  })

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      setLoading(true)
      // In a real app, this would fetch from your API
      // const response = await fetch('/api/v1/projects')
      // const data = await response.json()
      
      // Mock data for now
      const mockProjects: Project[] = [
        {
          id: 1,
          name: "User Management API",
          description: "RESTful API for user authentication and management",
          repository_url: "https://github.com/company/user-api",
          language: "Python",
          status: "active",
          created_at: "2024-01-10T10:00:00Z",
          updated_at: "2024-01-15T14:30:00Z"
        },
        {
          id: 2,
          name: "Payment Gateway",
          description: "Secure payment processing service",
          repository_url: "https://github.com/company/payment-service",
          language: "TypeScript",
          status: "active",
          created_at: "2024-01-08T09:00:00Z",
          updated_at: "2024-01-14T16:45:00Z"
        },
        {
          id: 3,
          name: "Authentication Service",
          description: "JWT-based authentication microservice",
          repository_url: "https://github.com/company/auth-service",
          language: "Go",
          status: "active",
          created_at: "2024-01-05T11:00:00Z",
          updated_at: "2024-01-12T13:20:00Z"
        }
      ]
      
      setProjects(mockProjects)
    } catch (err) {
      setError('Failed to load projects')
      console.error('Projects error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenDialog = (project?: Project) => {
    if (project) {
      setEditingProject(project)
      setFormData({
        name: project.name,
        description: project.description,
        repository_url: project.repository_url,
        language: project.language
      })
    } else {
      setEditingProject(null)
      setFormData({
        name: '',
        description: '',
        repository_url: '',
        language: ''
      })
    }
    setOpenDialog(true)
  }

  const handleCloseDialog = () => {
    setOpenDialog(false)
    setEditingProject(null)
    setFormData({
      name: '',
      description: '',
      repository_url: '',
      language: ''
    })
  }

  const handleSubmit = async () => {
    try {
      if (editingProject) {
        // Update existing project
        // await fetch(`/api/v1/projects/${editingProject.id}`, {
        //   method: 'PUT',
        //   headers: { 'Content-Type': 'application/json' },
        //   body: JSON.stringify(formData)
        // })
        console.log('Updating project:', editingProject.id, formData)
      } else {
        // Create new project
        // await fetch('/api/v1/projects', {
        //   method: 'POST',
        //   headers: { 'Content-Type': 'application/json' },
        //   body: JSON.stringify(formData)
        // })
        console.log('Creating project:', formData)
      }
      
      handleCloseDialog()
      fetchProjects() // Refresh the list
    } catch (err) {
      setError('Failed to save project')
      console.error('Save error:', err)
    }
  }

  const handleDelete = async (projectId: number) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        // await fetch(`/api/v1/projects/${projectId}`, { method: 'DELETE' })
        console.log('Deleting project:', projectId)
        setProjects(projects.filter(p => p.id !== projectId))
      } catch (err) {
        setError('Failed to delete project')
        console.error('Delete error:', err)
      }
    }
  }

  const handleStartAnalysis = (projectId: number) => {
    navigate(`/analysis/${projectId}`)
  }

  const filteredProjects = projects.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         project.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesLanguage = !languageFilter || project.language === languageFilter
    return matchesSearch && matchesLanguage
  })

  const paginatedProjects = filteredProjects.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  )

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" gutterBottom>
          Projects
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          New Project
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Filters */}
      <Grid container spacing={2} mb={3}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            placeholder="Search projects..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Language Filter</InputLabel>
            <Select
              value={languageFilter}
              label="Language Filter"
              onChange={(e) => setLanguageFilter(e.target.value)}
            >
              <MenuItem value="">All Languages</MenuItem>
              {LANGUAGES.map((lang) => (
                <MenuItem key={lang} value={lang}>{lang}</MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      {/* Projects Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Language</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Created</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {paginatedProjects.map((project) => (
              <TableRow key={project.id}>
                <TableCell>
                  <Box display="flex" alignItems="center">
                    <CodeIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="subtitle2">{project.name}</Typography>
                  </Box>
                </TableCell>
                <TableCell>
                  <Typography variant="body2" color="textSecondary">
                    {project.description}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip label={project.language} size="small" />
                </TableCell>
                <TableCell>
                  <Chip
                    label={project.status}
                    size="small"
                    color={project.status === 'active' ? 'success' : 'default'}
                  />
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {new Date(project.created_at).toLocaleDateString()}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Box display="flex" gap={1}>
                    <IconButton
                      size="small"
                      onClick={() => handleStartAnalysis(project.id)}
                      color="primary"
                    >
                      <CodeIcon />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleOpenDialog(project)}
                      color="primary"
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => handleDelete(project.id)}
                      color="error"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={filteredProjects.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={(_, newPage) => setPage(newPage)}
          onRowsPerPageChange={(e) => {
            setRowsPerPage(parseInt(e.target.value, 10))
            setPage(0)
          }}
        />
      </TableContainer>

      {/* Create/Edit Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingProject ? 'Edit Project' : 'New Project'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Project Name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                multiline
                rows={3}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Repository URL"
                value={formData.repository_url}
                onChange={(e) => setFormData({ ...formData, repository_url: e.target.value })}
                placeholder="https://github.com/username/repo"
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Primary Language</InputLabel>
                <Select
                  value={formData.language}
                  label="Primary Language"
                  onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                >
                  {LANGUAGES.map((lang) => (
                    <MenuItem key={lang} value={lang}>{lang}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingProject ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}