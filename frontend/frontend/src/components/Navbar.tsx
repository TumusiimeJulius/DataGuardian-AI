export default function Navbar() {
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
      }}
    >
      <h2>AI Operations Center</h2>

      <div>
        🟢 System Online
      </div>
    </div>
  );
}