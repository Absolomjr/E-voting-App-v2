"use client";
import { useAuth, isStaffRole } from "@/lib/auth";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";

function Icon({ d, size = 18 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      {Array.isArray(d) ? d.map((p, i) => <path key={i} d={p} />) : <path d={d} />}
    </svg>
  );
}

const ICONS = {
  dashboard: ["M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z", "M9 22V12h6v10"],
  verify: ["M9 11l3 3L22 4", "M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"],
  accounts: ["M12 1v22", "M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"],
  members: ["M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2", "M9 7a4 4 0 100 8 4 4 0 000-8z"],
  staff: ["M12 15a7 7 0 100-14 7 7 0 000 14z", "M8.21 13.89L7 23l5-3 5 3-1.21-9.12"],
  audit: ["M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z", "M14 2v6h6", "M16 13H8", "M16 17H8"],
};

function buildNav(role) {
  const ops = [
    { label: "Dashboard", href: "/admin", icon: "dashboard" },
    { label: "Verify savings", href: "/admin/verify", icon: "verify" },
    { label: "Accounts", href: "/admin/accounts", icon: "accounts" },
  ];
  const people = [];
  if (role === "super_admin" || role === "secretary") {
    people.push({ label: "Members", href: "/admin/members", icon: "members" });
  }
  if (role === "super_admin") {
    people.push({ label: "Staff", href: "/admin/staff", icon: "staff" });
  }
  const reports = [{ label: "Audit log", href: "/admin/audit", icon: "audit" }];
  return [
    { section: "Operations", items: ops },
    ...(people.length ? [{ section: "People", items: people }] : []),
    { section: "Governance", items: reports },
  ];
}

export default function AdminLayout({ children }) {
  const { user, loading, logout } = useAuth();
  const pathname = usePathname();
  const router = useRouter();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!loading && (!user || !isStaffRole(user.role))) router.push("/login");
  }, [user, loading, router]);

  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  if (loading || !user) return null;

  const nav = buildNav(user.role);

  return (
    <>
      <header className="topbar">
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <button type="button" className="menu-toggle" onClick={() => setOpen((v) => !v)} aria-label="Menu">
            ☰
          </button>
          <div className="topbar-brand">
            <div className="brand-mark">S</div>
            <span>Sacco App</span>
          </div>
        </div>
        <div className="topbar-right">
          <div className="topbar-user">
            <strong>{user.full_name}</strong>
            <span style={{ fontSize: "0.7rem", color: "var(--gold-light)" }}>
              {user.role?.replace("_", " ").toUpperCase()}
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

      <div className={`sidebar-backdrop ${open ? "open" : ""}`} onClick={() => setOpen(false)} />

      <aside className={`sidebar ${open ? "open" : ""}`}>
        {nav.map((group) => (
          <div className="sidebar-section" key={group.section}>
            <div className="sidebar-section-title">{group.section}</div>
            {group.items.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`sidebar-link ${pathname === item.href ? "active" : ""}`}
              >
                <span style={{ width: 20, display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <Icon d={ICONS[item.icon]} />
                </span>
                {item.label}
              </Link>
            ))}
          </div>
        ))}
      </aside>

      <main className="main-content">{children}</main>
    </>
  );
}
