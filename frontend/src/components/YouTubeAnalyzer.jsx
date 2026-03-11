import { useState } from 'react';
import { analyzeYouTubeChat } from '../api';
import { Youtube, Search, AlertTriangle, CheckCircle, Users, Loader2, BarChart3 } from 'lucide-react';
import PerformanceDashboard from './PerformanceDashboard';

export default function YouTubeAnalyzer() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    const trimmed = url.trim();
    if (!trimmed) {
      setError('Please enter a YouTube URL');
      return;
    }

    // Basic validation: check if it looks like a YouTube URL or video ID
    const looksValid =
      trimmed.includes('youtube.com') ||
      trimmed.includes('youtu.be') ||
      /^[a-zA-Z0-9_-]{11}$/.test(trimmed);

    if (!looksValid) {
      setError('This doesn\'t look like a valid YouTube URL. Please paste a URL like: https://www.youtube.com/watch?v=VIDEO_ID');
      return;
    }

    setError('');
    setLoading(true);
    setResult(null);

    try {
      const data = await analyzeYouTubeChat(trimmed);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const sampleUrls = [
    { label: 'Rick Astley - Never Gonna Give You Up', url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' },
    { label: 'Despacito - Luis Fonsi', url: 'https://www.youtube.com/watch?v=kJQP7kiw5Fk' },
  ];
  // Average algorithm times across all comments
  const getAverageTimes = () => {
    if (!result || !result.comments.length) return null;
    const totals = {};
    result.comments.forEach((c) => {
      if (c.algorithm_times) {
        Object.entries(c.algorithm_times).forEach(([key, val]) => {
          totals[key] = (totals[key] || 0) + val;
        });
      }
    });
    const count = result.comments.length;
    const avg = {};
    Object.entries(totals).forEach(([key, val]) => {
      avg[key] = Math.round((val / count) * 100) / 100;
    });
    return avg;
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <div className="glass-card p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-red-500/10 flex items-center justify-center">
            <Youtube className="w-5 h-5 text-red-400" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-white">YouTube Chat Analyzer</h2>
            <p className="text-sm text-gray-400">Paste a YouTube Live Chat or Video URL to analyze comments</p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
            placeholder="https://www.youtube.com/watch?v=..."
            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-red-500/50 focus:ring-1 focus:ring-red-500/25 transition-all"
          />
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="px-6 py-3 bg-gradient-to-r from-red-600 to-pink-600 text-white font-medium rounded-xl hover:from-red-500 hover:to-pink-500 transition-all duration-300 disabled:opacity-50 flex items-center justify-center gap-2 shadow-lg shadow-red-500/20 whitespace-nowrap"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Search className="w-4 h-4" />
                Analyze Chat
              </>
            )}
          </button>
        </div>

        <p className="mt-2 text-xs text-gray-500">
          💡 Tip: If no YouTube API key is configured, the system will use simulated chat data for demonstration.
        </p>

        {/* Sample URLs */}
        <div className="mt-3 flex flex-wrap items-center gap-2">
          <span className="text-xs text-gray-500">Try a sample:</span>
          {sampleUrls.map((sample, i) => (
            <button
              key={i}
              onClick={() => setUrl(sample.url)}
              className="text-xs px-3 py-1 rounded-full bg-white/5 border border-white/10 text-gray-400 hover:text-white hover:border-red-500/30 transition-all"
            >
              🎬 {sample.label}
            </button>
          ))}
        </div>

        {error && (
          <div className="mt-3 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm flex items-center gap-2">
            <AlertTriangle className="w-4 h-4" />
            {error}
          </div>
        )}
      </div>

      {/* Loading */}
      {loading && (
        <div className="glass-card p-8 flex flex-col items-center">
          <Loader2 className="w-10 h-10 text-red-400 animate-spin mb-3" />
          <p className="text-gray-400">Fetching and analyzing comments...</p>
        </div>
      )}

      {/* Results */}
      {result && !loading && (
        <div className="space-y-6">
          {/* Data Source Banner */}
          {result.source && result.source !== 'youtube_api' && (
            <div className="p-3 rounded-lg bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 text-sm flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 flex-shrink-0" />
              <span>
                <strong>Note:</strong> Showing simulated demo data. To fetch real YouTube comments, ensure your YouTube Data API key is valid and the YouTube Data API v3 is enabled in Google Cloud Console.
              </span>
            </div>
          )}
          {result.source === 'youtube_api' && (
            <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20 text-green-400 text-sm flex items-center gap-2">
              <CheckCircle className="w-4 h-4 flex-shrink-0" />
              <span>
                <strong>Live Data:</strong> Showing real comments fetched from YouTube API.
              </span>
            </div>
          )}

          {/* Stats Bar */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="glass-card p-4 text-center">
              <Users className="w-5 h-5 text-blue-400 mx-auto mb-1" />
              <div className="text-2xl font-bold text-white">{result.total_analyzed}</div>
              <div className="text-xs text-gray-400">Total Comments</div>
            </div>
            <div className="glass-card p-4 text-center">
              <AlertTriangle className="w-5 h-5 text-red-400 mx-auto mb-1" />
              <div className="text-2xl font-bold text-red-400">{result.offensive_count}</div>
              <div className="text-xs text-gray-400">Offensive</div>
            </div>
            <div className="glass-card p-4 text-center">
              <CheckCircle className="w-5 h-5 text-green-400 mx-auto mb-1" />
              <div className="text-2xl font-bold text-green-400">{result.safe_count}</div>
              <div className="text-xs text-gray-400">Safe</div>
            </div>
            <div className="glass-card p-4 text-center">
              <BarChart3 className="w-5 h-5 text-purple-400 mx-auto mb-1" />
              <div className="text-2xl font-bold text-purple-400">
                {result.total_analyzed > 0 ? Math.round((result.offensive_count / result.total_analyzed) * 100) : 0}%
              </div>
              <div className="text-xs text-gray-400">Toxicity Rate</div>
            </div>
          </div>

          {/* Comments Table */}
          <div className="glass-card overflow-hidden">
            <div className="p-4 border-b border-white/5">
              <h3 className="text-lg font-semibold text-white">Analysis Results</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-white/5">
                    <th className="text-left p-4 text-xs font-medium text-gray-400 uppercase tracking-wider">User</th>
                    <th className="text-left p-4 text-xs font-medium text-gray-400 uppercase tracking-wider">Comment</th>
                    <th className="text-left p-4 text-xs font-medium text-gray-400 uppercase tracking-wider">Detected Words</th>
                    <th className="text-left p-4 text-xs font-medium text-gray-400 uppercase tracking-wider">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {result.comments.map((item, i) => (
                    <tr key={i} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                      <td className="p-4">
                        <div className="flex items-center gap-2">
                          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-xs font-bold text-white">
                            {item.user.charAt(0).toUpperCase()}
                          </div>
                          <span className="text-sm text-gray-300 font-medium">{item.user}</span>
                        </div>
                      </td>
                      <td className="p-4">
                        <p className="text-sm text-gray-300 max-w-md">
                          {highlightOffensiveWords(item.comment, item.detected_words)}
                        </p>
                      </td>
                      <td className="p-4">
                        <div className="flex flex-wrap gap-1">
                          {item.detected_words.length > 0 ? (
                            item.detected_words.map((word, j) => (
                              <span key={j} className="offensive-highlight text-xs">
                                {word}
                              </span>
                            ))
                          ) : (
                            <span className="text-xs text-gray-500">None</span>
                          )}
                        </div>
                      </td>
                      <td className="p-4">
                        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold ${
                          item.status === 'offensive'
                            ? 'bg-red-500/10 text-red-400 border border-red-500/20'
                            : 'bg-green-500/10 text-green-400 border border-green-500/20'
                        }`}>
                          {item.status === 'offensive' ? (
                            <AlertTriangle className="w-3 h-3" />
                          ) : (
                            <CheckCircle className="w-3 h-3" />
                          )}
                          {item.status.toUpperCase()}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Average Performance */}
          {getAverageTimes() && (
            <PerformanceDashboard
              times={getAverageTimes()}
              totalTime={Object.values(getAverageTimes()).reduce((a, b) => a + b, 0)}
              title="Average Algorithm Performance (per comment)"
            />
          )}
        </div>
      )}
    </div>
  );
}

function highlightOffensiveWords(text, detectedWords) {
  if (!detectedWords || detectedWords.length === 0) return text;

  const parts = [];
  let remaining = text;
  let key = 0;

  for (const word of detectedWords) {
    const lowerRemaining = remaining.toLowerCase();
    const lowerWord = word.toLowerCase();
    const idx = lowerRemaining.indexOf(lowerWord);

    if (idx !== -1) {
      if (idx > 0) {
        parts.push(<span key={key++}>{remaining.slice(0, idx)}</span>);
      }
      parts.push(
        <span key={key++} className="offensive-highlight">
          {remaining.slice(idx, idx + word.length)}
        </span>
      );
      remaining = remaining.slice(idx + word.length);
    }
  }

  if (remaining) {
    parts.push(<span key={key++}>{remaining}</span>);
  }

  return parts.length > 0 ? parts : text;
}
