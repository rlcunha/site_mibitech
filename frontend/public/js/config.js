/**
 * Configurações do frontend
 * 
 * A URL base da API pode ser configurada de 3 formas (por ordem de prioridade):
 * 1. Através da variável de ambiente API_BASE_URL
 * 2. Através da meta tag <meta name="app-config" content='{"API_BASE_URL":"..."}'>
 * 3. Usando valores padrão baseados no ambiente (desenvolvimento/produção)
 */
const FRONTEND_CONFIG = {
    /**
     * URL base da API
     * @type {string}
     */
    // API_BASE_URL: window.APP_CONFIG?.API_BASE_URL
    //     || (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    //         ? 'http://localhost:8000'
    //         : 'http://apirest.mibitech.com.br:8000')

    API_BASE_URL: process.env.API_BASE_URL || 'http://localhost:8000'            
};

// Carrega configurações adicionais da meta tag se disponível
const configMeta = document.querySelector('meta[name="app-config"]');
if (configMeta) {
    try {
        Object.assign(FRONTEND_CONFIG, JSON.parse(configMeta.content));
    } catch (e) {
        console.warn('Failed to parse app config', e);
    }
}

export default FRONTEND_CONFIG;