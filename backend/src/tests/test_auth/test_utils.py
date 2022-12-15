from datetime import timedelta, datetime

from jose import jwt

from backend.src.auth.config import JWT_SECRET_KEY, JWT_ALGORITHM, pwd_context, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.src.auth.models import User
from backend.src.auth.utils import create_access_token, get_password_hash, verify_password, check_user_is_superuser


def test_create_access_token():
    data_to_encode = {"sub": "test_value", "test": "value"}
    expires_delta = timedelta(minutes=60 * 3)
    expires_secs_from_epoch = (datetime.utcnow() + expires_delta).timestamp()
    encoded_jwt_token = create_access_token(data_to_encode, expires_delta)
    assert type(encoded_jwt_token) == str

    decoded_jwt_token = jwt.decode(encoded_jwt_token, JWT_SECRET_KEY, JWT_ALGORITHM)
    assert decoded_jwt_token['exp'] == int(expires_secs_from_epoch)
    assert decoded_jwt_token['test'] == 'value'
    assert decoded_jwt_token['sub'] == 'test_value'

    encoded_jwt_token = create_access_token(data_to_encode)
    decoded_jwt_token = jwt.decode(encoded_jwt_token, JWT_SECRET_KEY, JWT_ALGORITHM)
    assert decoded_jwt_token['exp'] == \
           int((datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())


def test_get_password_hash():
    plain_password = 'test_password'
    hashed_password = get_password_hash(plain_password)
    assert pwd_context.verify(plain_password, hashed_password)
    assert not pwd_context.verify('test', hashed_password)


def test_verify_password():
    plain_password = 'test_password'
    hashed_password = pwd_context.hash(plain_password)
    assert verify_password(plain_password, hashed_password)
    assert not verify_password('test', hashed_password)


def test_check_user_is_superuser():
    user = User(
        email='test',
        hashed_password=pwd_context.hash('test'),
        is_superuser=False,
    )
    assert not check_user_is_superuser(user)
    setattr(user, 'is_superuser', True)
    assert check_user_is_superuser(user)
    user = None
    assert not check_user_is_superuser(user)
