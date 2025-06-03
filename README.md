# 🧠 Inventrack Backend

**Inventrack** is a robust backend system built with Django and Django REST Framework to manage inventory, users, roles (staff/admin), and media uploads. Designed with scalability and security in mind, it powers the backend logic for the Inventrack ERP system.

---

## 🚀 Features

- ✅ User registration and authentication (Admin & Staff roles)
- 🔒 Staff access control with admin approval/deactivation
- 📦 Full CRUD support for Products (name, SKU, price, quantity, image)
- 📤 Image/media upload via multipart form
- 🧾 Clean and scalable project structure
- 🌐 RESTful API integration ready for any frontend (Flutter, React, etc.)
- 🗃️ Django Admin for full control and data management

---

## 🏗️ Tech Stack

- **Python 3.10+**
- **Django 4.x**
- **Django REST Framework**
- **PostgreSQL (or SQLite for dev)**
- **Pillow (for image support)**

---

## ⚙️ Installation


### 1. Clone the repo

```bash
git clone https://github.com/yourusername/inventrack_backend.git
cd inventrack_backend
```

### 2. Set up a virtual environment 

```bash
python -m venv venv 
source venv/bin/activate
``` 
### 3. Install dependencies
``` bash
pip install -r requirements.txt
```
### 4. Configure .env
```bash
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```
### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Create superuser
```bash
python manage.py createsuperuser
```

### 7. Run the server
```bash
python manage.py runserver
```
### 📁 Project Structure

```bash
inventrack_backend/
├── api/                   # All app logic (inventory, users, etc.)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── media/                 # Uploaded images
├── inventrack_backend/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── requirements.txt
```
---
## 📡 API Endpoints (Examples)

| Method | Endpoint                  | Description         |
|--------|---------------------------|---------------------|
| POST   | `/api/accounts/register/` | User registration   |
| POST   | `/api/login/`             | User login          |
| GET    | `/api/inventory/`         | List all products   |
| POST   | `/api/inventory/create/`  | Create a new product|

> ⚠️ Ensure requests sending images use `multipart/form-data`.
---
## ✅ To Do

- 🔐 Add token-based authentication  
- 🔍 Add pagination and search filters  
- 🧪 Unit tests & API docs (Swagger/OpenAPI)  
- 🔔 Webhooks or notifications for staff approval  

---

## 💬 Contributing

Have a feature idea or found a bug?  
Pull requests and issues are welcome!

---

## 📝 License

This project is licensed under the **MIT License**.

---

## 📞 Contact

**Developer**: [Md. Atikuzzaman Hridoy]  
**Email**: atik.hridoy.00@gmail.com  




---

Let me know if you'd like me to update this with your actual GitHub repo URL, email, or name before you publish it.



