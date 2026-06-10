import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card } from '../common/index';
import { formatDiseaseName } from '../../utils/formatters';

export const DiseaseCard = ({ disease }) => {
  const [expandedSection, setExpandedSection] = useState('symptoms');

  if (!disease) return null;

  const getSeverityColor = (severity) => {
    const colors = {
      none: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100',
      low_to_medium: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100',
      medium: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100',
      high: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100',
      unknown: 'bg-neutral-100 text-neutral-800 dark:bg-neutral-900 dark:text-neutral-100',
    };
    return colors[severity] || colors.unknown;
  };

  const sections = [
    {
      id: 'symptoms',
      label: '🔍 Symptoms',
      icon: '🔍',
      content: disease.symptoms,
    },
    {
      id: 'treatment',
      label: '💊 Treatment',
      icon: '💊',
      content: disease.treatment,
    },
    {
      id: 'prevention',
      label: '🛡️ Prevention',
      icon: '🛡️',
      content: disease.prevention,
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full"
    >
      <Card>
        {/* Header */}
        <div className="mb-6 pb-6 border-b border-neutral-200 dark:border-neutral-700">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h2 className="text-3xl font-display font-bold text-neutral-900 dark:text-white mb-1">
                {formatDiseaseName(disease.name)}
              </h2>
              <p className="text-neutral-700 dark:text-neutral-300 italic">
                {disease.scientific_name}
              </p>
            </div>
            <span
              className="text-3xl"
              style={{ backgroundColor: disease.color + '20', color: disease.color }}
            >
              ●
            </span>
          </div>

          <div className="flex flex-wrap gap-3">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSeverityColor(disease.severity)}`}>
              Severity: {disease.severity.replace('_', ' ').toUpperCase()}
            </span>
          </div>

          <p className="mt-4 text-neutral-700 dark:text-neutral-300">
            {disease.description}
          </p>
        </div>

        {/* Sections */}
        <div className="space-y-4">
          {sections.map((section) => (
            <div key={section.id} className="border border-neutral-200 dark:border-neutral-700 rounded-lg overflow-hidden">
              {/* Section Header */}
              <motion.button
                onClick={() => setExpandedSection(expandedSection === section.id ? null : section.id)}
                className="w-full px-4 py-3 flex items-center justify-between bg-neutral-50 dark:bg-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition"
                whileHover={{ backgroundColor: expandedSection === section.id ? undefined : '#f3f4f6' }}
              >
                <span className="font-semibold text-neutral-900 dark:text-white flex items-center gap-2">
                  <span>{section.icon}</span>
                  {section.label}
                </span>
                <motion.span
                  animate={{ rotate: expandedSection === section.id ? 180 : 0 }}
                  className="text-xl"
                >
                  ▼
                </motion.span>
              </motion.button>

              {/* Section Content */}
              <AnimatePresence>
                {expandedSection === section.id && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="px-4 py-4 bg-white dark:bg-neutral-900"
                  >
                    <ul className="space-y-2">
                      {section.content.map((item, idx) => (
                        <motion.li
                          key={idx}
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: idx * 0.05 }}
                          className="flex gap-3 text-neutral-700 dark:text-neutral-300"
                        >
                          <span className="text-emerald-500 flex-shrink-0 mt-1">✓</span>
                          <span>{item}</span>
                        </motion.li>
                      ))}
                    </ul>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))}
        </div>
      </Card>
    </motion.div>
  );
};
