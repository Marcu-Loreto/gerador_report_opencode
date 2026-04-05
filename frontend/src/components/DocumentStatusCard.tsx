import React from 'react';
import { CheckCircle, AlertCircle, Clock, XCircle } from 'lucide-react';
import type { AnalysisData } from '../types';

interface DocumentStatusCardProps {
  document: {
    nome_arquivo: string;
    tipo_arquivo: string;
    request_id: string;
  } | null;
  analysis: AnalysisData | null;
  uploading: boolean;
}

export function DocumentStatusCard({ document, analysis, uploading }: DocumentStatusCardProps) {
  if (!document) return null;

  const getStatusIcon = () => {
    if (uploading) return <Clock className="w-5 h-5 text-yellow-500 animate-pulse" />;
    if (analysis?.status_analise === 'completed') return <CheckCircle className="w-5 h-5 text-green-500" />;
    return <AlertCircle className="w-5 h-5 text-gray-400" />;
  };

  const getStatusText = () => {
    if (uploading) return 'Processando...';
    if (analysis?.status_analise === 'completed') return 'Análise concluída';
    return 'Aguardando análise';
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
      <div className="flex items-center gap-3 mb-3">
        {getStatusIcon()}
        <span className="font-medium text-gray-800 dark:text-white">{getStatusText()}</span>
      </div>
      
      {document && (
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-500 dark:text-gray-400">Arquivo:</span>
            <span className="text-gray-800 dark:text-white font-medium truncate ml-2">{document.nome_arquivo}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500 dark:text-gray-400">Tipo:</span>
            <span className="text-gray-800 dark:text-white uppercase">{document.tipo_arquivo}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500 dark:text-gray-400">ID:</span>
            <span className="text-gray-800 dark:text-white text-xs font-mono">{document.request_id.slice(0, 8)}...</span>
          </div>
        </div>
      )}

      {analysis?.alertas && analysis.alertas.length > 0 && (
        <div className="mt-3 p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded text-sm">
          <p className="font-medium text-yellow-800 dark:text-yellow-200 mb-1">Alertas:</p>
          {analysis.alertas.map((alert, i) => (
            <p key={i} className="text-yellow-700 dark:text-yellow-300 text-xs">{alert}</p>
          ))}
        </div>
      )}

      {analysis?.limitacoes && analysis.limitacoes.length > 0 && (
        <div className="mt-2 p-2 bg-red-50 dark:bg-red-900/20 rounded text-sm">
          <p className="font-medium text-red-800 dark:text-red-200 mb-1">Limitações:</p>
          {analysis.limitacoes.map((limitation, i) => (
            <p key={i} className="text-red-700 dark:text-red-300 text-xs">{limitation}</p>
          ))}
        </div>
      )}
    </div>
  );
}
