'use client';

import { RepositoryIntelligence } from '@/lib/api/types';
import { MetadataCard, MedicalSignalCard } from './IntelligenceCards';
import WorkflowVisualization from './WorkflowVisualization';
import ImportantFilesExplorer from './ImportantFilesExplorer';
import FrameworkIntelligence from './FrameworkIntelligence';
import StatisticsVisualization from './StatisticsVisualization';
import {
  AIReasoningSection,
  MaturitySection,
  ArchitectureInsightsSection,
  ExecutiveSummarySection
} from './PremiumIntelligence';

interface RepositoryDashboardProps {
  data: RepositoryIntelligence;
  revealStage: number;
}

export default function RepositoryDashboard({ data, revealStage }: RepositoryDashboardProps) {
  const {
    metadata_card,
    frameworks,
    workflow_nodes,
    medical_signals,
    important_files,
    classification,
    statistics,
    llm_summary,
    ai_reasoning,
    maturity_badge,
    maturity_indicators,
    architecture_insights,
    executive_summary
  } = data;

  return (
    <div className="w-full max-w-7xl mx-auto space-y-8">
      {/* Stage 1: Repository Overview - Metadata Card */}
      {metadata_card && revealStage >= 1 && (
        <section className="animate-fade-in-up">
          <div className="mb-3">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></span>
              Repository Overview
            </h2>
          </div>
          <MetadataCard metadata={metadata_card} delay={0} />
        </section>
      )}

      {/* Stage 2: Repository Classification */}
      {classification.primary_type && revealStage >= 2 && (
        <section className="animate-fade-in-up" style={{ animationDelay: '100ms' }}>
          <div className="mb-3">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-purple-500 rounded-full animate-pulse"></span>
              Classification
            </h2>
          </div>
          <div className="group relative bg-gradient-to-br from-purple-900/30 via-gray-800/50 to-gray-900/50 backdrop-blur-xl border border-purple-500/30 rounded-3xl p-8 shadow-2xl overflow-hidden transition-all duration-500 hover:scale-[1.01] hover:border-purple-400/50">
            {/* Animated background gradient */}
            <div className="absolute inset-0 bg-gradient-to-r from-purple-500/0 via-purple-500/10 to-purple-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            
            <div className="relative z-10">
              <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                <div className="w-12 h-12 bg-gradient-to-br from-purple-500/30 to-pink-500/30 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-7 h-7 text-purple-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                </div>
                Repository Classification
              </h3>
              <div className="flex items-center gap-4 flex-wrap">
                <span className="px-6 py-3 bg-gradient-to-r from-purple-500/20 to-pink-500/20 text-purple-200 rounded-2xl border-2 border-purple-500/40 font-bold text-lg hover:scale-105 transition-transform duration-300">
                  {classification.primary_type.replace(/_/g, ' ').toUpperCase()}
                </span>
                {classification.confidence && (
                  <span className="text-gray-400 flex items-center gap-2">
                    <span className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></span>
                    Confidence: <span className="text-white font-bold">{classification.confidence}</span>
                  </span>
                )}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Stage 3: Framework Intelligence */}
      {frameworks.length > 0 && revealStage >= 3 && (
        <section className="animate-fade-in-up" style={{ animationDelay: '200ms' }}>
          <div className="mb-3">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
              Framework Intelligence
            </h2>
          </div>
          <FrameworkIntelligence frameworks={frameworks} />
        </section>
      )}

      {/* Stage 4: Workflow Pipeline */}
      {workflow_nodes.length > 0 && revealStage >= 4 && (
        <section className="animate-fade-in-up" style={{ animationDelay: '300ms' }}>
          <div className="mb-3">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-pulse"></span>
              ML Workflow Components
            </h2>
          </div>
          <WorkflowVisualization nodes={workflow_nodes} />
        </section>
      )}

      {/* Stage 5: Medical AI Signals */}
      {medical_signals.length > 0 && revealStage >= 5 && (
        <section className="animate-fade-in-up" style={{ animationDelay: '400ms' }}>
          <div className="mb-3">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-red-500 rounded-full animate-pulse"></span>
              Medical AI Signals
            </h2>
          </div>
          <div className="relative bg-gradient-to-br from-red-900/20 via-gray-800/50 to-gray-900/50 backdrop-blur-xl border border-red-500/30 rounded-3xl p-8 shadow-2xl overflow-hidden">
            {/* Subtle pulse effect */}
            <div className="absolute inset-0 bg-red-500/5 animate-pulse"></div>
            
            <div className="relative z-10">
              {/* Section header */}
              <div className="mb-8">
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-12 h-12 bg-gradient-to-br from-red-500/30 to-pink-500/30 rounded-2xl flex items-center justify-center animate-pulse">
                    <svg className="w-7 h-7 text-red-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-white">Medical AI Signals</h3>
                  <span className="px-3 py-1 bg-red-500/20 text-red-300 text-xs font-bold rounded-full border border-red-500/40">
                    {medical_signals.length} detected
                  </span>
                </div>
                <div className="h-1 w-24 bg-gradient-to-r from-red-500 to-pink-500 rounded-full"></div>
              </div>

              {/* Medical signal cards */}
              <div className="space-y-4">
                {medical_signals.map((signal, index) => (
                  <MedicalSignalCard key={index} signal={signal} index={index} />
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Stage 6: Important Files */}
      {important_files.length > 0 && revealStage >= 6 && (
        <section className="animate-fade-in-up" style={{ animationDelay: '500ms' }}>
          <div className="mb-3">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-teal-500 rounded-full animate-pulse"></span>
              Important Files
            </h2>
          </div>
          <ImportantFilesExplorer files={important_files} />
        </section>
      )}

      {/* Stage 7: Statistics */}
      {statistics && Object.keys(statistics).length > 0 && revealStage >= 7 && (
        <section className="animate-fade-in-up" style={{ animationDelay: '600ms' }}>
          <div className="mb-3">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></span>
              Repository Statistics
            </h2>
          </div>
          <StatisticsVisualization statistics={statistics} classification={classification} />
        </section>
      )}

      {/* Stage 8: Executive Summary */}
      {executive_summary && revealStage >= 8 && (
        <section className="animate-fade-in-up" style={{ animationDelay: '700ms' }}>
          <ExecutiveSummarySection summary={executive_summary} delay={700} />
        </section>
      )}

      {/* Stage 9: AI Reasoning */}
      {ai_reasoning && revealStage >= 9 && (
        <section className="animate-fade-in-up" style={{ animationDelay: '800ms' }}>
          <AIReasoningSection reasoning={ai_reasoning} delay={800} />
        </section>
      )}

      {/* Stage 10: Repository Maturity */}
      {maturity_badge && revealStage >= 10 && (
        <section className="animate-fade-in-up" style={{ animationDelay: '900ms' }}>
          <MaturitySection
            badge={maturity_badge}
            indicators={maturity_indicators || []}
            delay={900}
          />
        </section>
      )}

      {/* Stage 11: Architecture Insights */}
      {architecture_insights && architecture_insights.length > 0 && revealStage >= 11 && (
        <section className="animate-fade-in-up" style={{ animationDelay: '1000ms' }}>
          <ArchitectureInsightsSection insights={architecture_insights} delay={1000} />
        </section>
      )}

      {/* Analysis completion indicator */}
      {data.processing_time_ms && revealStage >= 7 && (
        <div className="text-center animate-fade-in" style={{ animationDelay: '800ms' }}>
          <div className="inline-flex items-center gap-3 px-6 py-3 bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-full">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-400">
              Analysis completed in <span className="text-white font-bold">{data.processing_time_ms}ms</span>
            </span>
          </div>
        </div>
      )}
    </div>
  );
}

// Made with Bob