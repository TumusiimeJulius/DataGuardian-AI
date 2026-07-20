import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Investigation from "./pages/Investigation";
import Agents from "./pages/Agents";
import Analytics from "./pages/Analytics";
import Settings from "./pages/Settings";
import Upload from "./pages/Upload";
import History from "./pages/History";
import CleanDatasets from "./pages/CleanDatasets";
import Reports from "./pages/Reports";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import ForgotPassword from "./pages/ForgotPassword";
import { authService } from "./services/auth";

// ProtectedRoute Wrapper Component
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem("dg_auth_token");
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    async function verify() {
      if (!token) {
        setLoading(false);
        setAuthenticated(false);
        return;
      }
      try {
        const response = await authService.getMe();
        if (response.status === "success" && response.user) {
          localStorage.setItem("dg_user", JSON.stringify(response.user));
          setAuthenticated(true);
        } else {
          localStorage.removeItem("dg_auth_token");
          localStorage.removeItem("dg_user");
          setAuthenticated(false);
        }
      } catch (e: any) {
        console.error("Auth verification failed:", e);
        const status = e.response?.status;
        // Only clear credentials if we get an explicit unauthorized code (401/403)
        if (status === 401 || status === 403) {
          localStorage.removeItem("dg_auth_token");
          localStorage.removeItem("dg_user");
          setAuthenticated(false);
        } else {
          // If server is offline/timeout, allow cached session access to preserve demo state
          const cachedUser = localStorage.getItem("dg_user");
          if (cachedUser) {
            setAuthenticated(true);
          } else {
            setAuthenticated(false);
          }
        }
      } finally {
        setLoading(false);
      }
    }
    verify();
  }, [token]);

  if (loading) {
    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "100vh",
          background: "#0f172a",
          color: "white",
          fontFamily: "Segoe UI, sans-serif",
        }}
      >
        <div style={{ textAlign: "center" }}>
          <h2>Loading DataGuardian AI...</h2>
          <p style={{ color: "#64748b" }}>Synchronizing secure session credentials</p>
        </div>
      </div>
    );
  }

  if (!authenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

// Public Route Guard (Redirects logged-in users away from /login and /signup)
function PublicRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem("dg_auth_token");
  if (token) {
    return <Navigate to="/" replace />;
  }
  return <>{children}</>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* PUBLIC ROUTES */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />
        <Route
          path="/signup"
          element={
            <PublicRoute>
              <Signup />
            </PublicRoute>
          }
        />
        <Route
          path="/forgot-password"
          element={
            <PublicRoute>
              <ForgotPassword />
            </PublicRoute>
          }
        />

        {/* PROTECTED ROUTES */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/upload"
          element={
            <ProtectedRoute>
              <Upload />
            </ProtectedRoute>
          }
        />
        <Route
          path="/investigation"
          element={
            <ProtectedRoute>
              <Investigation />
            </ProtectedRoute>
          }
        />
        <Route
          path="/agents"
          element={
            <ProtectedRoute>
              <Agents />
            </ProtectedRoute>
          }
        />
        <Route
          path="/history"
          element={
            <ProtectedRoute>
              <History />
            </ProtectedRoute>
          }
        />
        <Route
          path="/clean"
          element={
            <ProtectedRoute>
              <CleanDatasets />
            </ProtectedRoute>
          }
        />
        <Route
          path="/reports"
          element={
            <ProtectedRoute>
              <Reports />
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
          path="/settings"
          element={
            <ProtectedRoute>
              <Settings />
            </ProtectedRoute>
          }
        />

        {/* FALLBACK */}
        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}