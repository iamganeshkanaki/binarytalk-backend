from django.urls import path, include
from . import views
from .views import connect_db
# , disconnect_db, execute_query

# This file defines the URL patterns for the binarytalk application.
urlpatterns = [
    path('connect-db/', connect_db, name='connect_db'),
    # path('disconnect-db/', disconnect_db, name='disconnect_db'),
    # path('sql-execute/', execute_query, name='sql_execute'),
]