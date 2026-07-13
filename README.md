# 💰 BudgetWise Desktop
⚠️ This project is currently under final testing and polishing before the v1.0 release.

BudgetWise Desktop is a full-stack **personal and family finance management application** built with **PySide6** and **FastAPI**.

The application helps users manage their finances through expense tracking, income management, recurring bills, savings goals, health records, appointments, memorable days, and shared family budgeting. It also supports user preferences such as currency conversion and date formatting while providing a modern desktop experience.

---

## 🚀 Tech Stack

### Frontend
- PySide6 (Qt for Python)

### Backend
- FastAPI
- SQLAlchemy
- Pydantic

### Database
- SQLite
- PostgreSQL (production ready)

### Authentication
- JWT (OAuth2)

### External API
- Frankfurter Exchange Rate API (Currency Exchange)

### Charts
- Matplotlib

---

# ✨ Features

## 👤 User & Authentication

- User registration and login
- JWT-based authentication
- Secure password hashing
- Automatic family creation
- Join existing family using a family code
- User profile management
- Persistent user preferences

---

## 📊 Dashboard

- Monthly financial overview
- Total expenses
- Total income
- Total recurring expenses
- Current balance
- Weekly expense chart
- Expense category chart
- Automatic currency conversion

---

## 💸 Expense Management

- Add, update and delete expenses
- Advanced filtering
- Sorting
- Pagination
- Category management
- Payment method tracking
- Shopping type tracking
- Notes support
- Responsive table layout

---

## 💰 Income Management

- One-off income
- Recurring income
- Multiple income categories
- Income history
- Detail dialog for large datasets
- Pagination support

---

## 📄 Recurring Bills

- Manage recurring expenses
- Frequency support
- Monthly dashboard integration
- Family shared recurring bills

---

## 🏦 Savings Goals

- Create multiple savings goals
- Progress bars
- Remaining balance calculation
- Target dates
- Goal notes

---

## ❤️ Health Tracker

Track personal health information including:

- Weight
- Blood Pressure
- Heart Rate
- Blood Sugar
- Period Tracking

Features include:

- Historical records
- Charts
- CRUD operations
- Timeline management

---

## 📅 Appointments

- Upcoming appointments
- Completed appointments
- Missed appointments
- Cancelled appointments
- Automatic expired status
- CRUD support

---

## 🎉 Memorable Days

- Birthdays
- Anniversaries
- Important family events
- Remaining days countdown
- Card-based layout

---

## 👨‍👩‍👧‍👦 Family Features

- Family invitation system
- Shared expenses
- Shared recurring expenses
- Multi-user financial visibility

---

## ⚙️ User Preferences

- Preferred display currency
    - GBP
    - USD
    - EUR
- Live exchange rate conversion
- Preferred date format
    - DD/MM/YYYY
    - YYYY-MM-DD
    - DD MMM YYYY
- Persistent user settings

---

## 🏗 Architecture

BudgetWise Desktop follows a layered architecture:

```
PySide6 Desktop UI
        │
Service Layer
        │
FastAPI REST API
        │
SQLAlchemy ORM
        │
SQLite / PostgreSQL
```

The project focuses on:

- Clean architecture
- Separation of concerns
- Reusable UI components
- Scalable backend design
- RESTful API principles

---

## 📸 Screenshots

### Register Page
![Register](/screenshots/register.png)

### Login Page
![Login](/screenshots/login.png)

### Dashboard
![Dashboard](/screenshots/dashboard.png)

### Expense List
![Expenses](/screenshots/expenses.png)

### Income Page
![Income](/screenshots/income.png)

### Recurring Bills
![Recurring Expenses](/screenshots/recurring_expenses.png)

### Savings
![Savings](/screenshots/savings.png)

### Health Tracker
![Health](/screenshots/health.png)

### Appointments
![Appointment](/screenshots/appointment.png)

### Memorable Days
![Memorable Day](/screenshots/memorable_day.png)

### Family
![Family](/screenshots/family.png)

### Settings
![Settings](/screenshots/settings.png)

---

## ⚙️ Getting Started

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Desktop Application

```bash
cd desktop
pip install -r requirements.txt
python main.py
```

---

## 🚧 Future Roadmap

Planned improvements include:

- Light / Dark theme support
- Mobile application
- Receipt OCR
- Budget forecasting
- Data export (PDF / Excel)
- Financial reports and analytics
- Cloud synchronization

---

## 👤 Author

**Yejun Guan**

📍 South Yorkshire, United Kingdom

🔗 LinkedIn  
https://www.linkedin.com/in/yejun-guan-6470138b

💻 GitHub  
https://github.com/wonton1979

---

## 📅 Project Timeline

- **Started:** 12 April 2026
- **Feature Complete:** 13 July 2026

Developed over **92 days (approximately 3 months)** as a portfolio project to demonstrate full-stack desktop application development using Python.