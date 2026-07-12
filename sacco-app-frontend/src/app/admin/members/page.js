"use client";
import { useCallback, useEffect, useState } from "react";
import { api, formatMoney } from "@/lib/api";
import Modal from "@/components/Modal";

const EMPTY = {
  full_name: "",
  email: "",
  password: "",
  national_id: "",
  phone: "",
  address: "",
};

export default function MembersPage() {
  const [members, setMembers] = useState([]);
  const [error, setError] = useState("");
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState(EMPTY);
  const [busy, setBusy] = useState(false);

  const load = useCallback(() => {
    const query = q ? `?q=${encodeURIComponent(q)}` : "";
    api
      .get(`/accounts/members/${query}`)
      .then(setMembers)
      .catch((err) => setError(err?.data?.detail || "Failed to load members."));
  }, [q]);

  useEffect(() => {
    load();
  }, [load]);

  async function createMember(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      await api.post("/accounts/members/", form);
      setOpen(false);
      setForm(EMPTY);
      load();
    } catch (err) {
      setError(err?.data?.detail || "Could not create member.");
    } finally {
      setBusy(false);
    }
  }

  async function verify(id) {
    try {
      await api.post(`/accounts/members/${id}/verify/`, {});
      load();
    } catch (err) {
      setError(err?.data?.detail || "Verify failed.");
    }
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Members</h1>
          <p className="subtitle">Onboard, verify, and manage membership</p>
        </div>
        <button type="button" className="btn btn-primary" onClick={() => setOpen(true)}>
          Add member
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="card" style={{ marginBottom: "1rem" }}>
        <div className="card-body" style={{ display: "flex", gap: "0.75rem" }}>
          <input
            className="form-input"
            placeholder="Search name, number, phone…"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
        </div>
      </div>

      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Number</th>
                <th>Balance</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {members.map((m) => (
                <tr key={m.id}>
                  <td>
                    <div style={{ fontWeight: 600 }}>{m.full_name}</div>
                    <div style={{ fontSize: "0.8rem", color: "var(--gray-500)" }}>{m.phone}</div>
                  </td>
                  <td>{m.member_number}</td>
                  <td>{formatMoney(m.balance)}</td>
                  <td>
                    {!m.is_active ? (
                      <span className="badge badge-danger">Inactive</span>
                    ) : m.is_verified ? (
                      <span className="badge badge-success">Verified</span>
                    ) : (
                      <span className="badge badge-warning">Pending</span>
                    )}
                  </td>
                  <td>
                    {!m.is_verified && m.is_active && (
                      <button type="button" className="btn btn-success btn-sm" onClick={() => verify(m.id)}>
                        Verify
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {open && (
        <Modal
          title="Add member"
          onClose={() => setOpen(false)}
          footer={
            <>
              <button type="button" className="btn btn-outline" onClick={() => setOpen(false)}>Cancel</button>
              <button type="submit" form="create-member" className="btn btn-primary" disabled={busy}>
                {busy ? "Saving…" : "Create"}
              </button>
            </>
          }
        >
          <form id="create-member" onSubmit={createMember}>
            {Object.entries({
              full_name: "Full name",
              email: "Email",
              national_id: "National ID",
              phone: "Phone",
              password: "Temp password",
              address: "Address",
            }).map(([name, label]) => (
              <div className="form-group" key={name}>
                <label className="form-label">{label}</label>
                {name === "address" ? (
                  <textarea
                    className="form-textarea"
                    name={name}
                    value={form[name]}
                    onChange={(e) => setForm((f) => ({ ...f, [name]: e.target.value }))}
                  />
                ) : (
                  <input
                    className="form-input"
                    type={name === "password" ? "password" : name === "email" ? "email" : "text"}
                    name={name}
                    value={form[name]}
                    onChange={(e) => setForm((f) => ({ ...f, [name]: e.target.value }))}
                    required={name !== "address"}
                  />
                )}
              </div>
            ))}
          </form>
        </Modal>
      )}
    </>
  );
}
