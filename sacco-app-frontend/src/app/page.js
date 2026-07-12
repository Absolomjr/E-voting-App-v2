"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getUser } from "@/lib/api";
import { isStaffRole } from "@/lib/auth";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    const user = getUser();
    if (!user) {
      router.replace("/login");
      return;
    }
    if (user.role === "member") router.replace("/member");
    else if (isStaffRole(user.role)) router.replace("/admin");
    else router.replace("/login");
  }, [router]);

  return null;
}
