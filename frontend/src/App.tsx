import React, { useState, useEffect } from "react";
import { apiService, Alert } from "./services/api";
import "./App.css";

function App() {
  const [email, setEmail] = useState("test@example.com");
  const [password, setPassword] = useState("testpassword");
  const [token, setToken] = useState<string | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);

  console.log("App render state:", {
    hasToken: !!token,
    alertCount: alerts.length,
    error,
  });

  useEffect(() => {
    console.log("Checking for stored token...");
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      console.log("Found stored token");
      setToken(storedToken);
    }
  }, []);

  useEffect(() => {
    if (token) {
      console.log("Token is set, setting up polling");

      // Load alerts immediately
      loadAlerts();

      // Set up polling every 5 seconds
      const interval = setInterval(() => {
        loadAlerts();
      }, 5000);

      return () => {
        console.log("Cleaning up polling interval");
        clearInterval(interval);
      };
    }
  }, [token]);

  const loadAlerts = async () => {
    if (!token) {
      console.warn("Cannot load alerts without token");
      return;
    }

    try {
      console.log("Loading alerts...");
      setLoading(true);
      const data = await apiService.getAlerts();
      console.log(`Loaded ${data.length} alerts`);
      setAlerts(data);
      setLastUpdated(new Date().toLocaleTimeString());
      setError(null);
    } catch (err) {
      console.error("Error loading alerts:", err);
      setError("Failed to load alerts. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      console.log("Logging in...");
      setLoading(true);
      setError(null);
      const data = await apiService.login(email, password);
      console.log("Login successful");
      setToken(data.access_token);
      localStorage.setItem("token", data.access_token);
    } catch (err) {
      console.error("Login error:", err);
      setError("Login failed. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    console.log("Logging out");
    setToken(null);
    localStorage.removeItem("token");
    setAlerts([]);
    setError(null);
  };

  if (!token) {
    return (
      <div className="container">
        <h1>Camera Alert System</h1>
        <form onSubmit={handleLogin}>
          <div>
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <div className="error">{error}</div>}
          <button type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="header">
        <h1>Camera Alert System</h1>
        <button onClick={handleLogout}>Logout</button>
      </div>
      <div className="alerts">
        <h2>Alerts ({alerts.length})</h2>
        <div className="actions">
          <button onClick={loadAlerts} disabled={loading}>
            {loading ? "Refreshing..." : "Refresh Alerts"}
          </button>
          {lastUpdated && <span>Last updated: {lastUpdated}</span>}
        </div>
        {error && <div className="error">{error}</div>}
        {alerts.length === 0 ? (
          <p>
            No alerts found. Generate some events using the simulation script.
          </p>
        ) : (
          alerts.map((alert) => (
            <div key={alert.id} className={`alert ${alert.severity}`}>
              <h3>{alert.severity.toUpperCase()}</h3>
              <p>{alert.description}</p>
              <small>{new Date(alert.created_at).toLocaleString()}</small>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
