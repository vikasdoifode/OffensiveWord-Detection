import { Shield, Activity } from 'lucide-react';

export default function Header() {
  return (
    <header className="border-b border-white/5 bg-[#0a0a0f]/80 backdrop-blur-xl sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Title */}
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-[#0a0a0f] pulse-dot" />
            </div>
            <div>
              <h1 className="text-lg font-bold gradient-text">
                Offensive Comment Detection
              </h1>
              <p className="text-xs text-gray-500">
                Real-Time Analysis using DAA Algorithms
              </p>
            </div>
          </div>

          {/* Status Indicator */}
          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-500/10 border border-green-500/20">
              <Activity className="w-3.5 h-3.5 text-green-500" />
              <span className="text-xs font-medium text-green-400">System Active</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
