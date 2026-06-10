import { SlideInUp } from '../animations/index';

export const About = () => {
  return (
    <div className="min-h-screen bg-gray-50 dark:from-neutral-900 dark:to-neutral-800">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <SlideInUp delay={0.1}>
          <div className="text-center mb-16">
            <h1 className="text-5xl font-display font-bold text-neutral-900 dark:text-white mb-4">
              About CropGuard
            </h1>
            <p className="text-xl text-neutral-800 dark:text-neutral-200 font-medium">
              Advanced AI-powered plant disease detection
            </p>
          </div>
        </SlideInUp>

        <div className="bg-white dark:bg-neutral-800 rounded-2xl shadow-xl p-8 space-y-8 border border-gray-200">
          <SlideInUp delay={0.2}>
            <section>
              <h2 className="text-3xl font-display font-bold text-neutral-900 dark:text-white mb-4">
                Our Mission
              </h2>
              <p className="text-lg text-neutral-800 dark:text-neutral-300 leading-relaxed font-medium">
                CropGuard is dedicated to empowering farmers and agricultural professionals with cutting-edge 
                AI technology to detect and manage plant diseases effectively. We believe that early detection 
                and informed treatment decisions can significantly improve crop yields and reduce agricultural losses.
              </p>
            </section>
          </SlideInUp>

          <SlideInUp delay={0.3}>
            <section>
              <h2 className="text-3xl font-display font-bold text-neutral-900 dark:text-white mb-4">
                How It Works
              </h2>
              <div className="space-y-4">
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 bg-emerald-500 text-white rounded-full flex items-center justify-center font-bold">
                    1
                  </div>
                  <div>
                    <h3 className="font-bold text-neutral-900 dark:text-white mb-2">Upload Image</h3>
                    <p className="text-neutral-800 dark:text-neutral-300 font-medium">
                      Simply take a photo of your plant leaf or upload an existing image
                    </p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 bg-emerald-500 text-white rounded-full flex items-center justify-center font-bold">
                    2
                  </div>
                  <div>
                    <h3 className="font-bold text-neutral-900 dark:text-white mb-2">AI Analysis</h3>
                    <p className="text-neutral-800 dark:text-neutral-300 font-medium">
                      Our neural network analyzes the image and compares it against thousands of known disease patterns
                    </p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 bg-emerald-500 text-white rounded-full flex items-center justify-center font-bold">
                    3
                  </div>
                  <div>
                    <h3 className="font-bold text-neutral-900 dark:text-white mb-2">Get Results</h3>
                    <p className="text-neutral-800 dark:text-neutral-300 font-medium">
                      Receive detailed diagnosis with confidence scores, treatment options, and prevention strategies
                    </p>
                  </div>
                </div>
              </div>
            </section>
          </SlideInUp>

          <SlideInUp delay={0.4}>
            <section>
              <h2 className="text-3xl font-display font-bold text-neutral-900 dark:text-white mb-4">
                Technology
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {['ResNet-50', 'PyTorch', 'ONNX Runtime', 'React', 'FastAPI', 'Tailwind CSS'].map((tech, idx) => (
                  <div key={idx} className="bg-gray-100 dark:bg-neutral-700 rounded-lg p-4 text-center border border-gray-200">
                    <p className="font-bold text-neutral-900 dark:text-white">{tech}</p>
                  </div>
                ))}
              </div>
            </section>
          </SlideInUp>

          <SlideInUp delay={0.5}>
            <section>
              <h2 className="text-3xl font-display font-bold text-neutral-900 dark:text-white mb-4">
                Supported Diseases
              </h2>
              <p className="text-neutral-800 dark:text-neutral-300 mb-4 font-medium">
                CropGuard can detect the following plant diseases:
              </p>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {[
                  'Early Blight',
                  'Late Blight',
                  'Septoria Leaf Spot',
                  'Yellow Leaf Curl Virus',
                  'Bacterial Spot',
                  'Target Spot',
                  'Plant Health Status',
                ].map((disease, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-neutral-700 dark:text-neutral-300">
                    <span className="text-emerald-500">✓</span>
                    {disease}
                  </li>
                ))}
              </ul>
            </section>
          </SlideInUp>

          <SlideInUp delay={0.6}>
            <section className="border-t border-neutral-200 dark:border-neutral-700 pt-8">
              <h2 className="text-3xl font-display font-bold text-neutral-900 dark:text-white mb-4">
                Model Performance
              </h2>
              <p className="text-lg text-neutral-700 dark:text-neutral-300 mb-6">
                CropGuard is powered by a ResNet-50 deep learning model trained on over 54,000 plant leaf images 
                spanning 38 disease and healthy crop classes from the PlantVillage dataset. The model has been 
                optimized using ONNX Runtime for fast and efficient real-time inference, enabling accurate disease 
                detection within seconds while maintaining high reliability across multiple crop species.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {[
                  { label: 'Accuracy', value: '98.35%', icon: '🎯' },
                  { label: 'Precision', value: '98.35%', icon: '✓' },
                  { label: 'Recall', value: '98.34%', icon: '🔍' },
                  { label: 'F1 Score', value: '98.34%', icon: '⭐' },
                ].map((metric, idx) => (
                  <div
                    key={idx}
                    className="bg-gradient-to-br from-emerald-50 to-emerald-100 dark:from-emerald-900/30 dark:to-emerald-800/30 
                               border-2 border-emerald-200 dark:border-emerald-700 rounded-xl p-6 text-center 
                               hover:shadow-lg hover:scale-105 transition-all duration-300"
                  >
                    <div className="text-4xl mb-3">{metric.icon}</div>
                    <p className="text-sm font-semibold text-neutral-600 dark:text-neutral-400 mb-2 uppercase tracking-wide">
                      {metric.label}
                    </p>
                    <p className="text-4xl font-bold text-emerald-600 dark:text-emerald-400">
                      {metric.value}
                    </p>
                  </div>
                ))}
              </div>
            </section>
          </SlideInUp>
        </div>
      </div>
    </div>
  );
};
