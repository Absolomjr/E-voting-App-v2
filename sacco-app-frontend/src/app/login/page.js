"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { loginStaff, loginMember } from "@/lib/api";
import { useAuth, isStaffRole } from "@/lib/auth";

export default function LoginPage() {
  const [tab, setTab] = useState("member");
  const [form, setForm] = useState({ username: "", member_number: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { updateUser } = useAuth();
  const router = useRouter();

  const onChange = (e) => setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const user =
        tab === "staff"
          ? await loginStaff(form.username, form.password)
          : await loginMember(form.member_number, form.password);
      updateUser(user);
      router.push(isStaffRole(user.role) ? "/admin" : "/member");
    } catch (err) {
      setError(err?.detail || "Login failed. Check your credentials.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="logo-area">
          <div className="brand-mark">S</div>
          <h1>Sacco App</h1>
          <p>Track shares. Verify savings. Stay accountable.</p>
        </div>

        <div className="login-tabs">
          <button type="button" className={`login-tab ${tab === "member" ? "active" : ""}`} onClick={() => setTab("member")}>
            Member
          </button>
          <button type="button" className={`login-tab ${tab === "staff" ? "active" : ""}`} onClick={() => setTab("staff")}>
            Staff
          </button>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={onSubmit}>
          {tab === "staff" ? (
            <div className="form-group">
              <label className="form-label">Username</label>
              <input className="form-input" name="username" value={form.username} onChange={onChange} required autoComplete="username" />
            </div>
          ) : (
            <div className="form-group">
              <label className="form-label">Member number</label>
              <input className="form-input" name="member_number" value={form.member_number} onChange={onChange} placeholder="SACCO0001" required autoComplete="username" />
            </div>
          )}
          <div className="form-group">
            <label className="form-label">Password</label>
            <input className="form-input" type="password" name="password" value={form.password} onChange={onChange} required autoComplete="current-password" />
          </div>
          <button className="btn btn-primary btn-block btn-lg" disabled={loading}>
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <p style={{ textAlign: "center", marginTop: "1.25rem", fontSize: "0.9rem", color: "var(--gray-500)" }}>
          New member? <Link href="/register">Register</Link>
        </p>
      </div>
    </div>
  );
}
