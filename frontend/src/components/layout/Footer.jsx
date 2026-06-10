export const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-50 dark:bg-neutral-900 border-t border-gray-200 dark:border-neutral-800 mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <h3 className="text-lg font-display font-bold text-gradient mb-2">
              CropGuard
            </h3>
            <p className="text-neutral-800 dark:text-neutral-300 text-sm font-medium">
              Advanced plant disease detection powered by AI
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-bold text-neutral-900 dark:text-white mb-4">
              Product
            </h4>
            <ul className="space-y-2 text-sm text-neutral-800 dark:text-neutral-300 font-medium">
              <li><a href="#" className="hover:text-emerald-600 transition">Detection</a></li>
              <li><a href="#" className="hover:text-emerald-600 transition">Features</a></li>
              <li><a href="#" className="hover:text-emerald-600 transition">Pricing</a></li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h4 className="font-bold text-neutral-900 dark:text-white mb-4">
              Support
            </h4>
            <ul className="space-y-2 text-sm text-neutral-800 dark:text-neutral-300 font-medium">
              <li><a href="#" className="hover:text-emerald-600 transition">Documentation</a></li>
              <li><a href="#" className="hover:text-emerald-600 transition">FAQ</a></li>
              <li><a href="#" className="hover:text-emerald-600 transition">Contact</a></li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h4 className="font-bold text-neutral-900 dark:text-white mb-4">
              Connect
            </h4>
            <div className="flex gap-4">
              <a href="#" className="text-neutral-800 dark:text-neutral-300 hover:text-emerald-600 transition font-medium">
                Twitter
              </a>
              <a href="#" className="text-neutral-800 dark:text-neutral-300 hover:text-emerald-600 transition font-medium">
                GitHub
              </a>
              <a href="#" className="text-neutral-800 dark:text-neutral-300 hover:text-emerald-600 transition font-medium">
                LinkedIn
              </a>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-gray-200 dark:border-neutral-800 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-neutral-800 dark:text-neutral-300 text-sm font-medium">
            © {currentYear} CropGuard. All rights reserved.
          </p>
          <div className="flex gap-6 text-sm text-neutral-800 dark:text-neutral-300 mt-4 md:mt-0 font-medium">
            <a href="#" className="hover:text-emerald-600 transition">Privacy Policy</a>
            <a href="#" className="hover:text-emerald-600 transition">Terms of Service</a>
          </div>
        </div>
      </div>
    </footer>
  );
};
