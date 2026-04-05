import React from 'react';
import { AlertTriangle, ShieldAlert } from 'lucide-react';

interface SecurityAlertsBannerProps {
  alerts: string[];
}

export function SecurityAlertsBanner({ alerts }: SecurityAlertsBannerProps) {
  if (!alerts || alerts.length === 0) return null;

  return (
    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
      <div className="flex items-center gap-2 mb-2">
        <ShieldAlert className="w-5 h-5 text-red-600 dark:text-red-400" />
        <h3 className="font-semibold text-red-800 dark:text-red-200">Alertas de Segurança</h3>
      </div>
      <ul className="space-y-1">
        {alerts.map((alert, i) => (
          <li key={i} className="flex items-center gap-2 text-sm text-red-700 dark:text-red-300">
            <AlertTriangle className="w-4 h-4 flex-shrink-0" />
            {alert}
          </li>
        ))}
      </ul>
    </div>
  );
}
