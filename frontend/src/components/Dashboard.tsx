import React, { useEffect, useState } from "react";
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Chip,
  IconButton,
  AppBar,
  Toolbar,
  Button,
} from "@mui/material";
import { Logout as LogoutIcon } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import { apiService, Alert } from "../services/api";
import { websocketService } from "../services/websocket";

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [filter, setFilter] = useState<"all" | "critical" | "normal">("all");

  useEffect(() => {
    // Load initial alerts
    loadAlerts();

    // Subscribe to WebSocket updates
    const unsubscribe = websocketService.subscribe((newAlert) => {
      setAlerts((prev) => [newAlert, ...prev]);
    });

    // Connect WebSocket
    websocketService.connect();

    return () => {
      unsubscribe();
      websocketService.disconnect();
    };
  }, []);

  const loadAlerts = async () => {
    try {
      const data = await apiService.getAlerts();
      setAlerts(data);
    } catch (error) {
      console.error("Failed to load alerts:", error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  const filteredAlerts = alerts.filter(
    (alert) => filter === "all" || alert.severity === filter
  );

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Camera Alert System
          </Typography>
          <Button color="inherit" onClick={handleLogout}>
            <LogoutIcon />
            Logout
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" gutterBottom>
            Alerts
          </Typography>
          <Box sx={{ mb: 2 }}>
            <Chip
              label="All"
              onClick={() => setFilter("all")}
              color={filter === "all" ? "primary" : "default"}
              sx={{ mr: 1 }}
            />
            <Chip
              label="Critical"
              onClick={() => setFilter("critical")}
              color={filter === "critical" ? "error" : "default"}
              sx={{ mr: 1 }}
            />
            <Chip
              label="Normal"
              onClick={() => setFilter("normal")}
              color={filter === "normal" ? "success" : "default"}
            />
          </Box>
        </Box>

        <Grid container spacing={3}>
          {filteredAlerts.map((alert) => (
            <Grid item xs={12} key={alert.id}>
              <Paper
                sx={{
                  p: 2,
                  display: "flex",
                  flexDirection: "column",
                  backgroundColor:
                    alert.severity === "critical" ? "#ffebee" : "#f1f8e9",
                }}
              >
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <Typography variant="h6" component="div">
                    {alert.description}
                  </Typography>
                  <Chip
                    label={alert.severity}
                    color={alert.severity === "critical" ? "error" : "success"}
                  />
                </Box>
                <Typography color="text.secondary" sx={{ mt: 1 }}>
                  {new Date(alert.created_at).toLocaleString()}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};
