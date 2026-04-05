import React from 'react';
import { CheckCircle, Circle, Loader2, AlertCircle } from 'lucide-react';
import type { LogEntry } from '../types';

interface ProcessingStepperProps {
  logs: LogEntry[];
  currentStep?: string;
}

const STEPS = [
  { key: 'validate_upload', label: 'Validação' },
  { key: 'parse_document', label: 'Extração' },
  { key: 'security_precheck', label: 'Segurança' },
  { key: 'document_analysis', label: 'Análise' },
  { key: 'route_report_type', label: 'Roteamento' },
  { key: 'technical_report', label: 'Geração' },
  { key: 'quality_validation', label: 'Validação' },
  { key: 'final_reviewer', label: 'Revisão' },
  { key: 'markdown_render', label: 'Formatação' },
];

export function ProcessingStepper({ logs, currentStep }: ProcessingStepperProps) {
  const getStepStatus = (stepKey: string) => {
    const log = logs.find(l => l.step.includes(stepKey));
    if (!log) return 'pending';
    if (log.status === 'success') return 'completed';
    if (log.status === 'error') return 'error';
    if (log.status === 'warning') return 'warning';
    return 'processing';
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold mb-4 text-gray-800 dark:text-white">
        Progresso
      </h2>
      
      <div className="space-y-2">
        {STEPS.map((step, index) => {
          const status = getStepStatus(step.key);
          
          return (
            <div key={step.key} className="flex items-center gap-3">
              <div className="flex-shrink-0">
                {status === 'completed' && <CheckCircle className="w-5 h-5 text-green-500" />}
                {status === 'error' && <AlertCircle className="w-5 h-5 text-red-500" />}
                {status === 'warning' && <AlertCircle className="w-5 h-5 text-yellow-500" />}
                {status === 'processing' && <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />}
                {status === 'pending' && <Circle className="w-5 h-5 text-gray-300 dark:text-gray-600" />}
              </div>
              
              <div className="flex-1">
                <span className={`text-sm ${
                  status === 'completed' ? 'text-green-600 dark:text-green-400' :
                  status === 'error' ? 'text-red-600 dark:text-red-400' :
                  status === 'processing' ? 'text-blue-600 dark:text-blue-400' :
                  'text-gray-500 dark:text-gray-400'
                }`}>
                  {step.label}
                </span>
              </div>
              
              {index < STEPS.length - 1 && (
                <div className="w-0.5 h-4 bg-gray-200 dark:bg-gray-700 ml-2" />
              )}
            </div>
          );
        })}
      </div>

      {logs.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Logs:</h3>
          <div className="max-h-40 overflow-y-auto space-y-1">
            {logs.map((log, i) => (
              <div key={i} className="text-xs text-gray-500 dark:text-gray-400">
                <span className="font-mono">[{log.timestamp?.split('T')[1]?.slice(0,8)}]</span> {log.message}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
