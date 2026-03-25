import { Bell } from 'lucide-react';
import { Outlet, useLocation } from 'react-router-dom';
import SideNav from './SideNav';
import StudentLoginScreen from './StudentLoginScreen';
import { Button } from './FormField';
import { useStudentPortal } from '../lib/student-portal';

function getPageCopy(pathname: string) {
  if (pathname === '/details') {
    return { title: 'Student Details', subtitle: 'Profile, notices, documents, and current academic information' };
  }
  return { title: 'Student Chat', subtitle: 'EduAgent AI Assistant' };
}

export default function StudentShell() {
  const location = useLocation();
  const { authenticated, initializing, reminders, unreadReminders, logout, markRemindersRead } = useStudentPortal();
  const page = getPageCopy(location.pathname);

  if (initializing) {
    return <div className="min-h-screen bg-cream-50" />;
  }

  if (!authenticated) {
    return <StudentLoginScreen />;
  }

  return (
    <div className="flex min-h-screen bg-cream-50">
      <SideNav />
      <main className="flex-1 min-w-0">
        <header className="sticky top-0 z-20 bg-white/80 backdrop-blur-xl border-b border-slate-200/60">
          <div className="max-w-[1250px] mx-auto px-6 lg:px-10 h-16 flex items-center justify-between">
            <div>
              <h1 className="text-lg font-bold text-slate-800">{page.title}</h1>
              <p className="text-xs text-slate-400 -mt-0.5">{page.subtitle}</p>
            </div>
            <div className="flex items-center gap-3">
              <div className="relative group">
                <button
                  type="button"
                  className="relative p-2 rounded-lg hover:bg-slate-100 transition-colors"
                  onClick={async () => {
                    if (unreadReminders > 0) {
                      await markRemindersRead();
                    }
                  }}
                >
                  <Bell size={18} className="text-slate-700" />
                  {unreadReminders > 0 && <span className="absolute -top-1 -right-1 text-[10px] min-w-[16px] h-4 px-1 rounded-full bg-danger text-white">{unreadReminders}</span>}
                </button>
                <div className="invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-opacity absolute right-0 top-11 w-[360px] max-h-[360px] overflow-y-auto bg-white border border-slate-200 rounded-xl shadow-lg p-3 z-30">
                  <p className="text-sm font-semibold text-slate-800 px-1 pb-2 border-b border-slate-100">Fee Reminders</p>
                  <div className="divide-y divide-slate-100">
                    {reminders.slice(0, 20).map((r) => (
                      <div key={r._id} className="py-2.5 px-1">
                        <p className="text-sm text-slate-700">{r.message}</p>
                        <p className="text-xs text-slate-400 mt-1">{r.sent_at.slice(0, 16)}</p>
                      </div>
                    ))}
                    {reminders.length === 0 && <p className="py-3 px-1 text-sm text-slate-500">No reminders yet.</p>}
                  </div>
                </div>
              </div>
              <Button variant="ghost" onClick={logout}>
                Logout
              </Button>
            </div>
          </div>
        </header>

        <Outlet />
      </main>
    </div>
  );
}
