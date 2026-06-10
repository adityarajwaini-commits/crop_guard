import { motion } from 'framer-motion';

export const ImagePreview = ({ src, onRemove }) => {
  if (!src) return null;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="relative rounded-xl overflow-hidden shadow-lg"
    >
      <img
        src={src}
        alt="Preview"
        className="w-full h-auto max-h-96 object-cover"
      />

      {onRemove && (
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={onRemove}
          className="absolute top-4 right-4 bg-red-500 hover:bg-red-600 text-white p-2 rounded-full shadow-lg transition"
        >
          ✕
        </motion.button>
      )}
    </motion.div>
  );
};
