from fastapi import Header, HTTPException


def require_roles(allowed_roles: list):
    def role_checker(x_role: str = Header(...)):
        if x_role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return x_role
    return role_checker