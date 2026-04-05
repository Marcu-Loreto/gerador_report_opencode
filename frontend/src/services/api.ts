import axios from 'axios';
import type { Document, AnalysisData, ReportData, SessionStatus, ReportType, ExportFormat } from '../types';

const API_BASE = 'http://localhost:8006/api/v1';

export const api = axios.create({
  baseURL: API_BASE,
  timeout: 300000,
});

export const uploadDocument = async (file: File): Promise<Document> => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post<Document>('/upload', formData);
  return response.data;
};

export const analyzeDocument = async (requestId: string): Promise<AnalysisData> => {
  const response = await api.post<AnalysisData>(`/analyze/${requestId}`);
  return response.data;
};

export const generateReport = async (requestId: string, tipoRelatorio: ReportType): Promise<ReportData> => {
  const response = await api.post<ReportData>('/generate', {
    request_id: requestId,
    tipo_relatorio: tipoRelatorio,
  });
  return response.data;
};

export const getReportStatus = async (requestId: string): Promise<SessionStatus> => {
  const response = await api.get<SessionStatus>(`/status/${requestId}`);
  return response.data;
};

export const getReportResult = async (requestId: string): Promise<{ request_id: string; content: string }> => {
  const response = await api.get(`/result/${requestId}`);
  return response.data;
};

export const updateReport = async (requestId: string, conteudo: string): Promise<void> => {
  await api.post('/update', {
    request_id: requestId,
    conteudo,
  });
};

export const exportReport = async (requestId: string, formato: ExportFormat): Promise<Blob> => {
  const response = await api.post('/export', {
    request_id: requestId,
    formato,
  }, {
    responseType: 'blob',
  });
  return response.data;
};

export const deleteSession = async (requestId: string): Promise<void> => {
  await api.delete(`/session/${requestId}`);
};
