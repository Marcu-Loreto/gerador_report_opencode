import React, { useState, useCallback } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import { Trash2, Play, RefreshCw } from 'lucide-react';

import {
  FileUploadPanel,
  DocumentStatusCard,
  ReportTypeSelector,
  ProcessingStepper,
  SecurityAlertsBanner,
  AnalysisSummaryCard,
  ReportEditor,
  ExportActions,
  ThemeToggle
} from './components';
import { useUpload } from './hooks/useUpload';
import { useReportGeneration } from './hooks/useReportGeneration';
import { updateReport, exportReport, deleteSession, getReportResult } from './services/api';
import type { ReportType, ExportFormat } from './types';

function App() {
  const [selectedReportType, setSelectedReportType] = useState<ReportType | null>(null);
  const [reportContent, setReportContent] = useState('');
  const [editedContent, setEditedContent] = useState('');
  const [hasEdited, setHasEdited] = useState(false);

  const { uploading, document, analysis, error, uploadFile, analyzeFile, reset: resetUpload } = useUpload();
  const { generating, report, status, error: genError, generate, checkStatus, reset: resetGen } = useReportGeneration();

  const handleFileSelect = useCallback(async (file: File) => {
    setReportContent('');
    setEditedContent('');
    setHasEdited(false);
    await uploadFile(file);
  }, [uploadFile]);

  const handleAnalyze = useCallback(async () => {
    await analyzeFile();
    toast.success('Análise concluída!');
  }, [analyzeFile]);

  const handleGenerate = useCallback(async () => {
    if (!document || !selectedReportType) {
      toast.error('Selecione o tipo de relatório');
      return;
    }
    
    await generate(document.request_id, selectedReportType);
    
    const result = await getReportResult(document.request_id);
    setReportContent(result.content);
    
    toast.success('Relatório gerado com sucesso!');
  }, [document, selectedReportType, generate]);

  const handleSaveEdit = useCallback(async () => {
    if (!document) return;
    await updateReport(document.request_id, editedContent);
    setReportContent(editedContent);
    setHasEdited(true);
    toast.success('Alterações salvas!');
  }, [document, editedContent]);

  const handleExport = useCallback(async (format: ExportFormat) => {
    if (!document) return;
    
    try {
      const blob = await exportReport(document.request_id, format);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `relatorio.${format}`;
      a.click();
      URL.revokeObjectURL(url);
      toast.success(`Exportado como ${format.toUpperCase()}`);
    } catch (err) {
      toast.error('Erro ao exportar');
    }
  }, [document]);

  const handleReset = useCallback(async () => {
    if (document) {
      await deleteSession(document.request_id);
    }
    resetUpload();
    resetGen();
    setSelectedReportType(null);
    setReportContent('');
    setEditedContent('');
    setHasEdited(false);
    toast.success('Sessão resetada');
  }, [document, resetUpload, resetGen]);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Toaster position="top-right" />
      
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-800 dark:text-white">
            Gerador de Relatórios
          </h1>
          <ThemeToggle />
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="space-y-6">
            <FileUploadPanel
              onFileSelect={handleFileSelect}
              selectedFile={null}
              uploading={uploading}
              disabled={!!document}
            />
            
            <DocumentStatusCard
              document={document}
              analysis={analysis}
              uploading={uploading}
            />

            {document && !analysis && (
              <button
                onClick={handleAnalyze}
                disabled={uploading}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 transition-colors"
              >
                <Play className="w-5 h-5" />
                Analisar Documento
              </button>
            )}

            {analysis && (
              <>
                <ReportTypeSelector
                  value={selectedReportType}
                  onChange={setSelectedReportType}
                  disabled={generating}
                />

                <button
                  onClick={handleGenerate}
                  disabled={!selectedReportType || generating}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 transition-colors"
                >
                  <RefreshCw className={`w-5 h-5 ${generating ? 'animate-spin' : ''}`} />
                  Gerar Relatório
                </button>
              </>
            )}

            {document && (
              <button
                onClick={handleReset}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-red-100 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-200 dark:hover:bg-red-900/40 transition-colors"
              >
                <Trash2 className="w-5 h-5" />
                Limpar Sessão
              </button>
            )}
          </div>

          <div className="lg:col-span-2 space-y-6">
            {analysis && (
              <AnalysisSummaryCard analysis={analysis} />
            )}

            {reportContent && (
              <>
                <ReportEditor
                  content={reportContent}
                  onChange={setEditedContent}
                  onSave={handleSaveEdit}
                  saving={generating}
                />
                
                <ExportActions onExport={handleExport} />
              </>
            )}

            {!reportContent && !analysis && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-12 text-center">
                <p className="text-gray-500 dark:text-gray-400">
                  Faça upload de um documento para começar
                </p>
              </div>
            )}

            {status && (
              <ProcessingStepper
                logs={status.completed_steps}
                currentStep={status.current_step}
              />
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
