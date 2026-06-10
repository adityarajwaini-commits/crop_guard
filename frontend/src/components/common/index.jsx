export const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md',
  className = '',
  ...props 
}) => {
  const baseStyles = 'font-semibold rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {
    primary: 'bg-emerald-500 text-white font-bold hover:bg-emerald-600 shadow-lg hover:shadow-xl',
    secondary: 'bg-blue-500 text-white font-bold hover:bg-blue-600 shadow-lg hover:shadow-xl',
    outline: 'border-2 border-emerald-500 text-emerald-600 font-bold hover:bg-emerald-50 dark:hover:bg-neutral-800',
    ghost: 'text-neutral-900 font-bold dark:text-white hover:bg-neutral-100 dark:hover:bg-neutral-800',
    cta: 'bg-white text-gray-900 font-bold hover:bg-gray-100 shadow-2xl border border-gray-300',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2.5 text-base',
    lg: 'px-6 py-3 text-lg',
    xl: 'px-8 py-4 text-xl',
  };

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export const Card = ({ children, className = '', ...props }) => {
  return (
    <div
      className={`bg-white dark:bg-neutral-800 rounded-xl shadow-md p-6 border border-gray-200 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export const Badge = ({ children, variant = 'default', className = '' }) => {
  const variants = {
    default: 'bg-neutral-200 text-neutral-800 dark:bg-neutral-700 dark:text-neutral-100',
    success: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100',
    warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100',
    danger: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100',
  };

  return (
    <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${variants[variant]} ${className}`}>
      {children}
    </span>
  );
};

export const ErrorAlert = ({ message, onClose }) => {
  if (!message) return null;

  return (
    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex items-start gap-3">
      <div className="flex-shrink-0 text-red-600 dark:text-red-400 text-xl">⚠️</div>
      <div className="flex-1">
        <p className="text-red-800 dark:text-red-200">{message}</p>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300"
        >
          ✕
        </button>
      )}
    </div>
  );
};

export const SuccessAlert = ({ message }) => {
  if (!message) return null;

  return (
    <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4 flex items-start gap-3">
      <div className="flex-shrink-0 text-green-600 dark:text-green-400 text-xl">✓</div>
      <p className="text-green-800 dark:text-green-200">{message}</p>
    </div>
  );
};
