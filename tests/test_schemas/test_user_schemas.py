import uuid
import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest

# Fixtures for common test data
@pytest.fixture
def user_base_data():
    return {
        "nickname": "john_doe_123",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "AUTHENTICATED",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe"
    }

@pytest.fixture
def user_create_data(user_base_data):
    return {**user_base_data, "password": "SecurePassword123!"}

@pytest.fixture
def user_update_data():
    return {
        "email": "john.doe.new@example.com",
        "nickname": "j_doe",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I specialize in backend development with Python and Node.js.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe_updated.jpg"
    }

@pytest.fixture
def user_response_data(user_base_data):
    return {
        "id": uuid.uuid4(),
        "nickname": user_base_data["nickname"],
        "first_name": user_base_data["first_name"],
        "last_name": user_base_data["last_name"],
        "role": user_base_data["role"],
        "email": user_base_data["email"],
        # "last_login_at": datetime.now(),
        # "created_at": datetime.now(),
        # "updated_at": datetime.now(),
        "links": []
    }

@pytest.fixture
def login_request_data():
    return {"email": "john_doe_123@emai.com", "password": "SecurePassword123!"}

# Tests for UserBase
def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data["nickname"]
    assert user.email == user_base_data["email"]

# Tests for UserCreate
def test_user_create_valid(user_create_data):
    user = UserCreate(**user_create_data)
    assert user.nickname == user_create_data["nickname"]
    assert user.password == user_create_data["password"]

# Tests for UserUpdate
def test_user_update_valid(user_update_data):
    user_update = UserUpdate(**user_update_data)
    assert user_update.email == user_update_data["email"]
    assert user_update.first_name == user_update_data["first_name"]

# Tests for UserResponse
def test_user_response_valid(user_response_data):
    user = UserResponse(**user_response_data)
    assert user.id == user_response_data["id"]
    # assert user.last_login_at == user_response_data["last_login_at"]

# Tests for LoginRequest
def test_login_request_valid(login_request_data):
    login = LoginRequest(**login_request_data)
    assert login.email == login_request_data["email"]
    assert login.password == login_request_data["password"]

# Parametrized tests for nickname and email validation
@pytest.mark.parametrize("nickname", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_nickname_valid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    user = UserBase(**user_base_data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", ["test user", "test?user", "", "us"])
def test_user_base_nickname_invalid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Parametrized tests for URL validation
@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", ["ftp://invalid.com/profile.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

@pytest.mark.parametrize("invalid_password, error_message", [
    ("weakpass", "Password must include at least one uppercase letter."),
    ("SHORT1!", "Password must include at least one lowercase letter."),
    ("noupper123!", "Password must include at least one uppercase letter."),
    ("NOLOWER123!", "Password must include at least one lowercase letter."),
    ("NoNumber!", "Password must include at least one number."),
    ("NoSpecial123", "Password must include at least one special character"),
])
def test_user_creation_with_invalid_password(invalid_password, error_message, generate_unique_user):
    """
    Test that user creation raises ValidationError for invalid passwords.
    """
    user_data = generate_unique_user
    user_data["password"] = invalid_password

    with pytest.raises(ValidationError) as validation_error:
        UserCreate(**user_data)

    assert error_message in str(validation_error.value)

@pytest.fixture
async def bulk_users_with_role(db_session):
    """
    Creates 50 users with the same role but unique email and nickname.
    """
    users_to_create = []
    for _ in range(50):
        users_to_create.append({
            "nickname": f"user_{uuid.uuid4().hex[:6]}",
            "email": f"user_{uuid.uuid4().hex[:6]}@example.com",
            "first_name": "Bulk",
            "last_name": "User",
            "role": "AUTHENTICATED"
        })

    db_session.add_all([UserCreate(**user) for user in users_to_create])
    await db_session.commit()
    return users_to_create

def test_user_base_optional_fields_are_none():
    user = UserBase(email="john@example.com", nickname="johnny", role="AUTHENTICATED")
    assert user.first_name is None
    assert user.bio is None

def test_user_response_id_is_valid_uuid(user_response_data):
    user = UserResponse(**user_response_data)
    assert isinstance(user.id, uuid.UUID)


def test_user_list_response_valid(user_response_data):
    resp = UserListResponse(items=[UserResponse(**user_response_data)], total=1, page=1, size=10)
    assert resp.total == 1 and resp.page == 1 and resp.size == 10

def test_user_update_no_values_raises():
    with pytest.raises(ValidationError):
        UserUpdate()

@pytest.mark.parametrize("nickname", ["test user", "invalid!", ""])
def test_invalid_nicknames_raise(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

def test_valid_password_passes(user_create_data):
    user = UserCreate(**user_create_data)
    assert user.password == user_create_data["password"]

def test_user_role_enum_works(user_base_data):
    user = UserBase(**user_base_data)
    assert user.role.value == "AUTHENTICATED"

def test_user_base_minimum_required_fields():
    user = UserBase(email="test@example.com", nickname="testuser", role="AUTHENTICATED")
    assert user.email == "test@example.com"
    assert user.first_name is None
    assert user.last_name is None

def test_invalid_email_in_user_base():
    with pytest.raises(ValidationError):
        UserBase(email="invalidemail", nickname="test", role="AUTHENTICATED")

def test_long_nickname_passes(user_base_data):
    long_nick = "a" * 50
    user_base_data["nickname"] = long_nick
    user = UserBase(**user_base_data)
    assert user.nickname == long_nick

@pytest.mark.parametrize("field", ["profile_picture_url", "linkedin_profile_url", "github_profile_url"])
def test_invalid_url_scheme(field, user_base_data):
    user_base_data[field] = "htp://invalid-url.com"
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

def test_user_base_accepts_none_urls(user_base_data):
    user_base_data["linkedin_profile_url"] = None
    user_base_data["github_profile_url"] = None
    user_base_data["profile_picture_url"] = None
    user = UserBase(**user_base_data)
    assert user.linkedin_profile_url is None

def test_user_update_partial_data():
    user = UserUpdate(email="updated@example.com")
    assert user.email == "updated@example.com"
    assert user.first_name is None

def test_user_update_empty_fails():
    with pytest.raises(ValidationError):
        UserUpdate()

def test_user_create_password_complexity(user_create_data):
    user = UserCreate(**user_create_data)
    assert any(c.isupper() for c in user.password)
    assert any(c.islower() for c in user.password)
    assert any(c.isdigit() for c in user.password)
    assert any(c in "!@#$%^&*(),.?\":{}|<>" for c in user.password)

def test_user_create_inherits_user_base(user_create_data):
    user = UserCreate(**user_create_data)
    assert isinstance(user, UserBase)
