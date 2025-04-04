/**
 * index.js
 * Entry point for the MibiTech frontend application
 */

// Import the main app
import App from './public/js/app.js';

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new App();
    app.init();
    
    // Make app globally accessible for debugging
    window.app = app;
    
    console.log('MibiTech application initialized');
});