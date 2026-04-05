import { useState, useCallback } from 'react';
import { generateReport, getReportStatus } from '../services/api';
import type { ReportData, ReportType, SessionStatus } from '../types';

interface UseReportGenerationReturn {
  generating: boolean;
  report: ReportData | null;
  status: SessionStatus | null;
  error: string | null;
  generate: (requestId: string, tipoRelatorio: ReportType) => Promise<void>;
  checkStatus: (requestId: string) => Promise<void>;
  reset: () => void;
}

export function useReportGeneration(): UseReportGenerationReturn {
  const [generating, setGenerating] = useState(false);
  const [report, setReport] = useState<ReportData | null>(null);
  const [status, setStatus] = useState<SessionStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  const generate = useCallback(async (requestId: string, tipoRelatorio: ReportType) => {
    setGenerating(true);
    setError(null);
    try {
      const reportData = await generateReport(requestId, tipoRelatorio);
      setReport(reportData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao gerar relatório');
    } finally {
      setGenerating(false);
    }
  }, []);

  const checkStatus = useCallback(async (requestId: string) => {
    try {
      const statusData = await getReportStatus(requestId);
      setStatus(statusData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao verificar status');
    }
  }, []);

  const reset = useCallback(() => {
    setReport(null);
    setStatus(null);
    setError(null);
  }, []);

  return { generating, report, status, error, generate, checkStatus, reset };
}
