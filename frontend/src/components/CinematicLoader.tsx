'use client';

import { ProcessingProgress } from '@/lib/api/types';

interface CinematicLoaderProps {
  processingStage?: ProcessingProgress;
}

export default function CinematicLoader({ processingStage }: CinematicLoaderProps) {
  const stages = [
    { key: 'parsing', label: 'Parsing Repository', icon: '🔍' },
    { key: 'fetching_metadata', label: 'Fetching Metadata', icon: '📦' },
    { key: 'analyzing_structure', label: 'Analyzing Structure', icon: '🏗️' },
    { key: 'detecting_frameworks', label: 'Detecting Frameworks', icon: '⚙️' },
    { key: 'generating_intelligence', label: 'Generating Intelligence', icon: '🧠' },
  ];

  const currentStageIndex = stages.findIndex(s => s.key === processingStage?.stage);

  return (
    <div className="w-full max-w-6xl mx-auto mt-12">
      <div className="relative bg-gradient-to-br from-gray-900/95 via-gray-800/95 to-gray-900/95 backdrop-blur-xl border border-gray-700/50 rounded-3xl p-12 shadow-2xl overflow-hidden">
        {/* Animated background gradients */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
        </div>

        <div className="relative z-10 flex flex-col items-center justify-center space-y-8">
          {/* Main animated spinner with glow */}
          <div className="relative">
            {/* Outer glow ring */}
            <div className="absolute inset-0 w-32 h-32 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full blur-2xl opacity-50 animate-pulse"></div>
            
            {/* Spinning rings */}
            <div className="relative w-32 h-32">
              {/* Outer ring */}
              <div className="absolute inset-0 border-4 border-gray-700/50 rounded-full"></div>
              
              {/* Animated ring 1 */}
              <div className="absolute inset-0 border-4 border-transparent border-t-blue-500 border-r-blue-500 rounded-full animate-spin"></div>
              
              {/* Animated ring 2 - slower, opposite direction */}
              <div className="absolute inset-2 border-4 border-transparent border-b-purple-500 border-l-purple-500 rounded-full animate-spin-slow-reverse"></div>
              
              {/* Center pulse */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full animate-pulse-scale"></div>
              </div>
            </div>
          </div>

          {/* Processing stage with smooth transitions */}
          {processingStage && (
            <div className="text-center space-y-4 w-full max-w-md animate-fade-in">
              {/* Stage icon and message */}
              <div className="flex items-center justify-center gap-3">
                <span className="text-4xl animate-bounce-subtle">
                  {stages[currentStageIndex]?.icon || '⚡'}
                </span>
                <h3 className="text-2xl font-bold text-white">
                  {processingStage.message}
                </h3>
              </div>

              {/* Progress bar with gradient */}
              <div className="relative w-full h-3 bg-gray-700/50 rounded-full overflow-hidden backdrop-blur-sm">
                {/* Background shimmer */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent animate-shimmer"></div>
                
                {/* Progress fill */}
                <div 
                  className="h-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-full transition-all duration-700 ease-out relative overflow-hidden"
                  style={{ width: `${processingStage.progress}%` }}
                >
                  {/* Animated shine effect */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shine"></div>
                </div>
              </div>

              {/* Progress percentage */}
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-400">{processingStage.progress}% complete</span>
                <span className="text-blue-400 font-semibold animate-pulse">Processing...</span>
              </div>
            </div>
          )}

          {/* Stage indicators */}
          <div className="flex items-center gap-3 mt-4">
            {stages.map((stage, index) => (
              <div
                key={stage.key}
                className={`transition-all duration-500 ${
                  index <= currentStageIndex
                    ? 'w-12 h-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full'
                    : 'w-8 h-2 bg-gray-700 rounded-full'
                }`}
              />
            ))}
          </div>

          {/* AI-style processing text */}
          <div className="text-center space-y-2 animate-fade-in-delay">
            <p className="text-gray-400 text-sm font-mono">
              <span className="inline-block animate-pulse">▸</span> AI-powered analysis in progress
            </p>
            <div className="flex items-center justify-center gap-2 text-xs text-gray-500">
              <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></div>
              <span>Neural networks active</span>
            </div>
          </div>
        </div>
      </div>

      {/* Custom animations in style tag */}
      <style jsx>{`
        @keyframes spin-slow-reverse {
          from {
            transform: rotate(360deg);
          }
          to {
            transform: rotate(0deg);
          }
        }

        @keyframes pulse-scale {
          0%, 100% {
            transform: scale(1);
            opacity: 0.8;
          }
          50% {
            transform: scale(1.1);
            opacity: 1;
          }
        }

        @keyframes bounce-subtle {
          0%, 100% {
            transform: translateY(0);
          }
          50% {
            transform: translateY(-5px);
          }
        }

        @keyframes shimmer {
          0% {
            transform: translateX(-100%);
          }
          100% {
            transform: translateX(100%);
          }
        }

        @keyframes shine {
          0% {
            transform: translateX(-100%);
          }
          100% {
            transform: translateX(200%);
          }
        }

        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fade-in-delay {
          0% {
            opacity: 0;
            transform: translateY(10px);
          }
          50% {
            opacity: 0;
            transform: translateY(10px);
          }
          100% {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-spin-slow-reverse {
          animation: spin-slow-reverse 3s linear infinite;
        }

        .animate-pulse-scale {
          animation: pulse-scale 2s ease-in-out infinite;
        }

        .animate-bounce-subtle {
          animation: bounce-subtle 2s ease-in-out infinite;
        }

        .animate-shimmer {
          animation: shimmer 2s ease-in-out infinite;
        }

        .animate-shine {
          animation: shine 2s ease-in-out infinite;
        }

        .animate-fade-in {
          animation: fade-in 0.5s ease-out forwards;
        }

        .animate-fade-in-delay {
          animation: fade-in-delay 1s ease-out forwards;
        }
      `}</style>
    </div>
  );
}

// Made with Bob