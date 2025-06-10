from django.shortcuts import render
import boto3
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Initialize S3 Client


# def get_s3_client():
#     return boto3.client(
#         's3',
#         endpoint_url=settings.AWS_S3_ENDPOINT_URL,
#         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
#     )


import boto3
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('image'):
        file = request.FILES['image']
        try:
            s3_client = boto3.client(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            s3_client.upload_fileobj(
                file,
                settings.AWS_STORAGE_BUCKET_NAME,
                file.name,
                ExtraArgs={'ContentType': file.content_type}
            )

            file_url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{file.name}"
            return JsonResponse({'message': 'Uploaded successfully', 'url': file_url})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'No file provided or invalid request'}, status=400)

