import React from 'react'
import { Card, Row, Col, Typography, Steps, Divider } from 'antd'
import {
  BranchesOutlined,
  BulbOutlined,
  SearchOutlined,
  SolutionOutlined,
  CheckCircleOutlined
} from '@ant-design/icons'
import { Link } from 'react-router-dom'

const { Title, Paragraph } = Typography

function HomePage() {
  return (
    <div>
      <div style={{ textAlign: 'center', padding: '40px 0' }}>
        <BranchesOutlined style={{ fontSize: 64, color: '#1890ff' }} />
        <Title level={2} style={{ marginTop: 16 }}>
          因果链分析 Agent
        </Title>
        <Paragraph style={{ fontSize: 16, color: '#666' }}>
          深挖分析问题背后的因果关系，结合 TRIZ 理论提供创新解决方案
        </Paragraph>
      </div>

      <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
        <Col xs={24} md={12}>
          <Link to="/analyze" style={{ textDecoration: 'none' }}>
            <Card
              hoverable
              style={{ height: 200 }}
              cover={
                <div style={{ background: '#e6f7ff', padding: 24, textAlign: 'center' }}>
                  <BranchesOutlined style={{ fontSize: 48, color: '#1890ff' }} />
                </div>
              }
            >
              <Card.Meta
                title="因果链分析"
                description="输入问题描述，AI 自动构建因果链条，追溯根本原因"
              />
            </Card>
          </Link>
        </Col>
        <Col xs={24} md={12}>
          <Link to="/triz" style={{ textDecoration: 'none' }}>
            <Card
              hoverable
              style={{ height: 200 }}
              cover={
                <div style={{ background: '#fff7e6', padding: 24, textAlign: 'center' }}>
                  <BulbOutlined style={{ fontSize: 48, color: '#fa8c16' }} />
                </div>
              }
            >
              <Card.Meta
                title="TRIZ 工具"
                description="识别技术矛盾，查询创新原理，获取创新解决方案"
              />
            </Card>
          </Link>
        </Col>
      </Row>

      <Divider style={{ margin: '40px 0' }} />

      <Title level={3} style={{ textAlign: 'center' }}>分析流程</Title>
      <Steps
        direction="horizontal"
        current={-1}
        items={[
          {
            title: '描述问题',
            description: '输入问题描述和背景信息',
            icon: <SearchOutlined />
          },
          {
            title: '因果分析',
            description: 'AI 构建因果链，识别根本原因',
            icon: <BranchesOutlined />
          },
          {
            title: 'TRIZ 分析',
            description: '识别矛盾，推荐创新原理',
            icon: <BulbOutlined />
          },
          {
            title: '解决方案',
            description: '生成具体可行的创新方案',
            icon: <SolutionOutlined />
          }
        ]}
        style={{ marginTop: 32 }}
      />

      <Divider style={{ margin: '40px 0' }} />

      <Title level={3} style={{ textAlign: 'center' }}>核心能力</Title>
      <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
        <Col xs={24} md={8}>
          <Card>
            <CheckCircleOutlined style={{ fontSize: 32, color: '#52c41a' }} />
            <Title level={4} style={{ marginTop: 12 }}>深度因果分析</Title>
            <Paragraph>多层因果链追溯，从表象直达根本原因</Paragraph>
          </Card>
        </Col>
        <Col xs={24} md={8}>
          <Card>
            <CheckCircleOutlined style={{ fontSize: 32, color: '#52c41a' }} />
            <Title level={4} style={{ marginTop: 12 }}>TRIZ 矛盾识别</Title>
            <Paragraph>自动识别技术矛盾，映射矛盾矩阵</Paragraph>
          </Card>
        </Col>
        <Col xs={24} md={8}>
          <Card>
            <CheckCircleOutlined style={{ fontSize: 32, color: '#52c41a' }} />
            <Title level={4} style={{ marginTop: 12 }}>创新原理推荐</Title>
            <Paragraph>基于 TRIZ 40 个创新原理，推荐针对性解决方案</Paragraph>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default HomePage
