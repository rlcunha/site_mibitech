/**
 * PortfolioModel.js
 * Model for handling portfolio data
 */

import DataModel from './DataModel.js';

class PortfolioModel extends DataModel {
    constructor() {
        super();
        // Initialize with sample portfolio data
        this.setData(this.getSampleProjects());
        this.categories = ['all', 'web', 'mobile', 'desktop', 'cloud'];
        this.activeCategory = 'all';
    }

    /**
     * Get all portfolio projects
     * @returns {Array} - All portfolio projects
     */
    getAllProjects() {
        return this.getData() || [];
    }

    /**
     * Get projects by category
     * @param {string} category - The category to filter by
     * @returns {Array} - Projects in the specified category
     */
    getProjectsByCategory(category) {
        const projects = this.getData() || [];
        
        if (category === 'all') {
            return projects;
        }
        
        return projects.filter(project => project.category === category);
    }

    /**
     * Get a project by ID
     * @param {number} id - The project ID
     * @returns {Object|null} - The project with the specified ID or null
     */
    getProjectById(id) {
        const projects = this.getData() || [];
        return projects.find(project => project.id === id) || null;
    }

    /**
     * Get all available categories
     * @returns {Array} - All available categories
     */
    getCategories() {
        return this.categories;
    }

    /**
     * Set the active category
     * @param {string} category - The category to set as active
     */
    setActiveCategory(category) {
        if (this.categories.includes(category)) {
            this.activeCategory = category;
        }
    }

    /**
     * Get the active category
     * @returns {string} - The active category
     */
    getActiveCategory() {
        return this.activeCategory;
    }

    /**
     * Add a new project
     * @param {Object} project - The project to add
     */
    addProject(project) {
        const projects = this.getData() || [];
        const newProject = {
            id: this.generateId(),
            ...project
        };
        
        this.setData([...projects, newProject]);
    }

    /**
     * Update an existing project
     * @param {number} id - The ID of the project to update
     * @param {Object} updatedData - The updated project data
     * @returns {boolean} - True if updated successfully, false otherwise
     */
    updateProject(id, updatedData) {
        const projects = this.getData() || [];
        const index = projects.findIndex(project => project.id === id);
        
        if (index === -1) {
            return false;
        }
        
        projects[index] = { ...projects[index], ...updatedData };
        this.setData(projects);
        return true;
    }

    /**
     * Delete a project
     * @param {number} id - The ID of the project to delete
     * @returns {boolean} - True if deleted successfully, false otherwise
     */
    deleteProject(id) {
        const projects = this.getData() || [];
        const filteredProjects = projects.filter(project => project.id !== id);
        
        if (filteredProjects.length === projects.length) {
            return false;
        }
        
        this.setData(filteredProjects);
        return true;
    }

    /**
     * Generate a unique ID for a new project
     * @returns {number} - A unique ID
     */
    generateId() {
        const projects = this.getData() || [];
        const ids = projects.map(project => project.id);
        return ids.length > 0 ? Math.max(...ids) + 1 : 1;
    }

    /**
     * Get sample portfolio projects data
     * @returns {Array} - Sample portfolio projects
     */
    getSampleProjects() {
        return [
            {
                id: 1,
                title: 'E-commerce Premium',
                description: 'Plataforma completa de e-commerce com integração de pagamentos, gestão de estoque e painel administrativo personalizado.',
                category: 'web',
                image: '../public/images/project-1.jpg',
                technologies: ['React', 'Node.js', 'MongoDB'],
                client: 'Moda Express',
                year: 2024,
                link: '#'
            },
            {
                id: 2,
                title: 'FastFood Delivery',
                description: 'Aplicativo de delivery para restaurantes com rastreamento em tempo real, pagamento in-app e sistema de avaliação.',
                category: 'mobile',
                image: '../public/images/project-2.jpg',
                technologies: ['Flutter', 'Firebase', 'Google Maps API'],
                client: 'Sabor Gourmet',
                year: 2024,
                link: '#'
            },
            {
                id: 3,
                title: 'ERP Empresarial',
                description: 'Sistema completo de gestão empresarial com módulos de finanças, RH, vendas, compras e relatórios avançados.',
                category: 'desktop',
                image: '../public/images/project-3.jpg',
                technologies: ['C#', '.NET', 'SQL Server'],
                client: 'Construtech',
                year: 2023,
                link: '#'
            },
            {
                id: 4,
                title: 'DataInsight',
                description: 'Plataforma de análise de dados em tempo real com dashboards personalizáveis e insights automatizados.',
                category: 'cloud',
                image: '../public/images/project-4.jpg',
                technologies: ['Python', 'AWS', 'Tableau'],
                client: 'Banco Nacional',
                year: 2023,
                link: '#'
            },
            {
                id: 5,
                title: 'EduLearn',
                description: 'Plataforma de ensino online com cursos, avaliações, fóruns de discussão e certificados digitais.',
                category: 'web',
                image: '../public/images/project-5.jpg',
                technologies: ['Vue.js', 'Laravel', 'MySQL'],
                client: 'Instituto Educacional',
                year: 2022,
                link: '#'
            },
            {
                id: 6,
                title: 'HealthTrack',
                description: 'Aplicativo de monitoramento de saúde com integração a dispositivos wearables, lembretes de medicação e telemedicina.',
                category: 'mobile',
                image: '../public/images/project-6.jpg',
                technologies: ['React Native', 'GraphQL', 'MongoDB'],
                client: 'Clínica Saúde Total',
                year: 2022,
                link: '#'
            }
        ];
    }
}

export default PortfolioModel;