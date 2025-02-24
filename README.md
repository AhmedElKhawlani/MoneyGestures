# MoneyGestures

MoneyGestures is a web application designed for personal money management. It allows users to manage their transactions, budgets, and accounts efficiently.

## Features
- Add and manage transactions with details like category, description, amount, and date.
- Create and track budgets.
- View detailed summaries of your financial data.

## Getting Started

### Prerequisites
- Ensure you have Python 3.10+ installed.
- Make sure `pip` is installed.
- Install MySQL and configure it to use the `money_management` database.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AhmedElKhawlani/MoneyGestures.git
   cd MoneyGestures
   ```

2. Run the installation script to install the required dependencies:
   ```bash
   ./install.sh
   ```

3. Set up the database:
   - Create a MySQL database named `money_management`.
   - Update the database configuration in the `model.py` file if needed.

### Running the Application

Start the application by running:
   ```bash
   ./run_app.sh
   ```

### Scripts

#### `install.sh`
This script installs all the required dependencies for the project. It ensures your environment is ready to run the application.

#### `run_app.sh`
This script starts the Flask application server, allowing you to use MoneyGestures locally.

## Contact
For any inquiries, please contact the project maintainer via [GitHub Issues](https://github.com/AhmedElKhawlani/MoneyGestures/issues).