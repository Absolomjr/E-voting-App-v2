"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { api, formatMoney } from "@/lib/api";

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/savings/dashboard/")
      .then(setStats)
      .catch(() => setError("Could not load dashboard."));
  }, []);

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p className="subtitle">SACCO pool health and pending work</p>
        </div>
        <Link href="/admin/verify" className="btn btn-primary">
          Review pending
        </Link>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {stats && (
        <div className="grid-stats">
          <div className="stat-card">
            <div className="stat-value">{formatMoney(stats.total_pool)}</div>
            <div className="stat-label">Total pool</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.pending_transactions}</div>
            <div className="stat-label">Pending verify</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.members_verified}</div>
            <div className="stat-label">Active members</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.members_pending}</div>
            <div className="stat-label">Awaiting verify</div>
          </div>
        </div>
      )}

      <div className="card">
        <div className="card-body">
          <h3 style={{ marginBottom: "0.5rem" }}>Quick actions</h3>
          <p style={{ color: "var(--gray-500)", marginBottom: "1rem", fontSize: "0.9rem" }}>
            Treasurers confirm member deposits. Secretaries manage membership. Admins govern roles and audit.
          </p>
          <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
            <Link href="/admin/verify" className="btn btn-primary btn-sm">Verify deposits</Link>
            <Link href="/admin/members" className="btn btn-outline btn-sm">Manage members</Link>
            <Link href="/admin/accounts" className="btn btn-outline btn-sm">View accounts</Link>
          </div>
        </div>
      </div>
    </>
  );
}
