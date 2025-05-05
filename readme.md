# User Management 📋

## Project Overview  
The **User Management System** is a secure and feature-rich platform to manage user profiles, roles, authentication, and file uploads. It includes image upload via MinIO, strong validation mechanisms, and containerized deployment for scalability.

---
## 🔧 Repository & Image Links  
- **GitHub**: [https://github.com/Satyabandi20/user_management](https://github.com/Satyabandi20/user_management)  
- **DockerHub**: [https://hub.docker.com/r/satya6644/user_management/](https://hub.docker.com/r/satya6644/user_management/)  

---
## ✅ Closed Issues (Bug Fixes & Enhancements)  
- [#15](https://github.com/Satyabandi20/user_management/issues/15): Profile Picture Upload with Minio  
- [#12](https://github.com/Satyabandi20/user_management/issues/12): Password strength validation  
- [#10](https://github.com/Satyabandi20/user_management/issues/10): Profile picture URL validation  
- [#8](https://github.com/Satyabandi20/user_management/issues/8): UniqueViolationError due to duplicate nickname values  
- [#7](https://github.com/Satyabandi20/user_management/issues/7): Unauthorized role downgrade during email verification  
- [#5](https://github.com/Satyabandi20/user_management/issues/5): User-ID is None upon clicking on Verify Email  
- [#3](https://github.com/Satyabandi20/user_management/issues/3): Docker Build Failure Due to libc-bin Conflict  
- [#1](https://github.com/Satyabandi20/user_management/issues/1): Dependency conflicts while scanning the docker image: Trivy vulnerabilities  

---
## Features Implemented & Issues/Bugs Fixed ✨  

### 📸 Profile Picture Upload (MinIO)
- Upload, resize, and store user profile pictures.
- File format validation (`.jpg`, `.jpeg`, `.png`).
- Generates secure MinIO-hosted image URLs.
- Handles large file validations and errors.

### 🔐 Strong Password Validation  
- Enforces rules for secure passwords:  
  - Min 8 characters  
  - At least one uppercase, lowercase, digit, and special character  

### 🔁 Unique Email/Nickname Check  
- Avoids duplicate account creation by validating against existing records.

### 🔗 Profile Picture URL Validation  
- Regex-based check to ensure only valid URLs are saved.

### 🚫 Role Preservation on Email Verification  
- Prevents role reset to default after email verification.

### 🐳 Docker & Dependency Cleanup  
- Fixed issues with `libc-bin`, updated Docker image, resolved Trivy vulnerabilities.

---
## Testing & Quality Assurance 🧪  
- ✅ Unit tests for profile picture uploads, password validation, and user updates.
- ✅ Validates duplicate values and proper error handling.
- ✅ Integration tested with FastAPI and async DB.

---
## Project Setup ⚙️  

```bash
# 1. Clone the repo
git clone https://github.com/Satyabandi20/user_management.git
cd user_management

# 2. Run with Docker
docker-compose up --build -d

# 3. Apply DB migrations
alembic upgrade head

# 4. Access locally
http://localhost:8000/docs
```

---
## Final Notes 📝  
This project showcases a well-rounded backend system with security, scalability, and developer convenience in mind. MinIO integration, validation systems, and automated testing make it production-ready.

---