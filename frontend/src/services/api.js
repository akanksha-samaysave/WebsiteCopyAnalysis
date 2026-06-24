import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const analysisService = {
  async analyzePages(urls) {
    const response = await api.post("/analyze", { urls });
    return response.data;
  },

  async getAnalysisResults(jobId) {
    const response = await api.get(`/analysis/${jobId}`);
    return response.data;
  },

  async getComparison(jobId) {
    const response = await api.get(`/comparison/${jobId}`);
    return response.data;
  },

  async generateReport(jobId) {
    const response = await api.get(`/report/${jobId}`);
    return response.data;
  },

  async downloadReport(jobId) {
    const response = await api.get(`/report/${jobId}/download`, {
      responseType: "blob",
    });
    return response.data;
  },

  async healthCheck() {
    const response = await axios.get("http://127.0.0.1:8000/health");
    return response.data;
  },
};

export default api;