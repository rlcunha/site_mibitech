/**
 * CompanyModel.js
 * Model for handling company information including contacts and social media
 */

import DataModel from './DataModel.js';

class CompanyModel extends DataModel {
    constructor() {
        super();
        this.socialMedia = null;
    }

    /**
     * Fetch company social media information from the API
     * @returns {Promise} - Promise resolving to the social media data
     */
    async fetchSocialMedia() {
        this.isLoading = true;
        this.error = null;

        try {
            console.log('Fetching social media from API...');
            const apiUrl = window.location.hostname === 'localhost'
                ? 'http://localhost:8000/api/v1/social-media/'
                : '/api/v1/social-media/';
            console.log('Using API URL:', apiUrl);
            
            const data = await this.fetchData(apiUrl);
            console.log('Social media data received:', data);
            
            if (!data || !Array.isArray(data)) {
                throw new Error('Dados inválidos recebidos da API');
            }
            
            this.socialMedia = data;
            return data;
        } catch (error) {
            this.error = `Erro ao buscar redes sociais: ${error.message}`;
            console.error('Error details:', {
                message: error.message,
                stack: error.stack,
                url: 'http://localhost:8000/api/v1/social-media/'
            });
            //TODO: ajustar
            throw error;
        } finally {
            this.isLoading = false;
        }
    }
/**
 * Get the current social media data
 * @returns {Array|null} - The current social media data
 */
getSocialMedia() {
    return this.socialMedia;
}


    /**
     * Get a specific social media by ID
     * @param {number} id - The social media ID
     * @returns {Object|null} - The social media object or null if not found
     */
    getSocialMediaById(id) {
        if (!this.socialMedia) return null;
        return this.socialMedia.find(social => social.id === id) || null;
    }
}

export default CompanyModel;