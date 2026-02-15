#!/bin/bash
# setup.sh - Quick setup script for Job Monitor

echo "🚀 Job Monitor Setup"
echo "===================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create virtual environment (optional but recommended)
read -p "Create virtual environment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✓ Dependencies installed"
echo ""

# Prompt for API keys
echo "API Keys Setup"
echo "=============="
echo ""
echo "You need to get API keys from:"
echo "1. Google AI Studio: https://aistudio.google.com/"
echo "2. Adzuna: https://developer.adzuna.com/signup"
echo "3. SendGrid: https://signup.sendgrid.com/"
echo ""

read -p "Have you obtained all API keys? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Please get your API keys first, then run this script again."
    echo "See README.md for detailed instructions."
    exit 0
fi

# Create .env file
echo ""
echo "Creating .env file..."
echo "# Job Monitor Environment Variables" > .env
echo "# DO NOT COMMIT THIS FILE!" >> .env
echo "" >> .env

read -p "Google AI Key: " GOOGLE_AI_KEY
echo "export GOOGLE_AI_KEY=\"$GOOGLE_AI_KEY\"" >> .env

read -p "Adzuna App ID: " ADZUNA_APP_ID
echo "export ADZUNA_APP_ID=\"$ADZUNA_APP_ID\"" >> .env

read -p "Adzuna App Key: " ADZUNA_APP_KEY
echo "export ADZUNA_APP_KEY=\"$ADZUNA_APP_KEY\"" >> .env

read -p "SendGrid API Key: " SENDGRID_API_KEY
echo "export SENDGRID_API_KEY=\"$SENDGRID_API_KEY\"" >> .env

read -p "Email FROM (verified sender): " EMAIL_FROM
echo "export EMAIL_FROM=\"$EMAIL_FROM\"" >> .env

read -p "Email TO (your email): " EMAIL_TO
echo "export EMAIL_TO=\"$EMAIL_TO\"" >> .env

echo ""
echo "✓ .env file created"
echo ""

# Add .env to .gitignore
if [ ! -f .gitignore ]; then
    echo ".env" > .gitignore
    echo "jobs_seen.json" >> .gitignore
    echo "__pycache__/" >> .gitignore
    echo "*.pyc" >> .gitignore
    echo "venv/" >> .gitignore
    echo "✓ .gitignore created"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Load environment variables: source .env"
echo "2. Test the system: python main.py"
echo "3. Follow README.md to set up GitHub Actions"
echo ""
