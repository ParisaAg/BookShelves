from rest_framework.routers import DefaultRouter
from .views import PostViewSet, BlogCategoryViewSet, TagViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', BlogCategoryViewSet, basename='blog-category')
router.register(r'tags', TagViewSet, basename='blog-tag')

urlpatterns = router.urls