const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const STUDENT_TOKEN_KEY = 'eduagent_student_token';

interface StoredStudentToken {
  token: string;
  expiresAt?: string;
}

function getStudentToken(): string {
  const raw = localStorage.getItem(STUDENT_TOKEN_KEY) || '';
  if (!raw) return '';
  try {
    const parsed = JSON.parse(raw) as StoredStudentToken;
    if (!parsed.token) {
      clearStudentToken();
      return '';
    }
    if (parsed.expiresAt) {
      const exp = Date.parse(parsed.expiresAt);
      if (Number.isFinite(exp) && Date.now() >= exp) {
        clearStudentToken();
        return '';
      }
    }
    return parsed.token;
  } catch {
    // Backward compatibility with legacy raw token string.
    return raw;
  }
}

function setStudentToken(token: string, expiresAt?: string): void {
  const payload: StoredStudentToken = { token, expiresAt };
  localStorage.setItem(STUDENT_TOKEN_KEY, JSON.stringify(payload));
}

export function clearStudentToken(): void {
  localStorage.removeItem(STUDENT_TOKEN_KEY);
}

async function request<T>(path: string, options: RequestInit = {}, withStudentAuth = false): Promise<T> {
  const headers = new Headers(options.headers || {});
  if (!(options.body instanceof FormData)) {
    headers.set('Content-Type', headers.get('Content-Type') || 'application/json');
  }
  if (withStudentAuth) {
    const token = getStudentToken();
    if (token) headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if ((response.status === 401 || response.status === 403) && withStudentAuth) {
    clearStudentToken();
  }

  if (!response.ok) {
    const body = await response.text();
    throw new Error(body || `Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export interface StudentLoginResponse {
  ok: boolean;
  token: string;
  token_type: string;
  expires_at: string;
  student_id: string;
  name: string;
}

export interface StudentProfile {
  student_id: string;
  enrollment_no?: string;
  full_name: string;
  program: string;
  semester?: number;
}

export interface StudentFeeLedger {
  _id: string;
  student_id: string;
  fee_type: string;
  total_amount: number;
  paid_amount: number;
  balance_amount: number;
  due_date: string;
  status: string;
  reminder_count?: number;
  last_reminder_at?: string;
}

export interface StudentDocument {
  _id: string;
  filename: string;
  original_name: string;
  title?: string;
  category?: string;
  pages: number;
  chunks: number;
  uploaded_at: string;
  download_count?: number;
}

export interface StudentReminder {
  _id: string;
  ledger_id: string;
  student_id: string;
  fee_type: string;
  message: string;
  is_read: boolean;
  sent_by: string;
  sent_at: string;
}

export async function studentLogin(studentId: string, password: string) {
  const res = await request<StudentLoginResponse>('/api/student/login', {
    method: 'POST',
    body: JSON.stringify({ identifier: studentId, password }),
  });
  if (res.token) setStudentToken(res.token, res.expires_at);
  return res;
}

export function getStudentMe() {
  return request<StudentProfile>('/api/student/me', {}, true);
}

export function getStudentFees() {
  return request<{ items: StudentFeeLedger[] }>('/api/student/fees', {}, true);
}

export function getStudentReminders() {
  return request<{ items: StudentReminder[]; unread_count: number }>('/api/student/reminders', {}, true);
}

export function markStudentRemindersRead() {
  return request<{ ok: boolean }>('/api/student/reminders/read', { method: 'POST' }, true);
}

export function getStudentDocuments() {
  return request<{ items: StudentDocument[] }>('/api/student/documents', {}, true);
}

export function changeStudentPassword(currentPassword: string, newPassword: string) {
  return request<{ ok: boolean }>(
    '/api/student/change-password',
    {
      method: 'POST',
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword,
      }),
    },
    true,
  );
}

export function buildStudentDocumentDownloadUrl(pdfId: string): string {
  const token = getStudentToken();
  const query = token ? `?token=${encodeURIComponent(token)}` : '';
  return `${API_BASE}/api/student/documents/${pdfId}/download${query}`;
}

export function buildApiUrl(path: string): string {
  return `${API_BASE}${path}`;
}

export function sendChat(message: string) {
  return request<{
    answer: string;
    escalated: boolean;
    meta: {
      faq_ids?: string[];
      downloads?: Array<{ id: string; name: string; url: string }>;
      [key: string]: unknown;
    };
  }>('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message }),
  });
}

export function recordFaqFeedback(faqId: string, isHelpful: boolean) {
  return request<{ ok: boolean }>(`/api/faqs/${faqId}/feedback`, {
    method: 'POST',
    body: JSON.stringify({ is_helpful: isHelpful }),
  });
}
