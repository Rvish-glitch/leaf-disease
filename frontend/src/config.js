// Centralized API configuration for the frontend
// Priority: explicit env var > default Railway URL

export const DEFAULT_API = "https://leaf-disease-production.up.railway.app";

export function getInitialApiBase() {
  const raw = process.env.REACT_APP_API_URL || DEFAULT_API;
  return raw.replace(/\/$/, "");
}

export const API_BASE_URL = getInitialApiBase();

// Tiny helper to log once on app start
export function logApiBase() {
  if (typeof window !== "undefined") {
    // eslint-disable-next-line no-console
  console.log("API_BASE_URL:", API_BASE_URL);
  }
}
