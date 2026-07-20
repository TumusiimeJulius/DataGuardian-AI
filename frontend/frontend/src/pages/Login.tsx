import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { FaShieldAlt, FaEnvelope, FaLock, FaGoogle, FaEye, FaEyeSlash } from "react-icons/fa";
import { authService } from "../services/auth";

declare global {
  interface Window {
    google?: any;
  }
}

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  
  const navigate = useNavigate();

  // Load Google Identity Services SDK
  useEffect(() => {
    const scriptId = "google-gsi-client";
    let script = document.getElementById(scriptId) as HTMLScriptElement;
    
    const initializeGoogle = () => {
      if (window.google) {
        const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
        
        if (clientId) {
          try {
            window.google.accounts.id.initialize({
              client_id: clientId,
              callback: handleGoogleCredentialResponse,
              auto_select: false,
              cancel_on_tap_outside: true
            });
            
            // Render the official Google Button if client ID is set
            const btnContainer = document.getElementById("google-official-btn");
            if (btnContainer) {
              window.google.accounts.id.renderButton(
                btnContainer,
                { 
                  theme: "filled_blue", 
                  size: "large", 
                  text: "continue_with",
                  shape: "rectangular",
                  width: 320 
                }
              );
            }
          } catch (err) {
            console.error("Error initializing Google GIS", err);
          }
        }
      }
    };

    if (!script) {
      script = document.createElement("script");
      script.src = "https://accounts.google.com/gsi/client";
      script.id = scriptId;
      script.async = true;
      script.defer = true;
      script.onload = initializeGoogle;
      document.body.appendChild(script);
    } else if (window.google) {
      initializeGoogle();
    }

    return () => {
      // Clean up script listeners if any, but keep script loaded
    };
  }, []);

  const handleGoogleCredentialResponse = async (response: any) => {
    if (!response.credential) return;
    setGoogleLoading(true);
    setError("");
    try {
      const data = await authService.googleLogin(response.credential);
      if (data.token) {
        localStorage.setItem("dg_auth_token", data.token);
        setSuccess("Successfully authenticated!");
        setTimeout(() => {
          navigate("/");
          window.location.reload(); // Ensure all contexts reload auth state
        }, 800);
      } else {
        setError("Failed to verify Google account credentials.");
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Google Login connection failed.");
    } finally {
      setGoogleLoading(false);
    }
  };

  const handleSimulatedGoogleLogin = async () => {
    setGoogleLoading(true);
    setError("");
    try {
      // Send a simulated token to backend
      const data = await authService.googleLogin("simulated_google_credential_token");
      if (data.token) {
        localStorage.setItem("dg_auth_token", data.token);
        setSuccess("Simulated Google login successful!");
        setTimeout(() => {
          navigate("/");
          window.location.reload();
        }, 800);
      } else {
        setError("Simulated authentication failed.");
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Connection to authorization server failed.");
    } finally {
      setGoogleLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setError("Please fill in all fields.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const data = await authService.login(email, password);
      if (data.token) {
        localStorage.setItem("dg_auth_token", data.token);
        setSuccess("Welcome back to DataGuardian!");
        setTimeout(() => {
          navigate("/");
          window.location.reload();
        }, 800);
      } else {
        setError("Authentication failed.");
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Invalid email or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        background: "radial-gradient(circle at center, #0f172a 0%, #020617 100%)",
        fontFamily: "Segoe UI, sans-serif",
        padding: "20px",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Background Graphic Accents */}
      <div
        style={{
          position: "absolute",
          width: "500px",
          height: "500px",
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(37, 99, 235, 0.15) 0%, rgba(37, 99, 235, 0) 70%)",
          top: "-10%",
          right: "-10%",
          zIndex: 1,
        }}
      />
      <div
        style={{
          position: "absolute",
          width: "600px",
          height: "600px",
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0) 70%)",
          bottom: "-15%",
          left: "-15%",
          zIndex: 1,
        }}
      />

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        style={{
          width: "100%",
          maxWidth: "460px",
          background: "rgba(15, 23, 42, 0.65)",
          backdropFilter: "blur(20px)",
          border: "1px solid rgba(255, 255, 255, 0.08)",
          borderRadius: "24px",
          padding: "45px 40px",
          boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.5)",
          zIndex: 10,
          color: "white",
        }}
      >
        {/* LOGO */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            marginBottom: "35px",
          }}
        >
          <div
            style={{
              background: "#22c55e",
              padding: "16px",
              borderRadius: "18px",
              boxShadow: "0 0 30px rgba(34, 197, 94, 0.35)",
              display: "inline-flex",
              marginBottom: "15px",
            }}
          >
            <FaShieldAlt size={32} color="white" />
          </div>
          <h1
            style={{
              fontSize: "26px",
              fontWeight: "800",
              margin: "0 0 5px 0",
              background: "linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}
          >
            DataGuardian AI
          </h1>
          <p style={{ color: "#94a3b8", fontSize: "14px", margin: 0 }}>
            Enter details to access the AI Operations Center
          </p>
        </div>

        {/* ALERTS */}
        {error && (
          <div
            style={{
              background: "rgba(239, 68, 68, 0.15)",
              border: "1px solid rgba(239, 68, 68, 0.3)",
              color: "#f87171",
              padding: "12px 16px",
              borderRadius: "12px",
              fontSize: "14px",
              marginBottom: "20px",
              display: "flex",
              alignItems: "center",
            }}
          >
            {error}
          </div>
        )}
        {success && (
          <div
            style={{
              background: "rgba(34, 197, 94, 0.15)",
              border: "1px solid rgba(34, 197, 94, 0.3)",
              color: "#4ade80",
              padding: "12px 16px",
              borderRadius: "12px",
              fontSize: "14px",
              marginBottom: "20px",
              display: "flex",
              alignItems: "center",
            }}
          >
            {success}
          </div>
        )}

        {/* LOGIN FORM */}
        <form onSubmit={handleSubmit}>
          {/* Email */}
          <div style={{ marginBottom: "20px" }}>
            <label
              style={{
                display: "block",
                fontSize: "13px",
                fontWeight: "600",
                color: "#94a3b8",
                marginBottom: "8px",
                textTransform: "uppercase",
                letterSpacing: "0.5px",
              }}
            >
              Email Address
            </label>
            <div style={{ position: "relative" }}>
              <div
                style={{
                  position: "absolute",
                  left: "14px",
                  top: "50%",
                  transform: "translateY(-50%)",
                  color: "#64748b",
                  display: "flex",
                }}
              >
                <FaEnvelope size={16} />
              </div>
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={{
                  width: "100%",
                  padding: "14px 14px 14px 44px",
                  background: "rgba(30, 41, 59, 0.5)",
                  border: "1px solid rgba(255, 255, 255, 0.1)",
                  borderRadius: "12px",
                  color: "white",
                  fontSize: "15px",
                  outline: "none",
                  transition: "all 0.3s ease",
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = "#2563eb";
                  e.target.style.boxShadow = "0 0 10px rgba(37, 99, 235, 0.25)";
                  e.target.style.background = "rgba(30, 41, 59, 0.7)";
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = "rgba(255, 255, 255, 0.1)";
                  e.target.style.boxShadow = "none";
                  e.target.style.background = "rgba(30, 41, 59, 0.5)";
                }}
              />
            </div>
          </div>

          {/* Password */}
          <div style={{ marginBottom: "25px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
              <label
                style={{
                  fontSize: "13px",
                  fontWeight: "600",
                  color: "#94a3b8",
                  textTransform: "uppercase",
                  letterSpacing: "0.5px",
                  margin: 0
                }}
              >
                Password
              </label>
              <Link
                to="/forgot-password"
                style={{
                  fontSize: "13px",
                  color: "#3b82f6",
                  textDecoration: "none",
                  fontWeight: "500",
                  transition: "color 0.2s"
                }}
                onMouseEnter={(e) => (e.currentTarget.style.color = "#60a5fa")}
                onMouseLeave={(e) => (e.currentTarget.style.color = "#3b82f6")}
              >
                Forgot Password?
              </Link>
            </div>
            <div style={{ position: "relative" }}>
              <div
                style={{
                  position: "absolute",
                  left: "14px",
                  top: "50%",
                  transform: "translateY(-50%)",
                  color: "#64748b",
                  display: "flex",
                }}
              >
                <FaLock size={16} />
              </div>
              <input
                type={showPassword ? "text" : "password"}
                placeholder="••••••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{
                  width: "100%",
                  padding: "14px 44px 14px 44px",
                  background: "rgba(30, 41, 59, 0.5)",
                  border: "1px solid rgba(255, 255, 255, 0.1)",
                  borderRadius: "12px",
                  color: "white",
                  fontSize: "15px",
                  outline: "none",
                  transition: "all 0.3s ease",
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = "#2563eb";
                  e.target.style.boxShadow = "0 0 10px rgba(37, 99, 235, 0.25)";
                  e.target.style.background = "rgba(30, 41, 59, 0.7)";
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = "rgba(255, 255, 255, 0.1)";
                  e.target.style.boxShadow = "none";
                  e.target.style.background = "rgba(30, 41, 59, 0.5)";
                }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: "absolute",
                  right: "14px",
                  top: "50%",
                  transform: "translateY(-50%)",
                  background: "none",
                  border: "none",
                  color: "#64748b",
                  cursor: "pointer",
                  display: "flex",
                  padding: 0,
                }}
              >
                {showPassword ? <FaEyeSlash size={16} /> : <FaEye size={16} />}
              </button>
            </div>
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "14px",
              background: "linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%)",
              border: "none",
              borderRadius: "12px",
              color: "white",
              fontSize: "15px",
              fontWeight: "600",
              cursor: "pointer",
              boxShadow: "0 4px 15px rgba(37, 99, 235, 0.4)",
              transition: "all 0.3s ease",
              marginBottom: "25px",
            }}
            onMouseEnter={(e) => {
              if (!loading) {
                e.currentTarget.style.transform = "translateY(-2px)";
                e.currentTarget.style.boxShadow = "0 6px 20px rgba(37, 99, 235, 0.55)";
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow = "0 4px 15px rgba(37, 99, 235, 0.4)";
            }}
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        {/* Divider */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            color: "#64748b",
            fontSize: "12px",
            textTransform: "uppercase",
            letterSpacing: "0.5px",
            margin: "0 0 25px 0",
          }}
        >
          <div style={{ flex: 1, height: "1px", background: "rgba(255,255,255,0.06)" }} />
          <span style={{ padding: "0 15px" }}>Or Continue With</span>
          <div style={{ flex: 1, height: "1px", background: "rgba(255,255,255,0.06)" }} />
        </div>

        {/* Google Buttons Container */}
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: "100%" }}>
          {/* Dynamic Google Login Button (if client-id configured) */}
          {import.meta.env.VITE_GOOGLE_CLIENT_ID ? (
            <div
              id="google-official-btn"
              style={{
                width: "100%",
                display: "flex",
                justifyContent: "center",
                minHeight: "45px",
                opacity: googleLoading ? 0.6 : 1,
                pointerEvents: googleLoading ? "none" : "auto",
              }}
            />
          ) : (
            /* Premium simulated button (if client-id not configured) */
            <button
              onClick={handleSimulatedGoogleLogin}
              disabled={googleLoading}
              style={{
                width: "100%",
                padding: "12px",
                background: "rgba(255, 255, 255, 0.08)",
                border: "1px solid rgba(255, 255, 255, 0.12)",
                borderRadius: "12px",
                color: "white",
                fontSize: "14px",
                fontWeight: "600",
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: "10px",
                transition: "all 0.3s ease",
              }}
              onMouseEnter={(e) => {
                if (!googleLoading) {
                  e.currentTarget.style.background = "rgba(255, 255, 255, 0.15)";
                  e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.2)";
                }
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "rgba(255, 255, 255, 0.08)";
                e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.12)";
              }}
            >
              <FaGoogle color="#ea4335" size={18} />
              <span>{googleLoading ? "Connecting Google..." : "Continue with Google (Demo)"}</span>
            </button>
          )}

          {!import.meta.env.VITE_GOOGLE_CLIENT_ID && (
            <p
              style={{
                fontSize: "11px",
                color: "#64748b",
                textAlign: "center",
                marginTop: "8px",
                marginRight: 0,
                marginLeft: 0,
                marginBottom: 0,
              }}
            >
              ⚙️ running Google OAuth in simulated sandbox mode.
            </p>
          )}
        </div>

        {/* Redirection Links */}
        <div
          style={{
            textAlign: "center",
            marginTop: "30px",
            fontSize: "14px",
            color: "#94a3b8",
          }}
        >
          Don't have an account?{" "}
          <Link
            to="/signup"
            style={{
              color: "#3b82f6",
              fontWeight: "600",
              textDecoration: "none",
              transition: "color 0.2s",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.color = "#60a5fa")}
            onMouseLeave={(e) => (e.currentTarget.style.color = "#3b82f6")}
          >
            Create an Account
          </Link>
        </div>
      </motion.div>
    </div>
  );
}
