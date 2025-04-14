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
        return `${config.API_BASE_URL}/${cleanEndpoint}`;
    }

    /**
     * Fetch data from an API endpoint
     * @param {string} endpoint - The API endpoint path (e.g. '/companies')
     * @param {Object} options - Fetch options
     * @returns {Promise} - Promise resolving to the fetched data
     */
    async fetchData(endpoint, options = {}) {
        this.isLoading = true;
        this.error = null;

        const url = this.buildApiUrl(endpoint);

        try {
            console.log(`Fetching data from: ${url}`);
            
            // Add CORS headers to options
            const fetchOptions = {
                ...options,
                headers: {
                    ...options.headers,
                    'Accept': 'application/json'
                },
                mode: 'cors'
            };
            
            const response = await fetch(url, fetchOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            this.data = data;
            return data;
        } catch (error) {
            this.error = error.message;
            console.error('Error fetching data:', error, 'from URL:', url);
            throw error;
        } finally {
            this.isLoading = false;
        }
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