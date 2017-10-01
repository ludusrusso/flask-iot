import pytest
import jwt

from ..models import User

def test_model_user(db, app):
    users = User.query.all()
    assert users == []

    user = User(username='Test', email='test@test.it', password="password")
    db.session.add(user)
    db.session.commit()

    users = User.query.all()
    assert len(users) == 1

    user = users[0]
    assert user.username == 'Test'
    assert user.email == 'test@test.it'
    assert user.check_password("password") == True
    assert user.check_password("other_password") == False

    user.password = 'new password'
    assert user.check_password("new password") == True
    assert user.check_password("password") == False
    with pytest.raises(AttributeError):
        password = user.password

def test_user_token(password, user, app):
    token = user.generate_auth_token()
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    assert 'user' in payload
    assert payload['user'] == user.id

    get_user = User.query_with_token(token)
    assert get_user.id == user.id
