import React from 'react';
import ReactMarkdown from 'react-markdown';
import { FileDown } from 'lucide-react';

interface MarkdownPreviewProps {
  content: string;
}

export function MarkdownPreview({ content }: MarkdownPreviewProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold mb-4 text-gray-800 dark:text-white">
        Pré-visualização Markdown
      </h2>
      
      <div className="prose dark:prose-invert max-w-none">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
    </div>
  );
}
