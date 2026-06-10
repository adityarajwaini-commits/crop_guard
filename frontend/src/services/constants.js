// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// File upload settings
export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
export const ALLOWED_FILE_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
export const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp'];

// UI Constants
export const SEVERITY_LEVELS = {
  none: { label: 'No Disease', color: '#10B981', bgColor: '#D1FAE5' },
  low_to_medium: { label: 'Low to Medium', color: '#F59E0B', bgColor: '#FEF3C7' },
  medium: { label: 'Medium', color: '#FFA500', bgColor: '#FED7AA' },
  high: { label: 'High', color: '#DC2626', bgColor: '#FEE2E2' },
  unknown: { label: 'Unknown', color: '#6B7280', bgColor: '#F3F4F6' },
};

// Messages
export const MESSAGES = {
  uploadError: 'Failed to upload image. Please try again.',
  analysisError: 'Failed to analyze image. Please try again.',
  invalidFile: 'Invalid file. Please upload a JPG, PNG, or WebP image.',
  fileTooLarge: `File is too large. Maximum size is ${MAX_FILE_SIZE / 1024 / 1024}MB.`,
  analyzing: 'Analyzing your plant image...',
  success: 'Analysis complete!',
};
