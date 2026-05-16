'use client';

import { RepositoryMetadataCard, FrameworkVisualization, MedicalAISignalCard } from '@/lib/api/types';

interface MetadataCardProps {
  metadata: RepositoryMetadataCard;
  delay?: number;
}

export function MetadataCard({ metadata, delay = 0 }: MetadataCardProps) {
  return (
    <div 
      className="group relative bg-gradient-to-br from-gray-800/90 via-gray-900/90 to-gray-800/90 backdrop-blur-xl border border-gray-700/50 rounded-3xl p-8 shadow-2xl overflow-hidden transition-all duration-500 hover:scale-[1.02] hover:border-blue-500/50 animate-slide-up"
      style={{ animationDelay: `${delay}ms` }}
    >
      {/* Glassmorphism overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
      
      {/* Animated gradient border glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-500/0 via-purple-500/20 to-blue-500/0 opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-500"></div>

      <div className="relative z-10 flex items-start gap-6">
        {metadata.avatar_url && (
          <div className="relative group/avatar">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-500 rounded-2xl blur-lg opacity-0 group-hover/avatar:opacity-50 transition-opacity duration-300"></div>
            <img 
              src={metadata.avatar_url} 
              alt={metadata.owner}
              className="relative w-24 h-24 rounded-2xl border-2 border-gray-600 group-hover/avatar:border-blue-500 transition-all duration-300 transform group-hover/avatar:scale-105"
            />
          </div>
        )}
        
        <div className="flex-1 space-y-4">
          <div className="flex items-center gap-3 mb-2">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-white via-blue-100 to-white bg-clip-text text-transparent">
              {metadata.name}
            </h2>
            <a 
              href={metadata.html_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 transition-all duration-300 hover:scale-110 transform"
            >
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
                <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
              </svg>
            </a>
          </div>
          
          <p className="text-gray-400 font-medium">{metadata.owner}</p>
          
          {metadata.description && (
            <p className="text-gray-300 leading-relaxed">{metadata.description}</p>
          )}
          
          {/* Stats with hover effects */}
          <div className="flex flex-wrap gap-3">
            <div className="group/stat flex items-center gap-2 px-4 py-2 bg-gradient-to-br from-gray-700/50 to-gray-800/50 rounded-xl border border-gray-600/50 hover:border-yellow-500/50 transition-all duration-300 hover:scale-105">
              <svg className="w-5 h-5 text-yellow-400 group-hover/stat:animate-pulse" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              <span className="text-sm font-bold text-white">{metadata.stars.toLocaleString()}</span>
            </div>
            
            <div className="group/stat flex items-center gap-2 px-4 py-2 bg-gradient-to-br from-gray-700/50 to-gray-800/50 rounded-xl border border-gray-600/50 hover:border-blue-500/50 transition-all duration-300 hover:scale-105">
              <svg className="w-5 h-5 text-blue-400 group-hover/stat:animate-pulse" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M7.707 3.293a1 1 0 010 1.414L5.414 7H11a7 7 0 017 7v2a1 1 0 11-2 0v-2a5 5 0 00-5-5H5.414l2.293 2.293a1 1 0 11-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              <span className="text-sm font-bold text-white">{metadata.forks.toLocaleString()}</span>
            </div>
            
            {metadata.language && (
              <div className="px-4 py-2 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl border border-purple-500/30 hover:border-purple-400/50 transition-all duration-300 hover:scale-105">
                <span className="text-sm font-bold text-purple-200">{metadata.language}</span>
              </div>
            )}
          </div>

          {/* Topics with staggered animation */}
          {metadata.topics.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {metadata.topics.map((topic, index) => (
                <span 
                  key={topic}
                  className="px-3 py-1.5 bg-blue-500/10 text-blue-300 text-xs font-medium rounded-full border border-blue-500/30 hover:bg-blue-500/20 hover:border-blue-400/50 transition-all duration-300 hover:scale-105 animate-fade-in"
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  {topic}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

interface FrameworkCardProps {
  framework: FrameworkVisualization;
  index: number;
}

export function FrameworkCard({ framework, index }: FrameworkCardProps) {
  const confidenceColors = {
    high: 'from-green-500/20 to-emerald-500/20 border-green-500/40 hover:border-green-400/60',
    medium: 'from-yellow-500/20 to-amber-500/20 border-yellow-500/40 hover:border-yellow-400/60',
    low: 'from-gray-500/20 to-slate-500/20 border-gray-500/40 hover:border-gray-400/60'
  };

  const confidenceBadgeColors = {
    high: 'bg-green-500/20 text-green-300 border-green-500/40',
    medium: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/40',
    low: 'bg-gray-500/20 text-gray-300 border-gray-500/40'
  };

  return (
    <div 
      className={`group relative bg-gradient-to-br ${confidenceColors[framework.confidence as keyof typeof confidenceColors]} backdrop-blur-sm rounded-2xl p-5 border-2 transition-all duration-500 hover:scale-105 hover:shadow-2xl animate-slide-up`}
      style={{ animationDelay: `${index * 100}ms` }}
    >
      {/* Glow effect on hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 rounded-2xl transition-opacity duration-500"></div>
      
      <div className="relative z-10 space-y-3">
        <div className="flex items-center justify-between">
          <h4 className="font-bold text-white text-lg group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-gray-300 group-hover:bg-clip-text transition-all duration-300">
            {framework.name}
          </h4>
          <span className={`px-3 py-1 text-xs font-semibold rounded-full border ${confidenceBadgeColors[framework.confidence as keyof typeof confidenceBadgeColors]} transition-all duration-300 group-hover:scale-110`}>
            {framework.confidence}
          </span>
        </div>
        
        <p className="text-sm text-gray-400 font-medium">{framework.category}</p>
        
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
          </svg>
          <span>{framework.evidence_count} evidence files</span>
        </div>
      </div>
    </div>
  );
}

interface MedicalSignalCardProps {
  signal: MedicalAISignalCard;
  index: number;
}

export function MedicalSignalCard({ signal, index }: MedicalSignalCardProps) {
  const confidenceColors = {
    high: 'from-red-500/15 to-pink-500/15 border-red-500/40',
    medium: 'from-orange-500/15 to-amber-500/15 border-orange-500/40',
    low: 'from-gray-500/15 to-slate-500/15 border-gray-500/40'
  };

  const confidenceBadgeColors = {
    high: 'bg-red-500/20 text-red-300 border-red-500/40',
    medium: 'bg-orange-500/20 text-orange-300 border-orange-500/40',
    low: 'bg-gray-500/20 text-gray-300 border-gray-500/40'
  };

  return (
    <div 
      className={`group relative bg-gradient-to-br ${confidenceColors[signal.confidence as keyof typeof confidenceColors]} backdrop-blur-sm rounded-2xl p-6 border-2 hover:border-red-400/60 transition-all duration-500 hover:scale-[1.02] hover:shadow-2xl animate-slide-up`}
      style={{ animationDelay: `${index * 100}ms` }}
    >
      {/* Pulse effect for high confidence */}
      {signal.confidence === 'high' && (
        <div className="absolute inset-0 bg-red-500/10 rounded-2xl animate-pulse"></div>
      )}
      
      {/* Glassmorphism overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 rounded-2xl transition-opacity duration-500"></div>
      
      <div className="relative z-10 space-y-4">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-red-500/30 to-pink-500/30 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
              <svg className="w-6 h-6 text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <h4 className="font-bold text-white text-lg">{signal.signal_type}</h4>
          </div>
          <span className={`px-3 py-1 text-xs font-semibold rounded-full border ${confidenceBadgeColors[signal.confidence as keyof typeof confidenceBadgeColors]} transition-all duration-300 group-hover:scale-110`}>
            {signal.confidence}
          </span>
        </div>
        
        <p className="text-sm text-gray-300 leading-relaxed">{signal.description}</p>
        
        {signal.evidence.length > 0 && (
          <div className="space-y-2">
            <p className="text-xs text-gray-500 font-semibold">Evidence:</p>
            <div className="flex flex-wrap gap-2">
              {signal.evidence.slice(0, 3).map((file, i) => (
                <span 
                  key={i} 
                  className="text-xs text-gray-400 bg-gray-800/50 px-3 py-1.5 rounded-lg border border-gray-700/50 hover:border-red-500/30 transition-all duration-300 hover:scale-105 font-mono"
                >
                  {file}
                </span>
              ))}
              {signal.evidence.length > 3 && (
                <span className="text-xs text-gray-500 px-3 py-1.5">
                  +{signal.evidence.length - 3} more
                </span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Made with Bob