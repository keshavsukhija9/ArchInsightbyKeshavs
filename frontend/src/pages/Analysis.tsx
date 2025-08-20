import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import {
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Paper,
  Button,
  Chip,
  LinearProgress,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider
} from '@mui/material'
import {
  Code as CodeIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon,
  Build as BuildIcon,
  ExpandMore as ExpandMoreIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Info as InfoIcon
} from '@mui/icons-material'

interface AnalysisData {
  id: number
  projectId: number
  projectName: string
  status: string
  progress: number
  analysisType: string
  startedAt: string
  completedAt?: string
  results?: {
    dependencyGraph: {
      nodes: Array<{
        id: string
        name: string
        type: string
        language: string
        complexity: number
        linesOfCode: number
      }>
      edges: Array<{
        source: string
        target: string
        type: string
        weight: number
      }>
    }
    metrics: {
      totalFiles: number
      totalLines: number
      averageComplexity: number
      cyclomaticComplexity: number
      maintainabilityIndex: number
      technicalDebt: string
    }
    risks: Array<{
      id: string
      severity: 'low' | 'medium' | 'high' | 'critical'
      title: string
      description: string
      file: string
      line: number
      category: string
    }>
    recommendations: Array<{
      id: string
      type: string
      title: string
      description: string
      severity: string
      confidence: number
      impactScore: number
      effortEstimate: string
    }>
  }
}

