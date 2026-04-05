import React from 'react';
import { FileText, List, AlertCircle } from 'lucide-react';
import type { AnalysisData } from '../types';

interface AnalysisSummaryCardProps {
  analysis: AnalysisData | null;
}

export function AnalysisSummaryCard({ analysis }: AnalysisSummaryCardProps) {
  if (!analysis) return null;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <div className="flex items-center gap-2 mb-4">
        <FileText className="w-5 h-5 text-blue-500" />
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white">
          Resumo da Análise
        </h2>
      </div>

      <div className="space-y-4">
        <div>
          <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">Resumo Analítico:</h3>
          <p className="text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700 p-3 rounded">
            {analysis.resumo_analitico}
          </p>
        </div>

        {analysis.temas_principais && analysis.temas_principais.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-2">
              <List className="w-4 h-4 text-gray-500" />
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">Principais Tópicos:</h3>
            </div>
            <ul className="space-y-1">
              {analysis.temas_principais.map((topic, i) => (
                <li key={i} className="text-sm text-gray-700 dark:text-gray-300 flex items-center gap-2">
                  <span className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
                  {topic}
                </li>
              ))}
            </ul>
          </div>
        )}

        {analysis.estrutura_detectada && (
          <div className="text-sm text-gray-500 dark:text-gray-400">
            <span>Títulos detectados: {analysis.estrutura_detectada.titulos?.length || 0}</span>
            <span className="mx-2">|</span>
            <span>Parágrafos: {analysis.estrutura_detectada.paragrafos || 0}</span>
          </div>
        )}

        {(analysis.alertas?.length > 0 || analysis.limitacoes?.length > 0) && (
          <div className="flex items-start gap-2 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded">
            <AlertCircle className="w-4 h-4 text-yellow-600 dark:text-yellow-400 mt-0.5" />
            <div className="text-sm text-yellow-800 dark:text-yellow-200">
              <p className="font-medium">Atenção:</p>
              <p>{analysis.alertas?.join(', ') || ''} {analysis.limitacoes?.join(', ')}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
