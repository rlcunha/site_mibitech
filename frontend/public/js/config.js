/**
 * Configurações do frontend
 * 
 * A configuração segue a seguinte ordem de prioridade:
 * 1. Objeto window.ENV (injetado pelo servidor a partir das variáveis de ambiente)
 * 2. Meta tag <meta name="app-config" content='{"API_BASE_URL":"..."}'>
 * 3. Valores padrão baseados no ambiente (desenvolvimento/produção)
 */
const FRONTEND_CONFIG = {
    /**
     * URL base da API
     * @type {string}
     */
    API_BASE_URL: window.ENV?.API_BASE_URL 
        || (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? 'http://localhost:8000'
            : 'http://apirest.mibitech.com.br:8000'),
            
    /**
     * Ambiente de execução
     * @type {string}
     */
    NODE_ENV: window.ENV?.NODE_ENV || 'development',
    
    /**
     * Versão da aplicação
     * @type {string}
     */
    VERSION: window.ENV?.VERSION || '1.0.0'
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