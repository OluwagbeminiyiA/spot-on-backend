# SpotOn Backend

The backend system for **SpotOn**, a campus utility service designed to help University of Lagos (UNILAG) students find study spots, hangout locations, and check real-time availability of lecture halls. This project relies on user-generated content (reviews and status reports) to provide up-to-date information.

## 🚀 Features

-   **Spot Management**: Detailed information on study spots and hangout locations (capacity, power outlets, quietness).
-   **Real-time Status Updates**: Users can report if a spot is "Empty", "Getting Full", or "Completely Full". Defaults to "Unknown" if no report in the last 45 minutes.
-   **Reviews & Ratings**: User-submitted reviews and 1-5 star ratings for locations.
-   **Lecture Hall Availability**: Track free periods for classrooms and lecture halls.
-   **Authentication**: Secure JWT authentication with strict validation for UNILAG emails (`@live.unilag.edu.ng`).

## 🛠️ Tech Stack

-   **Framework**: [Django 5.2](https://www.djangoproject.com/) & [Django Rest Framework](https://www.django-rest-framework.org/)
-   **Database**: SQLite (Development)
-   **Authentication**: `djangorestframework_simplejwt`
-   **Environment Management**: `python-decouple`

## 📋 Prerequisites

-   Python 3.10+
-   Pip

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd SpotOn
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the root directory:

```ini
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Start the Server
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`.

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register/` | Register a new user (Requires UNILAG email) |
| `POST` | `/api/token/` | Login to get Access & Refresh tokens |
| `POST` | `/api/token/refresh/` | Refresh expired access token |

### Spots & Reviews
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/spots/` | List all available spots |
| `POST` | `/api/spots/create/` | Add a new spot (Auth required) |
| `GET` | `/api/spots/<id>/` | Get details for a specific spot |
| `POST` | `/api/review/create/` | Submit a review for a spot (Auth required) |

### Real-time Status
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/status-reports/create/` | Report current fullness of a spot (Auth required) |
| `GET` | `/api/free-halls/` | List currently free lecture halls |

## 🧪 Development Notes

-   **Caching**: `SpotListView` and `SpotDetailView` are cached for 60 minutes. During development, you may need to clear the cache or restart the server to see immediate changes to spot data.
-   **Status Expiration**: Status reports older than 45 minutes are considered expired and will show as "Unknown" in the API response.
-   **Email Validation**: The registration endpoint strictly enforces that the email ends with `@live.unilag.edu.ng` and validates matriculation year logic.

## 📝 Logging Placement Rationale

-   **Registration (`register_user`)**: info and warning logs capture attempts and validation failures to help diagnose onboarding issues without logging passwords or full emails.
-   **Email verification (`VerifyEmailView`)**: info on success and warning on failure provide an audit trail for account activation problems.
-   **Content creation (spots, reviews, status reports, saved spots)**: info logs record the creation events so operational and audit questions can be answered quickly.
-   **Filtering and cache-backed queries**: debug logs note filter parameters and cache-hit paths to make it easier to trace inconsistent results during development.
-   **Maintenance command (`clear_statuses`)**: info logs record when cleanup runs and how many rows were deleted; exceptions are logged for ops visibility.
-   **PII safety**: logs intentionally exclude passwords and full email addresses; only coarse metadata (e.g., domain or IDs) is recorded.

## 🤝 Contributing

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request
