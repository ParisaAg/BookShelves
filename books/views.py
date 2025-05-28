from rest_framework import generics, filters
from rest_framework.generics import RetrieveAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView,ListAPIView
from .models import Book,Category,Author
from .serializers import BookSerializer,CategorySerializer,AuthorSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permission import IsAdminOrStaff
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # برای تست موقت، در پروداکشن CSRF token رو مدیریت کنید
import cloudinary.uploader



class BookListView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author'] 
    search_fields = ['title', 'description']  
    ordering_fields = ['published_year', 'price']  
    #ordering = ['-published_year']





class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



class BookCreateAPIView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrStaff]


class BookUpdateAPIView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrStaff]
    lookup_field = 'id'



class BookDeleteAPIView(DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAdminOrStaff]
    lookup_field = 'id'




class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff]

class CategoryRetrieveView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff]

class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff]

class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff]

class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer



class LatestBooksView(ListAPIView):
    queryset = Book.objects.all().order_by('-created_at')[:10] 
    serializer_class = BookSerializer






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

class UploadImageToCloudinaryView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('imageFile')  # 'imageFile' نامی است که از فرانت‌اند می‌آید

        if not image_file:
            return Response({'error': 'فایلی برای آپلود انتخاب نشده است.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # آپلود فایل به Cloudinary
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder="my_app_uploads",  # نام پوشه دلخواه در Cloudinary
                # میتونید گزینه‌های بیشتری مثل public_id و... رو هم اینجا اضافه کنید
            )

            # URL امن تصویر آپلود شده
            image_url = upload_result.get('secure_url')
            public_id = upload_result.get('public_id')  # برای مدیریت یا حذف عکس در آینده

            # اینجا می‌تونید image_url و public_id رو در دیتابیس ذخیره کنید
            # مثلا: MyImageModel.objects.create(user=request.user, image_url=image_url, public_id=public_id)

            return Response({
                'message': 'عکس با موفقیت در Cloudinary آپلود شد!',
                'imageUrl': image_url,
                'publicId': public_id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'خطا در آپلود به Cloudinary: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)