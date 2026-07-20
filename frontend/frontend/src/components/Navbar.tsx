import { useState, useEffect } from "react";
import { authService } from "../services/auth";
import type { User } from "../services/auth";
import { FaUserCircle, FaSignOutAlt, FaChevronDown } from "react-icons/fa";

export default function Navbar() {
  const [user, setUser] = useState<User | null>(null);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  useEffect(() => {
    try {
      const cached = localStorage.getItem("dg_user");
      if (cached) {
        setUser(JSON.parse(cached));
      }
    } catch (e) {
      console.error("Failed to read user from cache", e);
    }
  }, []);

  const handleLogout = async () => {
    await authService.logout();
    window.location.href = "/login";
  };

  return (
    <div
      style={{
        height: 70,
        background: "#111827",
        color: "white",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "0 30px",
        borderBottom: "1px solid #374151",
        position: "relative",
        zIndex: 999,
      }}
    >
      <h2>AI Operations Center</h2>

      <div style={{ display: "flex", alignItems: "center", gap: "20px" }}>
        <div style={{ color: "#22c55e", fontSize: "14px", fontWeight: "600" }}>
          🟢 System Online
        </div>

        {user && (
          <div style={{ position: "relative" }}>
            <div
              onClick={() => setDropdownOpen(!dropdownOpen)}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                cursor: "pointer",
                padding: "6px 12px",
                borderRadius: "8px",
                background: "rgba(255, 255, 255, 0.05)",
                border: "1px solid rgba(255, 255, 255, 0.08)",
                transition: "all 0.2s",
                userSelect: "none"
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "rgba(255, 255, 255, 0.1)";
              }}
              onMouseLeave={(e) => {
                if (!dropdownOpen) {
                  e.currentTarget.style.background = "rgba(255, 255, 255, 0.05)";
                }
              }}
            >
              {user.profile_picture ? (
                <img
                  src={user.profile_picture}
                  alt="Profile"
                  style={{
                    width: "28px",
                    height: "28px",
                    borderRadius: "50%",
                    objectFit: "cover",
                    border: "1px solid rgba(255,255,255,0.2)"
                  }}
                />
              ) : (
                <FaUserCircle size={28} color="#94a3b8" />
              )}
              <span style={{ fontSize: "14px", fontWeight: "500" }}>{user.name}</span>
              <FaChevronDown
                size={12}
                color="#64748b"
                style={{
                  transform: dropdownOpen ? "rotate(180deg)" : "none",
                  transition: "0.2s"
                }}
              />
            </div>

            {dropdownOpen && (
              <>
                <div
                  onClick={() => setDropdownOpen(false)}
                  style={{
                    position: "fixed",
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    zIndex: 1000,
                  }}
                />
                <div
                  style={{
                    position: "absolute",
                    right: 0,
                    top: "45px",
                    background: "#1e293b",
                    border: "1px solid rgba(255,255,255,0.08)",
                    borderRadius: "12px",
                    width: "240px",
                    padding: "15px",
                    boxShadow: "0 10px 25px rgba(0,0,0,0.5)",
                    zIndex: 1001,
                    display: "flex",
                    flexDirection: "column",
                    gap: "12px",
                  }}
                >
                  <div>
                    <div style={{ fontWeight: "600", fontSize: "14px", color: "white" }}>
                      {user.name}
                    </div>
                    <div
                      style={{
                        fontSize: "12px",
                        color: "#94a3b8",
                        wordBreak: "break-all",
                        marginTop: "2px"
                      }}
                    >
                      {user.email}
                    </div>
                  </div>
                  <div style={{ height: "1px", background: "rgba(255,255,255,0.06)" }} />
                  <button
                    onClick={handleLogout}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "10px",
                      background: "none",
                      border: "none",
                      color: "#ef4444",
                      cursor: "pointer",
                      fontSize: "14px",
                      fontWeight: "600",
                      padding: "8px 0",
                      width: "100%",
                      textAlign: "left",
                    }}
                  >
                    <FaSignOutAlt size={16} />
                    Sign Out
                  </button>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}