'use client';

interface StatisticsVisualizationProps {
  statistics: Record<string, any>;
  classification?: Record<string, any>;
}

export default function StatisticsVisualization({ statistics, classification }: StatisticsVisualizationProps) {
  if (!statistics || Object.keys(statistics).length === 0) return null;

  // Define stat categories with icons and colors
  const statConfig: Record<string, { icon: string; color: string; gradient: string }> = {
    total_files: {
      icon: '📁',
      color: 'text-blue-400',
      gradient: 'from-blue-500 to-cyan-500'
    },
    python_files: {
      icon: '🐍',
      color: 'text-yellow-400',
      gradient: 'from-yellow-500 to-amber-500'
    },
    notebook_files: {
      icon: '📓',
      color: 'text-orange-400',
      gradient: 'from-orange-500 to-red-500'
    },
    config_files: {
      icon: '⚙️',
      color: 'text-purple-400',
      gradient: 'from-purple-500 to-pink-500'
    },
    framework_count: {
      icon: '🔧',
      color: 'text-green-400',
      gradient: 'from-green-500 to-emerald-500'
    },
    medical_signal_count: {
      icon: '🏥',
      color: 'text-red-400',
      gradient: 'from-red-500 to-pink-500'
    },
    workflow_stages: {
      icon: '⚡',
      color: 'text-indigo-400',
      gradient: 'from-indigo-500 to-purple-500'
    },
    confidence_score: {
      icon: '🎯',
      color: 'text-cyan-400',
      gradient: 'from-cyan-500 to-blue-500'
    }
  };

  const getStatConfig = (key: string) => {
    return statConfig[key] || {
      icon: '📊',
      color: 'text-gray-400',
      gradient: 'from-gray-500 to-slate-500'
    };
  };

  // Format stat labels
  const formatLabel = (key: string) => {
    return key
      .replace(/_/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  // Calculate percentage for progress bars (normalize to 100)
  const getPercentage = (value: any, key: string) => {
    const numValue = typeof value === 'number' ? value : parseInt(value) || 0;
    
    // Different normalization based on stat type
    if (key.includes('confidence') || key.includes('score')) {
      return Math.min(numValue, 100);
    }
    if (key.includes('count')) {
      return Math.min((numValue / 20) * 100, 100); // Normalize counts to max 20
    }
    if (key.includes('files')) {
      return Math.min((numValue / 100) * 100, 100); // Normalize files to max 100
    }
    return Math.min((numValue / 10) * 100, 100);
  };

  // Separate stats into categories
  const fileStats = Object.entries(statistics).filter(([key]) => 
    key.includes('file') || key === 'total_files'
  );
  
  const detectionStats = Object.entries(statistics).filter(([key]) => 
    key.includes('count') || key.includes('detected')
  );
  
  const otherStats = Object.entries(statistics).filter(([key]) => 
    !key.includes('file') && !key.includes('count') && !key.includes('detected')
  );

  return (
    <div className="relative bg-gradient-to-br from-blue-900/20 via-gray-800/50 to-gray-900/50 backdrop-blur-xl border border-blue-500/30 rounded-3xl p-8 shadow-2xl overflow-hidden">
      {/* Section header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-500/30 to-cyan-500/30 rounded-2xl flex items-center justify-center">
            <svg className="w-7 h-7 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold text-white">Repository Statistics</h3>
        </div>
        <div className="h-1 w-24 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full"></div>
      </div>

      {/* Main statistics grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {Object.entries(statistics).slice(0, 8).map(([key, value], index) => {
          const config = getStatConfig(key);
          
          return (
            <div
              key={key}
              className="group relative bg-gradient-to-br from-gray-700/30 to-gray-800/30 backdrop-blur-sm rounded-2xl p-6 text-center border border-gray-600/50 hover:border-blue-500/50 transition-all duration-500 hover:scale-105 hover:shadow-xl animate-slide-up"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              {/* Glow effect */}
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 to-blue-500/10 opacity-0 group-hover:opacity-100 rounded-2xl transition-opacity duration-500"></div>

              <div className="relative z-10">
                {/* Icon */}
                <div className="text-3xl mb-3 group-hover:scale-110 transition-transform duration-300">
                  {config.icon}
                </div>

                {/* Value */}
                <p className={`text-3xl font-bold bg-gradient-to-r ${config.gradient} bg-clip-text text-transparent mb-2 group-hover:scale-110 transition-transform duration-300`}>
                  {String(value)}
                </p>

                {/* Label */}
                <p className="text-xs text-gray-400 font-medium">
                  {formatLabel(key)}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Detailed statistics with progress bars */}
      {fileStats.length > 0 && (
        <div className="mb-8 animate-fade-in-up" style={{ animationDelay: '400ms' }}>
          <h4 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <span>📁</span>
            File Statistics
          </h4>
          <div className="space-y-3">
            {fileStats.map(([key, value], index) => {
              const config = getStatConfig(key);
              const percentage = getPercentage(value, key);
              
              return (
                <div key={key} className="group">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{config.icon}</span>
                      <span className="text-sm text-gray-300 font-medium">{formatLabel(key)}</span>
                    </div>
                    <span className={`text-sm font-bold ${config.color}`}>{String(value)}</span>
                  </div>
                  <div className="h-2 bg-gray-700/50 rounded-full overflow-hidden">
                    <div
                      className={`h-full bg-gradient-to-r ${config.gradient} rounded-full transition-all duration-1000 ease-out`}
                      style={{ 
                        width: `${percentage}%`,
                        animationDelay: `${index * 100}ms`
                      }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Detection statistics */}
      {detectionStats.length > 0 && (
        <div className="mb-8 animate-fade-in-up" style={{ animationDelay: '500ms' }}>
          <h4 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <span>🔍</span>
            Detection Statistics
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {detectionStats.map(([key, value], index) => {
              const config = getStatConfig(key);
              const percentage = getPercentage(value, key);
              
              return (
                <div
                  key={key}
                  className="bg-gradient-to-br from-gray-700/20 to-gray-800/20 backdrop-blur-sm rounded-xl p-4 border border-gray-600/30 hover:border-blue-500/30 transition-all duration-300"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">{config.icon}</span>
                      <span className="text-sm text-gray-300 font-medium">{formatLabel(key)}</span>
                    </div>
                    <span className={`text-xl font-bold ${config.color}`}>{String(value)}</span>
                  </div>
                  <div className="h-1.5 bg-gray-700/50 rounded-full overflow-hidden">
                    <div
                      className={`h-full bg-gradient-to-r ${config.gradient} rounded-full transition-all duration-1000 ease-out`}
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Classification confidence if available */}
      {classification?.confidence && (
        <div className="animate-fade-in-up" style={{ animationDelay: '600ms' }}>
          <div className="bg-gradient-to-br from-purple-500/10 to-pink-500/10 backdrop-blur-sm rounded-xl p-6 border border-purple-500/30">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <span className="text-2xl">🎯</span>
                <div>
                  <h4 className="text-lg font-bold text-white">Classification Confidence</h4>
                  <p className="text-sm text-gray-400">Overall detection accuracy</p>
                </div>
              </div>
              <span className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                {classification.confidence}
              </span>
            </div>
            <div className="h-3 bg-gray-700/50 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full transition-all duration-1000 ease-out animate-pulse"
                style={{ width: `${classification.confidence}` }}
              ></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Made with Bob