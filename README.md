# DevOps Assignment

## Overview

The DevOps Oct 2024 project aims to develop a gamification system for students, allowing them to redeem points for various items. The system will be built using open-source development tools and will prioritize security, user experience, and maintainability.

## Features

- **User Authentication**

  - Secure login for students and admins
  - Password recovery functionality

- **Admin Features**

  - Create, modify, and delete student accounts
  - Manage redeemable items
  - Search and list all student accounts

- **Student Features**

  - View user details and total points
  - Access redeemable and redeemed items pages

- **Redeemable Items Management**

  - Display and redeem items based on available points
  - Prevent redemption beyond available points

- **Database Management**

  - Store student information and redeemable items
  - Initial data seeding for testing

- **User Interface**

  - User-friendly login and dashboard interfaces
  - Responsive design for various devices

- **Security Features**

  - Implement security checks for sensitive data
  - Secure password storage

- **Testing and Quality Assurance**

  - Unit and integration testing for all features
  - Stakeholder feedback during testing phases

- **Deployment and Documentation**
  - Automated deployment scripts
  - Comprehensive user and technical documentation


## Installing Dependencies

To set up the required dependencies for this project:

1. Make sure you have Python installed (preferably version 3.10 or higher).

2. Create a virtual environment (optional but recommended):

   - On **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. Install the dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt


# Project Setup

## Environment Variables

Create a `.env` file in the root directory with the following content:

```env
DB_HOST=your-database-host
DB_NAME=your-database-name
DB_USER=your-database-username
DB_PASSWORD=your-database-password
```

Notes

- Replace the placeholder values with your actual database credentials.
- Important: Ensure .env is added to .gitignore to prevent sensitive data from being pushed to version control.



# PostgreSQL Database Setup

Follow these steps to set up the PostgreSQL database for this project.

## Prerequisites

- PostgreSQL installed on your system.
- `.env` file configured as described in the [Environment Variables Setup](./env-setup.md).

## Steps to Set Up the Database

1. **Start PostgreSQL**  
   Ensure the PostgreSQL service is running on your system.

2. **Create the Database**  
   Use the credentials from your `.env` file to create the database. Run the following command in your terminal or PostgreSQL CLI:

       psql -U <DB_USER> -h <DB_HOST>
      
    Replace `<DB_USER>` and `<DB_HOST>` with the values from your .env file. Once connected, create the database:
       
        CREATE DATABASE <DB_NAME>; 

    
    Replace `<DB_NAME>` with the database name from your `.env` file.
    
    Run the SQL Setup Script
    Import the database-setup.sql file to configure your database schema and initial data:
    
        psql -U <DB_USER> -h <DB_HOST> -p <DB_PORT> -d <DB_NAME> -f database-setup.sql
    
    Verify the Setup
    Confirm the tables and data have been correctly set up by connecting to the database:
    
        psql -U <DB_USER> -h <DB_HOST> -p <DB_PORT> -d <DB_NAME>
    
    
    This will list all the tables in the database.
    
    Your PostgreSQL database is now ready to use!

# Running the Server

Follow these steps to navigate to the server directory and run the application:

## Steps

1. Open a terminal and navigate to the `./server` directory:

   ```bash
   cd ./server

2. Run the application:

        python app.py
    
    This will start the server.
    
3. Access the Web Server

    Once the server starts, it will typically display a URL (e.g., http://127.0.0.1:5000). Open this URL in your web browser to access the application.
