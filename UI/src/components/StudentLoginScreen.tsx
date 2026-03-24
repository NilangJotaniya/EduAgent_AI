import { ChevronRight, Download, Loader2, LockKeyhole, ShieldCheck } from 'lucide-react';
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
    <div className="h-screen overflow-hidden bg-[linear-gradient(180deg,#fffaf0_0%,#fffdf8_100%)] px-4 py-4 lg:px-8">
      <div className="mx-auto flex h-full max-w-[1040px] items-center justify-center">
        <div className="w-full overflow-hidden rounded-[30px] border border-slate-200 bg-white shadow-[0_28px_70px_rgba(15,23,42,0.08)]">
          <div className="border-b border-slate-200 bg-[linear-gradient(135deg,#f7efe7_0%,#fff8ef_50%,#f5f0ea_100%)] px-6 py-5 lg:px-8 lg:py-6">
            <div className="mb-4 inline-flex items-center gap-3 rounded-full border border-slate-200 bg-white/90 px-4 py-2 text-sm text-slate-700 shadow-sm">
              <span className="flex h-9 w-9 items-center justify-center rounded-full bg-burgundy-600 text-xs font-bold text-white">EA</span>
              <div>
                <p className="font-semibold text-slate-900">EduAgent Student Portal</p>
                <p className="text-xs text-slate-500">Academic services and student support</p>
              </div>
            </div>

            <div className="grid gap-5 lg:grid-cols-[1.15fr_0.85fr] lg:items-center">
              <div className="space-y-3">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">Institution Access</p>
                <h1 className="max-w-xl text-[34px] font-bold tracking-tight text-slate-900 leading-[1.08] lg:text-[38px]">
                  Student academic access
                </h1>
                <p className="max-w-xl text-[15px] leading-6 text-slate-600">
                  Sign in with your enrollment number to access fee status, documents, reminders, and academic support.
                </p>
              </div>

              <div className="grid gap-2 sm:grid-cols-3 lg:grid-cols-1">
                <div className="rounded-2xl border border-white/90 bg-white/92 px-4 py-2.5 shadow-sm">
                  <div className="mb-2 flex items-center gap-2 text-slate-700">
                    <ShieldCheck size={15} />
                    <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Identity</p>
                  </div>
                  <p className="text-sm leading-5 text-slate-600">Enrollment-based access</p>
                </div>
                <div className="rounded-2xl border border-white/90 bg-white/92 px-4 py-2.5 shadow-sm">
                  <div className="mb-2 flex items-center gap-2 text-slate-700">
                    <Download size={15} />
                    <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Documents</p>
                  </div>
                  <p className="text-sm leading-5 text-slate-600">Secure academic files</p>
                </div>
                <div className="rounded-2xl border border-white/90 bg-white/92 px-4 py-2.5 shadow-sm">
                  <div className="mb-2 flex items-center gap-2 text-slate-700">
                    <ChevronRight size={15} />
                    <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Services</p>
                  </div>
                  <p className="text-sm leading-5 text-slate-600">Fees, reminders, support</p>
                </div>
              </div>
            </div>
          </div>

          <div className="grid gap-0 lg:grid-cols-[1fr_320px]">
            <div className="px-6 py-5 lg:px-8 lg:py-6">
              <div className="mb-4">
                <h2 className="text-[26px] font-bold text-slate-900">Student Sign In</h2>
                <p className="mt-1 text-sm text-slate-500">Use your enrollment number and password to access the portal</p>
              </div>

              <div className="space-y-3">
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
                <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-xs leading-5 text-slate-500">
                  <div className="mb-1 flex items-center gap-2 text-slate-700">
                    <LockKeyhole size={13} />
                    Secure student access
                  </div>
                  Use the credentials assigned by your institute. Contact the administration office if your account has not been issued or activated.
                </div>
                {error && <p className="text-sm text-danger">{error}</p>}
              </div>
            </div>

            <div className="border-t border-slate-200 bg-slate-50 px-6 py-5 lg:border-l lg:border-t-0 lg:px-8 lg:py-6">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Portal Access</p>
              <div className="mt-4 space-y-3">
                <div className="rounded-2xl border border-slate-200 bg-white p-3.5 shadow-sm">
                  <p className="text-sm font-semibold text-slate-800">Fee visibility</p>
                  <p className="mt-1 text-xs leading-5 text-slate-500">Track current due status, balance, and admin reminders.</p>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-white p-3.5 shadow-sm">
                  <p className="text-sm font-semibold text-slate-800">Document center</p>
                  <p className="mt-1 text-xs leading-5 text-slate-500">Download notices, PDFs, schedules, and shared academic files.</p>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-white p-3.5 shadow-sm">
                  <p className="text-sm font-semibold text-slate-800">Academic assistant</p>
                  <p className="mt-1 text-xs leading-5 text-slate-500">Get institute-specific responses for exams, attendance, and policies.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
