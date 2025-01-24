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