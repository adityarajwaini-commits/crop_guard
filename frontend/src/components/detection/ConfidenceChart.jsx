import { motion } from 'framer-motion';
import { formatDiseaseName } from '../../utils/formatters';

export const ConfidenceChart = ({ predictions = [] }) => {
  if (predictions.length === 0) return null;

  const maxValue = Math.max(...predictions.map(p => p.confidence), 1);

  return (
    <div className="bg-white dark:bg-neutral-800 rounded-xl p-6 shadow-lg">
      <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-6">
        Confidence Scores
      </h3>

      <div className="space-y-4">
        {predictions.map((pred, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex items-center gap-4"
          >
            {/* Label */}
            <div className="w-32 flex-shrink-0">
              <p className="font-medium text-neutral-900 dark:text-white text-sm">
                #{pred.rank} {formatDiseaseName(pred.disease_name)}
              </p>
            </div>

            {/* Bar */}
            <div className="flex-1">
              <div className="bg-neutral-200 dark:bg-neutral-700 rounded-full h-8 overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${(pred.confidence / maxValue) * 100}%` }}
                  transition={{ delay: index * 0.1 + 0.3, duration: 0.8 }}
                  className="h-full rounded-full"
                  style={{ backgroundColor: pred.color }}
                />
              </div>
            </div>

            {/* Percentage */}
            <div className="w-16 text-right flex-shrink-0">
              <p className="font-bold text-neutral-900 dark:text-white">
                {(pred.confidence * 100).toFixed(1)}%
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};
