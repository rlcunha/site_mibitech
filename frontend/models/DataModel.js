/**
 * DataModel.js
 * Base model class for handling data operations
 */

class DataModel {
    constructor() {
        this.data = null;
        this.error = null;
        this.isLoading = false;
    }

    /**
     * Fetch data from an API endpoint
     * @param {string} url - The API endpoint URL
     * @param {Object} options - Fetch options
     * @returns {Promise} - Promise resolving to the fetched data
     */
    async fetchData(url, options = {}) {
        this.isLoading = true;
        this.error = null;

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
     * @param {string} url - The API endpoint URL
     * @param {Object} data - The data to post
     * @param {Object} options - Additional fetch options
     * @returns {Promise} - Promise resolving to the response data
     */
    async postData(url, data, options = {}) {
        this.isLoading = true;
        this.error = null;

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

    /**
     * Get the current data
     * @returns {Object} - The current data
     */
    getData() {
        return this.data;
    }

    /**
     * Get the current error
     * @returns {string|null} - The current error message or null
     */
    getError() {
        return this.error;
    }

    /**
     * Check if data is currently loading
     * @returns {boolean} - True if data is loading, false otherwise
     */
    getIsLoading() {
        return this.isLoading;
    }

    /**
     * Set data manually
     * @param {Object} data - The data to set
     */
    setData(data) {
        this.data = data;
    }

    /**
     * Clear the current data
     */
    clearData() {
        this.data = null;
    }

    /**
     * Clear the current error
     */
    clearError() {
        this.error = null;
    }
}

export default DataModel;