"use client";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import BottomNav from "@/components/BottomNav";

export default function MemberLayout({ children }) {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && (!user || user.role !== "member")) router.push("/login");
  }, [user, loading, router]);

  if (loading || !user) return null;

  return (
    <>
      <header className="topbar">
        <div className="topbar-brand">
          <div className="brand-mark">S</div>
          <span>Sacco App</span>
        </div>
        <div className="topbar-right">
          <div className="topbar-user">
            <strong>{user.full_name}</strong>
            <span style={{ fontSize: "0.7rem", color: "var(--gold-light)" }}>
              {user.member_number}
            </span>
          </div>
          <button
            type="button"
            className="btn btn-outline btn-sm"
            style={{ color: "var(--gray-400)", borderColor: "var(--gray-600)" }}
            onClick={logout}
          >
            Logout
          </button>
        </div>
      </header>
      <main className="member-main">{children}</main>
      <BottomNav />
    </>
  );
}
