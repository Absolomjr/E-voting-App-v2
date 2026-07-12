"use client";
import { useCallback, useEffect, useState } from "react";
import { api, formatMoney } from "@/lib/api";

export default function VerifyPage() {
  const [txns, setTxns] = useState([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(null);

  const load = useCallback(() => {
    api
      .get("/savings/transactions/?status=pending")
      .then(setTxns)
      .catch((err) => setError(err?.data?.detail || "Failed to load queue."));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  async function verify(id) {
    setBusy(id);
    setError("");
    try {
      await api.post(`/savings/transactions/${id}/verify/`, {});
      load();
    } catch (err) {
      setError(err?.data?.detail || "Verify failed.");
    } finally {
      setBusy(null);
    }
  }

  async function reject(id) {
    const reason = window.prompt("Rejection reason (optional)") ?? "";
    setBusy(id);
    setError("");
    try {
      await api.post(`/savings/transactions/${id}/reject/`, { reason });
      load();
    } catch (err) {
      setError(err?.data?.detail || "Reject failed.");
    } finally {
      setBusy(null);
    }
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Verify savings</h1>
          <p className="subtitle">Treasurer queue — pending deposits</p>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="card">
        <div className="card-body" style={{ padding: 0 }}>
          {!txns.length ? (
            <div className="empty-state">
              <p>No pending transactions. You’re clear.</p>
            </div>
          ) : (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Member</th>
                    <th>Amount</th>
                    <th>Reference</th>
                    <th>Submitted</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {txns.map((t) => (
                    <tr key={t.id}>
                      <td>
                        <div style={{ fontWeight: 600 }}>{t.member_name}</div>
                        <div style={{ fontSize: "0.8rem", color: "var(--gray-500)" }}>{t.member_number}</div>
                      </td>
                      <td>{formatMoney(t.amount)}</td>
                      <td>{t.reference || "—"}</td>
                      <td>{new Date(t.created_at).toLocaleString()}</td>
                      <td>
                        <div style={{ display: "flex", gap: "0.4rem", flexWrap: "wrap" }}>
                          <button className="btn btn-success btn-sm" disabled={busy === t.id} onClick={() => verify(t.id)}>
                            Confirm
                          </button>
                          <button className="btn btn-outline btn-sm" disabled={busy === t.id} onClick={() => reject(t.id)}>
                            Reject
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

    </>
  );
}
