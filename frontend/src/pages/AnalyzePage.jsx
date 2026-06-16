import React, { useState } from 'react'
import {
  Card, Input, Button, Form, Slider, Typography, Space,
  Tag, List, Divider, Spin, Alert, Row, Col
} from 'antd'
import { BranchesOutlined, BulbOutlined, ArrowRightOutlined } from '@ant-design/icons'
import { analyzeCausalChain } from '../utils/api'
import CausalChainGraph from '../components/CausalChainGraph'

const { Title, Paragraph, Text } = Typography
const { TextArea } = Input

function AnalyzePage() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [form] = Form.useForm()

  const handleAnalyze = async (values) => {
    setLoading(true)
    setError(null)
    try {
      const response = await analyzeCausalChain(
        values.problem,
        values.context,
        values.depth
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

  return (
    <div>
      <Title level={2}>
        <BranchesOutlined /> 因果链分析
      </Title>
      <Paragraph type="secondary">
        输入问题描述，AI 将自动构建因果链条，追溯根本原因，并结合 TRIZ 理论提供创新解决方案。
      </Paragraph>

      <Card style={{ marginTop: 24 }}>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleAnalyze}
          initialValues={{ depth: 3 }}
        >
          <Form.Item
            label="问题描述"
            name="problem"
            rules={[{ required: true, message: '请输入问题描述' }]}
          >
            <TextArea
              rows={4}
              placeholder="例如：我们的产品在高温环境下频繁出现故障..."
            />
          </Form.Item>

          <Form.Item
            label="背景信息（可选）"
            name="context"
          >
            <TextArea
              rows={3}
              placeholder="补充相关背景信息，帮助 AI 更准确分析..."
            />
          </Form.Item>

          <Form.Item
            label="分析深度"
            name="depth"
          >
            <Slider min={1} max={5} marks={{ 1: '浅层', 3: '中等', 5: '深层' }} />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              icon={<BranchesOutlined />}
              size="large"
            >
              开始分析
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

          {/* 因果链图 */}
          <Card title="因果链图" style={{ marginTop: 16 }}>
            <CausalChainGraph causalChain={result.causal_chain} />
            <div style={{ marginTop: 16 }}>
              <Space>
                <Tag color="red">红色 = 问题事件</Tag>
                <Tag color="orange">橙色 = 中间因素</Tag>
                <Tag color="green">绿色 = 根本原因</Tag>
              </Space>
            </div>
          </Card>

          {/* 根本原因 */}
          <Card title="根本原因" style={{ marginTop: 16 }}>
            <List
              dataSource={result.root_causes || []}
              renderItem={(item, index) => (
                <List.Item>
                  <Text strong>{index + 1}.</Text> {item}
                </List.Item>
              )}
            />
          </Card>

          {/* TRIZ 矛盾 */}
          {result.triz_contradictions && result.triz_contradictions.length > 0 && (
            <Card title="识别的 TRIZ 矛盾" style={{ marginTop: 16 }}>
              {result.triz_contradictions.map((c, i) => (
                <div key={i} style={{ marginBottom: 12 }}>
                  <Tag color="blue">改善：{c.improving_parameter}</Tag>
                  <ArrowRightOutlined style={{ margin: '0 8px' }} />
                  <Tag color="red">恶化：{c.worsening_parameter}</Tag>
                  <Paragraph style={{ marginTop: 8 }}>{c.description}</Paragraph>
                </div>
              ))}
            </Card>
          )}

          {/* 创新原理 */}
          {result.recommended_principles && result.recommended_principles.length > 0 && (
            <Card title="推荐创新原理" style={{ marginTop: 16 }}>
              <Row gutter={[16, 16]}>
                {result.recommended_principles.map((p, i) => (
                  <Col xs={24} md={12} key={i}>
                    <Card size="small" title={`#${p.id} ${p.name}`}>
                      <Paragraph>{p.description}</Paragraph>
                      {p.examples && p.examples.length > 0 && (
                        <div>
                          <Text type="secondary">示例：</Text>
                          {p.examples.map((ex, j) => (
                            <Tag key={j}>{ex}</Tag>
                          ))}
                        </div>
                      )}
                    </Card>
                  </Col>
                ))}
              </Row>
            </Card>
          )}

          {/* 解决方案 */}
          {result.solutions && result.solutions.length > 0 && (
            <Card title="解决方案建议" style={{ marginTop: 16 }}>
              <List
                dataSource={result.solutions}
                renderItem={(item, index) => (
                  <List.Item>
                    <div>
                      <Text strong style={{ color: '#1890ff' }}>方案 {index + 1}：</Text>
                      <Paragraph style={{ marginTop: 4 }}>{item}</Paragraph>
                    </div>
                  </List.Item>
                )}
              />
            </Card>
          )}
        </div>
      )}
    </div>
  )
}

export default AnalyzePage
