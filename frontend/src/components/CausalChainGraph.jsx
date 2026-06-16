import React, { useEffect, useState } from 'react'
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType
} from 'react-flow-renderer'
import 'react-flow-renderer/dist/style.css'
import dagre from 'dagre'

const nodeWidth = 180
const nodeHeight = 60

const getLayoutedElements = (nodes, edges, direction = 'TB') => {
  const dagreGraph = new dagre.graphlib.Graph()
  dagreGraph.setDefaultEdgeLabel(() => ({}))
  dagreGraph.setGraph({ rankdir: direction })

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight })
  })

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target)
  })

  dagre.layout(dagreGraph)

  nodes.forEach((node) => {
    const nodeWithPosition = dagreGraph.node(node.id)
    node.targetPosition = 'top'
    node.sourcePosition = 'bottom'
    node.position = {
      x: nodeWithPosition.x - nodeWidth / 2,
      y: nodeWithPosition.y - nodeHeight / 2
    }
    return node
  })

  return { nodes, edges }
}

const nodeColors = {
  event: '#ff4d4f',
  factor: '#faad14',
  root: '#52c41a'
}

function CausalChainGraph({ causalChain }) {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])

  useEffect(() => {
    if (!causalChain || !causalChain.nodes) return

    const flowNodes = causalChain.nodes.map((node) => ({
      id: node.id,
      data: { label: node.label },
      position: { x: 0, y: 0 },
      style: {
        background: nodeColors[node.type] || '#1890ff',
        color: '#fff',
        border: '1px solid #ccc',
        borderRadius: 8,
        padding: 10,
        width: nodeWidth
      }
    }))

    const flowEdges = causalChain.edges.map((edge, index) => ({
      id: `e${index}`,
      source: edge.source,
      target: edge.target,
      label: edge.label,
      animated: true,
      style: { stroke: '#666' },
      markerEnd: {
        type: MarkerType.ArrowClosed
      }
    }))

    const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
      flowNodes,
      flowEdges
    )

    setNodes(layoutedNodes)
    setEdges(layoutedEdges)
  }, [causalChain])

  return (
    <div style={{ width: '100%', height: 500, border: '1px solid #eee', borderRadius: 8 }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
      >
        <Controls />
        <MiniMap nodeColor={(n) => n.style?.background} />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>
    </div>
  )
}

export default CausalChainGraph
