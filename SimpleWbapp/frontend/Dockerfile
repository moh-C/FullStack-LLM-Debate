FROM node:16-alpine

WORKDIR /app

# Install create-react-app globally
RUN npm install -g create-react-app

# Copy the setup script into the container
COPY setup-react-app.sh /app/setup-react-app.sh

# Make the script executable
RUN chmod +x /app/setup-react-app.sh

# Set the command to run the setup script
CMD ["/app/setup-react-app.sh"]