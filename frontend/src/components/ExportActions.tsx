import React from 'react';
import { Download, FileText, File, FileCode } from 'lucide-react';
import type { ExportFormat } from '../types';

interface ExportActionsProps {
  onExport: (format: ExportFormat) => void;
  exporting?: boolean;
}

export function ExportActions({ onExport, exporting }: ExportActionsProps) {
  const formats: { format: ExportFormat; label: string; icon: React.ReactNode }[] = [
    { format: 'md', label: 'Markdown', icon: <FileCode className="w-4 h-4" /> },
    { format: 'pdf', label: 'PDF', icon: <FileText className="w-4 h-4" /> },
    { format: 'docx', label: 'Word', icon: <File className="w-4 h-4" /> },
  ];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <div className="flex items-center gap-2 mb-4">
        <Download className="w-5 h-5 text-blue-500" />
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white">
          Exportar
        </h2>
      </div>

      <div className="grid grid-cols-3 gap-3">
        {formats.map(({ format, label, icon }) => (
          <button
            key={format}
            onClick={() => onExport(format)}
            disabled={exporting}
            className="flex flex-col items-center gap-2 p-4 border-2 border-gray-200 dark:border-gray-700 rounded-lg hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors disabled:opacity-50"
          >
            {icon}
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
