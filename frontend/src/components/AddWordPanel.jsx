import { useState, useEffect } from 'react';
import { addWord, getWords } from '../api';
import { BookOpen, Plus, Search, AlertTriangle, CheckCircle, Loader2, X } from 'lucide-react';

export default function AddWordPanel() {
  const [newWord, setNewWord] = useState('');
  const [words, setWords] = useState([]);
  const [totalWords, setTotalWords] = useState(0);
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);
  const [message, setMessage] = useState(null);
  const [searchFilter, setSearchFilter] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchWords();
  }, []);

  const fetchWords = async () => {
    setFetching(true);
    try {
      const data = await getWords();
      setWords(data.words || []);
      setTotalWords(data.total || 0);
    } catch (err) {
      setError('Failed to load dictionary. Make sure the backend is running.');
    } finally {
      setFetching(false);
    }
  };

  const handleAddWord = async () => {
    if (!newWord.trim()) return;
    setLoading(true);
    setMessage(null);

    try {
      const data = await addWord(newWord.trim());
      setMessage({ type: data.status === 'success' ? 'success' : 'info', text: data.message });
      if (data.status === 'success') {
        setNewWord('');
        fetchWords();
      }
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to add word' });
    } finally {
      setLoading(false);
    }
  };

  const filteredWords = searchFilter
    ? words.filter((w) => w.toLowerCase().includes(searchFilter.toLowerCase()))
    : words;

  return (
    <div className="space-y-6">
      {/* Add Word Section */}
      <div className="glass-card p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-green-500/10 flex items-center justify-center">
            <Plus className="w-5 h-5 text-green-400" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-white">Add New Word</h2>
            <p className="text-sm text-gray-400">Dynamically add offensive words to the detection dictionary</p>
          </div>
        </div>

        <div className="flex gap-3">
          <input
            type="text"
            value={newWord}
            onChange={(e) => setNewWord(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAddWord()}
            placeholder="Enter a new offensive word..."
            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-green-500/50 focus:ring-1 focus:ring-green-500/25 transition-all"
          />
          <button
            onClick={handleAddWord}
            disabled={loading || !newWord.trim()}
            className="px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-medium rounded-xl hover:from-green-500 hover:to-emerald-500 transition-all duration-300 disabled:opacity-50 flex items-center gap-2 shadow-lg shadow-green-500/20"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Plus className="w-4 h-4" />
            )}
            Add
          </button>
        </div>

        {message && (
          <div className={`mt-3 p-3 rounded-lg text-sm flex items-center gap-2 ${
            message.type === 'success'
              ? 'bg-green-500/10 border border-green-500/20 text-green-400'
              : message.type === 'error'
              ? 'bg-red-500/10 border border-red-500/20 text-red-400'
              : 'bg-blue-500/10 border border-blue-500/20 text-blue-400'
          }`}>
            {message.type === 'success' ? (
              <CheckCircle className="w-4 h-4" />
            ) : message.type === 'error' ? (
              <AlertTriangle className="w-4 h-4" />
            ) : (
              <CheckCircle className="w-4 h-4" />
            )}
            {message.text}
          </div>
        )}

        <p className="mt-3 text-xs text-gray-500">
          💡 Adding a word updates the Trie and rebuilds the Aho-Corasick automaton in real-time.
        </p>
      </div>

      {/* Dictionary Browser */}
      <div className="glass-card p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center">
              <BookOpen className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">Offensive Words Dictionary</h2>
              <p className="text-sm text-gray-400">{totalWords} words loaded</p>
            </div>
          </div>
        </div>

        {/* Search */}
        <div className="relative mb-4">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            type="text"
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            placeholder="Search dictionary..."
            className="w-full bg-white/5 border border-white/10 rounded-xl pl-10 pr-10 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 transition-all"
          />
          {searchFilter && (
            <button
              onClick={() => setSearchFilter('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {error && (
          <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm flex items-center gap-2 mb-4">
            <AlertTriangle className="w-4 h-4" />
            {error}
          </div>
        )}

        {/* Words Grid */}
        {fetching ? (
          <div className="text-center py-8 text-gray-400">Loading dictionary...</div>
        ) : (
          <>
            <div className="text-xs text-gray-500 mb-3">
              Showing {filteredWords.length} of {totalWords} words
            </div>
            <div className="flex flex-wrap gap-2 max-h-96 overflow-y-auto pr-2">
              {filteredWords.map((word, i) => (
                <span
                  key={i}
                  className="px-3 py-1.5 rounded-lg bg-white/5 text-sm text-gray-300 border border-white/5 hover:border-red-500/30 hover:text-red-400 transition-all cursor-default"
                >
                  {word}
                </span>
              ))}
              {filteredWords.length === 0 && (
                <div className="text-center py-8 text-gray-500 w-full">
                  {searchFilter ? 'No words match your search' : 'No words loaded'}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
