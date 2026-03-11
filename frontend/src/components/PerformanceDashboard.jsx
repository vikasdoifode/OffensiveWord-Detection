import { Clock, Gauge } from 'lucide-react';

const ALGO_INFO = {
  greedy: { label: 'Greedy Scan', color: '#eab308', bg: 'bg-yellow-500' },
  aho_corasick: { label: 'Aho-Corasick', color: '#3b82f6', bg: 'bg-blue-500' },
  levenshtein: { label: 'Levenshtein (DP)', color: '#a855f7', bg: 'bg-purple-500' },
  backtracking: { label: 'Backtracking', color: '#ec4899', bg: 'bg-pink-500' },
};

export default function PerformanceDashboard({ times, totalTime, title }) {
  if (!times) return null;

  const maxTime = Math.max(...Object.values(times), 0.1);

  return (
    <div className="glass-card p-6">
      <div className="flex items-center justify-between mb-5">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <Gauge className="w-5 h-5 text-blue-400" />
          {title || 'Algorithm Performance Dashboard'}
        </h3>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
          <Clock className="w-4 h-4 text-gray-400" />
          <span className="text-sm font-mono text-gray-300">
            Total: <span className="text-white font-semibold">{totalTime.toFixed(2)}ms</span>
          </span>
        </div>
      </div>

      <div className="space-y-4">
        {Object.entries(times).map(([key, time]) => {
          const info = ALGO_INFO[key] || { label: key, color: '#6b7280', bg: 'bg-gray-500' };
          const percentage = maxTime > 0 ? (time / maxTime) * 100 : 0;

          return (
            <div key={key} className="space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-300">{info.label}</span>
                <span className="text-sm font-mono text-gray-400">{time.toFixed(2)}ms</span>
              </div>
              <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-1000 ease-out ${info.bg}`}
                  style={{
                    width: `${Math.max(percentage, 2)}%`,
                    opacity: 0.7,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Execution Timeline */}
      <div className="mt-6 pt-4 border-t border-white/5">
        <p className="text-xs text-gray-500 mb-3">Execution Pipeline</p>
        <div className="flex items-center gap-1">
          {Object.entries(times).map(([key, time], i) => {
            const info = ALGO_INFO[key] || { label: key, color: '#6b7280', bg: 'bg-gray-500' };
            const widthPct = totalTime > 0 ? (time / totalTime) * 100 : 25;

            return (
              <div key={key} className="flex items-center" style={{ width: `${Math.max(widthPct, 10)}%` }}>
                <div
                  className="h-6 rounded flex items-center justify-center text-[10px] font-medium text-white/80 w-full min-w-0"
                  style={{ backgroundColor: info.color + '40', border: `1px solid ${info.color}60` }}
                  title={`${info.label}: ${time.toFixed(2)}ms`}
                >
                  <span className="truncate px-1">{info.label}</span>
                </div>
                {i < Object.entries(times).length - 1 && (
                  <span className="text-gray-600 mx-0.5 flex-shrink-0">→</span>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
