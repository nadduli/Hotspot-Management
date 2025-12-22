import pytest
from httpx import AsyncClient
from app.models.role import Role
from app.models.organization import Organization
from app.models.branch import Branch

@pytest.fixture
async def setup_data(db_session):
    role = Role(name="AGENT", description="Agent Role")
    db_session.add(role)
    await db_session.flush()

    org = Organization(name="Test Org")
    db_session.add(org)
    await db_session.flush()

    branch = Branch(name="Test Branch", organization_id=org.id)
    db_session.add(branch)

    await db_session.commit()

    return {
        "role_id": role.id,
        "branch_id": branch.id
    }

@pytest.mark.asyncio
async def test_user_registration(client: AsyncClient, setup_data):
    user_data = {
        "email": "newuser@example.com",
        "password": "StrongPassword123!",
        "confirm_password": "StrongPassword123!",
        "full_name": "Test User",
        "branch_id": str(setup_data["branch_id"])
    }

    response = await client.post("/api/v1/auth/register", json=user_data)
    if response.status_code == 422:
        print(response.json())
    assert response.status_code == 201
    
    json_response = response.json()
    user_info = json_response["data"] 

    assert user_info["email"] == "newuser@example.com"
    assert "id" in user_info
    assert "password" not in user_info