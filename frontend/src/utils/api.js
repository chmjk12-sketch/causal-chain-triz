import axios from 'axios'

const API_BASE = ''

const api = axios.create({
  baseURL: API_BASE,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const analyzeCausalChain = async (problem, context = '', depth = 3) => {
  const response = await api.post('/api/v1/analyze', {
    problem,
    context,
    depth
  })
  return response.data
}

export const analyzeContradiction = async (problem, improving, worsening) => {
  const response = await api.post('/api/v1/triz/contradictions', {
    problem,
    improving,
    worsening
  })
  return response.data
}

export const getPrinciples = async () => {
  const response = await api.get('/api/v1/triz/principles')
  return response.data
}

export const getParameters = async () => {
  const response = await api.get('/api/v1/triz/parameters')
  return response.data
}

export const getHealth = async () => {
  const response = await api.get('/health')
  return response.data
}

export default api
