import { useState, useEffect } from 'react'
import { 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  Box, 
  Button,
  CircularProgress,
  Alert,
  Paper
} from '@mui/material'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import { useNavigate } from 'react-router-dom'

// Dashboard data types
interface DashboardStats {
  totalProjects: number
  totalAnalyses: number
  totalRisks: number
  recentAnalyses: Array<{
    id: number
    projectName: string
    status: string
    createdAt: string
  }>
  riskBreakdown: Array<{
    severity: string
    count: number
    color: string
  }>
  languageDistribution: Array<{
    language: string
    count: number
  }>
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetchDashboardStats()
  }, [])

  const fetchDashboardStats = async () => {
    try {
      setLoading(true)
      // TODO: Replace with actual API call
      // const response = await fetch('/api/v1/dashboard/stats')
      // const data = await response.json()
      
      // Mock data for now
      const mockData: DashboardStats = {
        totalProjects: 12,
        totalAnalyses: 45,
        totalRisks: 8,
        recentAnalyses: [
          { id: 1, projectName: "User Management API", status: "completed", createdAt: "2024-01-15T10:30:00Z" },
          { id: 2, projectName: "Payment Gateway", status: "running", createdAt: "2024-01-15T09:15:00Z" },
          { id: 3, projectName: "Auth Service", status: "completed", createdAt: "2024-01-15T08:45:00Z" },
        ],
        riskBreakdown: [
          { severity: "Critical", count: 2, color: "#f44336" },
          { severity: "High", count: 3, color: "#ff9800" },
          { severity: "Medium", count: 2, color: "#ffc107" },
          { severity: "Low", count: 1, color: "#4caf50" }
        ],
        languageDistribution: [
          { language: "Python", count: 8 },
          { language: "JavaScript", count: 6 },
          { language: "TypeScript", count: 4 },
          { language: "Java", count: 3 },
          { language: "Go", count: 2 }
        ]
      }
      
      setStats(mockData)
    } catch (err) {
      setError('Failed to load dashboard data')
      console.error('Dashboard error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateProject = () => {
    navigate('/projects')
  }

  const handleStartAnalysis = () => {
    navigate('/projects')
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    )
  }

  if (error) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>
        <Button variant="contained" onClick={fetchDashboardStats}>
          Retry
        </Button>
      </Box>
    )
  }

  if (!stats) {
    return null
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" gutterBottom>
          ArchInsight Dashboard
        </Typography>
        <Box>
          <Button 
            variant="contained" 
            onClick={handleCreateProject}
            sx={{ mr: 1 }}
          >
            New Project
          </Button>
          <Button 
            variant="outlined" 
            onClick={handleStartAnalysis}
          >
            Start Analysis
          </Button>
        </Box>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="textSecondary" gutterBottom>
                Total Projects
              </Typography>
              <Typography variant="h3" color="primary">
                {stats.totalProjects}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="textSecondary" gutterBottom>
                Total Analyses
              </Typography>
              <Typography variant="h3" color="secondary">
                {stats.totalAnalyses}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="textSecondary" gutterBottom>
                Risks Found
              </Typography>
              <Typography variant="h3" color="error">
                {stats.totalRisks}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts Section */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Risk Severity Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={stats.riskBreakdown}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ severity, percent }) => `${severity} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {stats.riskBreakdown.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Language Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={stats.languageDistribution}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="language" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Recent Analyses */}
      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Recent Analyses
        </Typography>
        <Grid container spacing={2}>
          {stats.recentAnalyses.map((analysis) => (
            <Grid item xs={12} key={analysis.id}>
              <Card variant="outlined">
                <CardContent>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Box>
                      <Typography variant="subtitle1">
                        {analysis.projectName}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        {new Date(analysis.createdAt).toLocaleDateString()}
                      </Typography>
                    </Box>
                    <Box display="flex" alignItems="center">
                      <Box
                        sx={{
                          width: 12,
                          height: 12,
                          borderRadius: '50%',
                          backgroundColor: analysis.status === 'completed' ? '#4caf50' : '#ff9800',
                          mr: 1
                        }}
                      />
                      <Typography variant="body2" textTransform="capitalize">
                        {analysis.status}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>
    </Box>
  )
}