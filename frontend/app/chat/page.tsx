'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../contexts/auth-context';
import { useChat } from '../../contexts/chat-context';
import { sendChatMessage } from '../../utils/api';

export default function ChatPage() {
  const { user, logout } = useAuth();
  const {
    messages,
    setMessages,
    conversationId,
    setConversationId,
    isLoading,
    setIsLoading,
    error,
    setError
  } = useChat();
  const [inputValue, setInputValue] = useState('');
  const router = useRouter();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Check if user is authenticated
  useEffect(() => {
    if (!user) {
      router.push('/login');
    }
  }, [user, router]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now().toString(),
      role: 'user' as const,
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError('');

    try {
      // Send message to backend API using the user ID from auth context
      const response = await sendChatMessage(user!.id, inputValue, conversationId || undefined);

      // Update conversation ID if new one was returned
      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response to messages
      const assistantMessage = {
        id: `assistant-${Date.now()}`,
        role: 'assistant' as const,
        content: response.response,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to send message. Please try again.');

      // Add error message to chat
      const errorMessage = {
        id: `error-${Date.now()}`,
        role: 'assistant' as const,
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-cyan-50 flex flex-col">
      {/* Header - More refined with better spacing */}
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-200/50 py-4 px-6 flex justify-between items-center sticky top-0 z-10">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-sky-500 to-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-sm font-bold">✓</span>
            </div>
            <div>
              <h1 className="text-lg font-semibold text-gray-900">Todo Assistant</h1>
              <p className="text-xs text-gray-500">AI-powered task management</p>
            </div>
          </div>
          <nav className="hidden md:flex gap-4">
            <button
              onClick={() => router.push('/dashboard')}
              className="px-4 py-2 text-gray-600 hover:text-gray-900 font-medium transition-colors"
            >
              Dashboard
            </button>
            <button
              onClick={() => router.push('/chat')}
              className="px-4 py-2 text-sky-600 font-semibold border-b-2 border-sky-600"
            >
              Chat
            </button>
          </nav>
        </div>
        <button
          onClick={handleLogout}
          className="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 px-4 rounded-lg transition-all duration-200 font-medium hover:shadow-sm"
        >
          Logout
        </button>
      </header>

      {/* Chat Container - Better max-width and spacing */}
      <div className="flex-1 flex flex-col max-w-5xl mx-auto w-full px-4 py-6">
        {/* Messages Area - Improved scrolling and spacing */}
        <div className="flex-1 overflow-y-auto mb-6 space-y-4 max-h-[calc(100vh-220px)] scroll-smooth">
          {messages.length === 0 ? (
            <div className="text-center py-16 animate-fade-in">
              <div className="w-16 h-16 bg-gradient-to-br from-sky-500 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                <span className="text-white text-2xl">✓</span>
              </div>
              <h2 className="text-3xl font-bold text-gray-900 mb-3">Welcome to Todo Assistant</h2>
              <p className="text-gray-600 text-lg mb-8 max-w-md mx-auto">
                Your AI-powered task manager. Just tell me what you need to do.
              </p>
              <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
                <div className="bg-white border border-gray-200 p-5 rounded-xl hover:shadow-md transition-shadow duration-200">
                  <p className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    <span className="text-blue-500">💬</span> Try saying:
                  </p>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start gap-2">
                      <span className="text-gray-400 mt-0.5">•</span>
                      <span>"Add a task to buy groceries"</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-gray-400 mt-0.5">•</span>
                      <span>"Show me all my tasks"</span>
                    </li>
                  </ul>
                </div>
                <div className="bg-white border border-gray-200 p-5 rounded-xl hover:shadow-md transition-shadow duration-200">
                  <p className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    <span className="text-green-500">✨</span> Or try:
                  </p>
                  <ul className="space-y-2 text-sm text-gray-600">
                    <li className="flex items-start gap-2">
                      <span className="text-gray-400 mt-0.5">•</span>
                      <span>"Mark task 1 as complete"</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-gray-400 mt-0.5">•</span>
                      <span>"Delete the meeting task"</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <div
                  className={`max-w-[75%] md:max-w-[65%] rounded-2xl px-5 py-3.5 shadow-sm ${
                    message.role === 'user'
                      ? 'bg-gradient-to-br from-sky-500 to-blue-600 text-white rounded-br-md'
                      : 'bg-white text-gray-800 rounded-bl-md border border-gray-200'
                  }`}
                >
                  <div className="whitespace-pre-wrap leading-relaxed text-[15px]">{message.content}</div>
                  <div
                    className={`text-[11px] mt-2 font-medium ${
                      message.role === 'user' ? 'text-blue-100' : 'text-gray-400'
                    }`}
                  >
                    {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex justify-start animate-fade-in">
              <div className="bg-white text-gray-800 rounded-2xl rounded-bl-md px-5 py-4 max-w-[75%] md:max-w-[65%] border border-gray-200 shadow-sm">
                <div className="flex space-x-1.5">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area - More polished with better focus states */}
        <form onSubmit={handleSubmit} className="mt-auto">
          {error && (
            <div className="mb-3 p-3 bg-red-50 border border-red-200 text-red-700 rounded-xl text-sm flex items-start gap-2 animate-slide-up">
              <span className="text-red-500 mt-0.5">⚠</span>
              <span>{error}</span>
            </div>
          )}
          <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-2 flex gap-2 focus-within:ring-2 focus-within:ring-sky-500/20 transition-all duration-200">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask me to add, list, or manage your tasks..."
              className="flex-1 px-4 py-3 bg-transparent focus:outline-none text-gray-900 placeholder:text-gray-400 text-[15px]"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !inputValue.trim()}
              className={`px-6 py-3 rounded-xl font-medium transition-all duration-200 flex items-center gap-2 ${
                isLoading || !inputValue.trim()
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-sky-500 to-blue-600 text-white hover:shadow-md hover:scale-[1.02] active:scale-[0.98]'
              }`}
            >
              <span>{isLoading ? 'Sending...' : 'Send'}</span>
              {!isLoading && <span className="text-lg">→</span>}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-3 text-center">
            💡 Try: "Add buy milk" • "Show my tasks" • "Complete task 1"
          </p>
        </form>
      </div>
    </div>
  );
}