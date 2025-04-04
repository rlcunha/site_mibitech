/**
 * CompanyController.js
 * Controller for handling company information display
 */

import CompanyModel from '../models/CompanyModel.js';

class CompanyController {
    constructor() {
        this.model = new CompanyModel();
        this.contactsContainer = null;
        this.socialMediaContainer = null;
        this.footerSocialContainer = null;
    }

    /**
     * Initialize the controller
     * @param {Object} options - Configuration options
     * @param {string} options.contactsContainer - Selector for contacts container
     * @param {string} options.socialMediaContainer - Selector for social media container
     * @param {string} options.footerSocialContainer - Selector for footer social media container
     */
    init(options = {}) {
        if (options.contactsContainer) {
            this.contactsContainer = document.querySelector(options.contactsContainer);
        }
        
        if (options.socialMediaContainer) {
            this.socialMediaContainer = document.querySelector(options.socialMediaContainer);
        }
        
        if (options.footerSocialContainer) {
            this.footerSocialContainer = document.querySelector(options.footerSocialContainer);
        }
        
        this.loadData();
    }

    /**
     * Load company data from the API
     */
    async loadData() {
        try {
            console.log('Loading company data...');
            // Load contacts and social media in parallel
            await Promise.all([
                this.loadContacts(),
                this.loadSocialMedia()
            ]);
            console.log('Company data loaded successfully');
        } catch (error) {
            console.error('Error loading company data:', error);
        }
    }

    /**
     * Load contact information
     */
    async loadContacts() {
        if (!this.contactsContainer) {
            console.warn('Contact container not found');
            return;
        }
        
        try {
            console.log('Loading contacts...');
            const contacts = await this.model.fetchContacts();
            console.log('Rendering contacts:', contacts);
            this.renderContacts(contacts);
        } catch (error) {
            console.error('Error loading contacts:', error);
            this.renderContactsError();
        }
    }

    /**
     * Load social media information
     */
    async loadSocialMedia() {
        try {
            console.log('Loading social media...');
            const socialMedia = await this.model.fetchSocialMedia();
            console.log('Social media loaded:', socialMedia);
            
            if (this.socialMediaContainer) {
                console.log('Rendering social media in container');
                this.renderSocialMedia(socialMedia, this.socialMediaContainer);
            } else {
                console.warn('Social media container not found');
            }
            
            if (this.footerSocialContainer) {
                console.log('Rendering social media in footer');
                this.renderFooterSocialMedia(socialMedia, this.footerSocialContainer);
            } else {
                console.warn('Footer social media container not found');
            }
        } catch (error) {
            console.error('Error loading social media:', error);
            
            if (this.socialMediaContainer) {
                this.renderSocialMediaError(this.socialMediaContainer);
            }
            
            if (this.footerSocialContainer) {
                this.renderSocialMediaError(this.footerSocialContainer);
            }
        }
    }

    /**
     * Render contacts in the container
     * @param {Array} contacts - Array of contact objects
     */
    renderContacts(contacts) {
        if (!this.contactsContainer) {
            console.warn('Contact container not found for rendering');
            return;
        }
        
        if (!contacts || contacts.length === 0) {
            console.warn('No contacts data to render');
            return;
        }
        
        console.log('Rendering contacts:', contacts);
        
        // Clear the container
        this.contactsContainer.innerHTML = '';
        
        // Create contact elements
        contacts.forEach(contact => {
            const contactElement = document.createElement('div');
            contactElement.className = 'contact-info mb-6';
            contactElement.innerHTML = `
                <h3 class="text-xl font-bold mb-2">${contact.name}</h3>
                <p class="mb-1"><i class="fas fa-envelope mr-2"></i> ${contact.email}</p>
                <p class="mb-1"><i class="fas fa-phone mr-2"></i> ${contact.phone}</p>
                <p class="mb-1"><i class="fas fa-map-marker-alt mr-2"></i> ${contact.address}</p>
            `;
            this.contactsContainer.appendChild(contactElement);
        });
    }

    /**
     * Render social media links in the container
     * @param {Array} socialMedia - Array of social media objects
     * @param {HTMLElement} container - Container element
     */
    renderSocialMedia(socialMedia, container) {
        if (!container) {
            console.warn('Social media container not found for rendering');
            return;
        }
        
        if (!socialMedia || socialMedia.length === 0) {
            console.warn('No social media data to render');
            return;
        }
        
        console.log('Rendering social media:', socialMedia);
        
        // Clear the container
        container.innerHTML = '';
        
        // Create social media elements
        socialMedia.forEach(social => {
            const socialElement = document.createElement('a');
            socialElement.href = social.url;
            socialElement.target = '_blank';
            socialElement.rel = 'noopener noreferrer';
            socialElement.className = 'social-icon bg-blue-600 text-white rounded-full w-10 h-10 flex items-center justify-center mr-3 hover:bg-blue-700 transition-colors';
            socialElement.innerHTML = `<i class="${social.icon}"></i>`;
            container.appendChild(socialElement);
        });
    }

    /**
     * Render social media links in the footer
     * @param {Array} socialMedia - Array of social media objects
     * @param {HTMLElement} container - Container element
     */
    renderFooterSocialMedia(socialMedia, container) {
        if (!container || !socialMedia || socialMedia.length === 0) return;
        
        // Clear the container
        container.innerHTML = '';
        
        // Create social media elements for footer (may have different styling)
        socialMedia.forEach(social => {
            const socialElement = document.createElement('a');
            socialElement.href = social.url;
            socialElement.target = '_blank';
            socialElement.rel = 'noopener noreferrer';
            socialElement.className = 'footer-social-icon';
            socialElement.innerHTML = `<i class="${social.icon}"></i>`;
            container.appendChild(socialElement);
        });
    }

    /**
     * Render error message for contacts
     */
    renderContactsError() {
        if (!this.contactsContainer) return;
        
        this.contactsContainer.innerHTML = `
            <div class="error-message">
                <p>Não foi possível carregar as informações de contato. Por favor, tente novamente mais tarde.</p>
            </div>
        `;
    }

    /**
     * Render error message for social media
     * @param {HTMLElement} container - Container element
     */
    renderSocialMediaError(container) {
        if (!container) return;
        
        container.innerHTML = `
            <div class="error-message">
                <p>Não foi possível carregar as redes sociais. Por favor, tente novamente mais tarde.</p>
            </div>
        `;
    }
}

export default CompanyController;