import React, { useState } from "react";

function App() {
  const [inputText, setInputText] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const MCP_URL =
    "https://miniature-invention-5gp7jr4jj4xvf664-8010.app.github.dev/mcp/llm_extract";
  const API_KEY = "vanghee-dev-key";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
    setError(null);

    try {
      const res = await fetch(MCP_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": API_KEY,
        },
        body: JSON.stringify({
          text: inputText,
          user_role: "user",
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data?.detail || "Failed to fetch");
      }

      setResponse(data);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch from backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: 600,
        margin: "50px auto",
        textAlign: "center",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>🤖 Vanghee AI MCP Chat</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Ask something like: Calculate GST for 1000"
          style={{
            width: "70%",
            padding: "10px",
            fontSize: "16px",
            borderRadius: "6px",
            border: "1px solid #ccc",
          }}
          required
        />
        <button
          type="submit"
          style={{
            padding: "10px 20px",
            marginLeft: "10px",
            fontSize: "16px",
            borderRadius: "6px",
            border: "none",
            background: "#2563eb",
            color: "#fff",
            cursor: "pointer",
          }}
        >
          Send
        </button>
      </form>

      {loading && <p>Processing... 🤔</p>}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* SUCCESS RESPONSE UI */}
      {response?.status === "SUCCESS" && response?.data && (
        <div
          style={{
            marginTop: 20,
            padding: 16,
            borderRadius: 8,
            background: "#f1f5f9",
            textAlign: "left",
          }}
        >
          <h3>✅ Result</h3>
          <p>
            <strong>Amount:</strong> ₹{response.data.amount}
          </p>
          <p>
            <strong>GST (18%):</strong> ₹{response.data.gst}
          </p>
          <p>
            <strong>Total:</strong> ₹{response.data.total}
          </p>
        </div>
      )}

      {/* REJECTED RESPONSE UI */}
      {response?.status === "REJECTED" && (
        <div style={{ marginTop: 20, color: "orange" }}>
          ⚠️ Rejected: {response.reason} (confidence:{" "}
          {response.confidence ?? "N/A"})
        </div>
      )}

      {/* RAW JSON (Debug Mode) */}
      {response && (
        <details style={{ marginTop: 20, textAlign: "left" }}>
          <summary>🔎 Debug JSON</summary>
          <pre
            style={{
              marginTop: 10,
              padding: 10,
              background: "#111827",
              color: "#e5e7eb",
              borderRadius: 6,
              overflowX: "auto",
            }}
          >
            {JSON.stringify(response, null, 2)}
          </pre>
        </details>
      )}
    </div>
  );
}

export default App;
