#!/bin/sh

# Check if the app has already been created
if [ ! -f "package.json" ]; then
    echo "Creating new React app..."
    npx create-react-app .
else
    echo "React app already exists, skipping creation."
fi

# Install Tailwind CSS and its dependencies
echo "Installing Tailwind CSS..."
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest

# Initialize Tailwind CSS if it hasn't been initialized yet
if [ ! -f "tailwind.config.js" ]; then
    echo "Initializing Tailwind CSS..."
    npx tailwindcss init -p
    
    # Update tailwind.config.js
    echo "module.exports = { content: ['./src/**/*.{js,jsx,ts,tsx}'], theme: { extend: {} }, plugins: [] }" > tailwind.config.js
    
    # Add Tailwind directives to index.css
    echo "@tailwind base; @tailwind components; @tailwind utilities;" > src/index.css
else
    echo "Tailwind CSS already initialized, skipping."
fi

# Start the development server
echo "Starting the development server..."
npm start