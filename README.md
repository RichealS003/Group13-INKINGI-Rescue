# INKINGI RESCUE
### Emergency Dispatch Management System

**INKINGI Rescue** is a Python-based, command-line emergency dispatch management system designed to support the reporting and management of emergencies, ambulance allocation, and emergency response tracking.

The system provides separate interfaces for reporters and dispatchers, allowing emergency information to be recorded, managed, and retrieved through a centralized MySQL database.

The project demonstrates how Python programming, database management, input validation, and object-oriented programming can be combined to develop a practical emergency management solution.

---

## Table of Contents

1. Project Overview
2. Key Features
3. System Users
4. Emergency Management Workflow
5. Technology Stack
6. Project Structure
7. Database Design
8. Installation and Setup
9. Running the Application
10. How to Use the System
11. Input Validation and Error Handling
12. Important Notes
13. Future Improvements

---

## 1. Project Overview

INKINGI Rescue aims to simplify the process of managing emergency reports and coordinating ambulance responses.

When an emergency occurs, a reporter can submit the emergency details, including the emergency type, location, severity, and caller's phone number.

Dispatchers can then view active emergencies, allocate available ambulances, update emergency statuses, manage trusted contacts, and generate response-time reports.

The system uses a MySQL database to store emergency records, ambulance information, contacts, and dispatch logs.

---

## 2. Key Features

### Emergency Reporting
- Report new emergencies through the reporter or dispatcher interface.
- Select from different emergency categories.
- Record the district and nearest landmark.
- Assign a severity level.
- Capture and validate the caller's phone number.
- Display a summary for confirmation before saving the report.
- Generate a unique emergency ID for each saved report.

### Ambulance Dispatch Management
- View active emergencies.
- Identify available ambulances.
- Prioritize available ambulances located in the same district as the emergency.
- Assign an available ambulance to an emergency.
- Update the emergency status to `DISPATCHED`.
- Update the assigned ambulance status to `BUSY`.
- Record dispatch activities in the dispatch log.

### Emergency Resolution
- Retrieve an emergency using its unique ID.
- Verify its current status before allowing resolution.
- Confirm whether the ambulance has arrived.
- Update the emergency status to `RESOLVED`.
- Record the ambulance's arrival timestamp.
- Return the ambulance to `AVAILABLE` status.
- Record the resolution event in the dispatch log.

### Response-Time Reporting
- Retrieve resolved emergencies with recorded arrival times.
- Calculate the response time for each emergency.
- Display individual response times in minutes.
- Calculate and display the average response time.

### Circle of Trust
- Allow reporters to register trusted contacts for a patient.
- Store patient names, contact names, phone numbers, and relationships.
- Allow dispatchers to retrieve the contacts associated with a patient.
- Simulate emergency alerts by displaying notification messages in the terminal.

### Input Validation
- Validate menu selections.
- Prevent empty inputs.
- Validate place and landmark information.
- Validate and normalize Rwandan phone numbers.
- Validate yes/no confirmations.

---

## 3. System Users

The application provides two main interfaces.

### Reporter

The reporter interface allows users to:

1. Report a new emergency.
2. Update Circle of Trust contacts.
3. Return to the main menu.

### Dispatcher

The dispatcher interface allows users to:

1. Report a new emergency.
2. View active emergencies.
3. Dispatch an available ambulance.
4. Update emergency status.
5. Manage Circle of Trust contacts.
6. View response-time reports.
7. Return to the main menu.

---

## 4. Emergency Management Workflow

The system follows a structured emergency management process.

**Step 1: Emergency Reported**

A reporter submits the emergency details. The system saves the information in the database and generates a unique emergency ID.

Initial status: `REPORTED`

**Step 2: Ambulance Dispatched**

The dispatcher selects an emergency. The system searches for an available ambulance, prioritizing one in the same district.

Once assigned, the emergency status changes to `DISPATCHED`, and the ambulance status changes to `BUSY`.

**Step 3: Emergency Resolved**

After confirming that the ambulance has arrived, the dispatcher resolves the emergency.

The system records the arrival time, changes the emergency status to `RESOLVED`, and makes the ambulance available again.

**Step 4: Response-Time Analysis**

The system calculates the time between when the emergency was reported and when the ambulance arrived.

Response time = Arrival Time − Reported Time

The system then calculates the average response time across eligible resolved emergencies.

---

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| MySQL | Relational database management |
| MySQL Connector/Python | Communication between Python and MySQL |
| SQL | Database queries and operations |
| Git and GitHub | Version control and team collaboration |

### Python Concepts Applied

- Functions and modular programming
- Dictionaries and lists
- Conditional statements and loops
- Input validation
- Exception handling
- Object-oriented programming
- Classes and objects
- Database connectivity
- Date and time calculations

---

## 6. Project Structure

The project is organized into separate directories to improve readability, maintainability, and collaboration.

```text
INKINGI-RESCUE/
│
├── database/
│   ├── __init__.py
│   ├── config.py
│   └── database.py
│
├── menus/
│   ├── __init__.py
│   ├── reporter.py
│   └── dispatcher.py
│
├── models/
│   ├── __init__.py
│   ├── emergency.py
│   ├── ambulance.py
│   └── contact.py
│
├── utils/
│   ├── __init__.py
│   └── validators.py
│
├── main.py
├── README.md
└── requirements.txt
```

**Directory descriptions:**

