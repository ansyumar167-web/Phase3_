'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Home() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated
    const user = localStorage.getItem('user');
    if (user) {
      setIsAuthenticated(true);
      // If authenticated, redirect to chat after a brief moment
      setTimeout(() => router.push('/chat'), 500);
    } else {
      setIsLoading(false);
    }
  }, [router]);

  // If authenticated, show loading state
  if (isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50 flex items-center justify-center">
        <div className="text-center animate-fade-in">
          <div className="w-16 h-16 border-4 border-sky-500/30 border-t-sky-500 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your workspace...</p>
        </div>
      </div>
    );
  }

  // Show landing page for non-authenticated users
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-gray-200/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-sky-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
              <span className="text-white text-lg font-bold">✓</span>
            </div>
            <span className="text-xl font-bold text-gray-900">Todo Assistant</span>
          </div>
          <button
            onClick={() => router.push('/login')}
            className="px-6 py-2.5 bg-gradient-to-r from-sky-500 to-blue-600 text-white rounded-xl font-semibold hover:shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-all duration-200"
          >
            Sign In
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center mb-16 animate-fade-in">
          {/* App Icon */}
          <div className="w-24 h-24 bg-gradient-to-br from-sky-500 to-blue-600 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-2xl">
            <span className="text-white text-4xl font-bold">✓</span>
          </div>

          {/* Headline */}
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Manage Tasks with
            <br />
            <span className="bg-gradient-to-r from-sky-500 to-blue-600 bg-clip-text text-transparent">
              AI-Powered Intelligence
            </span>
          </h1>

          {/* Subheadline */}
          <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed">
            Say goodbye to complex task managers. Just chat with our AI assistant
            and let it handle your todos naturally and effortlessly.
          </p>

          {/* CTA Button */}
          <button
            onClick={() => router.push('/login')}
            className="px-8 py-4 bg-gradient-to-r from-sky-500 to-blue-600 text-white rounded-2xl font-bold text-lg hover:shadow-2xl hover:scale-[1.05] active:scale-[0.98] transition-all duration-200 inline-flex items-center gap-3"
          >
            Get Started Free
            <span className="text-2xl">→</span>
          </button>

          <p className="text-sm text-gray-500 mt-4">No credit card required • Free forever</p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mt-20 animate-slide-up">
          {/* Feature 1 */}
          <div className="bg-white border border-gray-200 rounded-2xl p-8 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="w-14 h-14 bg-blue-100 rounded-xl flex items-center justify-center mb-6">
              <span className="text-3xl">💬</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Natural Conversations</h3>
            <p className="text-gray-600 leading-relaxed">
              Just talk to the AI like you would to a friend. No complex forms or buttons to click.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="bg-white border border-gray-200 rounded-2xl p-8 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="w-14 h-14 bg-green-100 rounded-xl flex items-center justify-center mb-6">
              <span className="text-3xl">⚡</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Lightning Fast</h3>
            <p className="text-gray-600 leading-relaxed">
              Add, complete, or delete tasks in seconds. The AI understands your intent instantly.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="bg-white border border-gray-200 rounded-2xl p-8 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="w-14 h-14 bg-purple-100 rounded-xl flex items-center justify-center mb-6">
              <span className="text-3xl">🎯</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Smart & Simple</h3>
            <p className="text-gray-600 leading-relaxed">
              No learning curve. Start managing your tasks immediately with zero setup required.
            </p>
          </div>
        </div>

        {/* How It Works Section */}
        <div className="mt-24 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">How It Works</h2>
          <p className="text-gray-600 mb-12 text-lg">Three simple steps to productivity</p>

          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-sky-500 to-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4 shadow-lg">
                1
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Sign Up</h3>
              <p className="text-gray-600 text-sm">Create your free account in seconds</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-sky-500 to-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4 shadow-lg">
                2
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Start Chatting</h3>
              <p className="text-gray-600 text-sm">Tell the AI what you need to do</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-sky-500 to-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4 shadow-lg">
                3
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Get Things Done</h3>
              <p className="text-gray-600 text-sm">Watch your productivity soar</p>
            </div>
          </div>
        </div>

        {/* Final CTA */}
        <div className="mt-24 text-center bg-gradient-to-br from-sky-500 to-blue-600 rounded-3xl p-12 text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to Get Organized?</h2>
          <p className="text-blue-100 mb-8 text-lg">Join thousands of users managing their tasks smarter</p>
          <button
            onClick={() => router.push('/login')}
            className="px-8 py-4 bg-white text-blue-600 rounded-2xl font-bold text-lg hover:shadow-2xl hover:scale-[1.05] active:scale-[0.98] transition-all duration-200"
          >
            Start Free Today
          </button>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 mt-20 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center text-gray-600 text-sm">
          <p>© 2026 Todo Assistant. Built with AI for productivity.</p>
        </div>
      </footer>
    </div>
  );
}
