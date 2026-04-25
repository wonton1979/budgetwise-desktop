# 💰 BudgetWise Desktop

A personal and family finance management system designed to track expenses, share financial data within families, and provide a foundation for future financial analysis.

> ⚠️ Current Stage: Backend-first development (frontend in progress)

---

## 🚀 Tech Stack

* Backend: FastAPI (Python)
* ORM: SQLAlchemy
* Database: PostgreSQL / SQLite
* UI (planned): PySide6 (desktop application)

---

## ✨ Current Features

### 👤 User & Authentication

* User registration and authentication system
* Each user is associated with a family group

### 👨‍👩‍👧‍👦 Family System

* Automatic family creation on user registration (if no family code is provided)
* Users can join an existing family using a shared **family code**
* Family-based data sharing model

### 💸 Expense Management

* Users can create expense records
* Each expense can be marked as:

  * **Private** (visible only to the user)
  * **Shared with family** (visible to all family members)

### 🔍 Data Access Logic

* Users can view:

  * Their own expenses
  * Family-shared expenses from other members

---

## 🧠 Architecture & Design Focus

* Backend-first development approach
* Clean separation of concerns (controller / service / database layers)
* Real-world data modeling (users, families, shared data access)
* Designed for scalability into a full financial management system

---

## 📸 Screenshots

(To be added once UI is implemented)

---

## ⚙️ How to Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🚧 Future Improvements

### 💰 Finance Features

* Add income tracking (salary, side income)
* Support recurring monthly expenses:

  * Mortgage
  * Loans
  * Credit cards
  * Subscriptions
* Savings tracking and financial overview

### 👨‍👩‍👧‍👦 Family Features

* Email-based family invitation system
* Automatic family joining via invitation links
* Improved family role management

### 📊 Analysis & Insights

* Monthly cash flow analysis (income vs expenses)
* Personal and family financial dashboards
* Affordability analysis for new expenses

### 🖥️ Frontend

* Build desktop UI using PySide6
* Add charts and visual dashboards

---

## 🎯 Project Goal

To evolve into a complete personal and family financial management system, providing not only tracking but also **insight-driven decision support** for real-world financial planning.
