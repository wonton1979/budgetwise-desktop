# 💰 BudgetWise Desktop

A modern **desktop personal and family finance management system** built with **PySide6 and FastAPI**, designed to track expenses, share financial data within families, and provide a foundation for future financial analysis.

---

## 🚀 Tech Stack

**Frontend (Desktop UI)**
- PySide6 (Qt for Python)

**Backend**
- FastAPI (Python)
- SQLAlchemy
- Pydantic

**Database**
- PostgreSQL / SQLite

**Authentication**
- JWT (OAuth2)

---

## ✨ Current Features

### 👤 User & Authentication
- User registration and login system
- JWT-based authentication
- Secure API communication

---

### 💸 Expense Management
- Add new expenses with validation
- View expenses in a structured table
- Real-time UI update after adding expenses
- Support for:
  - Category
  - Payment method
  - Shopping type
  - Optional notes and tags

---

### 📅 Expense Filtering
- Filter expenses by date range
- Default view: current month
- Dynamic table refresh based on selected range

---

### 🧩 User Interface
- Tab-based layout (Expenses / Add Expense)
- Clean and modern desktop UI
- Styled data table with responsive layout

---

### 👨‍👩‍👧‍👦 Family System (Backend)
- Automatic family creation on user registration
- Join family via shared code
- Support for shared expense visibility

---

## 🧠 Architecture & Design Focus

- Full-stack architecture (desktop UI + API backend)
- Clear separation of concerns (UI / service / backend layers)
- Real-world data modeling (users, families, shared access)
- Designed for scalability into a complete financial system

---

## 📸 Screenshots

### Register Page
![Register](/screenshots/register.png)

### Login Page
![Login](/screenshots/login.png)

### Expense List
![Expenses](/screenshots/expenses.png)

### Add Expense
![Add Expense](/screenshots/add-expense.png)

### Income Page
![Income](/screenshots/income.png)

### Recurring Bill Page
![Recurring Expenses](/screenshots/recurring_expenses.png)

### Savings Page
![Savings](/screenshots/savings.png)

### Health Page
![Health](/screenshots/health.png)

### Appointment Page
![Appointment](/screenshots/appointment.png)

### Memorable Day Page
![Memorable Day](/screenshots/memorable_day.png)

- Register Page
- Login Page
- Expense List (Table view with date filtering)
- Add Expense Form
- Income Page
- Recurring Bill Page
- Savings Page
- Health Page
- Appointment Page
- Memorable Day Page

---

## ⚙️ How to Run

### 1️⃣ Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
### 2️⃣ Desktop App (Frontend)

```bash
cd desktop
pip install -r requirements.txt
python main.py
```

## 🚧 Future Improvements

This project is actively being expanded with additional features, including:

- Personal Health Recording and Tracking
- Income Tracking
- Financial Dashboards and Analytics
- Family Collaboration Enhancements

---

## 👤 Author

**Yejun Guan**  

📍 South Yorkshire, UK  
🔗 [LinkedIn](https://www.linkedin.com/in/yejun-guan-6470138b)  
💻 [GitHub](https://github.com/wonton1979)