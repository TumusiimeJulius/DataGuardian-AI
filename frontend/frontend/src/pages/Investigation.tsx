import { useState } from "react";
import api from "../services/api";
import {
  FaSearch,
  FaCheckCircle,
  FaExclamationTriangle,
  FaTools,
  FaHeartbeat,
  FaClock,
  FaProjectDiagram,
  FaRobot,
} from "react-icons/fa";

export default function Investigation() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const investigate = async () => {
    if (!question.trim()) return;

    setLoading(true);

    try {
      const res = await api.get("/investigate", {
        params: { question },
      });

      // Map backend response structure to the nested layout expected by the frontend
      const mappedData = {
        ...res.data,
        execution_time: res.data.execution_time_seconds,
        health: {
          pipeline: res.data.pipeline_report || { status: "UNKNOWN", health_score: 0 },
          anomaly: res.data.anomaly_report || { anomaly_score: 0, anomalies: [] },
          repair: res.data.repair_report || { status: "UNKNOWN", repair_actions: [], root_cause_reference: null, quality_before: null }
        }
      };

      setResult(mappedData);
    } catch (err) {
      console.error(err);
      alert("Investigation failed");
    }

    setLoading(false);
  };

  return (
    <div
      style={{
        background: "#0f172a",
        color: "white",
        minHeight: "100vh",
        padding: 35,
        fontFamily: "Arial",
      }}
    >
      <h1>🔍 DataGuardian AI Investigation Center</h1>

      <p>
        Ask questions about your datasets, ETL pipelines, dashboards and AI
        systems.
      </p>

      <div
        style={{
          display: "flex",
          gap: 12,
          marginTop: 25,
        }}
      >
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Why is my sales dashboard showing wrong revenue?"
          style={{
            flex: 1,
            padding: 15,
            borderRadius: 8,
            border: "none",
            fontSize: 16,
          }}
        />

        <button
          onClick={investigate}
          style={{
            background: "#2563eb",
            color: "white",
            border: "none",
            padding: "15px 30px",
            borderRadius: 8,
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          <FaSearch /> Investigate
        </button>
      </div>

      {loading && (
        <div
          style={{
            marginTop: 30,
            fontSize: 22,
          }}
        >
          🤖 AI Agents are investigating...
        </div>
      )}

      {result && (
        <>
          {/* SUMMARY CARDS */}

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(4,1fr)",
              gap: 20,
              marginTop: 35,
            }}
          >
            <Card
              title="Status"
              value={result.status}
              icon={<FaCheckCircle />}
              color="#22c55e"
            />

            <Card
              title="Execution Time"
              value={`${result.execution_time} sec`}
              icon={<FaClock />}
              color="#3b82f6"
            />

            <Card
              title="Pipeline Health"
              value={result.health.pipeline.status}
              icon={<FaProjectDiagram />}
              color="#f59e0b"
            />

            <Card
              title="Repair Status"
              value={result.health.repair.status}
              icon={<FaTools />}
              color="#8b5cf6"
            />
          </div>

          {/* HEALTH */}

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: 20,
              marginTop: 30,
            }}
          >
            <Panel title="Pipeline">
              <h2>{result.health.pipeline.status}</h2>

              <p>
                Health Score:{" "}
                {result.health.pipeline.health_score}
              </p>
            </Panel>

            <Panel title="Anomaly Detection">
              <h2>{result.health.anomaly.anomaly_score}</h2>

              <p>Anomaly Score</p>
            </Panel>
          </div>

          {/* ANOMALIES */}

          <Panel title="Detected Anomalies">
            {result.health.anomaly.anomalies.map(
              (a: any, i: number) => (
                <div
                  key={i}
                  style={{
                    padding: 12,
                    marginBottom: 10,
                    background: "#0f172a",
                    borderRadius: 8,
                  }}
                >
                  <FaExclamationTriangle color="orange" />{" "}
                  <b>{a.type}</b>

                  <br />

                  Severity: {a.severity}
                </div>
              )
            )}
          </Panel>

          {/* REPAIRS */}

          <Panel title="Automatic Repairs">
            {result.health.repair.repair_actions.map(
              (r: any, i: number) => (
                <div
                  key={i}
                  style={{
                    padding: 12,
                    marginBottom: 10,
                    background: "#0f172a",
                    borderRadius: 8,
                  }}
                >
                  ✅ <b>{r.issue}</b>

                  <br />

                  Action: {r.action}
                </div>
              )
            )}
          </Panel>

          {/* ROOT CAUSES */}

          {result.health.repair.root_cause_reference && (
            <Panel title="Root Cause Analysis">
              {result.health.repair.root_cause_reference.root_causes.map(
                (r: any, i: number) => (
                  <div
                    key={i}
                    style={{
                      marginBottom: 20,
                    }}
                  >
                    <b>{r.problem}</b>

                    <br />

                    Cause: {r.possible_cause}

                    <br />

                    Confidence: {r.confidence}
                  </div>
                )
              )}
            </Panel>
          )}

          {/* QUALITY */}

          <Panel title="Quality Report">
            <pre
              style={{
                whiteSpace: "pre-wrap",
              }}
            >
              {JSON.stringify(
                result.health.repair.quality_before,
                null,
                2
              )}
            </pre>
          </Panel>

          {/* AI REPORT */}

          {result.report && (
            <Panel title="🤖 AI Explanation">
              <div
                style={{
                  whiteSpace: "pre-wrap",
                  lineHeight: 1.8,
                }}
              >
                {typeof result.report === "string"
                  ? result.report
                  : JSON.stringify(result.report, null, 2)}
              </div>
            </Panel>
          )}

          {/* AGENTS */}

          <h2 style={{ marginTop: 40 }}>
            AI Agents Used
          </h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(5,1fr)",
              gap: 20,
            }}
          >
            <Agent name="Investigator" />
            <Agent name="Pipeline" />
            <Agent name="Repair" />
            <Agent name="Anomaly" />
            <Agent name="Decision" />
          </div>
        </>
      )}
    </div>
  );
}

function Card({
  title,
  value,
  icon,
  color,
}: any) {
  return (
    <div
      style={{
        background: "#1e293b",
        padding: 20,
        borderRadius: 12,
      }}
    >
      <div
        style={{
          color,
          fontSize: 28,
        }}
      >
        {icon}
      </div>

      <h3>{title}</h3>

      <h2>{value}</h2>
    </div>
  );
}

function Panel({
  title,
  children,
}: any) {
  return (
    <div
      style={{
        background: "#1e293b",
        marginTop: 25,
        padding: 20,
        borderRadius: 12,
      }}
    >
      <h2>{title}</h2>

      <hr />

      {children}
    </div>
  );
}

function Agent({
  name,
}: any) {
  return (
    <div
      style={{
        background: "#1e293b",
        padding: 20,
        borderRadius: 12,
        textAlign: "center",
      }}
    >
      <FaRobot
        size={35}
        color="#22c55e"
      />

      <h3>{name}</h3>

      <p>
        <FaHeartbeat color="#22c55e" /> Running
      </p>
    </div>
  );
}