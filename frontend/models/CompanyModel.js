/**
 * CompanyModel.js
 * Model for handling company information including contacts and social media
 */

import DataModel from './DataModel.js';

class CompanyModel extends DataModel {
    constructor() {
        super();
        this.contacts = null;
        this.socialMedia = null;
    }

    /**
     * Fetch company contact information from the API
     * @returns {Promise} - Promise resolving to the contact data
     */
    async fetchContacts() {
        this.isLoading = true;
        this.error = null;

        try {
            console.log('Fetching contacts from API...');
            const data = await this.fetchData('http://127.0.0.1:8000/api/contacts/');
            console.log('Contacts data received:', data);
            this.contacts = data;
            return data;
        } catch (error) {
            this.error = error.message;
            console.error('Error fetching contacts:', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
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
            const data = await this.fetchData('http://127.0.0.1:8000/api/social-media/');
            console.log('Social media data received:', data);
            this.socialMedia = data;
            return data;
        } catch (error) {
            this.error = error.message;
            console.error('Error fetching social media:', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Get the current contacts data
     * @returns {Array|null} - The current contacts data
     */
    getContacts() {
        return this.contacts;
    }

    /**
     * Get the current social media data
     * @returns {Array|null} - The current social media data
     */
    getSocialMedia() {
        return this.socialMedia;
    }

    /**
     * Get a specific contact by ID
     * @param {number} id - The contact ID
     * @returns {Object|null} - The contact object or null if not found
     */
    getContactById(id) {
        if (!this.contacts) return null;
        return this.contacts.find(contact => contact.id === id) || null;
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