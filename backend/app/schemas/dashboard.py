from pydantic import BaseModel

class DashboardResponse(BaseModel):
    restaurant_id: int
    restaurant_name: str
    total_orders: int
    pending_orders: int
    confirmed_orders: int
    preparing_orders: int
    ready_orders: int
    delivered_orders: int
    cancelled_orders: int
    total_revenue: float