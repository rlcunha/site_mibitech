// Frontend configuration
const FRONTEND_CONFIG = {
    API_BASE_URL: window.location.hostname === 'localhost'
        ? window.APP_CONFIG?.API_BASE_URL || 'http://localhost:8000'
        : '/api'
};

// Load config from meta tag if available
const configMeta = document.querySelector('meta[name="app-config"]');
if (configMeta) {
    try {
        Object.assign(FRONTEND_CONFIG, JSON.parse(configMeta.content));
    } catch (e) {
        console.warn('Failed to parse app config', e);
    }
}

export default FRONTEND_CONFIG;