/**
 * app.js
 * Main application file that initializes the MVC structure
 */

import RouterController from '../../controllers/RouterController.js';
import ContactController from '../../controllers/ContactController.js';
import PortfolioController from '../../controllers/PortfolioController.js';
import CompanyController from '../../controllers/CompanyController.js';

class App {
    constructor() {
        // Initialize controllers
        this.router = new RouterController();
        this.contactController = new ContactController();
        this.portfolioController = new PortfolioController();
        
        // Get DOM elements
        this.loadingIndicator = document.getElementById('loading-indicator');
        this.contentContainer = document.getElementById('content-container');
        
        // Bind methods to this instance
        this.initializeRoutes = this.initializeRoutes.bind(this);
        this.loadPage = this.loadPage.bind(this);
    }

    /**
     * Initialize the application
     */
    init() {
        // Initialize routes
        this.initializeRoutes();
        
        // Initialize page-specific functionality based on current route
        this.initializeCurrentPage();
        
        console.log('MibiTech application initialized');
    }

    /**
     * Initialize routes
     */
    initializeRoutes() {
        // Register routes
        this.router.registerRoute('/', () => this.loadPage('index'));
        this.router.registerRoute('/index.html', () => this.loadPage('index'));
        this.router.registerRoute('/sobre.html', () => this.loadPage('sobre'));
        this.router.registerRoute('/portfolio.html', () => this.loadPage('portfolio'));
        this.router.registerRoute('/blog.html', () => this.loadPage('blog'));
        this.router.registerRoute('/contato.html', () => this.loadPage('contato'));
        
        // Register 404 route
        this.router.registerNotFound(() => this.loadPage('404'));
    }

    /**
     * Load a page
     * @param {string} pageName - The name of the page to load
     */
    async loadPage(pageName) {
        try {
            console.log(`Loading page: ${pageName}`);
            
            // Show loading indicator
            if (this.loadingIndicator) {
                this.loadingIndicator.style.display = 'flex';
            }
            if (this.contentContainer) {
                this.contentContainer.style.display = 'none';
            }
            
            // Load page content
            const response = await fetch(`/views/${pageName}.html`);
            
            if (!response.ok) {
                throw new Error(`Failed to load ${pageName}: ${response.status} ${response.statusText}`);
            }
            
            let html = await response.text();
            
            // Fix relative paths in the HTML content
            html = html.replace(/\.\.\/public\//g, '/public/');
            
            // Update content container
            if (this.contentContainer) {
                this.contentContainer.innerHTML = html;
                this.contentContainer.style.display = 'block';
            } else {
                // Fallback to router's loadContent method
                this.router.loadContent(html);
            }
            
            console.log(`Page ${pageName} loaded successfully`);
            
            // Hide loading indicator
            if (this.loadingIndicator) {
                this.loadingIndicator.style.display = 'none';
            }
            
            // Initialize page-specific functionality
            this.initializePage(pageName);
            
            // Scroll to top
            window.scrollTo(0, 0);
            
            // Update page title
            this.updatePageTitle(pageName);
        } catch (error) {
            console.error(`Error loading page ${pageName}:`, error);
            
            // Show error message
            if (this.contentContainer) {
                this.contentContainer.innerHTML = `
                    <div class="text-center py-20">
                        <h2 class="text-2xl font-bold text-red-600 mb-4">Erro ao carregar a página</h2>
                        <p class="text-gray-700">${error.message}</p>
                    </div>
                `;
                this.contentContainer.style.display = 'block';
            }
            
            // Hide loading indicator
            if (this.loadingIndicator) {
                this.loadingIndicator.style.display = 'none';
            }
        }
    }

    /**
     * Initialize page-specific functionality
     * @param {string} pageName - The name of the page to initialize
     */
    initializePage(pageName) {
        switch (pageName) {
            case 'index':
                this.initializeHomePage();
                break;
            case 'sobre':
                this.initializeAboutPage();
                break;
            case 'portfolio':
                this.initializePortfolioPage();
                break;
            case 'blog':
                this.initializeBlogPage();
                break;
            case 'contato':
                this.initializeContactPage();
                break;
            case '404':
                // No specific initialization for 404 page
                break;
            default:
                console.warn(`No specific initialization for page ${pageName}`);
        }
    }

    /**
     * Initialize the current page based on the current route
     */
    initializeCurrentPage() {
        const path = window.location.pathname;
        
        if (path === '/' || path.endsWith('index.html')) {
            this.initializeHomePage();
        } else if (path.endsWith('sobre.html')) {
            this.initializeAboutPage();
        } else if (path.endsWith('portfolio.html')) {
            this.initializePortfolioPage();
        } else if (path.endsWith('blog.html')) {
            this.initializeBlogPage();
        } else if (path.endsWith('contato.html')) {
            this.initializeContactPage();
        }
    }

    /**
     * Initialize home page functionality
     */
    initializeHomePage() {
        console.log('Initializing home page');
        
        // Initialize animations
        this.initializeAnimations();
        
        // Initialize service cards hover effect
        const serviceCards = document.querySelectorAll('.service-card');
        
        serviceCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                const icon = card.querySelector('.service-icon');
                if (icon) icon.classList.add('scale-in');
            });
            
