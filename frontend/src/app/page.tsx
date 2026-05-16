'use client';

import { useState } from 'react';
import { analyzeRepository } from '@/lib/api/client';
import { RepositoryIntelligence, ProcessingProgress, RepositoryAnalysisError } from '@/lib/api/types';
import RepositoryInput from '@/components/RepositoryInput';
import RepositoryResults from '@/components/RepositoryResults';

export default function Home() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisData, setAnalysisData] = useState<RepositoryIntelligence | null>(null);
  const [processingStage, setProcessingStage] = useState<ProcessingProgress | undefined>();
  const [error, setError] = useState<string>('');

  const handleAnalyze = async (url: string) => {
    setIsAnalyzing(true);
    setError('');
    setAnalysisData(null);
    
    // Simulate processing stages for better UX - Enhanced for premium intelligence
    const stages: ProcessingProgress[] = [
      { stage: 'parsing', progress: 8, message: 'Parsing repository URL...' },
      { stage: 'fetching_metadata', progress: 20, message: 'Fetching repository metadata...' },
      { stage: 'analyzing_structure', progress: 35, message: 'Analyzing repository structure...' },
      { stage: 'detecting_frameworks', progress: 50, message: 'Detecting frameworks and tools...' },
      { stage: 'generating_intelligence', progress: 65, message: 'Generating AI reasoning...' },
      { stage: 'generating_intelligence', progress: 75, message: 'Assessing repository maturity...' },
      { stage: 'generating_intelligence', progress: 85, message: 'Analyzing architecture patterns...' },
      { stage: 'generating_intelligence', progress: 95, message: 'Creating executive summary...' },
    ];

    let stageIndex = 0;
    const stageInterval = setInterval(() => {
      if (stageIndex < stages.length) {
        setProcessingStage(stages[stageIndex]);
        stageIndex++;
      }
    }, 800);

    try {
      const result = await analyzeRepository({ url });
      clearInterval(stageInterval);
      setProcessingStage({ stage: 'complete', progress: 100, message: 'Analysis complete!' });
      
      setTimeout(() => {
        setAnalysisData(result);
        setIsAnalyzing(false);
        setProcessingStage(undefined);
      }, 500);
    } catch (err: any) {
      clearInterval(stageInterval);
      setIsAnalyzing(false);
      setProcessingStage(undefined);
      
      // Handle structured error response
      if (err.error && err.error.message) {
        const errorDetail = err.error as RepositoryAnalysisError['error'];
        setError(errorDetail.message);
      } else if (err.message) {
        setError(err.message);
      } else {
        setError('Failed to analyze repository. Please try again.');
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
      {/* Animated background effect */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-pink-500/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16 pt-8 animate-fade-in-down">
          {/* Logo/Icon */}
          <div className="flex justify-center mb-6">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl blur-xl opacity-50"></div>
              <div className="relative bg-gradient-to-br from-gray-800 to-gray-900 p-4 rounded-2xl border border-gray-700">
                <svg className="w-12 h-12 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
            </div>
          </div>

          {/* Title */}
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              NeuroCode AI
            </span>
          </h1>

          {/* Tagline */}
          <p className="text-xl md:text-2xl text-gray-300 mb-3 font-light">
            Repository Intelligence & AI Research Acceleration
          </p>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Instantly analyze GitHub repositories to discover frameworks, detect medical AI signals, 
            and understand project architecture with AI-powered intelligence.
          </p>

          {/* Feature badges */}
          <div className="flex flex-wrap justify-center gap-3 mt-8">
            {[
              { icon: '🔍', text: 'Smart Analysis' },
              { icon: '🧠', text: 'AI Detection' },
              { icon: '⚡', text: 'Instant Results' },
              { icon: '🏥', text: 'Medical AI Focus' }
            ].map((feature, i) => (
              <div 
                key={i}
                className="px-4 py-2 bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-full text-sm text-gray-300 flex items-center gap-2"
              >
                <span>{feature.icon}</span>
                <span>{feature.text}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Repository Input */}
        <RepositoryInput onAnalyze={handleAnalyze} isLoading={isAnalyzing} />

        {/* Error Display */}
        {error && (
          <div className="max-w-3xl mx-auto mt-6">
            <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 backdrop-blur-sm">
              <div className="flex items-start gap-3">
                <svg className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <div className="flex-1">
                  <h3 className="text-red-300 font-semibold mb-1">Analysis Failed</h3>
                  <p className="text-red-200 text-sm">{error}</p>
                </div>
                <button 
                  onClick={() => setError('')}
                  className="text-red-400 hover:text-red-300 transition-colors"
                >
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        <RepositoryResults 
          data={analysisData} 
          isLoading={isAnalyzing}
          processingStage={processingStage}
        />

        {/* Features Section (shown when no analysis) */}
        {!isAnalyzing && !analysisData && !error && (
          <div className="max-w-6xl mx-auto mt-20">
            <h2 className="text-3xl font-bold text-center text-white mb-12">
              Powerful Repository Intelligence
            </h2>
            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  icon: (
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                  ),
                  title: 'Framework Detection',
                  description: 'Automatically identify ML frameworks, medical imaging libraries, and development tools used in the repository.'
                },
                {
                  icon: (
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                    </svg>
                  ),
                  title: 'Medical AI Signals',
                  description: 'Detect medical imaging capabilities, healthcare AI patterns, and clinical research indicators.'
                },
                {
                  icon: (
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  ),
                  title: 'Project Analytics',
                  description: 'Get comprehensive statistics, repository classification, and structural insights at a glance.'
                }
              ].map((feature, i) => (
                <div 
                  key={i}
                  className="bg-gray-800/30 backdrop-blur-sm border border-gray-700 rounded-2xl p-6 hover:border-blue-500/50 transition-all"
                >
                  <div className="text-blue-400 mb-4">{feature.icon}</div>
                  <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
                  <p className="text-gray-400">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="mt-20 text-center text-gray-500 text-sm">
          <p>Powered by NeuroCode AI • Built for AI Research Acceleration</p>
        </footer>
      </div>
    </div>
  );
}

// Made with Bob
