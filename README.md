# Natural Language Search for PostgreSQL Database

## Objective

This project implements a Natural Language Search interface for querying a PostgreSQL database using Streamlit. It allows users to query the database using natural language, which is then converted to SQL using a Large Language Model (LLM).

## Database Schema

The project uses a PostgreSQL database with the following tables:

### 1. employees (Employee details)

| Column Name   | Data Type         | Description                                   |
|---------------|-------------------|-----------------------------------------------|
| id            | SERIAL PRIMARY KEY | Unique identifier for an employee             |
| name          | VARCHAR(100)      | Full name                                     |
| department_id | INT               | Foreign key linking to departments            |
| email         | VARCHAR(255)      | Email address                                 |
| salary        | DECIMAL(10,2)     | Monthly salary                                |

### 2. departments (List of company departments)

| Column Name | Data Type         | Description                 |
|-------------|-------------------|-----------------------------|
| id          | SERIAL PRIMARY KEY | Unique department ID        |
| name        | VARCHAR(100)      | Department name (e.g., HR, Engineering) |

### 3. orders (Customer orders data)

| Column Name   | Data Type         | Description                               |
|---------------|-------------------|-------------------------------------------|
| id            | SERIAL PRIMARY KEY | Unique order ID                           |
| customer_name | VARCHAR(100)      | Name of the customer                      |
| employee_id   | INT               | Foreign key linking to employees (who handled the order) |
| order_total   | DECIMAL(10,2)     | Total order amount                        |
| order_date    | DATE              | Date of order                             |

### 4. products (Product catalog)

| Column Name | Data Type         | Description           |
|-------------|-------------------|-----------------------|
| id          | SERIAL PRIMARY KEY | Unique product ID      |
| name        | VARCHAR(100)      | Product name          |
| price       | DECIMAL(10,2)     | Price per unit        |

### Relationships

* `employees.department_id` → `departments.id` (Each employee belongs to a department)
* `orders.employee_id` → `employees.id` (Each order is handled by an employee)

## Task Steps

### 1. Set Up the PostgreSQL Database

1.  Create the tables as described above.
2.  Populate the database with sample data.
3.  Store vector embeddings for text fields (e.g., product names, customer names) using `pgvector`.
4.  Create HNSW indexes on the vector embedding columns for efficient similarity searches.

### 2. Implement Natural Language Search

1.  Use an LLM (e.g., Gemini) to convert user queries into SQL.
2.  Validate the generated SQL queries before execution to prevent SQL injection.
3.  Implement hybrid search (vector search + SQL) for improved accuracy.

### 3. Build a Streamlit Prototype

1.  Create an input box for users to enter their natural language queries.
2.  Add a search button to trigger the query execution.
3.  Display the query results in a simple and user-friendly UI using Streamlit's `dataframe` or `table` components.

### 4. Deliverables

* GitHub repository with the code and this `README.md` file.
* Screen recording demonstrating the working application.
* Suggestions for improving the system's effectiveness.

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/rhcp1303/database_rag
    ```

2.  Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Set up the PostgreSQL database:

    * Create the database and tables as described above.
    * Update the database connection settings in `settings.py`.
    * Ensure the `pgvector` extension is installed in your PostgreSQL database.
    * Populate the database with sample data.
    * Generate and store vector embeddings.
    * Create HNSW indexes with `python manage.py create_hnsw_indexes`

5.  Set the google api key as an environment variable called GOOGLE_API_KEY.

6.  Run the Streamlit application:

    ```bash
    streamlit run streamlit_app.py
    ```

## Usage

1.  Open the Streamlit application in your browser.
2.  Enter your natural language query in the input box.
3.  Click the "Search" button.
4.  View the query results displayed in the UI.

## Suggestions for Improvement
* **Advanced Prompt Engineering:** Writing refined and detailed prompt to handle all possible cases of natural language query to enhance semantic search and database retrieval.
* **Indexing** Creating indexes over fields other than vector field.
* **Embedding Model Selection** Using advanced models which create embeddings with higher dimension for generating embedings.
* **Advanced UI/UX:** Implement a more sophisticated UI with features like query history, result filtering, and visualization.
* **Improved LLM Integration:** Fine-tune the LLM for better SQL generation accuracy.
* **Enhanced Hybrid Search:** Optimize the hybrid search strategy by adjusting weights and thresholds.
* **Caching:** Implement caching mechanisms to improve performance for frequently used queries.
* **Error Handling:** Add more robust error handling by handling all the cases for erroneous sql and user feedback.
* **Security:** Add more stringent SQL validation and sanitization.
* **Logging:** Add more detailed logging for debugging and monitoring.
* **Authentication:** Add user authentication and authorization.