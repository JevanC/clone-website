"use client";

import { useState } from "react";

export default function Home() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [fileUrl, setFileUrl] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    setFileUrl("");

    try {
      const res = await fetch("http://localhost:8000/submit-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);

      const data = await res.json();
      if (!data.file_url) throw new Error("No file URL returned from server");
      
      setFileUrl(`http://localhost:8000${data.file_url}`);

    } catch {
      setError("Failed to fetch website content. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-8">
      <div className="bg-white w-full max-w-xl p-10 rounded-2xl shadow-lg">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Website Copier</h1>
        <p className="text-gray-500 text-sm mb-6">
          Enter any URL and get a downloadable version of the site.
        </p>

        <form onSubmit={handleSubmit} className="flex gap-4 items-center">
          <input
            type="url"
            placeholder="https://example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
            disabled={loading}
            className="flex-grow px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 placeholder-gray-400 text-gray-800"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg transition-all disabled:opacity-50 flex items-center gap-2"
          >
            {loading ? (
              <>
                <span className="loader" />
                Loading...
              </>
            ) : (
              "Submit"
            )}
          </button>
        </form>

        {error && (
          <div className="mt-6 text-sm text-red-700 bg-red-100 px-4 py-2 rounded-lg border border-red-300">
            ❌ {error}
          </div>
        )}

        {fileUrl && (
          <div className="mt-6 text-sm text-green-700 bg-green-100 px-4 py-2 rounded-lg border border-green-300 break-words">
            ✅ Your copy is ready:{" "}
            <a
              href={fileUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="underline text-blue-700"
            >
              Open generated file
            </a>
          </div>
        )}
      </div>


      <style jsx>{`
        .loader {
          border: 3px solid transparent;
          border-top: 3px solid white;
          border-right: 3px solid white;
          border-radius: 50%;
          width: 18px;
          height: 18px;
          animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
          0% {
            transform: rotate(0deg);
          }
          100% {
            transform: rotate(360deg);
          }
        }
      `}</style>
    </div>
  );
}
