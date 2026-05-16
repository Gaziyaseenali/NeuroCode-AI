'use client';

import { useState } from 'react';
import { validateGitHubUrl } from '@/lib/api/client';

interface RepositoryInputProps {
  onAnalyze: (url: string) => void;
  isLoading: boolean;
}

export default function RepositoryInput({ onAnalyze, isLoading }: RepositoryInputProps) {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!url.trim()) {
      setError('Please enter a GitHub repository URL');
      return;
    }

    if (!validateGitHubUrl(url)) {
      setError('Please enter a valid GitHub repository URL (e.g., https://github.com/owner/repo)');
      return;
    }

    onAnalyze(url.trim());
  };

  return (
    <div className="w-full max-w-3xl mx-auto animate-fade-in-up animation-delay-200">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative group">
          {/* Glow effect on focus */}
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500/0 via-blue-500/20 to-purple-500/0 rounded-xl blur-xl opacity-0 group-focus-within:opacity-100 transition-opacity duration-500"></div>
          
          <input
            type="text"
            value={url}
            onChange={(e) => {
              setUrl(e.target.value);
              setError('');
            }}
            placeholder="https://github.com/owner/repository"
            disabled={isLoading}
            className={`relative w-full px-6 py-4 bg-gray-800/50 backdrop-blur-sm border-2 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:bg-gray-800/70 transition-all duration-300 ${
              error ? 'border-red-500 animate-shake' : 'border-gray-700'
            } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
          />
          {error && (
            <p className="mt-2 text-sm text-red-400 flex items-center gap-2">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {error}
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="relative w-full px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-semibold rounded-xl transition-all transform hover:scale-[1.02] disabled:scale-100 disabled:cursor-not-allowed shadow-lg hover:shadow-2xl hover:shadow-blue-500/50 overflow-hidden group"
        >
          {/* Shine effect on hover */}
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-200%] group-hover:translate-x-[200%] transition-transform duration-1000"></div>
          
          {isLoading ? (
            <span className="flex items-center justify-center gap-3">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Analyzing Repository...
            </span>
          ) : (
            <span className="flex items-center justify-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              Analyze Repository
            </span>
          )}
        </button>
      </form>

      {/* Example URLs */}
      <div className="mt-6 text-center">
        <p className="text-sm text-gray-400 mb-2">Try an example:</p>
        <div className="flex flex-wrap gap-2 justify-center">
          {[
            'https://github.com/Project-MONAI/MONAI',
            'https://github.com/facebookresearch/segment-anything',
            'https://github.com/huggingface/transformers'
          ].map((exampleUrl) => (
            <button
              key={exampleUrl}
              onClick={() => {
                setUrl(exampleUrl);
                setError('');
              }}
              disabled={isLoading}
              className="px-3 py-1 text-xs bg-gray-800/50 hover:bg-gray-700/50 text-gray-300 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {exampleUrl.split('/').slice(-2).join('/')}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

// Made with Bob
