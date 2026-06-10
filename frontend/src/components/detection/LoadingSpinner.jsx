import { motion } from 'framer-motion';

export const LoadingSpinner = ({ message = 'Analyzing your plant...' }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col items-center justify-center py-12"
    >
      <div className="relative w-16 h-16">
        {/* Outer ring */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          className="absolute inset-0 border-4 border-transparent border-t-emerald-500 border-r-emerald-500 rounded-full"
        />
        {/* Inner ring */}
        <motion.div
          animate={{ rotate: -360 }}
          transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
          className="absolute inset-2 border-4 border-transparent border-b-blue-500 border-l-blue-500 rounded-full"
        />
      </div>

      <motion.p
        animate={{ opacity: [1, 0.7, 1] }}
        transition={{ duration: 1.5, repeat: Infinity }}
        className="mt-6 text-neutral-600 dark:text-neutral-400 text-lg font-medium text-center"
      >
        {message}
      </motion.p>

      <motion.p
        animate={{ opacity: [0.7, 1, 0.7] }}
        transition={{ duration: 1.5, repeat: Infinity }}
        className="mt-2 text-neutral-500 dark:text-neutral-500 text-sm"
      >
        This usually takes a few seconds...
      </motion.p>
    </motion.div>
  );
};
