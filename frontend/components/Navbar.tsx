"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Cpu,
  BarChart3,
  ShieldCheck,
  AlertTriangle,
  Search,
  BrainCircuit,
  Flame,
  Sparkles
} from "lucide-react";

const NAV_ITEMS = [
  { name: "Overview", href: "/", icon: BarChart3 },
  { name: "Data Quality", href: "/data-quality", icon: ShieldCheck },
  { name: "Yield & Failures", href: "/yield", icon: Cpu },
  { name: "Anomalies", href: "/anomalies", icon: AlertTriangle },
  { name: "Investigation", href: "/investigation", icon: Search },
  { name: "AI Analysis", href: "/ai-analysis", icon: Sparkles },
  { name: "ML Prediction", href: "/prediction", icon: Flame },
  { name: "Model Performance", href: "/model-performance", icon: BrainCircuit },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <Cpu className="h-7 w-7 text-blue-500 animate-pulse" />
            <span className="font-bold text-lg tracking-wide text-white">
              VERILUMEN <span className="text-blue-400 font-medium text-sm">ATE INTELLIGENCE</span>
            </span>
          </div>

          <div className="hidden md:flex space-x-1 lg:space-x-2">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center space-x-1.5 px-3 py-2 rounded-md text-xs font-medium transition-colors ${isActive
                      ? "bg-blue-600 text-white shadow-sm"
                      : "text-slate-300 hover:bg-slate-800 hover:text-white"
                    }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}
