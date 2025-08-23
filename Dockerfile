# Intentionally broken Dockerfile for testing
# Multiple Docker-related issues

FROM node:18-alpine

# Missing WORKDIR
COPY package.json .  # Will fail because package.json doesn't exist
RUN npm install      # Will fail because of missing package.json

# Copy source code
COPY src/ /app/src/

# Invalid instruction syntax
EXPOSE port 3000  # Should be just "EXPOSE 3000"

# Missing executable permissions
COPY broken-script.sh /usr/local/bin/
RUN broken-script.sh  # Will fail because script doesn't exist

# Wrong base image for Python code
RUN pip install flask  # pip doesn't exist in Node image

# Invalid environment variable syntax
ENV DATABASE_URL=postgresql://user:password@localhost:5432/db
ENV MISSING_VALUE  # Missing value

# Wrong CMD format
CMD npm start  # Should be ["npm", "start"] for exec form

# Unreachable instruction (after CMD)
RUN echo "This will never run"
