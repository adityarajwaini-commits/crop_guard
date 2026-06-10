import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ThemeToggle } from '../common/ThemeToggle';

export const Navbar = () => {
  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="bg-white dark:bg-neutral-900 shadow-md sticky top-0 z-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link
            to="/"
            className="text-2xl font-display font-bold text-gradient hover:opacity-80 transition"
          >
            🌿 CropGuard
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center gap-8">
            <Link
              to="/"
              className="text-neutral-700 dark:text-neutral-300 hover:text-emerald-500 transition"
            >
              Home
            </Link>
            <Link
              to="/detection"
              className="text-neutral-700 dark:text-neutral-300 hover:text-emerald-500 transition"
            >
              Detection
            </Link>
            <Link
              to="/about"
              className="text-neutral-700 dark:text-neutral-300 hover:text-emerald-500 transition"
            >
              About
            </Link>
          </div>

          {/* Theme Toggle */}
          <ThemeToggle />
        </div>
      </div>
    </motion.nav>
  );
};
