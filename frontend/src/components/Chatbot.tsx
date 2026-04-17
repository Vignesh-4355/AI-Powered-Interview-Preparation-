import { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Minimize2, Maximize2 } from 'lucide-react';
import { chatbotService, type ChatMessage as ChatMessageType } from '../services/chatbotService';
import './Chatbot.css';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const sessionId = useRef(
    sessionStorage.getItem('chat_session_id') || 
    sessionStorage.setItem('chat_session_id', crypto.randomUUID()) || 
    crypto.randomUUID()
  ).current;

  const quickActions = [
    'Prepare for TCS',
    'HR Questions',
    'Coding Tips',
    'Resume Advice'
  ];

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      setMessages([{
        message: '',
        response: "Hello! 👋 I'm your AI interview assistant. How can I help you today?",
        category: 'General',
        timestamp: new Date().toISOString(),
        suggestions: ['Interview preparation tips', 'Coding guidance', 'Company preparation', 'Resume building advice']
      }]);
    }
  }, [isOpen]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async (messageText?: string) => {
    const text = messageText || input;
    if (!text.trim() || loading) return;

    const userMessage = text.trim();
    setInput('');
    setLoading(true);

    // Add user message immediately
    setMessages(prev => [...prev, {
      message: userMessage,
      response: '',
      category: 'User',
      timestamp: new Date().toISOString()
    }]);

    try {
      const data = await chatbotService.sendMessage(userMessage, sessionId);
      setMessages(prev => [...prev, {
        message: userMessage,
        response: data.response,
        category: data.category,
        timestamp: data.timestamp,
        suggestions: data.suggestions
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        message: userMessage,
        response: 'Sorry, I encountered an error. Please try again.',
        category: 'Error',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAction = (action: string) => {
    handleSend(action);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isOpen) {
    return (
      <button className="chatbot-toggle" onClick={() => setIsOpen(true)}>
        <MessageSquare size={28} />
        <span className="badge">1</span>
      </button>
    );
  }

  return (
    <div className={`chatbot-container ${isMinimized ? 'minimized' : ''}`}>
      <div className="chatbot-header">
        <div className="header-left">
          <div className="bot-icon-wrapper">
            <MessageSquare size={24} />
          </div>
          <div>
            <h3>AI Interview Assistant</h3>
            <span className="status">● Online</span>
          </div>
        </div>
        <div className="header-actions">
          <button onClick={() => setIsMinimized(!isMinimized)} className="min-btn" title={isMinimized ? 'Maximize' : 'Minimize'}>
            {isMinimized ? <Maximize2 size={18} /> : <Minimize2 size={18} />}
          </button>
          <button onClick={() => setIsOpen(false)} className="close-btn" title="Close">
            <X size={20} />
          </button>
        </div>
      </div>

      {!isMinimized && (
        <>
          <div className="chatbot-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message-row ${msg.category === 'User' ? 'user' : 'bot'}`}>
                {msg.category !== 'User' && (
                  <div className="avatar bot">🤖</div>
                )}
                <div className="message-wrapper">
                  {msg.message && (
                    <div className="message-bubble user">
                      {msg.message}
                    </div>
                  )}
                  {msg.response && (
                    <div className="message-bubble bot">
                      <div className="bot-response">{msg.response}</div>
                      <div className="message-time">
                        {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>
                  )}
                  
                  {/* Quick suggestions after bot message */}
                  {msg.suggestions && msg.suggestions.length > 0 && msg.category !== 'User' && (
                    <div className="suggestions-container">
                      {msg.suggestions.slice(0, 3).map((suggestion, sIdx) => (
                        <button
                          key={sIdx}
                          className="suggestion-btn"
                          onClick={() => handleSend(suggestion)}
                          disabled={loading}
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
                {msg.category === 'User' && (
                  <div className="avatar user">👤</div>
                )}
              </div>
            ))}
            
            {loading && (
              <div className="message-row bot">
                <div className="avatar bot">🤖</div>
                <div className="message-bubble typing">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Actions Bar */}
          {messages.length <= 2 && (
            <div className="quick-actions">
              <div className="quick-actions-label">Quick Actions:</div>
              <div className="quick-actions-grid">
                {quickActions.map((action, idx) => (
                  <button
                    key={idx}
                    className="quick-action-btn"
                    onClick={() => handleQuickAction(action)}
                    disabled={loading}
                  >
                    {action}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="chatbot-input-area">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Ask about interviews, coding, companies..."
              disabled={loading}
              rows={2}
            />
            <button 
              onClick={() => handleSend()} 
              disabled={loading || !input.trim()}
              className="send-btn"
              title="Send message"
            >
              <Send size={20} />
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default Chatbot;
