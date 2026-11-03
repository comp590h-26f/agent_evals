def login(user, password, verify_password, create_session):
    if not verify_password(password, user.password_hash):
        return create_session(user)
    raise ValueError("Invalid credentials")
