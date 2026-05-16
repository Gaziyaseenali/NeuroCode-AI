interface StatusIndicatorProps {
  status: boolean;
  label: string;
}

export default function StatusIndicator({ status, label }: StatusIndicatorProps) {
  return (
    <div className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800">
      <div
        className={`w-3 h-3 rounded-full ${
          status ? 'bg-green-500' : 'bg-red-500'
        }`}
      />
      <span className="text-sm font-medium">{label}</span>
      <span
        className={`ml-auto text-xs font-semibold ${
          status ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
        }`}
      >
        {status ? 'OK' : 'FAIL'}
      </span>
    </div>
  );
}

// Made with Bob
