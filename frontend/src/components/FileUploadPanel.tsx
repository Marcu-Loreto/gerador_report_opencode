import React from 'react';
import { Upload, FileText, File, FileSpreadsheet, Presentation, FileCode } from 'lucide-react';

const ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.xlsx', '.csv', '.pptx', '.txt', '.md'];

interface FileUploadPanelProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  uploading: boolean;
  disabled?: boolean;
}

export function FileUploadPanel({ onFileSelect, selectedFile, uploading, disabled }: FileUploadPanelProps) {
  const getFileIcon = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase();
    switch (ext) {
      case 'pdf': return <FileText className="w-8 h-8 text-red-500" />;
      case 'docx': return <File className="w-8 h-8 text-blue-500" />;
      case 'xlsx': case 'csv': return <FileSpreadsheet className="w-8 h-8 text-green-500" />;
      case 'pptx': return <Presentation className="w-8 h-8 text-orange-500" />;
      case 'md': return <FileCode className="w-8 h-8 text-purple-500" />;
      default: return <File className="w-8 h-8 text-gray-500" />;
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold mb-4 text-gray-800 dark:text-white">
        Upload de Documento
      </h2>
      
      <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center hover:border-blue-500 transition-colors">
        <input
          type="file"
          accept={ALLOWED_EXTENSIONS.join(',')}
          onChange={(e) => e.target.files?.[0] && onFileSelect(e.target.files[0])}
          disabled={disabled || uploading}
          className="hidden"
          id="file-upload"
        />
        <label htmlFor="file-upload" className="cursor-pointer">
          <Upload className="w-12 h-12 mx-auto text-gray-400 mb-3" />
          <p className="text-gray-600 dark:text-gray-300 mb-2">
            Clique para selecionar ou arraste o arquivo
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Formatos: {ALLOWED_EXTENSIONS.join(', ')}
          </p>
        </label>
      </div>

      {selectedFile && (
        <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg flex items-center gap-3">
          {getFileIcon(selectedFile.name)}
          <div className="flex-1 min-w-0">
            <p className="font-medium text-gray-800 dark:text-white truncate">{selectedFile.name}</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {(selectedFile.size / 1024).toFixed(1)} KB
            </p>
          </div>
          {uploading && (
            <div className="animate-spin w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full" />
          )}
        </div>
      )}

      <div className="mt-4">
        <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Formatos aceitos:</h3>
        <div className="flex flex-wrap gap-2">
          {ALLOWED_EXTENSIONS.map(ext => (
            <span key={ext} className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-xs rounded text-gray-600 dark:text-gray-400">
              {ext}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
