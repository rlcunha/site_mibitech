/**
 * CompanyController.js
 * Controller for handling company social media information
 */

import CompanyModel from '../models/CompanyModel.js';

class CompanyController {
    constructor() {
        this.model = new CompanyModel();
        this.socialMediaContainer = null;
        this.footerSocialContainer = null;
    }

    /**
     * Initialize the controller
     * @param {Object} options - Configuration options
     * @param {string} options.socialMediaContainer - Selector for social media container
     * @param {string} options.footerSocialContainer - Selector for footer social media container
     */
    init(options = {}) {
        if (options.socialMediaContainer) {
            this.socialMediaContainer = document.querySelector(options.socialMediaContainer);
        }
        
        if (options.footerSocialContainer) {
            this.footerSocialContainer = document.querySelector(options.footerSocialContainer);
        }
        
        this.loadSocialMedia();
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