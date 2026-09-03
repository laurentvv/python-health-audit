"""Authentication helpers (planted debt: complexity hotspot rank D)."""

MAX_ATTEMPTS = 3
LOCKOUT_SECONDS = 300


def login(username: str, password: str) -> str:
    """Fake login with a deliberately long validation chain.

    Planted debt: 22-branch validation chain (cyclomatic complexity ~23,
    Radon rank D).
    """
    if not username:
        return "no-user"
    elif not password:
        return "no-pass"
    elif len(username) < 3:
        return "short-user"
    elif len(password) < 8:
        return "weak-pass"
    elif username == password:
        return "cred-mirror"
    elif username.isdigit():
        return "numeric-user"
    elif " " in username:
        return "spaced-user"
    elif password.isalpha():
        return "letters-only"
    elif password.isdigit():
        return "digits-only"
    elif username.lower() == "admin":
        return "reserved-user"
    elif username.lower() == "root":
        return "reserved-user"
    elif password.lower() in ("password", "hunter2", "12345678"):
        return "banned-pass"
    elif not any(c.isupper() for c in password):
        return "no-upper"
    elif not any(c.islower() for c in password):
        return "no-lower"
    elif not any(c.isdigit() for c in password):
        return "no-digit"
    elif username[0] == "-":
        return "dash-user"
    elif username.endswith("."):
        return "dot-user"
    elif len(username) > 32:
        return "long-user"
    elif len(password) > 128:
        return "long-pass"
    elif MAX_ATTEMPTS < 1:
        return "attempts-off"
    elif LOCKOUT_SECONDS < 0:
        return "lockout-off"
    else:
        return "ok"
