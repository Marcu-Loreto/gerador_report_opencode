import React from 'react';
import { FileText, Briefcase, Building, Microscope, GraduationCap, BookOpen } from 'lucide-react';
import type { ReportType } from '../types';

interface ReportTypeSelectorProps {
  value: ReportType | null;
  onChange: (type: ReportType) => void;
  disabled?: boolean;
}

const REPORT_TYPES: { value: ReportType; label: string; description: string; icon: React.ReactNode }[] = [
  { value: 'relatorio_tecnico', label: 'Relatório Técnico', description: 'Análise técnica profissional', icon: <FileText className="w-5 h-5" /> },
  { value: 'relatorio_finep', label: 'Relatório FINEP', description: 'Padrão de organisme de fomento', icon: <Building className="w-5 h-5" /> },
  { value: 'parecer_tecnico', label: 'Parecer Técnico', description: 'Análise pericial formal', icon: <Briefcase className="w-5 h-5" /> },
  { value: 'relato_cientifico', label: 'Relato Científico', description: 'Formato acadêmico', icon: <Microscope className="w-5 h-5" /> },
  { value: 'dissertacao_ou_tese', label: 'Dissertação/Tese', description: 'Trabalho acadêmico longo', icon: <GraduationCap className="w-5 h-5" /> },
];

export function ReportTypeSelector({ value, onChange, disabled }: ReportTypeSelectorProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold mb-4 text-gray-800 dark:text-white">
        Tipo de Relatório
      </h2>
      
      <div className="space-y-3">
        {REPORT_TYPES.map(type => (
          <button
            key={type.value}
            onClick={() => onChange(type.value)}
            disabled={disabled}
            className={`w-full p-4 rounded-lg border-2 transition-all text-left ${
              value === type.value
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
            } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <div className="flex items-center gap-3">
              <div className={`${value === type.value ? 'text-blue-500' : 'text-gray-400'}`}>
                {type.icon}
              </div>
              <div>
                <p className="font-medium text-gray-800 dark:text-white">{type.label}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">{type.description}</p>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
