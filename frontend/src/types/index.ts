export interface Document {
  request_id: string;
  nome_arquivo: string;
  tipo_arquivo: string;
  status: string;
}

export interface AnalysisData {
  request_id: string;
  nome_arquivo: string;
  tipo_arquivo: string;
  status_analise: string;
  resumo_analitico: string;
  temas_principais: string[];
  estrutura_detectada: Record<string, unknown>;
  alertas: string[];
  limitacoes: string[];
}

export interface ReportData {
  request_id: string;
  status: string;
  rascunho_gerado?: string;
  relatorio_revisado?: string;
  message: string;
}

export interface LogEntry {
  step: string;
  message: string;
  status: string;
  timestamp: string;
}

export interface SessionStatus {
  request_id: string;
  status_fluxo: string;
  current_step: string;
  completed_steps: LogEntry[];
  erros: string[];
}

export type ReportType = 
  | 'resumo'
  | 'relatorio_tecnico'
  | 'relatorio_finep'
  | 'parecer_tecnico'
  | 'relato_cientifico'
  | 'dissertacao_ou_tese';

export type ExportFormat = 'md' | 'pdf' | 'docx';

export type Theme = 'light' | 'dark';
