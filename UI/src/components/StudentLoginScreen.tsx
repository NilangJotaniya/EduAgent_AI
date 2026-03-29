import { Loader2, MessageCircle } from 'lucide-react';
import { useState } from 'react';
import { Button, Input } from './FormField';
import { useStudentPortal } from '../lib/student-portal';

export default function StudentLoginScreen() {
  const { login } = useStudentPortal();
  const [studentId, setStudentId] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async () => {
    setLoading(true);
    setError('');
    try {
      await login(studentId, password);
      setPassword('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-cream-50 lg:flex">
      <aside className="hidden lg:flex w-64 bg-burgundy-700 border-r border-burgundy-600 flex-col">
        <div className="p-6 border-b border-burgundy-600">
          <div className="flex items-center gap-3">
            <span className="w-9 h-9 rounded-lg bg-gold-400 text-burgundy-800 font-bold text-sm inline-flex items-center justify-center">EA</span>
            <div>
              <p className="text-white font-bold text-base leading-tight">EduAgent AI</p>
            </div>
          </div>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          <div className="flex items-center gap-3 px-4 py-3 rounded-lg bg-burgundy-500/60 text-white text-sm font-medium shadow-sm">
            <MessageCircle size={18} />
            Student Chat
          </div>
        </nav>
        <div className="p-4 border-t border-burgundy-600">
          <p className="text-burgundy-300 text-xs text-center">Student Site</p>
        </div>
      </aside>

      <main className="flex-1 flex items-center justify-center p-6 lg:p-10">
        <div className="w-full max-w-[620px] rounded-2xl border border-slate-200 bg-white shadow-sm">
          <div className="px-7 py-6 border-b border-slate-200">
            <h2 className="text-base font-semibold text-slate-800">Student Login</h2>
            <p className="mt-0.5 text-xs text-slate-400">Secure student access portal</p>
          </div>
          <div className="px-7 py-6 space-y-4">
            <Input placeholder="Enrollment Number" value={studentId} onChange={(e) => setStudentId(e.target.value)} />
            <Input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') void handleLogin();
              }}
            />
            <Button variant="primary" className="w-full" onClick={handleLogin} disabled={!studentId || !password || loading}>
              {loading ? <Loader2 size={14} className="animate-spin" /> : 'Login'}
            </Button>
            <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-500">
              <div className="mb-1 flex items-center gap-2 text-slate-700 text-sm font-medium">
                <MessageCircle size={16} />
                Enrollment-based sign in
              </div>
              <p>Use credentials issued by your institute. Contact the student support desk if your account is not active.</p>
            </div>
            {error && <p className="text-sm text-danger">{error}</p>}
          </div>
        </div>
      </main>
    </div>
  );
}
