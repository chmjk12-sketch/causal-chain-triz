import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import AnalyzePage from './pages/AnalyzePage'
import TrizPage from './pages/TrizPage'

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/analyze" element={<AnalyzePage />} />
            <Route path="/triz" element={<TrizPage />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </ConfigProvider>
  )
}

export default App
