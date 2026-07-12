const BASE = "/api";

async function request(endpoint, options = {}) {
  const token =
    typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  const headers = { "Content-Type": "application/json", ...options.headers };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${BASE}${endpoint}`, { ...options, headers });

  if (res.status === 401 && token) {
    const refreshed = await refreshToken();
    if (refreshed) return request(endpoint, options);
    if (typeof window !== "undefined") {
      localStorage.clear();
      window.location.href = "/login";
    }
    throw new Error("Session expired");
  }

  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw { status: res.status, data };
  return data;
}

async function refreshToken() {
  const refresh = localStorage.getItem("refresh_token");
  if (!refresh) return false;
  try {
    const res = await fetch(`${BASE}/accounts/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh }),
    });
    if (!res.ok) return false;
    const data = await res.json();
    localStorage.setItem("access_token", data.access);
    return true;
  } catch {
    return false;
  }
}

function storeSession(data) {
  localStorage.setItem("access_token", data.access);
  localStorage.setItem("refresh_token", data.refresh);
  localStorage.setItem("user", JSON.stringify(data.user));
  return data.user;
}

export const api = {
  get: (url) => request(url),
  post: (url, body) =>
    request(url, { method: "POST", body: JSON.stringify(body) }),
  patch: (url, body) =>
    request(url, { method: "PATCH", body: JSON.stringify(body) }),
  del: (url) => request(url, { method: "DELETE" }),
};

export async function loginStaff(username, password) {
  const res = await fetch(`${BASE}/accounts/login/staff/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json();
  if (!res.ok) throw data;
  return storeSession(data);
}

export async function loginMember(member_number, password) {
  const res = await fetch(`${BASE}/accounts/login/member/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ member_number, password }),
  });
  const data = await res.json();
  if (!res.ok) throw data;
  return storeSession(data);
}

export async function registerMember(formData) {
  const res = await fetch(`${BASE}/accounts/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });
  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

export function logout() {
  localStorage.clear();
  window.location.href = "/login";
}

export function getUser() {
  if (typeof window === "undefined") return null;
  const u = localStorage.getItem("user");
  return u ? JSON.parse(u) : null;
}

export function formatMoney(value) {
  const n = Number(value || 0);
  return n.toLocaleString(undefined, {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  });
}

export function statusBadge(status) {
  if (status === "verified") return "badge-success";
  if (status === "rejected") return "badge-danger";
  return "badge-warning";
}
