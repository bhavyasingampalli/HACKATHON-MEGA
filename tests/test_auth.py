"""
Automated Test Suite for CareBridge AI Authentication & Route Protection.
Tests real patient/user registration, login, session cookies, password hashing,
profile updates, protected dashboard routes, and per-user care plan isolation.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import get_connection
from app.data.synthetic_samples import SYNTHETIC_SAMPLES

client = TestClient(app, follow_redirects=False)


def test_login_page_accessible():
    """Verify login page serves HTTP 200 with HTML content."""
    response = client.get("/login")
    assert response.status_code == 200
    assert "CareBridge AI" in response.text
    assert "Sign In" in response.text
    assert "Create Account" in response.text


def test_protected_dashboard_redirects_unauthenticated():
    """Verify accessing / without session cookie redirects to /login."""
    response = client.get("/")
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_real_user_registration_and_login_flow():
    """Test creating a real user account with name, email, password, and signing in."""
    test_email = "sarah.jenkins@patientportal.org"
    test_password = "SecurePassword#2026"
    test_name = "Sarah Jenkins"

    # Clean up test user if previously created
    with get_connection() as conn:
        conn.execute("DELETE FROM users WHERE email = ?", (test_email,))
        conn.commit()

    # 1. Register new real user
    reg_resp = client.post("/api/auth/register", json={
        "email": test_email,
        "password": test_password,
        "confirm_password": test_password,
        "full_name": test_name,
        "role": "Patient"
    })
    assert reg_resp.status_code == 200
    reg_data = reg_resp.json()
    assert reg_data["success"] is True
    assert reg_data["user"]["email"] == test_email
    assert reg_data["user"]["full_name"] == test_name
    assert "cb_session" in reg_resp.cookies

    session_cookie = reg_resp.cookies["cb_session"]

    # 2. Access protected route with received cookie
    dash_resp = client.get("/", cookies={"cb_session": session_cookie})
    assert dash_resp.status_code == 200
    assert "CareBridge AI" in dash_resp.text

    # 3. Check /api/auth/me returns actual registered details
    me_resp = client.get("/api/auth/me", cookies={"cb_session": session_cookie})
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["email"] == test_email
    assert me_data["full_name"] == test_name

    # 4. Update profile name
    update_resp = client.put("/api/auth/profile", json={"full_name": "Sarah Jenkins, RN"}, cookies={"cb_session": session_cookie})
    assert update_resp.status_code == 200
    assert update_resp.json()["user"]["full_name"] == "Sarah Jenkins, RN"

    # 5. Sign out
    logout_resp = client.post("/api/auth/logout", cookies={"cb_session": session_cookie})
    assert logout_resp.status_code == 200

    # 6. Sign back in with the created credentials
    login_resp = client.post("/api/auth/login", json={
        "email": test_email,
        "password": test_password,
        "remember_me": True
    })
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert login_data["success"] is True
    assert login_data["user"]["email"] == test_email
    # Name persisted in database
    assert login_data["user"]["full_name"] == "Sarah Jenkins, RN"


def test_register_validation_errors():
    """Test validation errors for registration."""
    # 1. Password mismatch
    resp = client.post("/api/auth/register", json={
        "email": "mismatch@patientportal.org",
        "password": "Password123",
        "confirm_password": "DifferentPassword123",
        "full_name": "Test User",
        "role": "Patient"
    })
    assert resp.status_code == 400

    # 2. Too short password
    resp = client.post("/api/auth/register", json={
        "email": "short@patientportal.org",
        "password": "short",
        "confirm_password": "short",
        "full_name": "Test User",
        "role": "Patient"
    })
    assert resp.status_code in [400, 422]


def test_login_invalid_credentials():
    """Test rejection of invalid credentials."""
    resp = client.post("/api/auth/login", json={
        "email": "nonexistent@patientportal.org",
        "password": "WrongPassword!999"
    })
    assert resp.status_code == 401
    assert "Invalid email or password" in resp.json()["detail"]


def test_forgot_and_reset_password_flow():
    """Test password reset token creation and new password reset."""
    email = "reset_test_user@patientportal.org"
    pwd1 = "InitialPassword#2026"
    pwd2 = "UpdatedPassword#2027"

    # Register user first
    with get_connection() as conn:
        conn.execute("DELETE FROM users WHERE email = ?", (email,))
        conn.commit()

    client.post("/api/auth/register", json={
        "email": email,
        "password": pwd1,
        "confirm_password": pwd1,
        "full_name": "Reset Test User",
        "role": "Patient"
    })

    # 1. Request reset token
    forgot_resp = client.post("/api/auth/forgot-password", json={"email": email})
    assert forgot_resp.status_code == 200
    token = forgot_resp.json()["token"]
    assert len(token) > 10

    # 2. Reset password
    reset_resp = client.post("/api/auth/reset-password", json={
        "token": token,
        "new_password": pwd2,
        "confirm_password": pwd2
    })
    assert reset_resp.status_code == 200

    # 3. Log in with new password
    login_resp = client.post("/api/auth/login", json={
        "email": email,
        "password": pwd2
    })
    assert login_resp.status_code == 200


def test_per_user_care_plan_isolation():
    """Verify that each user can only access their own care plans."""
    user1_email = "user_one@carebridge.ai"
    user2_email = "user_two@carebridge.ai"
    password = "TestPassword#2026"

    # Register User 1
    with get_connection() as conn:
        conn.execute("DELETE FROM users WHERE email IN (?, ?)", (user1_email, user2_email))
        conn.commit()

    u1_reg = client.post("/api/auth/register", json={
        "email": user1_email, "password": password, "confirm_password": password,
        "full_name": "User One", "role": "Patient"
    })
    u1_cookie = u1_reg.cookies["cb_session"]

    # Register User 2
    u2_reg = client.post("/api/auth/register", json={
        "email": user2_email, "password": password, "confirm_password": password,
        "full_name": "User Two", "role": "Patient"
    })
    u2_cookie = u2_reg.cookies["cb_session"]

    # User 1 creates a care plan
    sample_text = SYNTHETIC_SAMPLES[0]["raw_text"]
    gen_resp = client.post("/api/generate", json={"text": sample_text}, cookies={"cb_session": u1_cookie})
    assert gen_resp.status_code == 200
    u1_plan_id = gen_resp.json()["id"]

    # User 1 checks /api/history -> sees plan
    u1_history = client.get("/api/history", cookies={"cb_session": u1_cookie}).json()
    u1_ids = [p["id"] for p in u1_history]
    assert u1_plan_id in u1_ids

    # User 2 checks /api/history -> does NOT see User 1's plan!
    u2_history = client.get("/api/history", cookies={"cb_session": u2_cookie}).json()
    u2_ids = [p["id"] for p in u2_history]
    assert u1_plan_id not in u2_ids

    # User 2 attempts to directly access User 1's plan -> 404 forbidden/not found
    u2_direct = client.get(f"/api/history/{u1_plan_id}", cookies={"cb_session": u2_cookie})
    assert u2_direct.status_code == 404
