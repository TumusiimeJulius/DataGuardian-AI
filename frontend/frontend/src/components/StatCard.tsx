import { ReactNode } from "react";

interface Props {
  title: string;
  value: string | number;
  icon: ReactNode;
  color?: string;
  subtitle?: string;
}

export default function StatCard({
  title,
  value,
  icon,
  color = "#3b82f6",
  subtitle,
}: Props) {
  return (
    <div
      style={{
        background: "#1e293b",
        color: "white",
        borderRadius: 16,
        padding: 25,
        minHeight: 150,
        border: "1px solid #334155",
        boxShadow: "0 0 20px rgba(0,0,0,.35)",
        transition: "0.3s ease",
      }}
    >

      {/* ICON */}

      <div
        style={{
          width: 55,
          height: 55,
          borderRadius: 12,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: `${color}22`,
          color: color,
          fontSize: 30,
          marginBottom: 20,
        }}
      >
        {icon}
      </div>


      {/* TITLE */}

      <h4
        style={{
          color: "#94a3b8",
          fontSize: 15,
          margin: 0,
          marginBottom: 8,
        }}
      >
        {title}
      </h4>


      {/* VALUE */}

      <h2
        style={{
          margin: 0,
          fontSize: 30,
          fontWeight: "bold",
        }}
      >
        {value}
      </h2>


      {/* OPTIONAL DESCRIPTION */}

      {subtitle && (
        <p
          style={{
            color: "#64748b",
            marginTop: 10,
            fontSize: 13,
          }}
        >
          {subtitle}
        </p>
      )}

    </div>
  );
}