'use client';

import { createContext, useContext, useState, ReactNode, Dispatch, SetStateAction } from 'react';

// Define the message type
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string; // Using string to avoid serialization issues
}

// Define the context type
interface ChatContextType {
  messages: Message[];
  setMessages: Dispatch<SetStateAction<Message[]>>;
  conversationId: number | null;
  setConversationId: Dispatch<SetStateAction<number | null>>;
  isLoading: boolean;
  setIsLoading: Dispatch<SetStateAction<boolean>>;
  error: string | null;
  setError: Dispatch<SetStateAction<string | null>>;
}

// Create the context
const ChatContext = createContext<ChatContextType | undefined>(undefined);

// Create the provider component
export function ChatProvider({ children }: { children: ReactNode }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const value = {
    messages,
    setMessages,
    conversationId,
    setConversationId,
    isLoading,
    setIsLoading,
    error,
    setError,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
}

// Create a custom hook to use the chat context
export function useChat() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}