- `database/`: Contains database configuration, connection management, database initialization, table creation, and sample ambulance records.
- `menus/`: Contains the reporter and dispatcher interfaces and their associated operations.
- `models/`: Contains classes representing emergencies, ambulances, and contacts.
- `utils/`: Contains reusable input validation and formatting functions.
- `main.py`: Application entry point. Initializes the database and launches the main menu.
- `requirements.txt`: Lists the external Python dependencies.

---

## 7. Database Design

The application uses MySQL to store and manage its records.

The database initialization module creates the project database and four main tables if they do not already exist.

### 7.1 Ambulances Table

Stores ambulance information.

| Column | Description |
|---|---|
| ambulance_id | Unique ambulance identifier |
| plate_number | Ambulance registration number |
| district | Ambulance's assigned district |
| status | Current availability status |

Possible statuses include `AVAILABLE` and `BUSY`.

### 7.2 Emergencies Table

Stores emergency reports and their progress.

| Column | Description |
|---|---|
| emergency_id | Unique emergency identifier |
| type | Type of emergency |
| district | District where the emergency occurred |
| landmark | Nearest landmark |
| severity | Emergency severity level |
| caller_number | Caller's phone number |
| status | Current emergency status |
| ambulance_id | Assigned ambulance identifier |
| arrival_time | Ambulance arrival timestamp |
| time_reported | Emergency reporting timestamp |

### 7.3 Contacts Table

Stores trusted contacts associated with patients.

| Column | Description |
|---|---|
| contact_id | Unique contact identifier |
| patient_name | Name of the patient |
| contact_name | Trusted contact's name |
| contact_phone | Trusted contact's phone number |
| relationship | Relationship to the patient |

### 7.4 Dispatch Log Table

Maintains a record of emergency dispatch status changes.

| Column | Description |
|---|---|
| log_id | Unique log identifier |
| emergency_id | Related emergency |
| ambulance_id | Related ambulance |
| status | Recorded dispatch status |
| logged_at | Date and time of the logged event |

The database uses primary keys to uniquely identify records and foreign keys to establish relationships between emergencies, ambulances, and dispatch logs.

---

## 8. Installation and Setup

### Prerequisites

Before running the application, ensure that you have:

- Python 3 installed.
- MySQL Server installed and running.
- MySQL Connector/Python installed.
- Access to the project source code.

### Step 1: Clone the Repository

```bash
git clone https://github.com/RichealS003/Group13-INKINGI-Rescue.git
```

Navigate into the project directory:

```bash
cd INKINGI-RESCUE
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On Linux or macOS:

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If the requirements file is not available, install the MySQL connector directly:

```bash
pip install mysql-connector-python
```

### Step 4: Configure the Database

Open:

```text
database/config.py
```

Configure the MySQL connection details, including:

- Host
- Username
- Password
- Database name

Use your own MySQL credentials and keep sensitive configuration information out of public repositories.

### Step 5: Initialize the Database

The application initializes the database automatically when it starts.

The initialization process:

1. Connects to the MySQL server.
2. Creates the project database if it does not exist.
3. Creates the required tables.
4. Inserts sample ambulance records without duplicating existing plate numbers.

---

## 9. Running the Application

From the root directory of the project, execute:

```bash
python main.py
```

The application initializes the database and displays the main menu.

---

## 10. How to Use the System

After launching the application, the welcome screen presents three options:

```text
WELCOME TO INKINGI RESCUE
Emergency Dispatch Management.

Who are you?

1. Reporter
2. Dispatcher
0. Exit
```

Select the appropriate option to access the corresponding interface.

Follow the prompts to report emergencies, manage ambulance dispatches, update trusted contacts, and view response-time reports.

---

## 11. Input Validation and Error Handling

INKINGI Rescue includes reusable validation functions to improve the reliability of user input.

The validation module handles:

- Empty input prevention.
- Numeric menu selection and range checking.
- Yes/no responses.
- Rwandan phone number validation.
- Phone number normalization.
- Place and landmark validation.

Database operations also include error handling in relevant functions. Transactions are committed after successful database changes, while rollback is used when dispatch or resolution operations fail.

---

## 12. Important Notes

- The project is a command-line prototype intended for demonstration and educational purposes.
- Circle of Trust alerts are simulated in the terminal and are not actual SMS or telephone notifications.
- Ambulance allocation prioritizes an available ambulance in the same district. It does not calculate real-time geographical distance.
- Response time is calculated from the emergency reporting timestamp to the ambulance arrival timestamp.
- The application requires a working MySQL server and correctly configured database credentials.
- Sample ambulance records are inserted automatically during database initialization.

---

## 13. Future Improvements

Potential improvements include:

- Integration with real SMS and notification services.
- GPS-based ambulance tracking.
- More advanced ambulance allocation based on distance and availability.
- A graphical user interface or web-based dashboard.
- User authentication and role-based access control.
- More detailed emergency analytics and reporting.
- Improved audit trails and historical dispatch analysis.

---

## Conclusion

INKINGI Rescue demonstrates how software development and database management can be applied to an emergency dispatch workflow.

By combining emergency reporting, ambulance allocation, contact management, status tracking, and response-time analysis, the system provides a foundation for exploring how digital tools can support emergency response coordination.

**Project: INKINGI Rescue**  
**Type: Command-Line Emergency Dispatch Management System**  
**Language: Python**  
**Database: MySQL**

