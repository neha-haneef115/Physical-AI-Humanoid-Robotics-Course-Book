// src/components/RAGChatWidget.tsx
import React, { useState, useEffect, useRef } from 'react';
import useTextSelection from './useTextSelection';
import { TbMessageChatbot, TbX, TbSend, TbRobot, TbUser } from 'react-icons/tb';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface RAGChatWidgetProps {
  onClose?: () => void;
  apiUrl?: string;
  theme?: 'light' | 'dark';
}

const RAGChatWidget: React.FC<RAGChatWidgetProps> = ({ 
  onClose: propOnClose, 
  apiUrl = 'http://localhost:5000', 
  theme = 'dark' 
}) => {
  const [isOpen, setIsOpen] = useState(true);
  
  // Use the provided onClose if available, otherwise use local state
  const handleClose = () => {
    if (propOnClose) {
      propOnClose();
    } else {
      setIsOpen(false);
    }
  };

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { selectedText, clearSelection } = useTextSelection();

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle sending a message
  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    // Update UI with user message immediately
    // Add user message to chat
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Call the RAG backend API
      const response = await fetch(`${apiUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ message: input }),
        credentials: 'include', // Include cookies for session management
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to get response from the server');
      }

      const data = await response.json();

      const botMessage: Message = {
        role: 'assistant',
        content: data.reply,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // More detailed error message
      let errorMessage = 'Sorry, I encountered an error. Please try again later.';
      if (error instanceof Error) {
        errorMessage = error.message || errorMessage;
      }
      
      const errorResponse: Message = {
        role: 'assistant',
        content: `Error: ${errorMessage}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle selected text
  useEffect(() => {
    if (selectedText) {
      setInput(selectedText);
      clearSelection();
    }
  }, [selectedText, clearSelection]);

  // If closed and no onClose handler was provided, show just the floating button
  if (!isOpen && !propOnClose) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          width: '56px',
          height: '56px',
          borderRadius: '50%',
          backgroundColor: theme === 'dark' ? '#3b82f6' : '#2563eb',
          color: 'white',
          border: 'none',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 999,
        }}
        aria-label="Open chat"
      >
        <TbMessageChatbot size={24} />
      </button>
    );
  }

  return (
    <div
      className={`rag-chat-widget ${theme}`}
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        width: '320px',
        maxWidth: 'calc(100% - 40px)',
        height: '500px',
        maxHeight: 'calc(100vh - 40px)',
        backgroundColor: theme === 'dark' ? '#1f2937' : 'white',
        borderRadius: '12px',
        boxShadow: '0 10px 25px rgba(0,0,0,0.2)',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        zIndex: 1000,
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: '12px 16px',
          backgroundColor: theme === 'dark' ? '#111827' : '#3b82f6',
          color: 'white',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <TbRobot size={20} />
          <span style={{ fontWeight: 600 }}>RAG Assistant</span>
        </div>
        <button
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            handleClose();
          }}
          style={{
            background: 'none',
            border: 'none',
            color: 'white',
            cursor: 'pointer',
            padding: '4px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
          aria-label="Close chat"
          type="button"
        >
          <TbX size={20} />
        </button>
      </div>

      {/* Messages */}
      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '16px',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
        }}
      >
        {messages.length === 0 ? (
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: theme === 'dark' ? '#9ca3af' : '#6b7280',
              textAlign: 'center',
              padding: '16px',
            }}
          >
            <TbMessageChatbot size={48} style={{ marginBottom: '16px' }} />
            <h3 style={{ margin: 0, marginBottom: '8px', fontSize: '1.1rem' }}>
              How can I help you today?
            </h3>
            <p style={{ margin: 0, fontSize: '0.875rem' }}>
              Ask me anything about the textbook content.
            </p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              style={{
                alignSelf: message.role === 'user' ? 'flex-end' : 'flex-start',
                maxWidth: '85%',
                backgroundColor:
                  message.role === 'user'
                    ? theme === 'dark'
                      ? '#3b82f6'
                      : '#3b82f6'
                    : theme === 'dark'
                    ? '#374151'
                    : '#f3f4f6',
                color: message.role === 'user' ? 'white' : theme === 'dark' ? 'white' : '#111827',
                padding: '8px 12px',
                borderRadius: '12px',
                borderTopLeftRadius: message.role === 'assistant' ? '4px' : '12px',
                borderTopRightRadius: message.role === 'user' ? '4px' : '12px',
              }}
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  marginBottom: '4px',
                }}
              >
                {message.role === 'assistant' ? (
                  <TbRobot size={16} />
                ) : (
                  <TbUser size={16} />
                )}
                <span style={{ fontWeight: 600, fontSize: '0.75rem', opacity: 0.8 }}>
                  {message.role === 'assistant' ? 'Assistant' : 'You'}
                </span>
                <span
                  style={{
                    fontSize: '0.7rem',
                    opacity: 0.6,
                    marginLeft: 'auto',
                  }}
                >
                  {message.timestamp.toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </span>
              </div>
              <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem' }}>
                {message.content}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <form
        onSubmit={handleSendMessage}
        style={{
          borderTop: `1px solid ${theme === 'dark' ? '#374151' : '#e5e7eb'}`,
          padding: '12px',
        }}
      >
        <div
          style={{
            display: 'flex',
            gap: '8px',
            backgroundColor: theme === 'dark' ? '#374151' : '#f3f4f6',
            borderRadius: '8px',
            padding: '8px',
          }}
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your question..."
            style={{
              flex: 1,
              border: 'none',
              background: 'transparent',
              color: theme === 'dark' ? 'white' : '#111827',
              padding: '8px',
              outline: 'none',
              fontSize: '0.9rem',
            }}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            style={{
              background: 'transparent',
              border: 'none',
              color: theme === 'dark' ? '#9ca3af' : '#6b7280',
              padding: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              opacity: isLoading || !input.trim() ? 0.5 : 1,
              cursor: isLoading || !input.trim() ? 'not-allowed' : 'pointer',
            }}
            aria-label="Send message"
          >
            {isLoading ? (
              <div
                style={{
                  width: '20px',
                  height: '20px',
                  border: '2px solid #9ca3af',
                  borderTopColor: 'transparent',
                  borderRadius: '50%',
                  animation: 'spin 1s linear infinite',
                }}
              />
            ) : (
              <TbSend size={20} />
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default RAGChatWidget;