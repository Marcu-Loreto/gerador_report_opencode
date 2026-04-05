import { useState, useCallback } from 'react';
import { uploadDocument, analyzeDocument } from '../services/api';
import type { Document, AnalysisData } from '../types';

interface UseUploadReturn {
  uploading: boolean;
  document: Document | null;
  analysis: AnalysisData | null;
  error: string | null;
  uploadFile: (file: File) => Promise<void>;
  analyzeFile: () => Promise<void>;
  reset: () => void;
}

export function useUpload(): UseUploadReturn {
  const [uploading, setUploading] = useState(false);
  const [document, setDocument] = useState<Document | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const uploadFile = useCallback(async (file: File) => {
    setUploading(true);
    setError(null);
    try {
      const doc = await uploadDocument(file);
      setDocument(doc);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao fazer upload');
    } finally {
      setUploading(false);
    }
  }, []);

  const analyzeFile = useCallback(async () => {
    if (!document) return;
    setUploading(true);
    setError(null);
    try {
      const analysisData = await analyzeDocument(document.request_id);
      setAnalysis(analysisData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao analisar documento');
    } finally {
      setUploading(false);
    }
  }, [document]);

  const reset = useCallback(() => {
    setDocument(null);
    setAnalysis(null);
    setError(null);
  }, []);

  return { uploading, document, analysis, error, uploadFile, analyzeFile, reset };
}
