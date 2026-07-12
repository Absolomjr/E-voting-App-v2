"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

function Icon({ d }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      {Array.isArray(d) ? d.map((p, i) => <path key={i} d={p} />) : <path d={d} />}
    </svg>
  );
}

const ITEMS = [
  { href: "/member", label: "Home", icon: ["M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z", "M9 22V12h6v10"] },
  { href: "/member/save", label: "Save", icon: "M12 5v14M5 12h14" },
  { href: "/member/history", label: "History", icon: ["M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z", "M14 2v6h6", "M16 13H8", "M16 17H8"] },
  { href: "/member/profile", label: "Profile", icon: ["M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2", "M12 11a4 4 0 100-8 4 4 0 000 8z"] },
];

export default function BottomNav() {
  const pathname = usePathname();
  return (
    <nav className="bottom-nav">
      {ITEMS.map((item) => {
        const active = pathname === item.href;
        return (
          <Link key={item.href} href={item.href} className={active ? "active" : ""}>
            <Icon d={item.icon} />
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}
