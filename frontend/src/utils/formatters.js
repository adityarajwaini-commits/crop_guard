/**
 * Utility function to format disease class names into user-friendly display names
 * 
 * Examples:
 * - "Tomato___Late_blight" → "Tomato – Late Blight"
 * - "Corn_(maize)___Northern_Leaf_Blight" → "Corn (Maize) – Northern Leaf Blight"
 * 
 * Transformation steps:
 * 1. Replace ___ with " – "
 * 2. Replace underscores with spaces
 * 3. Convert to Title Case
 */
export const formatDiseaseName = (name) => {
  if (!name || typeof name !== 'string') return name;
  
  // Replace ___ with " – "
  let formatted = name.replace(/___/g, ' – ');
  
  // Replace underscores with spaces
  formatted = formatted.replace(/_/g, ' ');
  
  // Convert to Title Case (capitalize first letter of each word)
  formatted = formatted
    .split(' ')
    .map(word => {
      // Handle special cases like (maize) and (including_sour)
      if (word.startsWith('(') && word.endsWith(')')) {
        // Keep parentheses, capitalize first letter inside
        const inner = word.slice(1, -1);
        return '(' + inner.charAt(0).toUpperCase() + inner.slice(1).toLowerCase() + ')';
      }
      // Capitalize first letter, lowercase the rest
      return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
    })
    .join(' ');
  
  return formatted;
};
