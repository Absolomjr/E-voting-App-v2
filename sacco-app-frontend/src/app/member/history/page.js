"use client";
import { useEffect, useState } from "react";
import { api, formatMoney, statusBadge } from "@/lib/api";

export default function HistoryPage() {
  const [txns, setTxns] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/savings/transactions/")
      .then(setTxns)
      .catch(() => setError("Failed to load history."));
  }, []);

  return (
    <>
      <div className="page-header">
        <div>
          <h1>History</h1>
          <p className="subtitle">All of your savings activity</p>
        </div>
      </div>
      {error && <div className="alert alert-error">{error}</div>}
      <div className="card">
        <div className="card-body">
          {!txns.length ? (
            <div className="empty-state"><p>No transactions yet.</p></div>
          ) : (
            txns.map((t) => (
              <div className="txn-row" key={t.id}>
                <div>
                  <div className="txn-title">{t.transaction_type}</div>
                  <div className="txn-meta">
                    {new Date(t.created_at).toLocaleString()}
                    {t.reference ? ` · ${t.reference}` : ""}
                    {" · "}
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
