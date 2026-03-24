import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import StudentShell from './components/StudentShell';
import { StudentPortalProvider } from './lib/student-portal';
import StudentDetails from './pages/StudentDetails';
import StudentChat from './pages/StudentChat';
import './index.css';

export default function App() {
  return (
    <StudentPortalProvider>
      <BrowserRouter>
          <Routes>
            <Route element={<StudentShell />}>
              <Route path="/" element={<StudentDetails />} />
              <Route path="/chat" element={<StudentChat />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
      </BrowserRouter>
    </StudentPortalProvider>
  );
}
