import './App.css';
import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/auth/Login';
import CEODashboard from './components/dashboard/CEODashboard';
import EmployerDashboard from './components/dashboard/EmployerDashboard';
import EmployeeDashboard from './components/dashboard/EmployeeDashboard';
import { AuthContext } from './context/AuthContext';

// PrivateRoute component to protect routes based on authentication and role
const PrivateRoute = ({ children, requiredRole }) => {
  const { isAuthenticated, getUserRole, getDashboardPath } = useContext(AuthContext);

  if (!isAuthenticated()) {
    // Redirect to login if the user is not authenticated
    return <Navigate to="/login" />;
  }

  const userRole = getUserRole();
  if (!userRole) {
    // If the role is missing, redirect to login for re-authentication
    return <Navigate to="/login" />
  }

  if (requiredRole && userRole !== requiredRole) {
    // Redirect to an unauthorized page or dashboard if the role does not match
    return <Navigate to={getDashboardPath(userRole)} />;
  }

  // Render the children if authenticated and role matches
  return children;
};

function App() {
  const { isAuthenticated, getUserRole, getDashboardPath } = useContext(AuthContext);
  const userRole = getUserRole();
  const dashboardPath = getDashboardPath(userRole);

  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Public Login Route */}
          <Route
            path="/login"
            element={isAuthenticated() ? <Navigate to={dashboardPath} /> : <Login />}
          />

          {/* Private Route for each dashboard based on role */}
          <Route
            path="/dashboard/ceo"
            element={
              <PrivateRoute requiredRole="CEO">
                <CEODashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/dashboard/employer"
            element={
              <PrivateRoute requiredRole="Employer">
                <EmployerDashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/dashboard/employee"
            element={
              <PrivateRoute requiredRole="Employee">
                <EmployeeDashboard />
              </PrivateRoute>
            }
          />
          {/* TODO: other routes */}

          {/* Redirect from default path to dashboard if authenticated, else login */}
          <Route path="/" element={<Navigate to={isAuthenticated() ? dashboardPath : "/login"} />} />
          {/* Catch-all route to redirect to login if no match is found */}
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
