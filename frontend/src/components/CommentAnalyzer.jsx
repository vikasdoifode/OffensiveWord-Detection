import { useState } from 'react';
import { analyzeComment } from '../api';
import { MessageSquare, Search, AlertTriangle, CheckCircle, Clock, Zap, Loader2 } from 'lucide-react';
import ResultCard from './ResultCard';
import PerformanceDashboard from './PerformanceDashboard';

export default function CommentAnalyzer() {
  const [comment, setComment] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!comment.trim()) {
      setError('Please enter a comment to analyze');
      return;
    }
    setError('');
    setLoading(true);
    setResult(null);

    try {
      const data = await analyzeComment(comment);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze comment. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      handleAnalyze();
    }
  };

  const exampleComments = [
    "You are stup1d and id10t",
    "You are not stupid at all",
    "s.t.u.p.i.d people like you should quit",
    "This is a great video, love it!",
    "You are a f00l and @$$hole",
    "What a m0r0n, go away l0ser",
    "You are $tup!d and should leave",
    "That's not stupid, just different",
    "Is that really stupid?",
    "That is so stupid lol",
  ];

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <div className="glass-card p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center">
            <MessageSquare className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-white">Comment Analyzer</h2>
            <p className="text-sm text-gray-400">Paste any comment to detect offensive content</p>
          </div>
        </div>

        <div className="relative">
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type or paste a comment here... (Ctrl+Enter to analyze)"
            className="w-full h-32 bg-white/5 border border-white/10 rounded-xl p-4 text-white placeholder-gray-500 resize-none focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/25 transition-all"
          />
          <div className="absolute bottom-3 right-3 text-xs text-gray-500">
            {comment.length} chars
          </div>
        </div>

        {/* Example Comments */}
        <div className="mt-3">
          <p className="text-xs text-gray-500 mb-2">Try an example:</p>
          <div className="flex flex-wrap gap-2">
            {exampleComments.map((ex, i) => (
              <button
                key={i}
                onClick={() => setComment(ex)}
                className="text-xs px-3 py-1.5 rounded-lg bg-white/5 text-gray-400 hover:text-white hover:bg-white/10 transition-all border border-white/5 hover:border-white/10"
              >
                {ex.length > 35 ? ex.substring(0, 35) + '...' : ex}
              </button>
            ))}
          </div>
        </div>

        {error && (
          <div className="mt-3 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm flex items-center gap-2">
            <AlertTriangle className="w-4 h-4" />
            {error}
          </div>
        )}

        <button
          onClick={handleAnalyze}
          disabled={loading || !comment.trim()}
          className="mt-4 w-full sm:w-auto px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium rounded-xl hover:from-blue-500 hover:to-purple-500 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg shadow-blue-500/20 hover:shadow-blue-500/40"
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <Search className="w-4 h-4" />
              Analyze Comment
            </>
          )}
        </button>
      </div>

      {/* Loading Animation */}
      {loading && (
        <div className="glass-card p-8 flex flex-col items-center justify-center">
          <div className="relative w-16 h-16 mb-4">
            <div className="absolute inset-0 rounded-full border-2 border-blue-500/20" />
            <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-blue-500 animate-spin" />
            <div className="absolute inset-2 rounded-full border-2 border-transparent border-t-purple-500 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }} />
            <Zap className="absolute inset-0 m-auto w-6 h-6 text-blue-400" />
          </div>
          <p className="text-gray-400 text-sm">Running DAA algorithms...</p>
          <div className="flex gap-4 mt-3 text-xs text-gray-500">
            <span>Greedy →</span>
            <span>Aho-Corasick →</span>
            <span>Levenshtein →</span>
            <span>Backtracking</span>
          </div>
        </div>
      )}

      {/* Results */}
      {result && !loading && (
        <div className="space-y-6">
          {/* Status Banner */}
          <div className={`glass-card p-6 border-l-4 ${
            result.status === 'offensive'
              ? 'border-l-red-500 bg-red-500/5'
              : 'border-l-green-500 bg-green-500/5'
          }`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                {result.status === 'offensive' ? (
                  <AlertTriangle className="w-8 h-8 text-red-500" />
                ) : (
                  <CheckCircle className="w-8 h-8 text-green-500" />
                )}
                <div>
                  <h3 className={`text-xl font-bold ${
                    result.status === 'offensive' ? 'text-red-400' : 'text-green-400'
                  }`}>
                    {result.status === 'offensive' ? '⚠️ OFFENSIVE' : '✅ SAFE'}
                  </h3>
                  <p className="text-sm text-gray-400 mt-0.5">
                    {result.detected_words.length > 0
                      ? `${result.detected_words.length} word(s) detected${result.high_confidence_detected?.length > 0 ? ` (${result.high_confidence_detected.length} high confidence)` : ''}`
                      : 'No offensive content detected'}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <Clock className="w-4 h-4" />
                <span className="text-sm font-mono">{result.total_time}ms</span>
              </div>
            </div>
          </div>

          {/* Detected Words */}
          {result.detected_words.length > 0 && (
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-red-500" />
                Detected Words
              </h3>
              <div className="space-y-3">
                {result.detected_words.map((word, i) => (
                  <ResultCard key={i} word={word} index={i} />
                ))}
              </div>
            </div>
          )}

          {/* Performance Dashboard */}
          <PerformanceDashboard times={result.algorithm_times} totalTime={result.total_time} />
        </div>
      )}
    </div>
  );
}
