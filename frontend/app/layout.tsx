import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "Verilumen ATE Intelligence Platform",
  description: "Advanced Semiconductor Automated Test Equipment Diagnostics & Yield Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {children}
        </main>
        <footer className="border-t border-slate-850 py-4 text-center text-xs text-slate-500">
          Verilumen Labs ATE Intelligence Platform &bull; Production Assessment Standard
        </footer>
      </body>
    </html>
  );
}
