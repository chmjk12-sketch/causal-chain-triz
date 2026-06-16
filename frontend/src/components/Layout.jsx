import React from 'react'
import { Layout as AntLayout, Menu, Typography, Badge } from 'antd'
import { Link, useLocation } from 'react-router-dom'
import {
  HomeOutlined,
  BranchesOutlined,
  BulbOutlined,
  CheckCircleOutlined
} from '@ant-design/icons'
import { useEffect, useState } from 'react'
import { getHealth } from '../utils/api'

const { Header, Content, Sider } = AntLayout
const { Title } = Typography

function LayoutComponent({ children }) {
  const location = useLocation()
  const [health, setHealth] = useState(null)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const data = await getHealth()
        setHealth(data.status === 'ok')
      } catch {
        setHealth(false)
      }
    }
    checkHealth()
    const interval = setInterval(checkHealth, 30000)
    return () => clearInterval(interval)
  }, [])

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: <Link to="/">首页</Link>
    },
    {
      key: '/analyze',
      icon: <BranchesOutlined />,
      label: <Link to="/analyze">因果链分析</Link>
    },
    {
      key: '/triz',
      icon: <BulbOutlined />,
      label: <Link to="/triz">TRIZ 工具</Link>
    }
  ]

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#001529', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <BranchesOutlined style={{ fontSize: 24, color: '#1890ff' }} />
          <Title level={4} style={{ color: '#fff', margin: 0 }}>
            因果链分析 Agent
          </Title>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ color: '#fff', fontSize: 12 }}>服务状态</span>
          <Badge
            status={health === null ? 'default' : health ? 'success' : 'error'}
            text={
              <span style={{ color: '#fff', fontSize: 12 }}>
                {health === null ? '检查中' : health ? '在线' : '离线'}
              </span>
            }
          />
        </div>
      </Header>
      <AntLayout>
        <Sider width={200} style={{ background: '#fff' }}>
          <Menu
            mode="inline"
            selectedKeys={[location.pathname]}
            style={{ height: '100%', borderRight: 0 }}
            items={menuItems}
          />
        </Sider>
        <AntLayout style={{ padding: '24px' }}>
          <Content style={{ background: '#fff', padding: 24, margin: 0, minHeight: 280, borderRadius: 8 }}>
            {children}
          </Content>
        </AntLayout>
      </AntLayout>
    </AntLayout>
  )
}

export default LayoutComponent
