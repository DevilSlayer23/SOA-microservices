cho "Creating necessary directories..."
mkdir -p dockerfiles nginx
# Creates the folders if they don't exist

echo "Creating Dockerfiles for each app..."

# List of all your apps
apps=("gateway" "products" "cart" "order" )

# Loop through each app and create its Dockerfile
for app in "${apps[@]}"; do
    cat > "dockerfiles/Dockerfile.$app" <<EOF
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    postgresql-client \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \\
    pip install -r requirements.txt

# Copy entire project
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media

EXPOSE 8001
EOF
    echo "Created Dockerfile.$app"
done

echo "Creating .dockerignore file..."
cat > .dockerignore <<EOF
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.venv
*.log
*.pot
*.db
*.sqlite3
.git
.gitignore
.dockerignore
docker-compose*.yml
README.md
*.md
.DS_Store
node_modules/
.idea/
.vscode/
*.swp
*.swo
*~
EOF

echo "Creating .env file template..."
cat > .env.example <<EOF
# Django Settings
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://admin:P@ssW0rd@db:5432/ecommerce_db

# Redis
REDIS_URL=redis://redis:6379/0

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EOF

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and update values"
echo "2. Ensure your Django settings.py is configured to use environment variables"
echo "3. Run: docker-compose up --build"