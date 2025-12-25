def test_signup_success(client):
    payload = {
        "name": "Ansh",
        "email": "ansh@test.com",
        "password": "123456",
        "confirmPassword": "123456"
    }

    response = client.post("/signup", json=payload)

    assert response.status_code == 201

    data = response.get_json()
    assert data["message"] == "Signup successful"
    assert data["email"] == "ansh@test.com"
    assert "access_token" in data
    assert "refresh_token" in data

    # 🔍 Verify DB state
    user = client.application.db.users.find_one({"email": "ansh@test.com"})
    assert user is not None
    assert user["username"] == "Ansh"
    assert user["password"] != "123456"  # password hashed

def test_signup_missing_fields(client):
    response = client.post("/signup", json={
        "email": "a@test.com"
    })

    assert response.status_code == 400
    assert response.get_json()["error"] == "All fields required"

def test_signup_password_mismatch(client):
    response = client.post("/signup", json={
        "name": "Test",
        "email": "test@test.com",
        "password": "123",
        "confirmPassword": "456"
    })

    assert response.status_code == 409
    assert "does not match" in response.get_json()["error"]

def test_signup_duplicate_email(client):
    payload = {
        "name": "User",
        "email": "test@test.com",
        "password": "123",
        "confirmPassword": "123"
    }

    client.post("/signup", json=payload)
    response = client.post("/signup", json=payload)

    assert response.status_code == 409
    assert response.get_json()["error"] == "User already exists"
