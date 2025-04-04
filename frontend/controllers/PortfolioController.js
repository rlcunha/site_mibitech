/**
 * PortfolioController.js
 * Controller for handling portfolio interactions
 */

import PortfolioModel from '../models/PortfolioModel.js';

class PortfolioController {
    constructor() {
        this.model = new PortfolioModel();
        this.portfolioGrid = null;
        this.filterButtons = [];
        
        // Bind methods to this instance
        this.handleFilterClick = this.handleFilterClick.bind(this);
        this.renderProjects = this.renderProjects.bind(this);
    }

    /**
     * Initialize the controller
     * @param {string} gridId - The ID of the portfolio grid element
     * @param {string} filterContainerId - The ID of the filter buttons container
     */
    init(gridId = 'portfolio-grid', filterContainerId = null) {
        // Get portfolio grid element
        this.portfolioGrid = document.getElementById(gridId);
        
        if (!this.portfolioGrid) {
            console.error(`Portfolio grid with ID "${gridId}" not found.`);
            return;
        }
        
        // Get filter buttons
        if (filterContainerId) {
            const filterContainer = document.getElementById(filterContainerId);
            
            if (filterContainer) {
                this.filterButtons = filterContainer.querySelectorAll('.filter-btn');
                
                // Add click event listeners to filter buttons
                this.filterButtons.forEach(button => {
                    button.addEventListener('click', () => {
                        const category = button.getAttribute('data-filter');
                        this.handleFilterClick(category, button);
                    });
                });
            }
        } else {
            // If no filter container ID is provided, look for filter buttons directly
            this.filterButtons = document.querySelectorAll('.filter-btn');
            
            // Add click event listeners to filter buttons
            this.filterButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const category = button.getAttribute('data-filter');
                    this.handleFilterClick(category, button);
                });
            });
        }
        
        // Render initial projects
        this.renderProjects();
    }

    /**
     * Handle filter button click
     * @param {string} category - The category to filter by
     * @param {HTMLElement} clickedButton - The clicked filter button
     */
    handleFilterClick(category, clickedButton) {
        // Update active category in model
        this.model.setActiveCategory(category);
        
        // Update active button styling
        this.filterButtons.forEach(button => {
            if (button === clickedButton) {
                button.classList.add('active', 'bg-blue-600', 'text-white');
                button.classList.remove('bg-gray-200', 'text-gray-700');
            } else {
                button.classList.remove('active', 'bg-blue-600', 'text-white');
                button.classList.add('bg-gray-200', 'text-gray-700');
            }
        });
        
        // Render filtered projects
        this.renderProjects();
    }

    /**
     * Render portfolio projects
     */
    renderProjects() {
        if (!this.portfolioGrid) return;
        
        // Get active category
        const activeCategory = this.model.getActiveCategory();
        
        // Get projects for the active category
        const projects = this.model.getProjectsByCategory(activeCategory);
        
        // Clear portfolio grid
        this.portfolioGrid.innerHTML = '';
        
        // Render projects
        projects.forEach(project => {
            const projectElement = this.createProjectElement(project);
            this.portfolioGrid.appendChild(projectElement);
        });
        
        // If no projects found, show a message
        if (projects.length === 0) {
            const noProjectsMessage = document.createElement('div');
            noProjectsMessage.className = 'col-span-full text-center py-12';
            noProjectsMessage.innerHTML = `
                <p class="text-gray-500 text-lg">Nenhum projeto encontrado na categoria "${activeCategory}".</p>
            `;
            this.portfolioGrid.appendChild(noProjectsMessage);
        }
    }

    /**
     * Create a project element
     * @param {Object} project - The project data
     * @returns {HTMLElement} - The project element
     */
    createProjectElement(project) {
        const projectElement = document.createElement('div');
        projectElement.className = 'portfolio-item';
        projectElement.setAttribute('data-category', project.category);
        
        // Create project HTML
        projectElement.innerHTML = `
            <div class="bg-white rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition duration-300">
                <div class="relative">
                    <img src="${project.image}" alt="${project.title}" class="w-full h-64 object-cover">
                    <div class="absolute inset-0 bg-blue-600 bg-opacity-80 flex items-center justify-center opacity-0 hover:opacity-100 transition duration-300">
                        <a href="#" class="text-white bg-transparent hover:bg-white hover:text-blue-600 border border-white font-bold py-2 px-4 rounded-lg transition duration-300 mx-2" data-project-id="${project.id}">Ver Detalhes</a>
                    </div>
                </div>
                <div class="p-6">
                    <h3 class="text-xl font-bold mb-2">${project.title}</h3>
                    <p class="text-gray-600 mb-4">${project.description}</p>
                    <div class="flex flex-wrap gap-2">
                        ${project.technologies.map(tech => `
                            <span class="px-3 py-1 bg-blue-100 text-blue-600 rounded-full text-sm">${tech}</span>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
        
        // Add click event listener to the "Ver Detalhes" button
        const detailsButton = projectElement.querySelector(`[data-project-id="${project.id}"]`);
        
        if (detailsButton) {
            detailsButton.addEventListener('click', (event) => {
                event.preventDefault();
                this.showProjectDetails(project.id);
            });
        }
        
        return projectElement;
    }

    /**
     * Show project details
     * @param {number} projectId - The ID of the project to show details for
     */
    showProjectDetails(projectId) {
        // Get project data
        const project = this.model.getProjectById(projectId);
        
        if (!project) {
            console.error(`Project with ID ${projectId} not found.`);
            return;
        }
        
        // Create modal element
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50';
        
        // Create modal content
        modal.innerHTML = `
            <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-90vh overflow-y-auto">
                <div class="relative">
                    <img src="${project.image}" alt="${project.title}" class="w-full h-64 md:h-80 object-cover">
                    <button class="absolute top-4 right-4 bg-white rounded-full p-2 shadow-md hover:bg-gray-100 transition duration-300 modal-close">
                        <i class="fas fa-times text-gray-600"></i>
                    </button>
                </div>
                <div class="p-6">
                    <h2 class="text-3xl font-bold mb-4">${project.title}</h2>
                    <p class="text-gray-600 mb-6">${project.description}</p>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div>
                            <h3 class="text-xl font-semibold mb-3">Detalhes do Projeto</h3>
                            <ul class="space-y-2">
                                <li class="flex items-start">
                                    <span class="font-medium mr-2">Cliente:</span>
                                    <span class="text-gray-600">${project.client}</span>
                                </li>
                                <li class="flex items-start">
                                    <span class="font-medium mr-2">Ano:</span>
                                    <span class="text-gray-600">${project.year}</span>
                                </li>
                                <li class="flex items-start">
                                    <span class="font-medium mr-2">Categoria:</span>
                                    <span class="text-gray-600">${project.category.charAt(0).toUpperCase() + project.category.slice(1)}</span>
                                </li>
                            </ul>
                        </div>
                        <div>
                            <h3 class="text-xl font-semibold mb-3">Tecnologias Utilizadas</h3>
                            <div class="flex flex-wrap gap-2">
                                ${project.technologies.map(tech => `
                                    <span class="px-3 py-1 bg-blue-100 text-blue-600 rounded-full text-sm">${tech}</span>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                    
                    <div class="flex justify-center mt-6">
                        <a href="${project.link}" target="_blank" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg transition duration-300">Visitar Projeto</a>
                    </div>
                </div>
            </div>
        `;
        
        // Add modal to the document
        document.body.appendChild(modal);
        
        // Prevent body scrolling
        document.body.style.overflow = 'hidden';
        
        // Add click event listener to close button
        const closeButton = modal.querySelector('.modal-close');
        
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                this.closeModal(modal);
            });
        }
        
        // Close modal when clicking outside
        modal.addEventListener('click', (event) => {
            if (event.target === modal) {
                this.closeModal(modal);
            }
        });
        
        // Close modal when pressing Escape key
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') {
                this.closeModal(modal);
            }
        });
    }

    /**
     * Close modal
     * @param {HTMLElement} modal - The modal element to close
     */
    closeModal(modal) {
        // Remove modal from the document
        modal.remove();
        
        // Restore body scrolling
        document.body.style.overflow = '';
    }
}

export default PortfolioController;