
# Mentor Appointment Scheduling Web Application

## 📖 Overview

The **Mentor Appointment Scheduling Web Application** is a backend system for scheduling and managing appointments between users and mentors. It provides core features like user registration, appointment management, and mentor availability scheduling. Additionally, it integrates a video consultation feature using Jitsi Meet.

### Core Features

- User registration and login
- Appointment booking, updating, and cancellation
- Mentor availability management
- Prevention of overlapping appointments
- Video consultation integration (using Jitsi Meet)

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8+
- PostgreSQL 12+
- Git
- Virtualenv (Python virtual environment)
- pgAdmin or any PostgreSQL management tool (optional)

## 🚀 Installation

Follow the steps below to set up the project on your local system:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/mentor-scheduler.git
cd mentor-scheduler
```

### 2. Set Up Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv venv
# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

- Install PostgreSQL from the official website: [PostgreSQL Downloads](https://www.postgresql.org/download/)
- Create a new PostgreSQL database and user:

```sql
CREATE DATABASE mentor_scheduler;
CREATE USER mentor_user WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE mentor_scheduler TO mentor_user;
```

### 5. Configure Environment Variables

Create a `.env` file in the project root directory with the following content:

```env
DATABASE_URL=postgresql://mentor_user:your_password@localhost/mentor_scheduler
SECRET_KEY=your_secret_key
```

Replace `your_password` and `your_secret_key` with your actual credentials.

### 6. Apply Database Migrations

Initialize and run database migrations using Alembic:

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 7. Run the Application

Start the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API documentation will be available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🧪 Testing the API

You can test the API endpoints using tools like [Postman](https://www.postman.com/) or the built-in Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Example Endpoints

- **POST /register**: Register a new user
- **GET /appointments**: Retrieve all appointments for the authenticated user
- **POST /appointments**: Book a new appointment
- **PUT /appointments/{id}**: Update an existing appointment
- **DELETE /appointments/{id}**: Cancel an appointment
- **POST /mentors/availability**: Set mentor availability
- **GET /mentors/availability**: View mentor availability

## 💻 Database Management (Optional)

You can use **pgAdmin** or **DBeaver** for managing your PostgreSQL database.

- **Download pgAdmin**: [pgAdmin Downloads](https://www.pgadmin.org/download/)
- **Download DBeaver**: [DBeaver Downloads](https://dbeaver.io/download/)

## 🛡️ Security Notes

- Store sensitive information (e.g., database credentials, secret keys) in the `.env` file and never commit this file to version control.
- Use strong, unique passwords for PostgreSQL users.
- Regularly update your dependencies using:

```bash
pip list --outdated
pip install --upgrade package_name
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Jitsi Meet Documentation](https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-web-api)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## 📧 Contact

For any questions or issues, please contact the repository owner.
