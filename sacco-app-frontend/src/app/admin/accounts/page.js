"use client";
import { useEffect, useState } from "react";
import { api, formatMoney } from "@/lib/api";

export default function AccountsPage() {
  const [accounts, setAccounts] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/savings/accounts/")
      .then(setAccounts)
      .catch(() => setError("Failed to load accounts."));
  }, []);

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Share accounts</h1>
          <p className="subtitle">Member balances across the pool</p>
        </div>
      </div>
      {error && <div className="alert alert-error">{error}</div>}
      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Member</th>
                <th>Number</th>
                <th>Balance</th>
                <th>Shares</th>
                <th>Updated</th>
              </tr>
            </thead>
            <tbody>
              {accounts.map((a) => (
                <tr key={a.id}>
                  <td>{a.member_name}</td>
                  <td>{a.member_number}</td>
                  <td>{formatMoney(a.balance)}</td>
                  <td>{a.total_shares}</td>
                  <td>{new Date(a.updated_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {!accounts.length && !error && (
          <div className="empty-state"><p>No accounts yet.</p></div>
        )}
      </div>
    </>
  );
}
