/**
 * server.js
 * Simple HTTP server for the MibiTech frontend application teste de git
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

// Define the port to use
const PORT = process.env.PORT || 3000;

// MIME types for different file extensions
const MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',  // Updated to modern MIME type
    '.mjs': 'application/javascript', // Add support for module files
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.ttf': 'font/ttf',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.eot': 'application/vnd.ms-fontobject',
    '.otf': 'font/otf',
    '.wasm': 'application/wasm'  // Add WebAssembly support
};

// Proxy configuration
const API_BASE_URL = 'http://apirest.mibitech.com.br:8000';

// Create the HTTP server
const server = http.createServer((req, res) => {
    console.log(`${req.method} ${req.url}`);
    
    // Handle API requests
    if (req.url.startsWith('/api/')) {
        const apiUrl = `${API_BASE_URL}${req.url}`;
        console.log(`Proxying to API: ${apiUrl}`);
        
        const proxyReq = http.request(apiUrl, (proxyRes) => {
            res.writeHead(proxyRes.statusCode, proxyRes.headers);
            proxyRes.pipe(res, { end: true });
        });
        
        req.pipe(proxyReq, { end: true });
        return;
    }
    
    // Parse the URL for static files
    let filePath = req.url;
    
    // Handle root URL
    if (filePath === '/') {
        filePath = '/index.html';
    }
    
    // Resolve the file path
    // Handle path traversal safely
    filePath = path.join(__dirname, ...filePath.split('/').filter(p => !p.includes('..')));
    
    // Get the file extension
    const extname = path.extname(filePath).toLowerCase();
    
    // Get the MIME type
    const contentType = MIME_TYPES[extname] || 'application/octet-stream';
    
    // Read the file
    fs.readFile(filePath, (err, content) => {
        if (err) {
            // If the file doesn't exist, check if it exists in the views directory
            if (err.code === 'ENOENT') {
                // Only fallback for HTML requests
                if (extname === '.html') {
                    // Extract the filename from the path
                    const filename = path.basename(filePath);
                    
                    // Check if the file exists in the views directory
                    const viewsFilePath = path.join(__dirname, 'views', filename);
                    
                    fs.readFile(viewsFilePath, (viewsErr, viewsContent) => {
                        if (viewsErr) {
                            // If not found in views either, fallback to index.html
                            fs.readFile(path.join(__dirname, 'views', 'index.html'), (indexErr, indexContent) => {
                                if (indexErr) {
                                    res.writeHead(404, { 'Content-Type': 'text/html' });
                                    res.end('<h1>404 Not Found</h1>');
                                    return;
                                }
                                
                                // Serve index.html
                                res.writeHead(200, { 'Content-Type': 'text/html' });
                                res.end(indexContent, 'utf-8');
                            });
                        } else {
                            // Serve the file from views directory
                            res.writeHead(200, { 'Content-Type': 'text/html' });
                            res.end(viewsContent, 'utf-8');
                        }
                    });
                } else {
                    // Not an HTML file, return 404
                    res.writeHead(404);
                    res.end(`File not found: ${req.url}`);
                }
            } else {
                // Server error
                res.writeHead(500);
                res.end(`Server Error: ${err.code}`);
            }
        } else {
            // Serve the file
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

// Start the server
server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
    console.log(`Press Ctrl+C to stop the server`);
});