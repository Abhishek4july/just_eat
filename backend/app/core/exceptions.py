from fastapi import HTTPException, status
from fastapi import HTTPException, status


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

class OrderNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action.",
        )

class RestaurantAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Restaurant already exists.",
        )

class RestaurantNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found.",
        )


class MenuItemNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found.",
        )



class MenuItemNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found.",
        )



from fastapi import HTTPException, status


class FavoriteNotFoundException(HTTPException):
    def __init__(
        self,
        menu_item_id: int,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu item {menu_item_id} is not in favorites.",
        )


class FavoriteAlreadyExistsException(HTTPException):
    def __init__(
        self,
        menu_item_id: int,
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Menu item {menu_item_id} is already in favorites.",
        )


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect.",
        )


class FavoriteRestaurantAlreadyExistsException(
    HTTPException,
):
    def __init__(
        self,
        restaurant_id: int,
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Restaurant {restaurant_id} is already in favorites.",
        )


class FavoriteRestaurantNotFoundException(
    HTTPException,
):
    def __init__(
        self,
        restaurant_id: int,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restaurant {restaurant_id} is not in favorites.",
        )