"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const login = async () => {
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        router.push("/admin");
      } else {
        setError("Invalid username or password");
      }
    } catch {
      setError("Unable to reach server");
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center px-4"
      style={{ background: "var(--background)", color: "var(--foreground)" }}
    >
      <div
        className="
          w-full max-w-md 
          rounded-2xl 
          p-8 
          shadow-[0_0_25px_rgba(0,255,170,0.1)]
          border border-[rgba(0,255,170,0.25)]
          bg-[rgba(20,20,35,0.85)]
          backdrop-blur-xl
        "
      >
        {/* Header */}
        <h1
          className="text-3xl font-extrabold mb-2 text-center"
          style={{
            color: "var(--violet)",
            textShadow: "0 0 12px rgba(123, 31, 162, 0.6)",
          }}
        >
          Admin Login
        </h1>

        <p className="text-sm text-center opacity-70 mb-6">
          Restricted access · Authorized users only
        </p>

        {/* Error */}
        {error && (
          <div
            className="
              mb-4 text-red-400 text-sm
              bg-[rgba(60,0,0,0.4)]
              border border-red-600/30
              p-3 rounded-md
            "
          >
            {error}
          </div>
        )}

        {/* Inputs */}
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="
              w-full px-4 py-3 rounded-lg
              bg-[rgba(20,20,30,0.7)]
              text-white
              placeholder-[rgba(0,255,170,0.5)]
              border border-teal-400
              focus:outline-none
              focus:ring-2
              focus:ring-teal-500
            "
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="
              w-full px-4 py-3 rounded-lg
              bg-[rgba(20,20,30,0.7)]
              text-white
              placeholder-[rgba(0,255,170,0.5)]
              border border-teal-400
              focus:outline-none
              focus:ring-2
              focus:ring-teal-500
            "
          />

          <button
            onClick={login}
            className="
              w-full py-3 rounded-lg font-semibold text-black
              bg-gradient-to-r from-teal-400 to-green-300
              hover:opacity-85
              transition-all shadow-[0_0_15px_rgba(0,255,170,0.4)]
            "
          >
            Login
          </button>
        </div>
      </div>
    </div>
  );
}
