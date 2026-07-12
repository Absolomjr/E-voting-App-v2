import "@/styles/globals.css";
import { AuthProvider } from "@/lib/auth";

export const metadata = {
  title: "Sacco App",
  description: "Group SACCO savings and member management",
  viewport: "width=device-width, initial-scale=1, maximum-scale=1",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
