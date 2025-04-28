/**
 * DataModel.js
 * Base model class for handling data operations
 */

let config;
try {
    // Try to load test config first
    config = (await import('../tests/config.test.js')).default;
} catch {
    // Fallback to regular config
    config = (await import('../public/js/config.js')).default;
}

class DataModel {
    constructor() {
        this.data = null;
        this.error = null;
        this.isLoading = false;
    }

    /**
     * Build full API URL from endpoint path
     * @param {string} endpoint - API endpoint path (e.g. '/companies')
     * @returns {string} Full API URL
     */
    buildApiUrl(endpoint) {
        // Remove leading/trailing slashes for consistency
        const cleanEndpoint = endpoint.replace(/^\/|\/$/g, '');
        // Usar a URL base da API definida na configuração
        const baseUrl = config.API_BASE_URL;
        return `${baseUrl}/${cleanEndpoint}`;
    }

    /**
     * Fetch data from an API endpoint with retry mechanism
     * @param {string} endpoint - The API endpoint path (e.g. '/companies')
     * @param {Object} options - Fetch options
     * @param {number} retries - Number of retries (default: 3)
     * @returns {Promise} - Promise resolving to the fetched data
     */
    async fetchData(endpoint, options = {}, retries = 3) {
        this.isLoading = true;
        this.error = null;

        const url = this.buildApiUrl(endpoint);

        // Implementação de retry com backoff exponencial
        for (let attempt = 0; attempt <= retries; attempt++) {
            try {
                console.log(`Fetching data from: ${url} (attempt ${attempt + 1}/${retries + 1})`);
                
                // Add CORS headers to options
                const fetchOptions = {
                    ...options,
                    headers: {
                        ...options.headers,
                        'Accept': 'application/json',
                        'Origin': window.location.origin
                    },
                    mode: 'cors',
                    // Adicionar cache: 'no-cache' para evitar problemas de cache
                    cache: 'no-cache',
                    // Adicionar credentials: 'same-origin' para cookies e autenticação
                    credentials: 'same-origin'
                };
                
                // Verificar se a URL é acessível
                console.log(`Tentando acessar: ${url} com opções:`, fetchOptions);
                
                const response = await fetch(url, fetchOptions);
                
                if (!response.ok) {
                    console.warn(`HTTP error! Status: ${response.status}, Statustext: ${response.statusText}`);
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                
                const data = await response.json();
                this.data = data;
                return data;
            } catch (error) {
                this.error = error.message;
                console.error(`Tentativa ${attempt + 1}/${retries + 1} falhou:`, error);
                
                // Se for o último retry, lança o erro
                if (attempt === retries) {
                    console.error('Todas as tentativas falharam ao acessar:', url);
                    console.error('Detalhes do erro:', error);
                    console.error('Verifique se o servidor está rodando e se as configurações CORS estão corretas');
                    throw error;
                }
                
                // Espera antes de tentar novamente (backoff exponencial)
                const waitTime = Math.min(1000 * Math.pow(2, attempt), 10000);
                console.log(`Aguardando ${waitTime}ms antes da próxima tentativa...`);
                await new Promise(resolve => setTimeout(resolve, waitTime));
            }
        }
        
        this.isLoading = false;
    }

    /**
     * Post data to an API endpoint
     * @param {string} endpoint - The API endpoint path (e.g. '/companies')
     * @param {Object} data - The data to post
     * @param {Object} options - Additional fetch options
     * @returns {Promise} - Promise resolving to the response data
     */
    async postData(endpoint, data, options = {}) {
        this.isLoading = true;
        this.error = null;

        const url = this.buildApiUrl(endpoint);

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                body: JSON.stringify(data),
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const responseData = await response.json();
            return responseData;
        } catch (error) {
            this.error = error.message;
            console.error('Error posting data:', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }
}

export default DataModel;