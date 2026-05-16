'use client';

import { WorkflowNode } from '@/lib/api/types';

interface WorkflowVisualizationProps {
  nodes: WorkflowNode[];
}

export default function WorkflowVisualization({ nodes }: WorkflowVisualizationProps) {
  if (!nodes || nodes.length === 0) return null;

  // Define workflow stages in order
  const workflowStages = [
    { id: 'preprocessing', label: 'Preprocessing', icon: '🔧' },
    { id: 'training', label: 'Training', icon: '🧠' },
    { id: 'inference', label: 'Inference', icon: '🎯' },
    { id: 'evaluation', label: 'Evaluation', icon: '📊' },
    { id: 'deployment', label: 'Deployment', icon: '🚀' }
  ];

  // Map nodes to stages
  const stageNodes = workflowStages.map(stage => {
    const node = nodes.find(n => n.type.toLowerCase().includes(stage.id));
    return {
      ...stage,
      node,
      hasImplementation: node?.has_implementation || false,
      confidence: node?.confidence || 'low',
      files: node?.files || []
    };
  });

  const confidenceColors = {
    high: 'from-green-500 to-emerald-500',
    medium: 'from-yellow-500 to-amber-500',
    low: 'from-gray-500 to-slate-500'
  };

  const confidenceBorderColors = {
    high: 'border-green-500/50',
    medium: 'border-yellow-500/50',
    low: 'border-gray-500/50'
  };

  return (
    <div className="relative bg-gradient-to-br from-indigo-900/20 via-gray-800/50 to-gray-900/50 backdrop-blur-xl border border-indigo-500/30 rounded-3xl p-8 shadow-2xl overflow-hidden">
      {/* Section header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 bg-gradient-to-br from-indigo-500/30 to-purple-500/30 rounded-2xl flex items-center justify-center">
            <svg className="w-7 h-7 text-indigo-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold text-white">ML Workflow Pipeline</h3>
        </div>
        <div className="h-1 w-24 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"></div>
      </div>

      {/* Workflow visualization */}
      <div className="relative">
        {/* Desktop view - horizontal flow */}
        <div className="hidden md:block">
          <div className="flex items-center justify-between gap-4">
            {stageNodes.map((stage, index) => (
              <div key={stage.id} className="flex items-center flex-1">
                {/* Workflow Node */}
                <div className="flex-1">
                  <div 
                    className={`group relative bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm rounded-2xl p-5 border-2 transition-all duration-500 hover:scale-105 hover:shadow-2xl animate-fade-in-up ${
                      stage.hasImplementation 
                        ? confidenceBorderColors[stage.confidence as keyof typeof confidenceBorderColors]
                        : 'border-gray-700/50'
                    }`}
                    style={{ animationDelay: `${index * 100}ms` }}
                  >
                    {/* Glow effect for implemented stages */}
                    {stage.hasImplementation && (
                      <div className={`absolute inset-0 bg-gradient-to-br ${confidenceColors[stage.confidence as keyof typeof confidenceColors]} opacity-10 rounded-2xl animate-pulse`}></div>
                    )}

                    <div className="relative z-10 text-center space-y-3">
                      {/* Icon */}
                      <div className="text-4xl mb-2 group-hover:scale-110 transition-transform duration-300">
                        {stage.icon}
                      </div>

                      {/* Label */}
                      <h4 className="font-bold text-white text-sm">
                        {stage.label}
                      </h4>

                      {/* Status indicator */}
                      <div className="flex items-center justify-center gap-2">
                        {stage.hasImplementation ? (
                          <>
                            <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${confidenceColors[stage.confidence as keyof typeof confidenceColors]} animate-pulse`}></div>
                            <span className="text-xs text-gray-400 capitalize">{stage.confidence}</span>
                          </>
                        ) : (
                          <span className="text-xs text-gray-500">Not detected</span>
                        )}
                      </div>

                      {/* File count */}
                      {stage.files.length > 0 && (
                        <div className="text-xs text-gray-500 flex items-center justify-center gap-1">
                          <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
                          </svg>
                          <span>{stage.files.length}</span>
                        </div>
                      )}
                    </div>

                    {/* Tooltip on hover */}
                    {stage.files.length > 0 && (
                      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none z-20">
                        <div className="bg-gray-900 border border-gray-700 rounded-lg p-3 shadow-xl max-w-xs">
                          <p className="text-xs text-gray-400 mb-2 font-semibold">Files:</p>
                          <div className="space-y-1">
                            {stage.files.slice(0, 3).map((file, i) => (
                              <p key={i} className="text-xs text-gray-300 font-mono truncate">
                                {file}
                              </p>
                            ))}
                            {stage.files.length > 3 && (
                              <p className="text-xs text-gray-500">+{stage.files.length - 3} more</p>
                            )}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {/* Arrow connector */}
                {index < stageNodes.length - 1 && (
                  <div className="flex items-center justify-center px-2">
                    <svg 
                      className="w-8 h-8 text-indigo-400/50 animate-pulse" 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                      style={{ animationDelay: `${index * 100 + 50}ms` }}
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Mobile view - vertical flow */}
        <div className="md:hidden space-y-4">
          {stageNodes.map((stage, index) => (
            <div key={stage.id}>
              {/* Workflow Node */}
              <div 
                className={`group relative bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm rounded-2xl p-5 border-2 transition-all duration-500 hover:scale-105 hover:shadow-2xl animate-fade-in-up ${
                  stage.hasImplementation 
                    ? confidenceBorderColors[stage.confidence as keyof typeof confidenceBorderColors]
                    : 'border-gray-700/50'
                }`}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {stage.hasImplementation && (
                  <div className={`absolute inset-0 bg-gradient-to-br ${confidenceColors[stage.confidence as keyof typeof confidenceColors]} opacity-10 rounded-2xl animate-pulse`}></div>
                )}

                <div className="relative z-10 flex items-center gap-4">
                  {/* Icon */}
                  <div className="text-3xl group-hover:scale-110 transition-transform duration-300">
                    {stage.icon}
                  </div>

                  <div className="flex-1">
                    {/* Label */}
                    <h4 className="font-bold text-white text-base mb-1">
                      {stage.label}
                    </h4>

                    {/* Status */}
                    <div className="flex items-center gap-2">
                      {stage.hasImplementation ? (
                        <>
                          <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${confidenceColors[stage.confidence as keyof typeof confidenceColors]} animate-pulse`}></div>
                          <span className="text-xs text-gray-400 capitalize">{stage.confidence}</span>
                          {stage.files.length > 0 && (
                            <span className="text-xs text-gray-500">• {stage.files.length} files</span>
                          )}
                        </>
                      ) : (
                        <span className="text-xs text-gray-500">Not detected</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Arrow connector */}
              {index < stageNodes.length - 1 && (
                <div className="flex justify-center py-2">
                  <svg 
                    className="w-6 h-6 text-indigo-400/50 animate-pulse" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="mt-8 pt-6 border-t border-gray-700/50">
        <div className="flex flex-wrap items-center justify-center gap-4 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-gradient-to-r from-green-500 to-emerald-500"></div>
            <span className="text-gray-400">High Confidence</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-gradient-to-r from-yellow-500 to-amber-500"></div>
            <span className="text-gray-400">Medium Confidence</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-gradient-to-r from-gray-500 to-slate-500"></div>
            <span className="text-gray-400">Low Confidence</span>
          </div>
        </div>
      </div>
    </div>
  );
}

// Made with Bob