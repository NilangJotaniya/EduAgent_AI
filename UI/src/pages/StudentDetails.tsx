import { Download } from 'lucide-react';
import Card from '../components/Card';
import { buildStudentDocumentDownloadUrl } from '../lib/api';
import { useStudentPortal } from '../lib/student-portal';

export default function StudentDetails() {
  const { student, documents, unreadReminders, reminders } = useStudentPortal();
  const latestReminder = reminders[0];

  return (
    <div className="max-w-[1250px] mx-auto px-6 lg:px-10 py-6 space-y-5">
      <div className="grid gap-5 lg:grid-cols-[1.2fr_0.8fr]">
        <Card title="Student Account" subtitle="Current academic profile" noPadding>
          <div className="grid gap-0 divide-y divide-slate-100">
            <div className="px-6 py-4">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Full Name</p>
              <p className="mt-1 text-sm font-semibold text-slate-800">{student?.full_name || 'Student'}</p>
            </div>
            <div className="px-6 py-4">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Enrollment Number</p>
              <p className="mt-1 text-sm font-semibold text-slate-800">{student?.enrollment_no || student?.student_id}</p>
            </div>
            <div className="px-6 py-4">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Programme</p>
              <p className="mt-1 text-sm font-semibold text-slate-800">{student?.program || 'Not assigned'}</p>
            </div>
            <div className="px-6 py-4">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Current Semester</p>
              <p className="mt-1 text-sm font-semibold text-slate-800">{student?.semester ? `Semester ${student.semester}` : 'Not assigned'}</p>
            </div>
          </div>
        </Card>

        <Card title="Portal Snapshot" subtitle="Current portal activity" noPadding>
          <div className="grid gap-0 divide-y divide-slate-100">
            <div className="px-6 py-4">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Available Documents</p>
              <p className="mt-1 text-2xl font-bold text-slate-900">{documents.length}</p>
            </div>
            <div className="px-6 py-4">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Unread Notices</p>
              <p className="mt-1 text-sm font-semibold text-slate-800">{unreadReminders} reminder(s)</p>
            </div>
            <div className="px-6 py-4">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Latest Reminder</p>
              <p className="mt-1 text-sm font-semibold text-slate-800">{latestReminder ? latestReminder.message : 'No reminders yet'}</p>
            </div>
          </div>
        </Card>
      </div>

      <Card title="Document Center" subtitle="Academic files and notices shared by administration" noPadding>
        <div className="divide-y divide-slate-100">
          {documents.map((doc) => (
            <div key={doc._id} className="px-6 py-4 flex items-center justify-between gap-3">
              <div>
                <p className="text-sm font-semibold text-slate-800">{doc.original_name || doc.filename}</p>
                <p className="text-xs text-slate-500">Category: {doc.category || 'General'} | Total downloads: {doc.download_count ?? 0}</p>
              </div>
              <a
                href={buildStudentDocumentDownloadUrl(doc._id)}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1 text-xs px-3 py-2 rounded-md bg-burgundy-50 text-burgundy-700 hover:bg-burgundy-100"
              >
                <Download size={12} />
                Download
              </a>
            </div>
          ))}
          {documents.length === 0 && <p className="px-6 py-4 text-sm text-slate-500">No documents uploaded yet.</p>}
        </div>
      </Card>
    </div>
  );
}
