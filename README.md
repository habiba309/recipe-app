<div align="center">

# 🍽️ SimpleDelicacy

### A Server-Rendered Django Recipe Application

Browse recipes, save favorites, and manage delicious content through a clean admin dashboard built with Django.

<img src="https://img.shields.io/badge/Django-4.2-green?style=for-the-badge&logo=django" />
<img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
<img src="https://img.shields.io/badge/SQLite-Database-lightgrey?style=for-the-badge&logo=sqlite" />
<img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" />

</div>

---

## 📖 About The Project

**SimpleDelicacy** is a fully server-rendered Django web application designed for recipe browsing and management.

The project focuses on traditional Django architecture using:

- Django Templates
- Sessions & Authentication
- Forms & ORM
- SQLite Database
- Standard HTML form submissions

No frontend framework or API layer is used — keeping the application lightweight, fast, and beginner-friendly.

---

# ✨ Features

## 👤 Authentication & Roles

- 🔐 Email-based authentication
- 👥 Custom Django user model
- 🛡️ Role-based access:
  - `User`
  - `Admin`

---

## 🍲 Recipe Experience

- 🏠 User home page with recipe cards
- 🔎 Server-side search functionality
- 🧁 Course-based filtering
- 📄 Detailed recipe pages
- ❤️ Save favorite recipes
- 🖼️ Recipe image uploads

---

## 🛠️ Admin Dashboard

- ➕ Add recipes
- ✏️ Edit recipes
- ❌ Delete recipes
- 🧾 Dynamic ingredient rows
- 📸 Image preview support
- 🔔 Flash messages for actions

---

## ⚙️ Django Admin Integration

Manage:

- Users
- Recipes
- Ingredients
- Favorites

through Django’s built-in admin panel.

---

# 🧰 Tech Stack

| Technology | Usage |
|---|---|
| Python | Backend language |
| Django 4.2 | Web framework |
| SQLite | Database |
| HTML/CSS/JS | Frontend |
| Django Templates | Server rendering |
| Pillow | Image handling |
| Font Awesome | Icons |

---

# 🚀 Getting Started

## 📋 Prerequisites

- Python 3.10+
- pip

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone <your-repository-url>
cd recipe-app
```

---

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Apply Migrations

```bash
python manage.py migrate
```

---

### 5️⃣ Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

### 6️⃣ Run Development Server

```bash
python manage.py runserver
```

---

### 7️⃣ Open the App

```txt
http://127.0.0.1:8000/
```

---

# 🌐 App Routes

| Route | Description |
|---|---|
| `/` | Sign in |
| `/signup/` | Create account |
| `/home/` | User home |
| `/recipes/` | Recipes catalog |
| `/recipes/<id>/` | Recipe details |
| `/favorites/` | Favorite recipes |
| `/admin_home/` | Admin homepage |
| `/dashboard/` | Recipe dashboard |
| `/dashboard/add/` | Add recipe |
| `/dashboard/edit/<id>/` | Edit recipe |
| `/admin/` | Django admin panel |

---

# 👥 User Roles

## 👤 User

Regular users can:

- Browse recipes
- Search & filter recipes
- View recipe details
- Save favorite recipes

---

## 👑 Admin

Admins can:

- Manage recipes
- Access dashboard
- Create/update/delete content
- Use protected admin-only routes

The project uses a custom:

```python
@admin_required
```

decorator for dashboard protection.

---

# 📂 Project Structure

```text
recipe-app/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── media/
│   └── recipes/
├── recipe_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── recipes/
│   ├── admin.py
│   ├── apps.py
│   ├── decorators.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── static/
│   ├── css/
│   └── js/
│       └── dashboard.js
└── templates/
    ├── base.html
    ├── home.html
    ├── admin_home.html
    ├── auth/
    ├── dashboard/
    └── recipes/
```

---

# 🗄️ Data Models

| Model | Description |
|---|---|
| `CustomUser` | Extended Django user model |
| `Recipe` | Recipe details & metadata |
| `Ingredient` | Recipe ingredients |
| `Favorite` | User favorite recipes |

---

# 🍴 Recipe Management

Each recipe includes:

- 📝 Name
- 🍽️ Course category
- 📄 Description
- 🖼️ Image
- 🧂 Ingredients
- 📋 Step-by-step instructions

Dashboard JavaScript only handles:

- Dynamic ingredient rows
- Image preview helpers

All data submissions are still handled using standard Django forms.

---

# 🧪 Development Notes

- SQLite is used for local development
- Uploaded images are served from `MEDIA_ROOT`
- Authentication uses Django sessions
- Search & filters use Django ORM queries
- Favorites use CSRF-protected POST requests

> ⚠️ `DEBUG = True` is currently enabled.  
> Update:
>
> - `SECRET_KEY`
> - `DEBUG`
> - `ALLOWED_HOSTS`
> - Database settings
>
> before deploying to production.

---

# 📦 Dependencies

```txt
Django>=4.2,<5.0
Pillow>=10.0
```

---

# 📌 Future Improvements

- Responsive UI enhancements
- Pagination
- Recipe comments & ratings
- REST API integration
- Docker support
- Deployment configuration

---

# 📄 License

No license has been added yet.

Consider adding an open-source license such as:

- MIT
- Apache 2.0
- GPL

before publishing publicly.

---

<div align="center">

### ⭐ If you like this project, consider giving it a star on GitHub!

Made with ❤️ using Django

</div>