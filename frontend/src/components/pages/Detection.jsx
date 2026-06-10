import { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '../common/index';
import { useImageUpload } from '../../hooks/useImageUpload';
import { usePrediction } from '../../hooks/usePrediction';
import { formatDiseaseName } from '../../utils/formatters';
import { DragDropZone } from '../detection/DragDropZone';
import { ImagePreview } from '../detection/ImagePreview';
import { LoadingSpinner } from '../detection/LoadingSpinner';
import { TopPredictions } from '../detection/TopPredictions';
import { ConfidenceChart } from '../detection/ConfidenceChart';
import { DiseaseCard } from '../detection/DiseaseCard';
import { ErrorAlert } from '../common/index';
import { SlideInUp, FadeIn } from '../animations/index';

export const Detection = () => {
  const { file, preview, error: uploadError, handleFileSelect, reset: resetUpload } = useImageUpload();
  const { prediction, loading, error: predictionError, predict, reset: resetPrediction } = usePrediction();

  const handleAnalyze = async () => {
    if (file) {
      await predict(file);
    }
  };

  const handleReset = () => {
    resetUpload();
    resetPrediction();
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:from-neutral-900 dark:to-neutral-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Header */}
        <SlideInUp delay={0.1}>
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-display font-bold text-gradient mb-4">
              Plant Disease Detection
            </h1>
            <p className="text-xl text-neutral-800 dark:text-neutral-200 font-medium">
              Upload a leaf image to get instant disease diagnosis
            </p>
          </div>
        </SlideInUp>

        {/* Guidelines & Supported Crops Info Card */}
        {!prediction && (
          <SlideInUp delay={0.15}>
            <div className="bg-white dark:bg-neutral-800 rounded-2xl shadow-xl p-6 mb-8 border border-gray-200">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Upload Guidelines */}
                <div>
                  <h3 className="text-lg font-display font-bold text-neutral-900 dark:text-white mb-3 flex items-center gap-2">
                    <span>📸</span> Upload Guidelines
                  </h3>
                  <ul className="space-y-2">
                    <li className="flex gap-2 text-neutral-700 dark:text-neutral-300 text-sm font-medium">
                      <span className="text-emerald-500">•</span>
                      Upload a clear close-up image of a single leaf
                    </li>
                    <li className="flex gap-2 text-neutral-700 dark:text-neutral-300 text-sm font-medium">
                      <span className="text-emerald-500">•</span>
                      Ensure good lighting and focus
                    </li>
                    <li className="flex gap-2 text-neutral-700 dark:text-neutral-300 text-sm font-medium">
                      <span className="text-emerald-500">•</span>
                      Capture visible disease symptoms
                    </li>
                    <li className="flex gap-2 text-neutral-700 dark:text-neutral-300 text-sm font-medium">
                      <span className="text-emerald-500">•</span>
                      Avoid blurry or distant images
                    </li>
                  </ul>
                </div>

                {/* Supported Crops */}
                <div>
                  <h3 className="text-lg font-display font-bold text-neutral-900 dark:text-white mb-3 flex items-center gap-2">
                    <span>🌱</span> Supported Crops (14)
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {['Apple', 'Tomato', 'Potato', 'Corn (Maize)', 'Grape', 'Pepper', 'Strawberry', 'Cherry', 'Orange', 'Peach', 'Blueberry', 'Raspberry', 'Soybean', 'Squash'].map((crop) => (
                      <span
                        key={crop}
                        className="inline-block px-3 py-1.5 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 rounded-full text-xs font-semibold"
                      >
                        {crop}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Note */}
              <div className="mt-4 pt-4 border-t border-gray-200 dark:border-neutral-700">
                <p className="text-xs text-neutral-600 dark:text-neutral-400 font-medium">
                  🚀 CropGuard is continuously evolving with improved detection accuracy and broader crop support. Currently supporting 38 disease and healthy plant categories across the crops listed above.
                </p>
              </div>
            </div>
          </SlideInUp>
        )}

        {/* Main Content */}
        {!prediction ? (
          <SlideInUp delay={0.2}>
            <div className="bg-white dark:bg-neutral-800 rounded-2xl shadow-xl p-8 mb-8 border border-gray-200">
              {/* Upload Section */}
              <div className="mb-8">
                {!preview ? (
                  <DragDropZone
                    onFileSelect={handleFileSelect}
                    isLoading={loading}
                  />
                ) : (
                  <div>
                    <ImagePreview
                      src={preview}
                      onRemove={() => {
                        resetUpload();
                        resetPrediction();
                      }}
                    />

                    <div className="mt-6 flex gap-4 justify-center">
                      <Button
                        onClick={handleAnalyze}
                        variant="primary"
                        size="lg"
                        disabled={loading}
                      >
                        {loading ? 'Analyzing...' : 'Analyze Image'}
                      </Button>
                      <Button
                        onClick={() => resetUpload()}
                        variant="outline"
                        size="lg"
                        disabled={loading}
                      >
                        Choose Another
                      </Button>
                    </div>
                  </div>
                )}
              </div>

              {/* Error Messages */}
              {(uploadError || predictionError) && (
                <ErrorAlert
                  message={uploadError || predictionError}
                />
              )}

              {/* Loading State */}
              {loading && <LoadingSpinner />}
            </div>
          </SlideInUp>
        ) : (
          /* Results View */
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-8"
          >
            {/* Image and Summary */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="lg:col-span-1"
              >
                <ImagePreview src={preview} />
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="lg:col-span-2"
              >
                <div className="bg-white dark:bg-neutral-800 rounded-xl p-6 shadow-lg">
                  <h2 className="text-2xl font-display font-bold text-neutral-900 dark:text-white mb-4">
                    Analysis Result
                  </h2>

                  <div className="mb-6 p-4 bg-emerald-50 dark:bg-emerald-900/20 border-l-4 border-emerald-500 rounded">
                    <p className="text-neutral-700 dark:text-neutral-300">
                      <span className="font-semibold">Primary Diagnosis:</span>{' '}
                      <span className="text-xl font-bold text-emerald-600 dark:text-emerald-400">
                        {formatDiseaseName(prediction?.prediction?.primary_disease)}
                      </span>
                    </p>
                    <p className="text-neutral-600 dark:text-neutral-400 mt-2">
                      <span className="font-semibold">Confidence:</span>{' '}
                      <span className="text-lg font-bold">
                        {(prediction?.prediction?.confidence * 100).toFixed(1)}%
                      </span>
                    </p>
                  </div>

                  <TopPredictions predictions={prediction?.top_3} />

                  <div className="mt-6 flex gap-4">
                    <Button
                      onClick={handleReset}
                      variant="primary"
                      size="lg"
                      className="flex-1"
                    >
                      Analyze Another
                    </Button>
                    <Button
                      onClick={() => window.print()}
                      variant="outline"
                      size="lg"
                      className="flex-1"
                    >
                      Print Report
                    </Button>
                  </div>
                </div>
              </motion.div>
            </div>

            {/* Charts */}
            <FadeIn delay={0.3}>
              <ConfidenceChart predictions={prediction?.top_3} />
            </FadeIn>

            {/* Disease Details */}
            <FadeIn delay={0.4}>
              <DiseaseCard disease={prediction?.disease_details} />
            </FadeIn>
          </motion.div>
        )}
      </div>
    </div>
  );
};
