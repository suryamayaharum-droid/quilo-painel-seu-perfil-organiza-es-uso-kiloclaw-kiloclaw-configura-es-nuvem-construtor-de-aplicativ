import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HoloOS Dashboard",
  description: "Super Intelligence Native AI Operating System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt">
      <body>{children}</body>
    </html>
  );
}