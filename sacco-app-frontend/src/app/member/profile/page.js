"use client";
import { useAuth } from "@/lib/auth";

export default function ProfilePage() {
  const { user, logout } = useAuth();

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Profile</h1>
          <p className="subtitle">Your membership details</p>
        </div>
      </div>
      <div className="card">
        <div className="card-body">
          {[
            ["Full name", user?.full_name],
            ["Member number", user?.member_number],
            ["Email", user?.email],
            ["Phone", user?.phone],
          ].map(([label, value]) => (
            <div key={label} style={{ marginBottom: "1rem" }}>
              <div className="form-label">{label}</div>
              <div style={{ fontWeight: 600 }}>{value || "—"}</div>
            </div>
          ))}
          <button type="button" className="btn btn-outline btn-block" onClick={logout}>
            Log out
          </button>
        </div>
      </div>
    </>
  );
}