            card.addEventListener('mouseleave', () => {
                const icon = card.querySelector('.service-icon');
                if (icon) icon.classList.remove('scale-in');
            });
        });
    }

    /**
     * Initialize about page functionality
     */
    initializeAboutPage() {
        console.log('Initializing about page');
        
        // Initialize animations
        this.initializeAnimations();
        
        // Initialize counter animation for stats
        const statCounters = document.querySelectorAll('.stat-counter');
        
        if (statCounters.length > 0) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const counter = entry.target;
                        const target = parseInt(counter.getAttribute('data-target'), 10);
                        const duration = 2000; // ms
                        const step = Math.ceil(target / (duration / 16)); // 60fps
                        
                        let current = 0;
                        const timer = setInterval(() => {
                            current += step;
                            counter.textContent = current;
                            
                            if (current >= target) {
                                counter.textContent = target;
                                clearInterval(timer);
                            }
                        }, 16);
                        
                        observer.unobserve(counter);
                    }
                });
            }, { threshold: 0.5 });
            
            statCounters.forEach(counter => {
                observer.observe(counter);
            });
        }
    }

    /**
     * Initialize portfolio page functionality
     */
    initializePortfolioPage() {
        console.log('Initializing portfolio page');
        
        // Initialize portfolio controller
        this.portfolioController.init('portfolio-grid');
        
        // Initialize animations
        this.initializeAnimations();
    }

    /**
     * Initialize blog page functionality
     */
    initializeBlogPage() {
        console.log('Initializing blog page');
        
        // Initialize animations
        this.initializeAnimations();
        
        // Initialize blog search functionality
        const searchInput = document.querySelector('.blog-search input');
        
        if (searchInput) {
            searchInput.addEventListener('input', (event) => {
                const searchTerm = event.target.value.toLowerCase();
                const blogPosts = document.querySelectorAll('.blog-post');
                
                blogPosts.forEach(post => {
                    const title = post.querySelector('h3').textContent.toLowerCase();
                    const content = post.querySelector('p').textContent.toLowerCase();
                    
                    if (title.includes(searchTerm) || content.includes(searchTerm)) {
                        post.style.display = 'block';
                    } else {
                        post.style.display = 'none';
                    }
                });
            });
        }
        
        // Initialize blog category filter
        const categoryLinks = document.querySelectorAll('.blog-category');
        
        categoryLinks.forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                
                // Remove active class from all category links
                categoryLinks.forEach(link => {
                    link.classList.remove('bg-blue-600', 'text-white');
                    link.classList.add('bg-gray-200', 'text-gray-700');
                });
                
                // Add active class to clicked link
                link.classList.remove('bg-gray-200', 'text-gray-700');
                link.classList.add('bg-blue-600', 'text-white');
                
                const category = link.getAttribute('data-category');
                const blogPosts = document.querySelectorAll('.blog-post');
                
                blogPosts.forEach(post => {
                    if (category === 'all' || post.getAttribute('data-category') === category) {
                        post.style.display = 'block';
                    } else {
                        post.style.display = 'none';
                    }
                });
            });
        });
    }

    /**
     * Initialize contact page functionality
     */
    initializeContactPage() {
        console.log('Initializing contact page');
        
        // Initialize contact form controller
        this.contactController.init({
            contactContainer: '.contact-info-container',
            messageForm: '#contactForm',
            messageLog: '#messageLog'
        });
        
        // Initialize company information (contacts and social media)
        const companyController = new CompanyController();
        companyController.init({
            socialMediaContainer: '.social-media-container',
            footerSocialContainer: '.footer-social-container'
        });
        
        // Initialize animations
        this.initializeAnimations();
        
        // Initialize FAQ accordion
        const faqToggles = document.querySelectorAll('.faq-toggle');
        
        faqToggles.forEach(toggle => {
            toggle.addEventListener('click', () => {
                const content = toggle.nextElementSibling;
                const icon = toggle.querySelector('i');
                
                // Toggle aria-expanded attribute
                const expanded = toggle.getAttribute('aria-expanded') === 'true' || false;
                toggle.setAttribute('aria-expanded', !expanded);
                
                // Toggle content visibility
                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                    content.classList.add('hidden');
                    icon.classList.remove('transform', 'rotate-180');
                } else {
                    content.classList.remove('hidden');
                    content.style.maxHeight = content.scrollHeight + 'px';
                    icon.classList.add('transform', 'rotate-180');
                }
            });
        });
    }

    /**
     * Initialize animations
     */
    initializeAnimations() {
        const animatedElements = document.querySelectorAll('.animate-on-scroll');
        
        if (animatedElements.length > 0) {
            // Create intersection observer
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const element = entry.target;
                        const animation = element.getAttribute('data-animation') || 'fade-in';
                        element.classList.add(animation);
                        observer.unobserve(element);
                    }
                });
            }, {
                threshold: 0.1
            });
            
            // Observe all elements with animation classes
            animatedElements.forEach(element => {
                observer.observe(element);
            });
        }
    }

    /**
     * Update page title based on the current page
     * @param {string} pageName - The name of the current page
     */
    updatePageTitle(pageName) {
        const baseTitle = 'MibiTech';
        let pageTitle = '';
        
        switch (pageName) {
            case 'index':
                pageTitle = 'Soluções em TI';
                break;
            case 'sobre':
                pageTitle = 'Sobre Nós';
                break;
            case 'portfolio':
                pageTitle = 'Portfólio';
                break;
            case 'blog':
                pageTitle = 'Blog';
                break;
            case 'contato':
                pageTitle = 'Contato';
                break;
            case '404':
                pageTitle = 'Página não encontrada';
                break;
            default:
                pageTitle = '';
        }
        
        document.title = pageTitle ? `${baseTitle} - ${pageTitle}` : baseTitle;
    }
}

// Export the App class
export default App;

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new App();
    app.init();
    
    // Make app globally accessible for debugging
    window.app = app;
});