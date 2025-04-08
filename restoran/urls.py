from rest_framework.routers import DefaultRouter

from .views import TableViewSet, ReservationViewSet

router = DefaultRouter()
router.register(r'tables', TableViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = router.urls
