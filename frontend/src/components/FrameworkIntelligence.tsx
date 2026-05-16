'use client';

import { FrameworkVisualization } from '@/lib/api/types';

interface FrameworkIntelligenceProps {
  frameworks: FrameworkVisualization[];
}

export default function FrameworkIntelligence({ frameworks }: FrameworkIntelligenceProps) {
  if (!frameworks || frameworks.length === 0) return null;

  // Group frameworks by category
  const groupedFrameworks = frameworks.reduce((acc, framework) => {
    const category = framework.category || 'Other';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(framework);
    return acc;
  }, {} as Record<string, FrameworkVisualization[]>);

  // Category configurations
  const categoryConfig: Record<string, { icon: string; color: string; bgColor: string; borderColor: string }> = {
    'ML Framework': {
      icon: '🧠',
      color: 'text-purple-300',
      bgColor: 'from-purple-500/20 to-pink-500/20',
      borderColor: 'border-purple-500/30'
    },
    'Deep Learning': {
      icon: '🔥',
      color: 'text-red-300',
      bgColor: 'from-red-500/20 to-orange-500/20',
      borderColor: 'border-red-500/30'
    },
    'Medical Imaging': {
      icon: '🏥',
      color: 'text-green-300',
      bgColor: 'from-green-500/20 to-emerald-500/20',
      borderColor: 'border-green-500/30'
    },
    'Computer Vision': {
      icon: '👁️',
      color: 'text-blue-300',
      bgColor: 'from-blue-500/20 to-cyan-500/20',
      borderColor: 'border-blue-500/30'
    },
    'Data Processing': {
      icon: '📊',
      color: 'text-yellow-300',
      bgColor: 'from-yellow-500/20 to-amber-500/20',
      borderColor: 'border-yellow-500/30'
    },
    'Visualization': {
      icon: '📈',
      color: 'text-indigo-300',
      bgColor: 'from-indigo-500/20 to-purple-500/20',
      borderColor: 'border-indigo-500/30'
    },
    'Development Tools': {
      icon: '🛠️',
      color: 'text-gray-300',
      bgColor: 'from-gray-500/20 to-slate-500/20',
      borderColor: 'border-gray-500/30'
    },
    'Other': {
      icon: '📦',
      color: 'text-gray-300',
      bgColor: 'from-gray-500/20 to-slate-500/20',
      borderColor: 'border-gray-500/30'
    }
  };

  const getCategoryConfig = (category: string) => {
    return categoryConfig[category] || categoryConfig['Other'];
  };

  const confidenceColors = {
    high: 'from-green-500 to-emerald-500',
    medium: 'from-yellow-500 to-amber-500',
    low: 'from-gray-500 to-slate-500'
  };

  const confidenceBadgeColors = {
    high: 'bg-green-500/20 text-green-300 border-green-500/40',
    medium: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/40',
    low: 'bg-gray-500/20 text-gray-300 border-gray-500/40'
  };

  // Calculate confidence percentage
  const getConfidencePercentage = (confidence: string) => {
    switch (confidence.toLowerCase()) {
      case 'high': return 90;
      case 'medium': return 60;
      case 'low': return 30;
      default: return 0;
    }
  };

  return (
    <div className="relative bg-gradient-to-br from-gray-800/50 via-gray-900/50 to-gray-800/50 backdrop-blur-xl border border-gray-700/50 rounded-3xl p-8 shadow-2xl overflow-hidden">
      {/* Section header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 bg-gradient-to-br from-green-500/30 to-emerald-500/30 rounded-2xl flex items-center justify-center">
            <svg className="w-7 h-7 text-green-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold text-white">Framework Intelligence</h3>
          <span className="px-3 py-1 bg-green-500/20 text-green-300 text-xs font-bold rounded-full border border-green-500/40">
            {frameworks.length} detected
          </span>
        </div>
        <div className="h-1 w-24 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full"></div>
      </div>

      {/* Grouped frameworks by category */}
      <div className="space-y-8">
        {Object.entries(groupedFrameworks).map(([category, categoryFrameworks], categoryIndex) => {
          const config = getCategoryConfig(category);
          
          return (
            <div 
              key={category}
              className="animate-fade-in-up"
              style={{ animationDelay: `${categoryIndex * 100}ms` }}
            >
              {/* Category header */}
              <div className="flex items-center gap-3 mb-4">
                <span className="text-2xl">{config.icon}</span>
                <h4 className={`text-lg font-bold ${config.color}`}>
                  {category}
                </h4>
                <span className="text-sm text-gray-500">
                  ({categoryFrameworks.length})
                </span>
              </div>

              {/* Framework cards in this category */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {categoryFrameworks.map((framework, index) => {
                  const confidencePercentage = getConfidencePercentage(framework.confidence);
                  
                  return (
                    <div
                      key={index}
                      className={`group relative bg-gradient-to-br ${config.bgColor} backdrop-blur-sm rounded-2xl p-5 border-2 ${config.borderColor} hover:border-opacity-60 transition-all duration-500 hover:scale-105 hover:shadow-2xl animate-slide-up`}
                      style={{ animationDelay: `${(categoryIndex * 100) + (index * 50)}ms` }}
                    >
                      {/* Glow effect on hover */}
                      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 rounded-2xl transition-opacity duration-500"></div>

                      <div className="relative z-10 space-y-3">
                        {/* Framework name and confidence badge */}
                        <div className="flex items-start justify-between gap-2">
                          <h5 className="font-bold text-white text-base group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-gray-300 group-hover:bg-clip-text transition-all duration-300 flex-1">
                            {framework.name}
                          </h5>
                          <span className={`px-2 py-1 text-xs font-semibold rounded-full border ${confidenceBadgeColors[framework.confidence as keyof typeof confidenceBadgeColors]} transition-all duration-300 group-hover:scale-110 whitespace-nowrap`}>
                            {framework.confidence}
                          </span>
                        </div>

                        {/* Confidence bar */}
                        <div className="space-y-1">
                          <div className="flex items-center justify-between text-xs">
                            <span className="text-gray-400">Confidence</span>
                            <span className="text-gray-300 font-bold">{confidencePercentage}%</span>
                          </div>
                          <div className="h-2 bg-gray-700/50 rounded-full overflow-hidden">
                            <div 
                              className={`h-full bg-gradient-to-r ${confidenceColors[framework.confidence as keyof typeof confidenceColors]} rounded-full transition-all duration-1000 ease-out`}
                              style={{ 
                                width: `${confidencePercentage}%`,
                                animationDelay: `${(categoryIndex * 100) + (index * 50) + 200}ms`
                              }}
                            ></div>
                          </div>
                        </div>

                        {/* Evidence count */}
                        <div className="flex items-center gap-2 text-xs text-gray-400">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
                          </svg>
                          <span>{framework.evidence_count} evidence {framework.evidence_count === 1 ? 'file' : 'files'}</span>
                        </div>

                        {/* Framework icon/badge if available */}
                        {framework.icon && (
                          <div className="pt-2 border-t border-gray-700/50">
                            <span className="text-2xl group-hover:scale-110 transition-transform duration-300 inline-block">
                              {framework.icon}
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      {/* Summary statistics */}
      <div className="mt-8 pt-6 border-t border-gray-700/50">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <p className="text-2xl font-bold text-green-400">{frameworks.length}</p>
            <p className="text-xs text-gray-400">Total Frameworks</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-green-400">
              {frameworks.filter(f => f.confidence === 'high').length}
            </p>
            <p className="text-xs text-gray-400">High Confidence</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-yellow-400">
              {frameworks.filter(f => f.confidence === 'medium').length}
            </p>
            <p className="text-xs text-gray-400">Medium Confidence</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-400">
              {Object.keys(groupedFrameworks).length}
            </p>
            <p className="text-xs text-gray-400">Categories</p>
          </div>
        </div>
      </div>
    </div>
  );
}

// Made with Bob