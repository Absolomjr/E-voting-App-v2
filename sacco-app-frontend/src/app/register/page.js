"use client";
import { useState } from "react";
import Link from "next/link";
import { registerMember } from "@/lib/api";

const INITIAL = {
  full_name: "",
  email: "",
  password: "",
  national_id: "",
  phone: "",
  address: "",
};

export default function RegisterPage() {
  const [form, setForm] = useState(INITIAL);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(null);
  const [loading, setLoading] = useState(false);

  const onChange = (e) => setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await registerMember(form);
      setSuccess(data);
      setForm(INITIAL);
    } catch (err) {
      const d = err?.data || err;
      setError(d?.detail || d?.email?.[0] || d?.national_id?.[0] || "Registration failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <div className="login-card" style={{ maxWidth: 480 }}>
        <div className="logo-area">
          <div className="brand-mark">S</div>
          <h1>Join the SACCO</h1>
          <p>Registration awaits staff verification.</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}
        {success && (
          <div className="alert alert-success">
            {success.detail} Your member number is <strong>{success.member_number}</strong>.
          </div>
        )}

        <form onSubmit={onSubmit}>
          {[
            ["full_name", "Full name", "text"],
            ["email", "Email", "email"],
            ["national_id", "National ID", "text"],
            ["phone", "Phone", "tel"],
            ["password", "Password", "password"],
          ].map(([name, label, type]) => (
            <div className="form-group" key={name}>
              <label className="form-label">{label}</label>
              <input className="form-input" type={type} name={name} value={form[name]} onChange={onChange} required />
            </div>
          ))}
          <div className="form-group">
            <label className="form-label">Address</label>
            <textarea className="form-textarea" name="address" value={form.address} onChange={onChange} />
          </div>
          <button className="btn btn-primary btn-block btn-lg" disabled={loading}>
            {loading ? "Submitting…" : "Register"}
          </button>
        </form>

        <p style={{ textAlign: "center", marginTop: "1.25rem", fontSize: "0.9rem", color: "var(--gray-500)" }}>
          Already a member? <Link href="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
