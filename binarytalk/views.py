from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import psycopg2  # For PostgreSQL connection
import json
conn = None
@csrf_exempt
def connect_db(request):
    global conn
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
            return JsonResponse({"success": True, "message": "Database connected successfully!"})  # ✅ Fix Response
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)  # ✅ Fix Response

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def execute_query(request):
    global conn  
    if request.method == "POST":
        if conn is None:  
            return JsonResponse({"success": False, "error": "No active database connection"}, status=400)

        try:
            data = json.loads(request.body)
            query = data.get("query")

            if not query:
                return JsonResponse({"success": False, "error": "Query is required"}, status=400)

            cursor = conn.cursor()
            cursor.execute(query)

            if query.lower().startswith("select"):
                result = cursor.fetchall()
            else:
                conn.commit()
                result = "Query executed successfully"

            cursor.close()
            return JsonResponse({"success": True, "result": result})

        except Exception as e:
            conn.rollback()  # 🔹 Rollback the failed transaction
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def disconnect_db(request):
    global conn
    if conn:
        conn.close()
        conn = None
        return JsonResponse({"success": True, "message": "Database disconnected successfully!"})
    return JsonResponse({"success": False, "error": "No active database connection"}, status=400)