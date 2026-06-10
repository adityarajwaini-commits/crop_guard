import { motion } from 'framer-motion';
import { Badge } from '../common/index';
import { formatDiseaseName } from '../../utils/formatters';

export const TopPredictions = ({ predictions = [] }) => {
  if (predictions.length === 0) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {predictions.map((pred, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="bg-white dark:bg-neutral-800 rounded-lg p-4 shadow-md border-l-4"
          style={{ borderColor: pred.color }}
        >
          <div className="flex items-center justify-between mb-2">
            <Badge variant={index === 0 ? 'success' : 'default'}>
              Rank #{pred.rank}
            </Badge>
            <span className="text-2xl font-bold text-neutral-900 dark:text-white">
              {(pred.confidence * 100).toFixed(1)}%
            </span>
          </div>

          <p className="text-neutral-900 dark:text-white font-semibold">
            {formatDiseaseName(pred.disease_name)}
          </p>

          {/* Progress bar */}
          <div className="mt-3 bg-neutral-200 dark:bg-neutral-700 rounded-full h-2 overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${pred.confidence * 100}%` }}
              transition={{ delay: index * 0.1 + 0.3, duration: 0.8 }}
              className="h-full rounded-full"
              style={{ backgroundColor: pred.color }}
            />
          </div>
        </motion.div>
      ))}
    </div>
  );
};
