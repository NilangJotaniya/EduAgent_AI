import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import type { ReactNode } from 'react';
import {
  clearStudentToken,
  getStudentDocuments,
  getStudentFees,
  getStudentMe,
  getStudentReminders,
  markStudentRemindersRead,
  studentLogin,
} from './api';
import type { StudentDocument, StudentFeeLedger, StudentProfile, StudentReminder } from './api';

interface StudentPortalContextValue {
  authenticated: boolean;
  initializing: boolean;
  student: StudentProfile | null;
  fees: StudentFeeLedger[];
  documents: StudentDocument[];
  reminders: StudentReminder[];
  unreadReminders: number;
  login: (identifier: string, password: string) => Promise<void>;
  logout: () => void;
  refresh: () => Promise<void>;
  markRemindersRead: () => Promise<void>;
}

const StudentPortalContext = createContext<StudentPortalContextValue | null>(null);

async function loadStudentBundle() {
  const [me, feeRes, docRes, reminderRes] = await Promise.all([
    getStudentMe(),
    getStudentFees(),
    getStudentDocuments(),
    getStudentReminders(),
  ]);

  return {
    me,
    fees: feeRes.items,
    documents: docRes.items,
    reminders: reminderRes.items,
    unread: reminderRes.unread_count,
  };
}

export function StudentPortalProvider({ children }: { children: ReactNode }) {
  const [authenticated, setAuthenticated] = useState(false);
  const [initializing, setInitializing] = useState(true);
  const [student, setStudent] = useState<StudentProfile | null>(null);
  const [fees, setFees] = useState<StudentFeeLedger[]>([]);
  const [documents, setDocuments] = useState<StudentDocument[]>([]);
  const [reminders, setReminders] = useState<StudentReminder[]>([]);
  const [unreadReminders, setUnreadReminders] = useState(0);

  const applyBundle = async () => {
    const bundle = await loadStudentBundle();
    setStudent(bundle.me);
    setFees(bundle.fees);
    setDocuments(bundle.documents);
    setReminders(bundle.reminders);
    setUnreadReminders(bundle.unread);
  };

  useEffect(() => {
    const init = async () => {
      const params = new URLSearchParams(window.location.search);
      if (params.get('fresh') === '1') {
        clearStudentToken();
      }
      try {
        await applyBundle();
        setAuthenticated(true);
      } catch {
        setAuthenticated(false);
      } finally {
        setInitializing(false);
      }
    };
    void init();
  }, []);

  const value = useMemo<StudentPortalContextValue>(
    () => ({
      authenticated,
      initializing,
      student,
      fees,
      documents,
      reminders,
      unreadReminders,
      login: async (identifier: string, password: string) => {
        await studentLogin(identifier, password);
        await applyBundle();
        setAuthenticated(true);
      },
      logout: () => {
        clearStudentToken();
        setAuthenticated(false);
        setStudent(null);
        setFees([]);
        setDocuments([]);
        setReminders([]);
        setUnreadReminders(0);
      },
      refresh: applyBundle,
      markRemindersRead: async () => {
        await markStudentRemindersRead();
        await applyBundle();
      },
    }),
    [authenticated, initializing, student, fees, documents, reminders, unreadReminders],
  );

  return <StudentPortalContext.Provider value={value}>{children}</StudentPortalContext.Provider>;
}

export function useStudentPortal() {
  const context = useContext(StudentPortalContext);
  if (!context) {
    throw new Error('useStudentPortal must be used within StudentPortalProvider');
  }
  return context;
}
