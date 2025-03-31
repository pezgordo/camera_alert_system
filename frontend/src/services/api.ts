import axios from "axios";

const API_URL = "http://localhost:7001";

console.log("Initializing API service with URL:", API_URL);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    console.log("Adding token to request:", config.url);
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log(
      `API response [${response.status}]:`,
      response.config.url,
      response.data
    );
    return response;
  },
  (error) => {
    console.error(
      "API error:",
      error.config?.url,
      error.response?.status,
      error.message
    );
    if (error.response) {
      console.error("Response data:", error.response.data);
    }
    return Promise.reject(error);
  }
);

export interface Event {
  id: number;
  device_id: string;
  event_type: string;
  confidence: number;
  timestamp: string;
  raw_data: any;
  user_id: number;
}

export interface Alert {
  id: number;
  event_id: number;
  severity: "critical" | "normal";
  description: string;
  created_at: string;
  user_id: number;
}

export const apiService = {
  // Authentication
  login: async (email: string, password: string) => {
    console.log("Logging in with:", email);
    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);

    const response = await api.post("/token", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    console.log(
      "Login successful, token:",
      response.data.access_token.substring(0, 20) + "..."
    );
    return response.data;
  },

  // Events
  createEvent: async (event: Omit<Event, "id" | "timestamp" | "user_id">) => {
    console.log("Creating event:", event);
    const response = await api.post("/events/", event);
    return response.data;
  },

  // Alerts
  getAlerts: async (params?: {
    skip?: number;
    limit?: number;
    severity?: string;
  }) => {
    console.log("Getting alerts with params:", params);
    const response = await api.get("/alerts/", { params });
    console.log("Received alerts:", response.data.length);
    return response.data;
  },
};
