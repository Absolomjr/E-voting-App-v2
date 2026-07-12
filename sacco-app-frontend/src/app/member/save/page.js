"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

export default function SavePage() {
  const [amount, setAmount] = useState("");
  const [reference, setReference] = useState("");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState("");
  const [ok, setOk] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setOk("");
    setLoading(true);
    try {
      await api.post("/savings/transactions/", {
        amount,
        reference,
        notes,
      });
      setOk("Saving submitted. It stays pending until the treasurer confirms.");
      setAmount("");
      setReference("");
      setNotes("");
      setTimeout(() => router.push("/member"), 1200);
    } catch (err) {
      setError(err?.data?.detail || "Could not submit saving.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Record saving</h1>
          <p className="subtitle">Submissions require treasurer confirmation</p>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {ok && <div className="alert alert-success">{ok}</div>}

      <div className="card">
        <div className="card-body">
          <form onSubmit={onSubmit}>
            <div className="form-group">
              <label className="form-label">Amount</label>
              <input
                className="form-input"
                type="number"
                min="1"
                step="0.01"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
                inputMode="decimal"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Payment reference</label>
              <input
                className="form-input"
                value={reference}
                onChange={(e) => setReference(e.target.value)}
                placeholder="Mobile money / bank ref"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Notes</label>
              <textarea
                className="form-textarea"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
              />
            </div>
            <button className="btn btn-primary btn-block btn-lg" disabled={loading}>
              {loading ? "Submitting…" : "Submit for verification"}
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
