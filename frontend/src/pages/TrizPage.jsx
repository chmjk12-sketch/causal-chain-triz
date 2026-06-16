import React, { useState, useEffect } from 'react'
import {
  Card, Button, Form, Input, Typography, Space, Tag, List,
  Divider, Spin, Alert, Row, Col, Tabs, Table
} from 'antd'
import { BulbOutlined, SearchOutlined, BookOutlined } from '@ant-design/icons'
import { analyzeContradiction, getPrinciples, getParameters } from '../utils/api'

const { Title, Paragraph, Text } = Typography
const { TextArea } = Input
const { TabPane } = Tabs

function TrizPage() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [principles, setPrinciples] = useState([])
  const [parameters, setParameters] = useState([])
  const [principlesLoading, setPrinciplesLoading] = useState(false)
  const [form] = Form.useForm()

  useEffect(() => {
    loadPrinciplesAndParameters()
  }, [])

  const loadPrinciplesAndParameters = async () => {
    setPrinciplesLoading(true)
    try {
      const [principlesRes, parametersRes] = await Promise.all([
        getPrinciples(),
        getParameters()
      ])
      if (principlesRes.code === 200) {
        setPrinciples(principlesRes.data)
      }
      if (parametersRes.code === 200) {
        setParameters(parametersRes.data)
      }
    } catch (err) {
      console.error('加载数据失败:', err)
    } finally {
      setPrinciplesLoading(false)
    }
  }

  const handleAnalyze = async (values) => {
    setLoading(true)
    setError(null)
    try {
      const response = await analyzeContradiction(
        values.problem,
        values.improving,
        values.worsening
      )
      if (response.code === 200) {
        setResult(response.data)
      } else {
        setError(response.message || '分析失败')
      }
    } catch (err) {
      setError(err.message || '请求失败')
    } finally {
      setLoading(false)
    }
  }

  const principleColumns = [
    {
      title: '编号',
      dataIndex: 'id',
      key: 'id',
      width: 80
    },
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
      width: 120
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description'
    }
  ]

  return (
    <div>
      <Title level={2}>
        <BulbOutlined /> TRIZ 工具
      </Title>
      <Paragraph type="secondary">
        识别技术矛盾，查询 TRIZ 创新原理，获取创新解决方案。
      </Paragraph>

      <Tabs defaultActiveKey="contradiction" style={{ marginTop: 24 }}>
        <TabPane tab="矛盾分析" key="contradiction">
          <Card>
            <Form
              form={form}
              layout="vertical"
              onFinish={handleAnalyze}
            >
              <Form.Item
                label="问题描述"
                name="problem"
                rules={[{ required: true, message: '请输入问题描述' }]}
              >
                <TextArea
                  rows={3}
                  placeholder="描述你要解决的技术问题..."
                />
              </Form.Item>

              <Row gutter={16}>
                <Col xs={24} md={12}>
                  <Form.Item
                    label="想要改善的参数"
                    name="improving"
                    rules={[{ required: true, message: '请输入改善参数' }]}
                  >
                    <Input placeholder="例如：速度、可靠性、生产率" />
                  </Form.Item>
                </Col>
                <Col xs={24} md={12}>
                  <Form.Item
                    label="可能恶化的参数"
                    name="worsening"
                    rules={[{ required: true, message: '请输入恶化参数' }]}
                  >
                    <Input placeholder="例如：成本、重量、复杂度" />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={loading}
                  icon={<SearchOutlined />}
                  size="large"
                >
                  分析矛盾
                </Button>
              </Form.Item>
            </Form>
          </Card>

          {error && (
            <Alert
              message="分析失败"
              description={error}
              type="error"
              showIcon
              style={{ marginTop: 24 }}
            />
          )}

          {result && (
            <div style={{ marginTop: 24 }}>
              <Title level={3}>分析结果</Title>

              {result.contradictions && result.contradictions.length > 0 && (
                <Card title="识别的矛盾" style={{ marginTop: 16 }}>
                  {result.contradictions.map((c, i) => (
                    <div key={i}>
                      <Space>
                        <Tag color="green">改善：{c.improving_parameter}</Tag>
                        <Text>vs</Text>
                        <Tag color="red">恶化：{c.worsening_parameter}</Tag>
                      </Space>
                      <Paragraph style={{ marginTop: 8 }}>{c.description}</Paragraph>
                    </div>
                  ))}
                </Card>
              )}

              {result.principles && result.principles.length > 0 && (
                <Card title="推荐创新原理" style={{ marginTop: 16 }}>
                  <Row gutter={[16, 16]}>
                    {result.principles.map((p, i) => (
                      <Col xs={24} md={12} key={i}>
                        <Card size="small" title={`#${p.id} ${p.name}`}>
                          <Paragraph>{p.description}</Paragraph>
                        </Card>
                      </Col>
                    ))}
                  </Row>
                </Card>
              )}

              {result.suggestions && result.suggestions.length > 0 && (
                <Card title="解决建议" style={{ marginTop: 16 }}>
                  <List
                    dataSource={result.suggestions}
                    renderItem={(item, index) => (
                      <List.Item>
                        <Text strong>{index + 1}.</Text> {item}
                      </List.Item>
                    )}
                  />
                </Card>
              )}

              {result.solutions && result.solutions.length > 0 && (
                <Card title="AI 生成方案" style={{ marginTop: 16 }}>
                  <List
                    dataSource={result.solutions}
                    renderItem={(item, index) => (
                      <List.Item>
                        <Text strong style={{ color: '#1890ff' }}>方案 {index + 1}：</Text>
                        <Paragraph style={{ marginTop: 4 }}>{item}</Paragraph>
                      </List.Item>
                    )}
                  />
                </Card>
              )}
            </div>
          )}
        </TabPane>

        <TabPane tab="创新原理库" key="principles">
          <Spin spinning={principlesLoading}>
            <Card>
              <Title level={4}>
                <BookOutlined /> TRIZ 40 个创新原理
              </Title>
              <Paragraph type="secondary">
                以下是 TRIZ 理论中的 40 个创新原理，可用于解决技术矛盾。
              </Paragraph>
              <Table
                dataSource={principles}
                columns={principleColumns}
                rowKey="id"
                pagination={{ pageSize: 10 }}
              />
            </Card>
          </Spin>
        </TabPane>

        <TabPane tab="工程参数" key="parameters">
          <Spin spinning={principlesLoading}>
            <Card>
              <Title level={4}>
                <BookOutlined /> TRIZ 39 个工程参数
              </Title>
              <Paragraph type="secondary">
                以下是 TRIZ 理论中用于描述技术矛盾的 39 个工程参数。
              </Paragraph>
              <Row gutter={[8, 8]}>
                {parameters.map((param, index) => (
                  <Col key={index}>
                    <Tag color="blue">{index + 1}. {param}</Tag>
                  </Col>
                ))}
              </Row>
            </Card>
          </Spin>
        </TabPane>
      </Tabs>
    </div>
  )
}

export default TrizPage
