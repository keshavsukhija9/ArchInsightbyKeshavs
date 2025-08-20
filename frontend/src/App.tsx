import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Container, AppBar, Toolbar, Typography, Box } from '@mui/material'
import Dashboard from './pages/Dashboard'
import Projects from './pages/Projects'
import Analysis from './pages/Analysis'

function App() {
  return (
    <Router>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              ArchInsight - AI Code Analyzer
            </Typography>
          </Toolbar>
        </AppBar>
        <Container maxWidth="xl" sx={{ mt: 4 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/analysis/:id" element={<Analysis />} />
          </Routes>
        </Container>
      </Box>
    </Router>
  )
}

export default App