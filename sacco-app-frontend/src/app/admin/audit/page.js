"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function AuditPage() {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/audit/logs/")
      .then(setLogs)
      .catch((err) => setError(err?.data?.detail || "Failed to load audit logs."));
  }, []);

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Audit log</h1>
          <p className="subtitle">Immutable trail of sensitive actions</p>
        </div>
      </div>
      {error && <div className="alert alert-error">{error}</div>}
      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Time</th>
                <th>Action</th>
                <th>User</th>
                <th>Details</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((l) => (
                <tr key={l.id}>
                  <td style={{ whiteSpace: "nowrap" }}>{new Date(l.timestamp).toLocaleString()}</td>
                  <td><span className="badge badge-info">{l.action}</span></td>
                  <td>{l.user_identifier}</td>
                  <td>{l.details}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {!logs.length && !error && (
          <div className="empty-state"><p>No audit events yet.</p></div>
        )}
      </div>
    </>
  );
}
