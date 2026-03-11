import { useState, useEffect } from 'react';
import { getAlgorithms } from '../api';
import { BookOpen, Clock, Target, Layers, ChevronRight, AlertTriangle } from 'lucide-react';

const CATEGORY_COLORS = {
  'Advanced Data Structure': 'from-blue-500 to-cyan-500',
  'Pattern Matching': 'from-blue-500 to-indigo-500',
  'Greedy': 'from-yellow-500 to-orange-500',
  'Dynamic Programming': 'from-purple-500 to-pink-500',
  'Backtracking': 'from-pink-500 to-rose-500',
};

const CATEGORY_BADGES = {
  'Advanced Data Structure': 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  'Pattern Matching': 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20',
  'Greedy': 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
  'Dynamic Programming': 'bg-purple-500/10 text-purple-400 border-purple-500/20',
  'Backtracking': 'bg-pink-500/10 text-pink-400 border-pink-500/20',
};

export default function AlgorithmAnalysis() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [expandedAlgo, setExpandedAlgo] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const result = await getAlgorithms();
      setData(result);
    } catch (err) {
      setError('Failed to load algorithm data. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="glass-card p-8 flex items-center justify-center">
        <div className="text-gray-400">Loading algorithm analysis...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-card p-6">
        <div className="flex items-center gap-2 text-red-400">
          <AlertTriangle className="w-5 h-5" />
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-card p-6">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center">
            <BookOpen className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-white">DAA Algorithm Analysis</h2>
            <p className="text-sm text-gray-400">Design and Analysis of Algorithms used in this system</p>
          </div>
        </div>
      </div>

      {/* DAA Paradigms */}
      <div className="glass-card p-6">
        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Algorithm Paradigms Used</h3>
        <div className="flex flex-wrap gap-2">
          {data?.paradigms?.map((paradigm, i) => (
            <span
              key={i}
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 text-sm font-medium text-blue-300"
            >
              {paradigm}
            </span>
          ))}
        </div>
      </div>

      {/* Algorithm Cards */}
      <div className="space-y-4">
        {data?.algorithms?.map((algo, i) => {
          const isExpanded = expandedAlgo === i;
          const gradientClass = CATEGORY_COLORS[algo.category] || 'from-gray-500 to-gray-600';
          const badgeClass = CATEGORY_BADGES[algo.category] || 'bg-gray-500/10 text-gray-400 border-gray-500/20';

          return (
            <div
              key={i}
              className="glass-card glass-card-hover overflow-hidden cursor-pointer transition-all duration-300"
              onClick={() => setExpandedAlgo(isExpanded ? null : i)}
            >
              {/* Gradient Top Bar */}
              <div className={`h-1 bg-gradient-to-r ${gradientClass}`} />

              <div className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-bold text-white">{algo.name}</h3>
                      <span className={`text-xs px-2.5 py-0.5 rounded-full border font-medium ${badgeClass}`}>
                        {algo.category}
                      </span>
                    </div>
                    <p className="text-sm text-gray-400">{algo.purpose}</p>
                  </div>
                  <ChevronRight
                    className={`w-5 h-5 text-gray-400 transition-transform duration-300 flex-shrink-0 mt-1 ${
                      isExpanded ? 'rotate-90' : ''
                    }`}
                  />
                </div>

                {/* Complexity Badges */}
                <div className="flex flex-wrap gap-3 mt-4">
                  <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
                    <Clock className="w-3.5 h-3.5 text-blue-400" />
                    <span className="text-xs text-gray-400">Time:</span>
                    <span className="text-xs font-mono text-white font-semibold">{algo.time_complexity}</span>
                  </div>
                  <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
                    <Layers className="w-3.5 h-3.5 text-purple-400" />
                    <span className="text-xs text-gray-400">Space:</span>
                    <span className="text-xs font-mono text-white font-semibold">{algo.space_complexity}</span>
                  </div>
                  <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
                    <Target className="w-3.5 h-3.5 text-green-400" />
                    <span className="text-xs text-gray-400">Used in:</span>
                    <span className="text-xs text-white">{algo.used_in}</span>
                  </div>
                </div>

                {/* Expanded Description */}
                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-white/5">
                    <p className="text-sm text-gray-300 leading-relaxed">{algo.description}</p>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Detection Pipeline */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-blue-500" />
          Detection Pipeline
        </h3>
        <div className="space-y-0">
          {data?.pipeline?.map((step, i) => (
            <div key={i} className="flex items-start gap-4">
              {/* Step indicator line */}
              <div className="flex flex-col items-center">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500/20 to-purple-500/20 border border-blue-500/30 flex items-center justify-center text-sm font-bold text-blue-400">
                  {step.step}
                </div>
                {i < data.pipeline.length - 1 && (
                  <div className="w-0.5 h-12 bg-gradient-to-b from-blue-500/30 to-transparent" />
                )}
              </div>
              <div className="pt-2 pb-8">
                <h4 className="text-sm font-semibold text-white">{step.algorithm}</h4>
                <p className="text-xs text-gray-400 mt-0.5">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Complexity Comparison Table */}
      <div className="glass-card overflow-hidden">
        <div className="p-4 border-b border-white/5">
          <h3 className="text-lg font-semibold text-white">Complexity Comparison</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/5">
                <th className="text-left p-4 text-xs font-medium text-gray-400 uppercase tracking-wider">Algorithm</th>
                <th className="text-left p-4 text-xs font-medium text-gray-400 uppercase tracking-wider">Category</th>
                <th className="text-left p-4 text-xs font-medium text-gray-400 uppercase tracking-wider">Time Complexity</th>
                <th className="text-left p-4 text-xs font-medium text-gray-400 uppercase tracking-wider">Space Complexity</th>
                <th className="text-left p-4 text-xs font-medium text-gray-400 uppercase tracking-wider">Purpose</th>
              </tr>
            </thead>
            <tbody>
              {data?.algorithms?.map((algo, i) => {
                const badgeClass = CATEGORY_BADGES[algo.category] || 'bg-gray-500/10 text-gray-400 border-gray-500/20';
                return (
                  <tr key={i} className="border-b border-white/5 hover:bg-white/[0.02]">
                    <td className="p-4 text-sm font-semibold text-white">{algo.name}</td>
                    <td className="p-4">
                      <span className={`text-xs px-2 py-0.5 rounded-md border ${badgeClass}`}>{algo.category}</span>
                    </td>
                    <td className="p-4 text-sm font-mono text-blue-400">{algo.time_complexity}</td>
                    <td className="p-4 text-sm font-mono text-purple-400">{algo.space_complexity}</td>
                    <td className="p-4 text-sm text-gray-400">{algo.purpose}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
