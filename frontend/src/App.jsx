import { useState } from 'react';
import Header from './components/Header';
import CommentAnalyzer from './components/CommentAnalyzer';
import YouTubeAnalyzer from './components/YouTubeAnalyzer';
import AlgorithmAnalysis from './components/AlgorithmAnalysis';
import AddWordPanel from './components/AddWordPanel';

const TABS = [
  { id: 'comment', label: 'Comment Analyzer', icon: '💬' },
  { id: 'youtube', label: 'YouTube Chat', icon: '📺' },
  { id: 'algorithms', label: 'DAA Analysis', icon: '📊' },
  { id: 'dictionary', label: 'Dictionary', icon: '📖' },
];

function App() {
  const [activeTab, setActiveTab] = useState('comment');

  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      {/* Background Effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl" />
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-pink-500/3 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10">
        <Header />

        {/* Tab Navigation */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
          <div className="flex flex-wrap gap-2 p-1.5 glass-card w-fit mx-auto">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-5 py-2.5 rounded-xl text-sm font-medium transition-all duration-300 flex items-center gap-2 ${
                  activeTab === tab.id
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <span>{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tab Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {activeTab === 'comment' && <CommentAnalyzer />}
          {activeTab === 'youtube' && <YouTubeAnalyzer />}
          {activeTab === 'algorithms' && <AlgorithmAnalysis />}
          {activeTab === 'dictionary' && <AddWordPanel />}
        </main>

        {/* Footer */}
        <footer className="text-center py-8 text-gray-500 text-sm border-t border-white/5">
          <p>Real-Time Offensive Comment Detection System — DAA Algorithms Project</p>
          <p className="mt-1 text-gray-600">
            Trie • Aho-Corasick • Greedy • Dynamic Programming • Backtracking
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
