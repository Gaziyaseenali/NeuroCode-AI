'use client';

import { useState, useEffect } from 'react';
import { RepositoryIntelligence, ProcessingProgress } from '@/lib/api/types';
import CinematicLoader from './CinematicLoader';
import RepositoryDashboard from './RepositoryDashboard';

interface RepositoryResultsProps {
  data: RepositoryIntelligence | null;
  isLoading: boolean;
  processingStage?: ProcessingProgress;
}

export default function RepositoryResults({ data, isLoading, processingStage }: RepositoryResultsProps) {
  // Progressive reveal state
  const [revealStage, setRevealStage] = useState(0);
  const [isRevealing, setIsRevealing] = useState(false);

  // Reset reveal stage when new data arrives
  useEffect(() => {
    if (data && !isLoading) {
      setIsRevealing(true);
      setRevealStage(0);
      
      // Progressive reveal timing - extended for premium intelligence sections
      const timings = [0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300]; // 12 stages
      
      timings.forEach((delay, index) => {
        setTimeout(() => {
          setRevealStage(index + 1);
          if (index === timings.length - 1) {
            setTimeout(() => setIsRevealing(false), 500);
          }
        }, delay);
      });
    }
  }, [data, isLoading]);

  // Show cinematic loader during analysis
  if (isLoading) {
    return <CinematicLoader processingStage={processingStage} />;
  }

  // No data state
  if (!data) {
    return null;
  }

  return (
    <div className="w-full mt-12">
      {/* Main Dashboard */}
      <RepositoryDashboard data={data} revealStage={revealStage} />

      {/* Global animation styles */}
      <style jsx>{`
        @keyframes fade-in-up {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes slide-up {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fade-in {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        .animate-fade-in-up {
          animation: fade-in-up 0.6s ease-out forwards;
        }

        .animate-slide-up {
          animation: slide-up 0.5s ease-out forwards;
        }

        .animate-fade-in {
          animation: fade-in 0.5s ease-out forwards;
        }
      `}</style>
    </div>
  );
}

// Made with Bob
