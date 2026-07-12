"use client";
import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";
import Modal from "@/components/Modal";

const EMPTY = {
  full_name: "",
  username: "",
  email: "",
  password: "",
  role: "treasurer",
};

export default function StaffPage() {
  const [staff, setStaff] = useState([]);
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState(EMPTY);
  const [busy, setBusy] = useState(false);

  const load = useCallback(() => {
    api
      .get("/accounts/staff/")
      .then(setStaff)
      .catch((err) => setError(err?.data?.detail || "Failed to load staff."));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  async function onCreate(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      await api.post("/accounts/staff/", form);
      setOpen(false);
      setForm(EMPTY);
      load();
    } catch (err) {
      setError(err?.data?.detail || "Could not create staff.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Staff</h1>
          <p className="subtitle">Admins, treasurers, and secretaries</p>
        </div>
        <button type="button" className="btn btn-primary" onClick={() => setOpen(true)}>
          Add staff
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Username</th>
                <th>Role</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {staff.map((s) => (
                <tr key={s.id}>
                  <td>{s.full_name}</td>
                  <td>{s.username}</td>
                  <td>{s.role.replace("_", " ")}</td>
                  <td>
                    {s.is_active ? (
                      <span className="badge badge-success">Active</span>
                    ) : (
                      <span className="badge badge-danger">Inactive</span>
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
          title="Add staff user"
          onClose={() => setOpen(false)}
          footer={
            <>
              <button type="button" className="btn btn-outline" onClick={() => setOpen(false)}>Cancel</button>
              <button type="submit" form="create-staff" className="btn btn-primary" disabled={busy}>
                {busy ? "Saving…" : "Create"}
              </button>
            </>
          }
        >
          <form id="create-staff" onSubmit={onCreate}>
            {["full_name", "username", "email", "password"].map((name) => (
              <div className="form-group" key={name}>
                <label className="form-label">{name.replace("_", " ")}</label>
                <input
                  className="form-input"
                  type={name === "password" ? "password" : name === "email" ? "email" : "text"}
                  value={form[name]}
                  onChange={(e) => setForm((f) => ({ ...f, [name]: e.target.value }))}
                  required
                />
              </div>
            ))}
            <div className="form-group">
              <label className="form-label">Role</label>
              <select
                className="form-select"
                value={form.role}
                onChange={(e) => setForm((f) => ({ ...f, role: e.target.value }))}
              >
                <option value="treasurer">Treasurer</option>
                <option value="secretary">Secretary</option>
                <option value="super_admin">Super admin</option>
              </select>
            </div>
          </form>
        </Modal>
      )}
    </>
  );
}