interface TabPanelProps {
  children?: React.ReactNode
  index: number
  value: number
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`analysis-tabpanel-${index}`}
      aria-labelledby={`analysis-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  )
}

export default function Analysis() {
  const { id } = useParams<{ id: string }>()
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [tabValue, setTabValue] = useState(0)

  useEffect(() => {
    if (id) {
      fetchAnalysis(parseInt(id))
    }
  }, [id])

  const fetchAnalysis = async (analysisId: number) => {
    try {
      setLoading(true)
      // In a real app, this would fetch from your API
      // const response = await fetch(`/api/v1/analysis/${analysisId}`)
      // const data = await response.json()
      
      // Mock data for now
      const mockAnalysis: AnalysisData = {
        id: analysisId,
        projectId: 1,
        projectName: "User Management API",
        status: "completed",
        progress: 100,
        analysisType: "full",
        startedAt: "2024-01-15T10:30:00Z",
        completedAt: "2024-01-15T10:35:00Z",
        results: {
          dependencyGraph: {
            nodes: [
              { id: "1", name: "main.py", type: "file", language: "python", complexity: 3, linesOfCode: 45 },
              { id: "2", name: "auth.py", type: "file", language: "python", complexity: 8, linesOfCode: 120 },
              { id: "3", name: "models.py", type: "file", language: "python", complexity: 2, linesOfCode: 35 },
              { id: "4", name: "utils.py", type: "file", language: "python", complexity: 5, linesOfCode: 80 }
            ],
            edges: [
              { source: "1", target: "2", type: "imports", weight: 1 },
              { source: "1", target: "3", type: "imports", weight: 1 },
              { source: "2", target: "3", type: "uses", weight: 0.8 },
              { source: "2", target: "4", type: "imports", weight: 1 }
            ]
          },
          metrics: {
            totalFiles: 4,
            totalLines: 280,
            averageComplexity: 4.5,
            cyclomaticComplexity: 18,
            maintainabilityIndex: 75,
            technicalDebt: "medium"
          },
          risks: [
            {
              id: "1",
              severity: "high",
              title: "High Cyclomatic Complexity",
              description: "The auth.py file has a cyclomatic complexity of 8, which indicates complex logic that may be difficult to maintain.",
              file: "auth.py",
              line: 45,
              category: "complexity"
            },
            {
              id: "2",
              severity: "medium",
              title: "Large Function",
              description: "The authenticate_user function in auth.py is 45 lines long and handles multiple responsibilities.",
              file: "auth.py",
              line: 23,
              category: "maintainability"
            }
          ],
          recommendations: [
            {
              id: "1",
              type: "refactoring",
              title: "Extract Authentication Logic",
              description: "Break down the authenticate_user function into smaller, more focused functions.",
              severity: "medium",
              confidence: 0.85,
              impactScore: 0.7,
              effortEstimate: "medium"
            },
            {
              id: "2",
              type: "security",
              title: "Add Input Validation",
              description: "Implement comprehensive input validation for user credentials.",
              severity: "high",
              confidence: 0.9,
              impactScore: 0.8,
              effortEstimate: "low"
            }
          ]
        }
      }
      
      setAnalysis(mockAnalysis)
    } catch (err) {
      setError('Failed to load analysis data')
      console.error('Analysis error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue)
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'error'
      case 'high': return 'error'
      case 'medium': return 'warning'
      case 'low': return 'info'
      default: return 'default'
    }
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical': return <ErrorIcon color="error" />
      case 'high': return <WarningIcon color="error" />
      case 'medium': return <WarningIcon color="warning" />
      case 'low': return <InfoIcon color="info" />
      default: return <InfoIcon />
    }
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
        <Button variant="contained" onClick={() => fetchAnalysis(parseInt(id!))}>
          Retry
        </Button>
      </Box>
    )
  }

  if (!analysis) {
    return <Typography>Analysis not found</Typography>
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Code Analysis: {analysis.projectName}
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Analysis ID: {analysis.id} | Type: {analysis.analysisType}
          </Typography>
        </Box>
        <Box display="flex" gap={2}>
          <Chip
            label={analysis.status}
            color={analysis.status === 'completed' ? 'success' : 'warning'}
            icon={analysis.status === 'completed' ? <CheckCircleIcon /> : <CircularProgress size={16} />}
          />
          <Chip label={`${analysis.progress}%`} />
        </Box>
      </Box>

      {analysis.status === 'running' && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Analysis in Progress
            </Typography>
            <LinearProgress variant="determinate" value={analysis.progress} sx={{ mb: 1 }} />
            <Typography variant="body2" color="textSecondary">
              Started at {new Date(analysis.startedAt).toLocaleString()}
            </Typography>
          </CardContent>
        </Card>
      )}

      {analysis.results && (
        <>
          {/* Metrics Overview */}
          <Grid container spacing={3} mb={3}>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography variant="h6" color="textSecondary" gutterBottom>
                    Total Files
                  </Typography>
                  <Typography variant="h3" color="primary">
                    {analysis.results.metrics.totalFiles}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography variant="h6" color="textSecondary" gutterBottom>
                    Lines of Code
                  </Typography>
                  <Typography variant="h3" color="secondary">
                    {analysis.results.metrics.totalLines}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography variant="h6" color="textSecondary" gutterBottom>
                    Avg Complexity
                  </Typography>
                  <Typography variant="h3" color="warning">
                    {analysis.results.metrics.averageComplexity}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography variant="h6" color="textSecondary" gutterBottom>
                    Maintainability
                  </Typography>
                  <Typography variant="h3" color="success">
                    {analysis.results.metrics.maintainabilityIndex}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Tabs for different views */}
          <Paper sx={{ width: '100%' }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="analysis tabs">
              <Tab label="Dependencies" icon={<CodeIcon />} />
              <Tab label="Risks" icon={<SecurityIcon />} />
              <Tab label="Recommendations" icon={<BuildIcon />} />
              <Tab label="Metrics" icon={<SpeedIcon />} />
            </Tabs>

            <TabPanel value={tabValue} index={0}>
              <Typography variant="h6" gutterBottom>
                Dependency Graph
              </Typography>
              <Typography variant="body2" color="textSecondary" paragraph>
                This shows the relationships between different code components.
              </Typography>
              <Grid container spacing={2}>
                {analysis.results.dependencyGraph.nodes.map((node) => (
                  <Grid item xs={12} md={6} key={node.id}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="subtitle1" gutterBottom>
                          {node.name}
                        </Typography>
                        <Box display="flex" gap={1} mb={1}>
                          <Chip label={node.type} size="small" />
                          <Chip label={node.language} size="small" />
                        </Box>
                        <Typography variant="body2" color="textSecondary">
                          Complexity: {node.complexity} | Lines: {node.linesOfCode}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
              <Typography variant="h6" gutterBottom>
                Security & Quality Risks
              </Typography>
              <List>
                {analysis.results.risks.map((risk) => (
                  <ListItem key={risk.id} divider>
                    <ListItemIcon>
                      {getSeverityIcon(risk.severity)}
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box display="flex" alignItems="center" gap={1}>
                          <Typography variant="subtitle1">{risk.title}</Typography>
                          <Chip
                            label={risk.severity}
                            color={getSeverityColor(risk.severity)}
                            size="small"
                          />
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" color="textSecondary" paragraph>
                            {risk.description}
                          </Typography>
                          <Typography variant="caption" color="textSecondary">
                            File: {risk.file}:{risk.line} | Category: {risk.category}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
              <Typography variant="h6" gutterBottom>
                AI-Powered Recommendations
              </Typography>
              <Grid container spacing={2}>
                {analysis.results.recommendations.map((rec) => (
                  <Grid item xs={12} key={rec.id}>
                    <Accordion>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Box display="flex" alignItems="center" gap={2} width="100%">
                          <Box display="flex" alignItems="center" gap={1}>
                            {getSeverityIcon(rec.severity)}
                            <Typography variant="subtitle1">{rec.title}</Typography>
                          </Box>
                          <Box display="flex" gap={1} ml="auto">
                            <Chip
                              label={rec.severity}
                              color={getSeverityColor(rec.severity)}
                              size="small"
                            />
                            <Chip
                              label={`${(rec.confidence * 100).toFixed(0)}% confidence`}
                              size="small"
                              variant="outlined"
                            />
                          </Box>
                        </Box>
                      </AccordionSummary>
                      <AccordionDetails>
                        <Typography variant="body2" paragraph>
                          {rec.description}
                        </Typography>
                        <Box display="flex" gap={2}>
                          <Chip
                            label={`Impact: ${(rec.impactScore * 100).toFixed(0)}%`}
                            size="small"
                            color="primary"
                          />
                          <Chip
                            label={`Effort: ${rec.effortEstimate}`}
                            size="small"
                            variant="outlined"
                          />
                        </Box>
                      </AccordionDetails>
                    </Accordion>
                  </Grid>
                ))}
              </Grid>
            </TabPanel>

            <TabPanel value={tabValue} index={3}>
              <Typography variant="h6" gutterBottom>
                Detailed Metrics
              </Typography>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Metric</TableCell>
                      <TableCell>Value</TableCell>
                      <TableCell>Status</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    <TableRow>
                      <TableCell>Total Files</TableCell>
                      <TableCell>{analysis.results.metrics.totalFiles}</TableCell>
                      <TableCell>
                        <Chip label="Good" color="success" size="small" />
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Total Lines of Code</TableCell>
                      <TableCell>{analysis.results.metrics.totalLines}</TableCell>
                      <TableCell>
                        <Chip label="Good" color="success" size="small" />
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Average Complexity</TableCell>
                      <TableCell>{analysis.results.metrics.averageComplexity}</TableCell>
                      <TableCell>
                        <Chip 
                          label={analysis.results.metrics.averageComplexity > 5 ? "High" : "Good"} 
                          color={analysis.results.metrics.averageComplexity > 5 ? "warning" : "success"} 
                          size="small" 
                        />
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Cyclomatic Complexity</TableCell>
                      <TableCell>{analysis.results.metrics.cyclomaticComplexity}</TableCell>
                      <TableCell>
                        <Chip 
                          label={analysis.results.metrics.cyclomaticComplexity > 20 ? "High" : "Good"} 
                          color={analysis.results.metrics.cyclomaticComplexity > 20 ? "warning" : "success"} 
                          size="small" 
                        />
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Maintainability Index</TableCell>
                      <TableCell>{analysis.results.metrics.maintainabilityIndex}</TableCell>
                      <TableCell>
                        <Chip 
                          label={analysis.results.metrics.maintainabilityIndex < 65 ? "Low" : "Good"} 
                          color={analysis.results.metrics.maintainabilityIndex < 65 ? "warning" : "success"} 
                          size="small" 
                        />
                      </TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Technical Debt</TableCell>
                      <TableCell>{analysis.results.metrics.technicalDebt}</TableCell>
                      <TableCell>
                        <Chip 
                          label={analysis.results.metrics.technicalDebt} 
                          color={analysis.results.metrics.technicalDebt === "high" ? "error" : "warning"} 
                          size="small" 
                        />
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </TabPanel>
          </Paper>
        </>
      )}
    </Box>
  )
}