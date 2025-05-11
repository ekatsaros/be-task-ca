class UserError(Exception):
    """Base exception for user domain"""
    pass

class UserNotFoundError(UserError):
    """Raised when user is not found"""
    pass

class UserAlreadyExistsError(UserError):
    """Raised when attempting to create a duplicate user"""
    pass