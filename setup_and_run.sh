#!/bin/bash

# Update system and install required packages
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip git postgresql postgresql-contrib

# Clone the repository (replace with your actual repository URL)
git clone https://github.com/your_username/your_repo_name.git
cd your_repo_name

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Set up the database (adjust these values according to your configuration)
sudo -u postgres psql -c "CREATE DATABASE your_database_name;"
sudo -u postgres psql -c "CREATE USER your_username WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "ALTER ROLE your_username SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE your_username SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE your_username SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;"

# Create .env file
cat << EOF > .env
PGHOST=localhost
PGDATABASE=your_database_name
PGUSER=your_username
PGPASSWORD=your_password
PGPORT=5432
GITHUB_API_TOKEN=your_github_token
GITLAB_API_TOKEN=your_gitlab_token
BITBUCKET_USERNAME=your_bitbucket_username
BITBUCKET_APP_PASSWORD=your_bitbucket_app_password
STACKOVERFLOW_API_KEY=your_stackoverflow_api_key
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_key
EOF

echo "Setup complete. Please edit the .env file with your actual API keys and database credentials."
echo "To run the project, use the following commands:"
echo "source venv/bin/activate"
echo "python main.py --collect --process --fine-tune"
echo "python app.py"
