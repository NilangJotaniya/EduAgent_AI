import { useState } from 'react';
import type { FormEvent } from 'react';
import { Bot, Loader2, Send, ThumbsUp, User } from 'lucide-react';
import Card from '../components/Card';
import { Button, Input } from '../components/FormField';
import { buildApiUrl, recordFaqFeedback, sendChat } from '../lib/api';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  faqIds?: string[];
  helpfulMarked?: boolean;
  downloads?: Array<{ id: string; name: string; url: string }>;
}

const quickPrompts = [
  'When are the upcoming semester exams?',
  'What is the complete fee structure?',
  'What is the minimum attendance requirement?',
  'What scholarships are available for students?',
];

export default function StudentChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: 'Hello! I am EduAgent AI. Ask me anything about exams, fees, attendance, scholarships, admissions, or policies.',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [info, setInfo] = useState('');

  const submit = async (raw?: string) => {
    const message = (raw ?? input).trim();
    if (!message || loading) return;

    setError('');
    setInfo('');
    setLoading(true);
    setMessages((prev) => [...prev, { role: 'user', content: message }]);
    setInput('');

    try {
      const result = await sendChat(message);
      const faqIds = Array.isArray(result.meta?.faq_ids)
        ? result.meta.faq_ids.filter((id): id is string => typeof id === 'string')
        : [];
      const downloads = Array.isArray(result.meta?.downloads)
        ? result.meta.downloads.filter(
            (d): d is { id: string; name: string; url: string } =>
              !!d && typeof d.id === 'string' && typeof d.name === 'string' && typeof d.url === 'string',
          )
        : [];
      setMessages((prev) => [...prev, { role: 'assistant', content: result.answer, faqIds, downloads }]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message.');
      setMessages((prev) => [...prev, { role: 'assistant', content: 'Could not connect to backend. Check API server and try again.' }]);
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    await submit();
  };

  return (
    <div className="max-w-[1250px] mx-auto px-6 lg:px-10 py-6">
      <Card title="Academic Assistant" subtitle="Ask institute-related questions">
        <div className="space-y-4">
          <div className="h-[520px] overflow-y-auto rounded-xl border border-slate-200 bg-white p-4 space-y-3">
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm ${
                    msg.role === 'user'
                      ? 'bg-burgundy-500 text-white rounded-br-md'
                      : 'bg-slate-50 text-slate-700 border border-slate-200 rounded-bl-md'
                  }`}
                >
                  <div className="flex items-center gap-2 text-xs mb-1 opacity-80">
                    {msg.role === 'user' ? <User size={12} /> : <Bot size={12} />}
                    <span>{msg.role === 'user' ? 'You' : 'EduAgent'}</span>
                  </div>
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                  {msg.role === 'assistant' && msg.faqIds && msg.faqIds.length > 0 && (
                    <div className="mt-2">
                      <button
                        type="button"
                        disabled={!!msg.helpfulMarked}
                        className="inline-flex items-center gap-1 text-xs text-slate-500 hover:text-burgundy-600 disabled:opacity-60"
                        onClick={async () => {
                          try {
                            await Promise.all(msg.faqIds!.map((id) => recordFaqFeedback(id, true)));
                            setMessages((prev) => prev.map((m, idx) => (idx === i ? { ...m, helpfulMarked: true } : m)));
                            setInfo('Thanks, feedback saved.');
                          } catch {
                            setError('Could not save feedback.');
                          }
                        }}
                      >
                        <ThumbsUp size={12} />
                        {msg.helpfulMarked ? 'Marked Helpful' : 'Helpful'}
                      </button>
                    </div>
                  )}
                  {msg.role === 'assistant' && msg.downloads && msg.downloads.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {msg.downloads.map((doc) => (
                        <a
                          key={doc.id}
                          href={buildApiUrl(doc.url)}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1 text-xs px-3 py-1.5 rounded-md bg-burgundy-50 text-burgundy-700 hover:bg-burgundy-100"
                        >
                          Download: {doc.name}
                        </a>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-slate-50 border border-slate-200 rounded-2xl rounded-bl-md px-4 py-3 text-sm text-slate-600 inline-flex items-center gap-2">
                  <Loader2 size={14} className="animate-spin" />
                  EduAgent is thinking...
                </div>
              </div>
            )}
          </div>

          <div className="flex flex-wrap gap-2">
            {quickPrompts.map((prompt) => (
              <button
                key={prompt}
                type="button"
                onClick={() => submit(prompt)}
                className="text-xs px-3 py-2 rounded-lg bg-burgundy-50 text-burgundy-600 hover:bg-burgundy-100 transition-colors"
              >
                {prompt}
              </button>
            ))}
          </div>

          <form className="flex gap-2" onSubmit={onSubmit}>
            <Input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask your academic question..." />
            <Button variant="primary" type="submit" disabled={loading}>
              <Send size={14} />
              Send
            </Button>
          </form>

          {error && <p className="text-sm text-danger">{error}</p>}
          {info && <p className="text-sm text-success">{info}</p>}
        </div>
      </Card>
    </div>
  );
}
