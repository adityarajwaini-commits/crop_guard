import { useTheme } from '../../context/ThemeContext';
import { motion } from 'framer-motion';

export const ThemeToggle = () => {
  const { isDark, toggleTheme } = useTheme();

  return (
    <motion.button
      onClick={toggleTheme}
      className="p-2 rounded-lg bg-neutral-200 dark:bg-neutral-700 text-neutral-800 dark:text-white hover:bg-neutral-300 dark:hover:bg-neutral-600 transition-colors"
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      aria-label="Toggle dark mode"
    >
      {isDark ? '☀️' : '🌙'}
    </motion.button>
  );
};
