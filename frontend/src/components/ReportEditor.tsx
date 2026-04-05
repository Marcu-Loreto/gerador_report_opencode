import React, { useState, useEffect } from 'react';
import { Edit3, Eye, Save } from 'lucide-react';

interface ReportEditorProps {
  content: string;
  onChange: (content: string) => void;
  onSave: () => void;
  saving?: boolean;
}

export function ReportEditor({ content, onChange, onSave, saving }: ReportEditorProps) {
  const [mode, setMode] = useState<'edit' | 'preview'>('preview');

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white">
          Relatório Gerado
        </h2>
        
        <div className="flex items-center gap-2">
          <button
            onClick={() => setMode('edit')}
            className={`p-2 rounded-lg transition-colors ${
              mode === 'edit' ? 'bg-blue-500 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
            }`}
          >
            <Edit3 className="w-4 h-4" />
          </button>
          <button
            onClick={() => setMode('preview')}
            className={`p-2 rounded-lg transition-colors ${
              mode === 'preview' ? 'bg-blue-500 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
            }`}
          >
            <Eye className="w-4 h-4" />
          </button>
        </div>
      </div>

      {mode === 'edit' ? (
        <div className="space-y-4">
          <textarea
            value={content}
            onChange={(e) => onChange(e.target.value)}
            className="w-full h-96 p-4 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900 text-gray-800 dark:text-white font-mono text-sm resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Edite o conteúdo do relatório aqui..."
          />
          
          <button
            onClick={onSave}
            disabled={saving}
            className="flex items-center gap-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 transition-colors"
          >
            <Save className="w-4 h-4" />
            {saving ? 'Salvando...' : 'Salvar'}
          </button>
        </div>
      ) : (
        <div className="prose dark:prose-invert max-w-none">
          <pre className="whitespace-pre-wrap text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-900 p-4 rounded-lg overflow-auto max-h-96">
            {content}
          </pre>
        </div>
      )}
    </div>
  );
}
