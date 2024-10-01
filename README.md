# C++ and Python Dataset Creation and Model Fine-tuning

This project creates a comprehensive dataset of C++ and Python code samples from various sources and fine-tunes a code generation model.

## Setup and Installation

1. Clone this repository:
   ```
   git clone https://github.com/your_username/your_repo_name.git
   cd your_repo_name
   ```

2. Run the setup script:
   ```
   ./setup_and_run.sh
   ```

   This script will:
   - Update the system and install required packages
   - Set up a virtual environment
   - Install Python dependencies
   - Set up the PostgreSQL database
   - Create a `.env` file for environment variables

3. After running the setup script, edit the `.env` file with your actual API keys and database credentials.

4. Initialize the database:
   ```
   python database/initialize_db.py
   ```

   This step creates all the necessary tables in the database.

## Running the Project

To run the project, use the following commands:

1. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

2. Run the main script to collect data, process it, and fine-tune the model:
   ```
   python main.py --collect --process --fine-tune
   ```

3. Start the web interface:
   ```
   python app.py
   ```

## Project Structure

- `data_collection/`: Scripts for collecting code samples from various sources
- `data_processing/`: Scripts for cleaning and organizing the collected samples
- `model_fine_tuning/`: Scripts for fine-tuning the code generation model
- `database/`: Database operations and schema
- `templates/`: HTML templates for the web interface
- `app.py`: Flask application for the web interface
- `config.py`: Configuration settings for the project
- `main.py`: Main script to run the entire pipeline

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.
