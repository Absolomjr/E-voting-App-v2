"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { api, formatMoney, statusBadge } from "@/lib/api";

export default function MemberHome() {
  const [summary, setSummary] = useState(null);
  const [txns, setTxns] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api.get("/savings/me/"),
      api.get("/savings/transactions/"),
    ])
      .then(([me, list]) => {
        setSummary(me);
        setTxns(list.slice(0, 5));
      })
      .catch(() => setError("Could not load your savings."));
  }, []);

  return (
    <>
      {error && <div className="alert alert-error">{error}</div>}

      {summary && (
        <div className="balance-hero">
          <div className="label">Your share balance</div>
          <div className="amount">{formatMoney(summary.balance)}</div>
          <div className="meta">
            {summary.total_shares} shares · {summary.pending_count} pending
          </div>
        </div>
      )}

      <Link href="/member/save" className="btn btn-primary btn-block btn-lg" style={{ marginBottom: "1.25rem" }}>
        Record a saving
      </Link>

      <div className="card">
        <div className="card-header">
          <h3>Recent activity</h3>
          <Link href="/member/history" style={{ fontSize: "0.85rem", fontWeight: 600 }}>
            See all
          </Link>
        </div>
        <div className="card-body">
          {!txns.length ? (
            <div className="empty-state" style={{ padding: "1.5rem" }}>
              <p>No transactions yet. Record your first saving.</p>
            </div>
          ) : (
            txns.map((t) => (
              <div className="txn-row" key={t.id}>
                <div>
                  <div className="txn-title">{t.transaction_type}</div>
                  <div className="txn-meta">
                    {new Date(t.created_at).toLocaleDateString()} ·{" "}
                    <span className={`badge ${statusBadge(t.status)}`}>{t.status}</span>
                  </div>
                </div>
                <div className="txn-amount">{formatMoney(t.amount)}</div>
              </div>
            ))
          )}
        </div>
      </div>
    </>
  );
}
