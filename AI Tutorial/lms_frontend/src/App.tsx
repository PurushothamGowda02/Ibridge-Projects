import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Login from './pages/Auth/Login';
import Signup from './pages/Auth/Signup';
import EligibilityTest from './pages/Auth/EligibilityTest';
import ProtectedRoute from './components/ProtectedRoute';
import CourseBuilder from './pages/Instructor/CourseBuilder';
import MyCourses from './pages/Learning/MyCourses';
import CoursePlayer from './pages/Learning/CoursePlayer';
import Library from './pages/Learning/Library';
import AICreator from './pages/Instructor/AICreator';
import AiTutorLab from './pages/Learning/AiTutorLab';
import AiCoursePlayer from './pages/Learning/AiCoursePlayer';
import DashboardHome from './pages/Learning/DashboardHome';
import PreEligibility from './pages/Learning/PreEligibility';
import Discussions from './pages/Learning/Discussions';
import Chatbot from './pages/Learning/Chatbot';
import { ToastProvider } from './components/ToastProvider';

const AppContent = () => {
  return (
    <Routes>
      {/* Public Routes - Registration First */}
      <Route path="/signup" element={<Signup />} />
      <Route path="/login" element={<Login />} />
      
      {/* Eligibility Test Route - Protected but accessible before passing */}
      <Route path="/pre-eligibility" element={
        <ProtectedRoute roles={['student']}>
          <EligibilityTest />
        </ProtectedRoute>
      } />
      
      {/* Protected Student Routes */}
      <Route path="/library" element={
        <ProtectedRoute roles={['student']}>
          <Library />
        </ProtectedRoute>
      } />

      <Route path="/dashboard" element={
        <ProtectedRoute roles={['student']}>
          <DashboardHome />
        </ProtectedRoute>
      } />

      <Route path="/my-courses" element={
        <ProtectedRoute roles={['student']}>
          <MyCourses />
        </ProtectedRoute>
      } />

      <Route path="/ai-tutor" element={
        <ProtectedRoute roles={['student']}>
          <AiTutorLab />
        </ProtectedRoute>
      } />

      <Route path="/chatbot" element={
        <ProtectedRoute roles={['student']}>
          <Chatbot />
        </ProtectedRoute>
      } />

      <Route path="/discussions" element={
        <ProtectedRoute roles={['student']}>
          <Discussions />
        </ProtectedRoute>
      } />

      <Route path="/learn/:courseId" element={
        <ProtectedRoute roles={['student']}>
          <CoursePlayer />
        </ProtectedRoute>
      } />

      <Route path="/learn-ai" element={
        <ProtectedRoute roles={['student']}>
          <AiCoursePlayer />
        </ProtectedRoute>
      } />

      {/* Protected Instructor Routes */}
      <Route path="/instructor/courses/new" element={
        <ProtectedRoute roles={['instructor', 'admin', 'super_admin']}>
          <CourseBuilder />
        </ProtectedRoute>
      } />

      <Route path="/instructor/ai-creator" element={
        <ProtectedRoute roles={['instructor', 'admin']}>
          <AICreator />
        </ProtectedRoute>
      } />

      {/* Default Route - Redirect to Signup (Registration First) */}
      <Route path="/" element={<Navigate to="/signup" replace />} />
    </Routes>
  );
};

function App() {
  return (
    <ToastProvider>
      <AuthProvider>
        <Router>
          <AppContent />
        </Router>
      </AuthProvider>
    </ToastProvider>
  );
}

export default App;
