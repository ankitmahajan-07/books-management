import pytest

@pytest.mark.asyncio
async def test_register_and_login(client):
    # register
    resp = await client.post('/v1/auth/register', json={"username":"alice","email":"a@example.com","password":"secret"})
    assert resp.status_code == 200
    # login
    resp = await client.post('/v1/auth/token', data={"username":"alice","password":"secret"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
