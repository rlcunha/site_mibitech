/**
 * RouterController.js
 * Controller for handling page routing and navigation
 */

class RouterController {
    constructor() {
        this.routes = {};
        this.currentRoute = null;
        this.notFoundCallback = null;
        this.rootElement = document.getElementById('app') || document.body;
        
        // Bind methods to this instance
        this.navigate = this.navigate.bind(this);
        this.handlePopState = this.handlePopState.bind(this);
        
        // Initialize router
        this.init();
    }

    /**
     * Initialize the router
     */
    init() {
        // Listen for popstate events (browser back/forward buttons)
        window.addEventListener('popstate', this.handlePopState);
        
        // Intercept link clicks for SPA navigation
        document.addEventListener('click', (event) => {
            // Check if the clicked element is a link
            const link = event.target.closest('a');
            
            if (link && link.href && link.href.startsWith(window.location.origin)) {
                // Prevent default link behavior
                event.preventDefault();
                
                // Extract the path from the link
                const path = link.pathname;
                
                // Navigate to the path
                this.navigate(path);
            }
        });
        
        // Initial route handling
        this.handlePopState();
    }

    /**
     * Register a route
     * @param {string} path - The route path
     * @param {Function} callback - The callback function to execute when the route is matched
     */
    registerRoute(path, callback) {
        this.routes[path] = callback;
    }

    /**
     * Register a not found handler
     * @param {Function} callback - The callback function to execute when no route is matched
     */
    registerNotFound(callback) {
        this.notFoundCallback = callback;
    }

    /**
     * Navigate to a path
     * @param {string} path - The path to navigate to
     * @param {boolean} pushState - Whether to push a new state to the history
     */
    navigate(path, pushState = true) {
        // Update browser history if pushState is true
        if (pushState) {
            window.history.pushState({ path }, '', path);
        }
        
        // Store the current route
        this.currentRoute = path;
        
        // Find and execute the matching route callback
        const routeCallback = this.routes[path];
        
        if (routeCallback) {
            routeCallback();
        } else if (this.notFoundCallback) {
            this.notFoundCallback();
        }
    }

    /**
     * Handle popstate events (browser back/forward buttons)
     */
    handlePopState() {
        const path = window.location.pathname;
        this.navigate(path, false);
    }

    /**
     * Get the current route
     * @returns {string} - The current route
     */
    getCurrentRoute() {
        return this.currentRoute;
    }

    /**
     * Load HTML content into the root element
     * @param {string} html - The HTML content to load
     */
    loadContent(html) {
        this.rootElement.innerHTML = html;
    }

    /**
     * Load HTML content from a file
     * @param {string} filePath - The path to the HTML file
     * @returns {Promise} - Promise resolving when the content is loaded
     */
    async loadContentFromFile(filePath) {
        try {
            const response = await fetch(filePath);
            
            if (!response.ok) {
                throw new Error(`Failed to load ${filePath}: ${response.status} ${response.statusText}`);
            }
            
            let html = await response.text();
            
            // Fix relative paths in the HTML content
            // Replace "../public/" with "/public/" to ensure paths resolve correctly
            html = html.replace(/\.\.\/public\//g, '/public/');
            
            this.loadContent(html);
        } catch (error) {
            console.error('Error loading content:', error);
            
            if (this.notFoundCallback) {
                this.notFoundCallback();
            }
        }
    }

    /**
     * Redirect to a different path
     * @param {string} path - The path to redirect to
     */
    redirect(path) {
        this.navigate(path);
    }

    /**
     * Extract parameters from a route pattern and path
     * @param {string} pattern - The route pattern (e.g., '/blog/:id')
     * @param {string} path - The actual path (e.g., '/blog/123')
     * @returns {Object|null} - The extracted parameters or null if the pattern doesn't match
     */
    extractParams(pattern, path) {
        // Convert pattern to regex
        const paramNames = [];
        const regexPattern = pattern.replace(/:([^/]+)/g, (match, paramName) => {
            paramNames.push(paramName);
            return '([^/]+)';
        });
        
        const regex = new RegExp(`^${regexPattern}$`);
        const match = path.match(regex);
        
        if (!match) {
            return null;
        }
        
        // Extract parameters
        const params = {};
        paramNames.forEach((name, index) => {
            params[name] = match[index + 1];
        });
        
        return params;
    }
}

export default RouterController;