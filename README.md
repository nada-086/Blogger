# Blog Website with Authentication and Role-Based Access Control

## Description
This project is a blog website built using **Flask**, featuring **authentication** and **role-based access control** (RBAC). The system supports three distinct roles: **Admin**, **Author**, and **Reader**, each with specific permissions.

## Roles and Permissions

### 1. **Admin**
- Full control over all blog posts (view, edit, delete).
- Manage users (promote users to **Author** or **Admin** roles).
- Access to user management features.

### 2. **Author**
- Can create, view, edit, and delete their **own** blog posts.
- Has access to a customized interface to manage personal blog posts.

### 3. **Reader**
- Can view all **published** blog posts.
- Can **like** or **dislike** posts and see the number of likes/dislikes on each post.

## Project Features

### Authentication
- Users can **register** and **login**.
- **Session-based** or **token-based** authentication is used.
- Upon registration, users are automatically assigned the **Reader** role.
- Only **Admins** can promote users to **Author** or **Admin** roles.

### Blog Management
- **Admins** can manage all posts (view, edit, delete any post).
- **Authors** can manage only their own posts.
- **Readers** can view all published posts and like/dislike them.

### Database Layers
The project implements two database layers to demonstrate both SQL and NoSQL capabilities:
1. **SQL Database** (e.g., SQLite, PostgreSQL, MySQL) for structured data such as blog posts and user roles.
2. **MongoDB** (NoSQL) as an alternative layer to handle the same data.

## Technologies Used
- **Flask**: Web framework for building the application.
- **Flask-Login**: For user session management.
- **Flask-SQLAlchemy**: For interacting with the SQL database.
- **MongoEngine**: For interacting with MongoDB.
- **Bootstrap**: For responsive UI design.

## Setup Instructions

### Prerequisites
Make sure you have the following installed:
- Python 3.x
- Virtualenv
- MongoDB
- SQLite Database 

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nada-086/Blogger
   cd Blogger
    ```
2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Configure the database**:
    - For the SQL database, update the SQLALCHEMY_DATABASE_URI in the config.py file.
    - For MongoDB, ensure that MongoDB is running and update the MONGO_URI in config.py.

5. **Run the Application**:
    ```bash
    flask run
    ```

6. Access the website: Open your browser and go to `http://127.0.0.1:5000`

## Future Enhancements
- Add pagination for viewing blog posts.
- Implement search functionality for posts.
- Add comment section for readers to comment on blog posts.


## Project Structure
## File Structure

```bash
.
├── app/                          # Main application directory
│   ├── routes/                   # Flask route handlers
│   │   └── user.py    
│   │   └── blog.py
│   ├── models/                   # Database models
│   │   ├── sql/                  # SQL models (SQLAlchemy)
│   │   │   └── user.py           # SQL model for users
│   │   │   └── blog.py
│   │   │   └── blog_action.py
│   │   └── mongo/                # MongoDB models (PyMongo)
│   │       └── blog.py           # MongoDB model for blogs
│   │       └── user.py
│   │       └── blog_action.py
│   ├── services/                 # Service layer for business logic
│   │   ├── blog/                 # Blog-related services
│   │   │   └── factory.py
│   │   │   └── mongo.py
│   │   │   └── sql.py
│   │   └── user/                 # User-related services
│   │       └── factory.py
│   │       └── mongo.py
│   │       └── sql.py
│   ├── templates/                # HTML templates for rendering views
│   │   ├── user/                 # User-related templates
│   │   │   └── profile.html      # User profile template
│   │   │   └── login.html
│   │   │   └── signup.html
│   │   │   └── user-management.hmtl
│   │   │   └── blog-management.html
│   │   ├── navbar/               # Navbar templates
│   │   │   └── admin.html       
│   │   │   └── reader.html
│   │   └── blog/                 # Blog-related templates
│   │       └── view.html         # Single blog post view template
│   │       └── create.html
│   │       └── list.html
│   │       └── edit.html
│   ├── __init__.py               # App initialization and configurations
├── .gitignore                    # Files to ignore in Git version control
├── README.md                     # Readme file with project information (this file)
├── main.py                       # Main entry point to run the Flask application
├── .env                          # Environment variables (e.g., API keys, DB URIs)
├── config.py                     # Configuration settings (database URIs, secret keys)
├── requirements.txt              # List of Python dependencies
```
