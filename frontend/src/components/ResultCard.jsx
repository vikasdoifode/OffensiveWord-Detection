import { ArrowRight, Fingerprint } from 'lucide-react';

export default function ResultCard({ word, index }) {
  const methods = word.methods || [];
  const methodLabels = {
    greedy: { label: 'Greedy', color: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20' },
    greedy_exact: { label: 'Greedy', color: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20' },
    greedy_longest: { label: 'Greedy', color: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20' },
    greedy_direct: { label: 'Greedy', color: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20' },
    aho_corasick: { label: 'Aho-Corasick', color: 'bg-blue-500/10 text-blue-400 border-blue-500/20' },
    levenshtein: { label: 'Levenshtein', color: 'bg-purple-500/10 text-purple-400 border-purple-500/20' },
    backtracking: { label: 'Backtracking', color: 'bg-pink-500/10 text-pink-400 border-pink-500/20' },
  };

  return (
    <div className="flex flex-col sm:flex-row sm:items-center gap-3 p-4 rounded-xl bg-white/[0.02] border border-white/5 hover:border-red-500/20 transition-all">
      {/* Word Mapping */}
      <div className="flex items-center gap-3 flex-1 min-w-0">
        <div className="flex items-center gap-2 font-mono">
          <span className="offensive-highlight text-sm font-semibold">{word.input}</span>
          <ArrowRight className="w-4 h-4 text-gray-500 flex-shrink-0" />
          <span className="text-sm font-semibold text-red-400">{word.matched}</span>
        </div>
      </div>

      {/* Similarity Score */}
      {word.similarity && (
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-purple-500/10 border border-purple-500/20">
          <Fingerprint className="w-3.5 h-3.5 text-purple-400" />
          <span className="text-xs text-purple-400 font-mono">
            {(word.similarity * 100).toFixed(0)}% match
          </span>
          {word.distance !== undefined && (
            <span className="text-xs text-gray-500">
              (edit dist: {word.distance})
            </span>
          )}
        </div>
      )}

      {/* Detection Methods */}
      <div className="flex flex-wrap gap-1.5">
        {methods.map((method, i) => {
          const info = methodLabels[method] || { label: method, color: 'bg-gray-500/10 text-gray-400 border-gray-500/20' };
          return (
            <span
              key={i}
              className={`text-xs px-2 py-0.5 rounded-md border font-medium ${info.color}`}
            >
              {info.label}
            </span>
          );
        })}
      </div>
    </div>
  );
}
