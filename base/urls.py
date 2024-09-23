from django.urls import path
from base.views import *
urlpatterns = [
    path('login/',MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('register', register),

    path("user", get_user),

    path('equipments/', get_all_equipment),
    path('equipment/', create_equipment, name='create-equipment'),
    path('equipment/update/<int:pk>/', update_equipment),
    path('equipment/details/<int:pk>/', get_equipment_by_id),
    path('equipment/delete/<str:pk>', delete_equipment),
]
