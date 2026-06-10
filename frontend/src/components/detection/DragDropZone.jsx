import { useRef } from 'react';
import { motion } from 'framer-motion';
import { Button } from '../common/index';

export const DragDropZone = ({ onFileSelect, isLoading, disabled = false }) => {
  const fileInputRef = useRef(null);
  const dragCounter = useRef(0);

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter.current += 1;
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter.current -= 1;
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounter.current = 0;

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      onFileSelect(files[0]);
    }
  };

  const handleFileSelect = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      onFileSelect(files[0]);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`border-2 border-dashed border-neutral-300 dark:border-neutral-600 rounded-xl p-8 text-center cursor-pointer transition-colors ${
        dragCounter.current > 0
          ? 'bg-emerald-50 dark:bg-emerald-900/10 border-emerald-500'
          : 'hover:border-emerald-500 hover:bg-emerald-50 dark:hover:bg-emerald-900/10'
      } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <div className="flex flex-col items-center gap-4">
        <div className="text-5xl">🖼️</div>
        <div>
          <p className="text-lg font-bold text-neutral-900 dark:text-white">
            Drag and drop your plant image here
          </p>
          <p className="text-neutral-800 dark:text-neutral-300 text-sm mt-1 font-medium">
            or click to browse (JPG, PNG, WebP)
          </p>
        </div>

        <Button
          onClick={() => fileInputRef.current?.click()}
          variant="primary"
          disabled={isLoading || disabled}
        >
          {isLoading ? 'Analyzing...' : 'Select Image'}
        </Button>

        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          className="hidden"
          disabled={isLoading || disabled}
        />

        <p className="text-xs text-neutral-500 dark:text-neutral-500 mt-4">
          Maximum file size: 10MB
        </p>
      </div>
    </motion.div>
  );
};
