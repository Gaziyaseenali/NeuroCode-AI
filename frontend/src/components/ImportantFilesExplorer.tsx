'use client';

import { ImportantFileHighlight } from '@/lib/api/types';

interface ImportantFilesExplorerProps {
  files: ImportantFileHighlight[];
}

export default function ImportantFilesExplorer({ files }: ImportantFilesExplorerProps) {
  if (!files || files.length === 0) return null;

  // File category icons and colors
  const categoryConfig: Record<string, { icon: string; color: string; bgColor: string; borderColor: string }> = {
    training: {
      icon: '🧠',
      color: 'text-purple-300',
      bgColor: 'from-purple-500/20 to-pink-500/20',
      borderColor: 'border-purple-500/40 hover:border-purple-400/60'
    },
    inference: {
      icon: '🎯',
      color: 'text-blue-300',
      bgColor: 'from-blue-500/20 to-cyan-500/20',
      borderColor: 'border-blue-500/40 hover:border-blue-400/60'
    },
    model: {
      icon: '🏗️',
      color: 'text-green-300',
      bgColor: 'from-green-500/20 to-emerald-500/20',
      borderColor: 'border-green-500/40 hover:border-green-400/60'
    },
    config: {
      icon: '⚙️',
      color: 'text-yellow-300',
      bgColor: 'from-yellow-500/20 to-amber-500/20',
      borderColor: 'border-yellow-500/40 hover:border-yellow-400/60'
    },
    notebook: {
      icon: '📓',
      color: 'text-orange-300',
      bgColor: 'from-orange-500/20 to-red-500/20',
      borderColor: 'border-orange-500/40 hover:border-orange-400/60'
    },
    requirements: {
      icon: '📦',
      color: 'text-indigo-300',
      bgColor: 'from-indigo-500/20 to-purple-500/20',
      borderColor: 'border-indigo-500/40 hover:border-indigo-400/60'
    },
    data: {
      icon: '💾',
      color: 'text-cyan-300',
      bgColor: 'from-cyan-500/20 to-blue-500/20',
      borderColor: 'border-cyan-500/40 hover:border-cyan-400/60'
    },
    documentation: {
      icon: '📚',
      color: 'text-gray-300',
      bgColor: 'from-gray-500/20 to-slate-500/20',
      borderColor: 'border-gray-500/40 hover:border-gray-400/60'
    },
    default: {
      icon: '📄',
      color: 'text-gray-300',
      bgColor: 'from-gray-500/20 to-slate-500/20',
      borderColor: 'border-gray-500/40 hover:border-gray-400/60'
    }
  };

  const importanceConfig = {
    critical: { label: 'Critical', color: 'text-red-300', bgColor: 'bg-red-500/20', borderColor: 'border-red-500/40' },
    high: { label: 'High', color: 'text-orange-300', bgColor: 'bg-orange-500/20', borderColor: 'border-orange-500/40' },
    medium: { label: 'Medium', color: 'text-yellow-300', bgColor: 'bg-yellow-500/20', borderColor: 'border-yellow-500/40' },
    low: { label: 'Low', color: 'text-gray-300', bgColor: 'bg-gray-500/20', borderColor: 'border-gray-500/40' }
  };

  const getConfig = (category: string) => {
    return categoryConfig[category.toLowerCase()] || categoryConfig.default;
  };

  const getImportanceConfig = (importance: string) => {
    return importanceConfig[importance.toLowerCase() as keyof typeof importanceConfig] || importanceConfig.low;
  };

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return '';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="relative bg-gradient-to-br from-teal-900/20 via-gray-800/50 to-gray-900/50 backdrop-blur-xl border border-teal-500/30 rounded-3xl p-8 shadow-2xl overflow-hidden">
      {/* Section header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 bg-gradient-to-br from-teal-500/30 to-cyan-500/30 rounded-2xl flex items-center justify-center">
            <svg className="w-7 h-7 text-teal-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold text-white">Important Files</h3>
          <span className="px-3 py-1 bg-teal-500/20 text-teal-300 text-xs font-bold rounded-full border border-teal-500/40">
            {files.length} files
          </span>
        </div>
        <div className="h-1 w-24 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-full"></div>
      </div>

      {/* Files grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {files.map((file, index) => {
          const config = getConfig(file.category);
          const importanceConf = getImportanceConfig(file.importance);

          return (
            <div
              key={index}
              className={`group relative bg-gradient-to-br ${config.bgColor} backdrop-blur-sm rounded-2xl p-5 border-2 ${config.borderColor} transition-all duration-500 hover:scale-105 hover:shadow-2xl animate-fade-in-up`}
              style={{ animationDelay: `${index * 50}ms` }}
            >
              {/* Glow effect on hover */}
              <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 rounded-2xl transition-opacity duration-500"></div>

              <div className="relative z-10 space-y-3">
                {/* Header with icon and importance */}
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="text-2xl group-hover:scale-110 transition-transform duration-300">
                      {config.icon}
                    </span>
                    <span className={`text-xs font-semibold px-2 py-1 rounded-full ${importanceConf.bgColor} ${importanceConf.color} border ${importanceConf.borderColor}`}>
                      {importanceConf.label}
                    </span>
                  </div>
                </div>

                {/* File name */}
                <h4 className={`font-bold ${config.color} text-base group-hover:text-white transition-colors duration-300 truncate`}>
                  {file.name}
                </h4>

                {/* Category badge */}
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-400 font-medium capitalize">
                    {file.category}
                  </span>
                  {file.size && (
                    <>
                      <span className="text-gray-600">•</span>
                      <span className="text-xs text-gray-500">
                        {formatFileSize(file.size)}
                      </span>
                    </>
                  )}
                </div>

                {/* Description */}
                <p className="text-sm text-gray-400 leading-relaxed line-clamp-2">
                  {file.description}
                </p>

                {/* File path */}
                <div className="pt-2 border-t border-gray-700/50">
                  <div className="flex items-center gap-2 text-xs text-gray-500">
                    <svg className="w-3 h-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M2 6a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1H8a3 3 0 00-3 3v1.5a1.5 1.5 0 01-3 0V6z" clipRule="evenodd" />
                      <path d="M6 12a2 2 0 012-2h8a2 2 0 012 2v2a2 2 0 01-2 2H2h2a2 2 0 002-2v-2z" />
                    </svg>
                    <span className="font-mono truncate">{file.path}</span>
                  </div>
                </div>
              </div>

              {/* Hover indicator */}
              <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </div>
            </div>
          );
        })}
      </div>

      {/* Category legend */}
      <div className="mt-8 pt-6 border-t border-gray-700/50">
        <p className="text-xs text-gray-500 mb-3 font-semibold">File Categories:</p>
        <div className="flex flex-wrap gap-3">
          {Object.entries(categoryConfig).filter(([key]) => key !== 'default').map(([key, config]) => (
            <div key={key} className="flex items-center gap-2 text-xs">
              <span className="text-lg">{config.icon}</span>
              <span className="text-gray-400 capitalize">{key}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// Made with Bob