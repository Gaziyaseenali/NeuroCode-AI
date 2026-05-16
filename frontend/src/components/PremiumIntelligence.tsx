'use client';

import { AIReasoning, MaturityBadge, MaturityIndicator, ArchitectureInsight, ExecutiveSummary } from '@/lib/api/types';

// ====================================================
// AI REASONING COMPONENTS
// ====================================================

interface AIReasoningProps {
  reasoning: AIReasoning;
  delay?: number;
}

export function AIReasoningSection({ reasoning, delay = 0 }: AIReasoningProps) {
  const allSteps = [
    ...reasoning.classification_reasoning,
    ...reasoning.framework_reasoning,
    ...reasoning.workflow_reasoning,
    ...reasoning.medical_reasoning
  ];

  if (allSteps.length === 0) return null;

  return (
    <div 
      className="space-y-6 animate-slide-up"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-gradient-to-br from-purple-500/20 to-blue-500/20 rounded-xl flex items-center justify-center">
          <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div>
          <h3 className="text-2xl font-bold text-white">AI Reasoning</h3>
          <p className="text-gray-400 text-sm">Understanding the detection process</p>
        </div>
      </div>

      <div className="grid gap-4">
        {allSteps.map((step, index) => (
          <ReasoningStepCard key={index} step={step} index={index} />
        ))}
      </div>

      {reasoning.summary && (
        <div className="mt-6 p-4 bg-gradient-to-r from-purple-500/10 to-blue-500/10 border border-purple-500/30 rounded-xl">
          <p className="text-sm text-gray-300 leading-relaxed">
            <span className="font-semibold text-purple-300">Summary:</span> {reasoning.summary}
          </p>
        </div>
      )}
    </div>
  );
}

interface ReasoningStepCardProps {
  step: any;
  index: number;
}

