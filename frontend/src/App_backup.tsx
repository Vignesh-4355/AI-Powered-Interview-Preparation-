import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Companies from './pages/Companies';
import CodingPractice from './pages/CodingPractice';
import Aptitude from './pages/Aptitude';
import HRDiscussion from './pages/HRDiscussion';
import MockInterview from './pages/MockInterview';
import Chatbot from './pages/Chatbot';
import Roadmap from './pages/Roadmap';
import Analytics from './pages/Analytics';
import ExpertTips from './pages/ExpertTips';
import CompanyPreparation from './pages/CompanyPreparation';
import CompanyDetail from './pages/CompanyDetail';
import CodingQuestionDetail from './pages/CodingQuestionDetail';
import './App.css';

function App() {
 return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
           path="/dashboard"
           element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
           path="/companies"
           element={
              <ProtectedRoute>
                <Companies />
              </ProtectedRoute>
            }
          />
          <Route
           path="/coding-practice"
           element={
              <ProtectedRoute>
                <CodingPractice />
              </ProtectedRoute>
            }
          />
          <Route
           path="/coding-practice/:id"
           element={
              <ProtectedRoute>
                <CodingQuestionDetail />
              </ProtectedRoute>
            }
          />
          <Route
           path="/aptitude"
           element={
              <ProtectedRoute>
                <Aptitude />
              </ProtectedRoute>
            }
          />
          <Route
           path="/hr-discussion"
           element={
              <ProtectedRoute>
                <HRDiscussion />
              </ProtectedRoute>
            }
          />
          <Route
           path="/mock-interview"
           element={
              <ProtectedRoute>
                <MockInterview />
              </ProtectedRoute>
            }
          />
          <Route
           path="/chatbot"
           element={
              <ProtectedRoute>
                <Chatbot />
              </ProtectedRoute>
            }
          />
          <Route
           path="/roadmap"
           element={
              <ProtectedRoute>
                <Roadmap />
              </ProtectedRoute>
            }
          />
          <Route
           path="/analytics"
           element={
              <ProtectedRoute>
                <Analytics />
              </ProtectedRoute>
            }
          />
          <Route
           path="/expert-tips"
           element={
              <ProtectedRoute>
                <ExpertTips />
              </ProtectedRoute>
            }
          />
          <Route
           path="/companies-prep"
           element={
              <ProtectedRoute>
                <CompanyPreparation />
              </ProtectedRoute>
            }
          />
          <Route
           path="/companies/:id"
           element={
              <ProtectedRoute>
                <CompanyDetail />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
