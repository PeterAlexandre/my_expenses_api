from jwt import decode

from app.config import settings
from app.security import create_access_token


def test_jwt():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    decoded = decode(token, settings.secret_key, algorithms=[settings.algorithm])
    assert decoded["sub"] == data["sub"]
    assert "exp" in decoded


# TODO: Implementar fixtures e estrutura de testes

# def test_get_token(client, test_user):
#     response = client.post(
#         "/token",
#         data={
#             "username": test_user.email,
#             "password": test_user.password
#         },
#     )
#     token = response.json()
#     assert response.status_code == status.HTTP_200_OK
#     assert token['token_type'] == 'bearer'
#     assert "access_token" in token

# def test_jwt_invalid_token(client):
#     response = client.delete(
#         '/account', headers={'Authorization': 'Bearer token-invalido'}
#     )

#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     assert response.json() == {'detail': 'Could not validate credentials'}
