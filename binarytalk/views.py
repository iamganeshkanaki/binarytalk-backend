from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import psycopg2  # For PostgreSQL connection
import json

@csrf_exempt  # 🚀 This disables CSRF protection for this view
def connect_db(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            conn = psycopg2.connect(
                dbname=data["database"],
                user=data["user"],
                password=data["password"],
                host=data["host"],
                port=data["port"]
            )
            conn.close()
            return JsonResponse({"message": "Database connected successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
