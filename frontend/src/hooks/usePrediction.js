import { useState } from 'react';
import { predictDisease } from '../services/api';

export const usePrediction = () => {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const predict = async (imageFile) => {
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const result = await predictDisease(imageFile);
      
      if (result.success) {
        setPrediction(result.data);
      } else {
        setError(result.error || 'Prediction failed');
      }
    } catch (err) {
      setError(err.message || 'Failed to predict disease');
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setPrediction(null);
    setError(null);
  };

  return {
    prediction,
    loading,
    error,
    predict,
    reset,
  };
};
