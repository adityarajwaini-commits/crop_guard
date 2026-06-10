import { useState } from 'react';
import { MAX_FILE_SIZE, ALLOWED_FILE_TYPES, MESSAGES } from '../services/constants';

export const useImageUpload = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState(null);

  const validateFile = (selectedFile) => {
    if (!selectedFile) {
      setError(MESSAGES.invalidFile);
      return false;
    }

    if (selectedFile.size > MAX_FILE_SIZE) {
      setError(MESSAGES.fileTooLarge);
      return false;
    }

    if (!ALLOWED_FILE_TYPES.includes(selectedFile.type)) {
      setError(MESSAGES.invalidFile);
      return false;
    }

    return true;
  };

  const handleFileSelect = (selectedFile) => {
    if (validateFile(selectedFile)) {
      setFile(selectedFile);
      setError(null);

      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target.result);
      };
      reader.readAsDataURL(selectedFile);
    }
  };

  const reset = () => {
    setFile(null);
    setPreview(null);
    setError(null);
  };

  return {
    file,
    preview,
    error,
    handleFileSelect,
    reset,
  };
};