function ReasoningStepCard({ step, index }: ReasoningStepCardProps) {
  const impactColors = {
    positive: 'from-green-500/10 to-emerald-500/10 border-green-500/30',
    neutral: 'from-blue-500/10 to-cyan-500/10 border-blue-500/30',
    negative: 'from-red-500/10 to-orange-500/10 border-red-500/30'
  };

  const impactIcons = {
    positive: '✓',
    neutral: '→',
    negative: '!'
  };

  return (
    <div 
      className={`group relative bg-gradient-to-br ${impactColors[step.confidence_impact as keyof typeof impactColors]} backdrop-blur-sm rounded-xl p-5 border transition-all duration-500 hover:scale-[1.02] hover:shadow-xl animate-fade-in`}
      style={{ animationDelay: `${index * 100}ms` }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 rounded-xl transition-opacity duration-500"></div>
      
      <div className="relative z-10 space-y-3">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">
                {step.category}
              </span>
              <span className="text-lg">
                {impactIcons[step.confidence_impact as keyof typeof impactIcons]}
              </span>
            </div>
            <h4 className="font-bold text-white text-lg mb-2">{step.title}</h4>
            <p className="text-sm text-gray-300 leading-relaxed">{step.explanation}</p>
          </div>
        </div>

        {step.evidence && step.evidence.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-700/50">
            <p className="text-xs text-gray-500 font-semibold mb-2">Evidence:</p>
            <div className="flex flex-wrap gap-2">
              {step.evidence.slice(0, 3).map((evidence: string, i: number) => (
                <span 
                  key={i}
                  className="text-xs text-gray-400 bg-gray-800/50 px-2 py-1 rounded border border-gray-700/50 font-mono"
                >
                  {evidence}
                </span>
              ))}
              {step.evidence.length > 3 && (
                <span className="text-xs text-gray-500 px-2 py-1">
                  +{step.evidence.length - 3} more
                </span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ====================================================
// MATURITY BADGE & INDICATORS
// ====================================================

interface MaturitySectionProps {
  badge: MaturityBadge;
  indicators: MaturityIndicator[];
  delay?: number;
}

export function MaturitySection({ badge, indicators, delay = 0 }: MaturitySectionProps) {
  return (
    <div 
      className="space-y-6 animate-slide-up"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-xl flex items-center justify-center">
          <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <h3 className="text-2xl font-bold text-white">Repository Maturity</h3>
          <p className="text-gray-400 text-sm">Production readiness assessment</p>
        </div>
      </div>

      {/* Maturity Badge */}
      <div className="relative group">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 rounded-2xl blur-xl opacity-50 group-hover:opacity-75 transition-opacity duration-500"></div>
        <div className="relative bg-gradient-to-br from-gray-800/90 to-gray-900/90 backdrop-blur-xl border border-gray-700/50 rounded-2xl p-6">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <div 
                  className="w-3 h-3 rounded-full animate-pulse"
                  style={{ backgroundColor: badge.color }}
                ></div>
                <h4 className="text-2xl font-bold text-white">{badge.label}</h4>
              </div>
              <p className="text-gray-400 text-sm mb-4">{badge.description}</p>
              
              {/* Score Bar */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500">Maturity Score</span>
                  <span className="font-bold text-white">{badge.score.toFixed(0)}/100</span>
                </div>
                <div className="h-3 bg-gray-800 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full transition-all duration-1000 ease-out"
                    style={{ width: `${badge.score}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Maturity Indicators */}
      {indicators.length > 0 && (
        <div className="grid gap-3">
          {indicators.map((indicator, index) => (
            <MaturityIndicatorCard key={index} indicator={indicator} index={index} />
          ))}
        </div>
      )}
    </div>
  );
}

interface MaturityIndicatorCardProps {
  indicator: MaturityIndicator;
  index: number;
}

function MaturityIndicatorCard({ indicator, index }: MaturityIndicatorCardProps) {
  const statusConfig = {
    present: { icon: '✓', color: 'text-green-400', bg: 'bg-green-500/10', border: 'border-green-500/30' },
    absent: { icon: '✗', color: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/30' },
    partial: { icon: '◐', color: 'text-yellow-400', bg: 'bg-yellow-500/10', border: 'border-yellow-500/30' }
  };

  const impactBadge = {
    high: 'bg-purple-500/20 text-purple-300 border-purple-500/40',
    medium: 'bg-blue-500/20 text-blue-300 border-blue-500/40',
    low: 'bg-gray-500/20 text-gray-300 border-gray-500/40'
  };

  const config = statusConfig[indicator.status as keyof typeof statusConfig] || statusConfig.partial;

  return (
    <div 
      className={`group flex items-center gap-4 p-4 ${config.bg} border ${config.border} rounded-xl transition-all duration-300 hover:scale-[1.02] animate-fade-in`}
      style={{ animationDelay: `${index * 80}ms` }}
    >
      <div className={`text-2xl ${config.color}`}>{config.icon}</div>
      <div className="flex-1">
        <div className="flex items-center gap-2 mb-1">
          <h5 className="font-semibold text-white">{indicator.name}</h5>
          <span className={`text-xs px-2 py-0.5 rounded-full border ${impactBadge[indicator.impact as keyof typeof impactBadge]}`}>
            {indicator.impact}
          </span>
        </div>
        <p className="text-sm text-gray-400">{indicator.description}</p>
      </div>
    </div>
  );
}

// ====================================================
// ARCHITECTURE INSIGHTS
// ====================================================

interface ArchitectureInsightsProps {
  insights: ArchitectureInsight[];
  delay?: number;
}

export function ArchitectureInsightsSection({ insights, delay = 0 }: ArchitectureInsightsProps) {
  if (insights.length === 0) return null;

  return (
    <div 
      className="space-y-6 animate-slide-up"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-gradient-to-br from-cyan-500/20 to-teal-500/20 rounded-xl flex items-center justify-center">
          <svg className="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <div>
          <h3 className="text-2xl font-bold text-white">Architecture Insights</h3>
          <p className="text-gray-400 text-sm">Detected patterns and structure</p>
        </div>
      </div>

      <div className="grid gap-4">
        {insights.map((insight, index) => (
          <ArchitectureInsightCard key={index} insight={insight} index={index} />
        ))}
      </div>
    </div>
  );
}

interface ArchitectureInsightCardProps {
  insight: ArchitectureInsight;
  index: number;
}

function ArchitectureInsightCard({ insight, index }: ArchitectureInsightCardProps) {
  const significanceColors = {
    high: 'from-cyan-500/15 to-teal-500/15 border-cyan-500/40',
    medium: 'from-blue-500/15 to-indigo-500/15 border-blue-500/40',
    low: 'from-gray-500/15 to-slate-500/15 border-gray-500/40'
  };

  return (
    <div 
      className={`group relative bg-gradient-to-br ${significanceColors[insight.significance as keyof typeof significanceColors]} backdrop-blur-sm rounded-xl p-5 border transition-all duration-500 hover:scale-[1.02] hover:shadow-xl animate-fade-in`}
      style={{ animationDelay: `${index * 100}ms` }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 rounded-xl transition-opacity duration-500"></div>
      
      <div className="relative z-10 space-y-3">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-cyan-500/30 to-teal-500/30 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform duration-300">
            <span className="text-xl">🏗️</span>
          </div>
          <div className="flex-1">
            <h4 className="font-bold text-white text-lg mb-2">{insight.title}</h4>
            <p className="text-sm text-gray-300 leading-relaxed">{insight.description}</p>
          </div>
        </div>

        {insight.evidence && insight.evidence.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-700/50">
            <div className="flex flex-wrap gap-2">
              {insight.evidence.map((evidence, i) => (
                <span 
                  key={i}
                  className="text-xs text-cyan-300 bg-cyan-500/10 px-2 py-1 rounded border border-cyan-500/30"
                >
                  {evidence}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ====================================================
// EXECUTIVE SUMMARY
// ====================================================

interface ExecutiveSummaryProps {
  summary: ExecutiveSummary;
  delay?: number;
}

export function ExecutiveSummarySection({ summary, delay = 0 }: ExecutiveSummaryProps) {
  return (
    <div 
      className="space-y-6 animate-slide-up"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-gradient-to-br from-amber-500/20 to-orange-500/20 rounded-xl flex items-center justify-center">
          <svg className="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <div>
          <h3 className="text-2xl font-bold text-white">Executive Summary</h3>
          <p className="text-gray-400 text-sm">High-level repository overview</p>
        </div>
      </div>

      <div className="relative group">
        <div className="absolute inset-0 bg-gradient-to-r from-amber-500/20 to-orange-500/20 rounded-2xl blur-xl opacity-50 group-hover:opacity-75 transition-opacity duration-500"></div>
        <div className="relative bg-gradient-to-br from-gray-800/90 to-gray-900/90 backdrop-blur-xl border border-gray-700/50 rounded-2xl p-6 space-y-6">
          
          {/* Headline */}
          <div>
            <h4 className="text-2xl font-bold bg-gradient-to-r from-amber-200 via-orange-200 to-amber-200 bg-clip-text text-transparent mb-3">
              {summary.headline}
            </h4>
            <p className="text-gray-300 leading-relaxed">{summary.overview}</p>
          </div>

          {/* Key Highlights */}
          {summary.key_highlights.length > 0 && (
            <div>
              <h5 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Key Highlights</h5>
              <div className="grid gap-2">
                {summary.key_highlights.map((highlight, index) => (
                  <div 
                    key={index}
                    className="flex items-center gap-3 p-3 bg-amber-500/5 border border-amber-500/20 rounded-lg animate-fade-in"
                    style={{ animationDelay: `${index * 100}ms` }}
                  >
                    <div className="w-2 h-2 bg-amber-400 rounded-full flex-shrink-0"></div>
                    <span className="text-sm text-gray-300">{highlight}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Technical Profile */}
          <div className="p-4 bg-gradient-to-r from-gray-800/50 to-gray-900/50 rounded-xl border border-gray-700/50">
            <h5 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Technical Profile</h5>
            <p className="text-sm text-gray-300">{summary.technical_profile}</p>
          </div>

          {/* Use Cases */}
          {summary.use_cases.length > 0 && (
            <div>
              <h5 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Use Cases</h5>
              <div className="flex flex-wrap gap-2">
                {summary.use_cases.map((useCase, index) => (
                  <span 
                    key={index}
                    className="text-sm text-amber-300 bg-amber-500/10 px-3 py-1.5 rounded-full border border-amber-500/30 animate-fade-in"
                    style={{ animationDelay: `${index * 100}ms` }}
                  >
                    {useCase}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Target Audience */}
          <div className="pt-4 border-t border-gray-700/50">
            <p className="text-sm text-gray-400">
              <span className="font-semibold text-amber-300">Target Audience:</span> {summary.target_audience}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

// Made with Bob