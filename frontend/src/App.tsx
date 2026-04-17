import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Companies from './pages/Companies';
import CompanySelection from './pages/CompanySelection';
import CompanyList from './pages/CompanyList';
import CodingPractice from './pages/CodingPractice';
// import Aptitude from './pages/Aptitude';
import AptitudeList from './pages/AptitudeList';
import AptitudePractice from './pages/AptitudePractice';
import HRGDPage from './pages/HRGDPage';
import MockInterview from './pages/MockInterview';
import Chatbot from './components/Chatbot';

import ExpertTips from './pages/ExpertTips';
import RoadmapPage from './pages/RoadmapPage';
import CompanyPreparation from './pages/CompanyPreparation';
import CompanyDetail from './pages/CompanyDetail';
import CodingQuestionDetail from './pages/CodingQuestionDetail';
import AnalyticsPage from './pages/AnalyticsPage';
import ResumeAnalyzer from './pages/ResumeAnalyzer';
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
           path="/company-selection"
           element={
              <ProtectedRoute>
                <CompanySelection />
              </ProtectedRoute>
            }
          />
          <Route
           path="/companies-list"
           element={
              <ProtectedRoute>
                <CompanyList />
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
                <AptitudeList />
              </ProtectedRoute>
            }
          />
          <Route
           path="/aptitude/:category"
           element={
              <ProtectedRoute>
                <AptitudePractice />
              </ProtectedRoute>
            }
          />
          <Route
           path="/hr-discussion"
           element={
              <ProtectedRoute>
                <HRGDPage />
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
                <RoadmapPage />
              </ProtectedRoute>
            }
          />
          <Route
           path="/analytics"
           element={
              <ProtectedRoute>
                <AnalyticsPage />
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
          <Route
           path="/resume-analyzer"
           element={
              <ProtectedRoute>
                <ResumeAnalyzer />
              </ProtectedRoute>
            }
          />
        </Routes>
        <Chatbot />
      </Router>
    </AuthProvider>
  );
}

export default App;
