import { motion } from 'framer-motion';
import { Button } from '../common/index';
import { useNavigate } from 'react-router-dom';
import { SlideInUp, FadeIn } from '../animations/index';

export const Landing = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: '🔍',
      title: 'AI-Powered Detection',
      description: 'Advanced machine learning identifies diseases with high accuracy',
    },
    {
      icon: '⚡',
      title: 'Instant Results',
      description: 'Get predictions in seconds, not hours',
    },
    {
      icon: '📊',
      title: 'Detailed Analysis',
      description: 'Symptoms, treatment, and prevention tips included',
    },
    {
      icon: '🛡️',
      title: 'Disease Prevention',
      description: 'Comprehensive preventive measures for each disease',
    },
    {
      icon: '📱',
      title: 'Mobile Friendly',
      description: 'Works on all devices, take it to the farm',
    },
    {
      icon: '🌍',
      title: 'Global Coverage',
      description: 'Trained on plants from around the world',
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-emerald-50 to-blue-50 dark:from-neutral-900 dark:to-neutral-800 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left: Text */}
            <SlideInUp delay={0.1}>
              <div>
                <h1 className="text-5xl md:text-6xl font-display font-bold text-neutral-900 dark:text-white mb-6">
                  Protect Your Crops with
                  <span className="text-gradient"> AI</span>
                </h1>
                <p className="text-xl text-neutral-800 dark:text-neutral-100 mb-8 leading-relaxed">
                  CropGuard uses cutting-edge artificial intelligence to detect plant diseases instantly. 
                  Get accurate diagnoses, treatment recommendations, and prevention tips.
                </p>
                <div className="flex flex-col sm:flex-row gap-4">
                  <Button
                    onClick={() => navigate('/detection')}
                    variant="primary"
                    size="lg"
                  >
                    Get Started
                  </Button>
                  <Button
                    onClick={() => navigate('/about')}
                    variant="outline"
                    size="lg"
                  >
                    Learn More
                  </Button>
                </div>
              </div>
            </SlideInUp>

            {/* Right: Illustration */}
            <FadeIn delay={0.3}>
              <div className="text-center">
                <div className="text-8xl mb-4 animate-bounce-slow">🌿</div>
                <div className="text-7xl mb-4">🤖</div>
                <div className="text-8xl">📊</div>
              </div>
            </FadeIn>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50 dark:bg-neutral-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SlideInUp delay={0.1}>
            <div className="text-center mb-16">
              <h2 className="text-4xl font-display font-bold text-neutral-900 dark:text-white mb-4">
                Why Choose CropGuard?
              </h2>
              <p className="text-xl text-neutral-800 dark:text-neutral-200 font-medium">
                Professional-grade disease detection for modern farming
              </p>
            </div>
          </SlideInUp>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 + idx * 0.1 }}
                className="bg-white dark:bg-neutral-800 rounded-xl p-6 border border-gray-200 hover:shadow-lg transition"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold text-neutral-900 dark:text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-neutral-800 dark:text-neutral-200 font-medium">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-emerald-500 to-blue-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <SlideInUp delay={0.1}>
            <h2 className="text-4xl font-display font-bold text-white mb-6">
              Ready to Protect Your Plants?
            </h2>
            <p className="text-xl text-white mb-8">
              Start analyzing your plants with CropGuard today. It's free and easy to use.
            </p>
            <Button
              onClick={() => navigate('/detection')}
              variant="cta"
              size="lg"
            >
              Launch Detection Tool
            </Button>
          </SlideInUp>
        </div>
      </section>
    </div>
  );
};
