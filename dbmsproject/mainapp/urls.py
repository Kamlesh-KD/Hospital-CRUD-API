from django.urls import path
from .views import UserSignup, UserSignIn, AddPatient, GetPatient, EditPatient, DeletePatient

urlpatterns = [
    path('api/signup/', UserSignup.as_view(), name='user_signup'),
    path('api/signin/', UserSignIn.as_view(), name='user_signin'),
    path('api/patients/', AddPatient.as_view(), name='add_patient'),
    path('api/patients/<int:patient_id>/', GetPatient.as_view(), name='get_patient'),
    path('api/edit-patient/<int:patient_id>/', EditPatient.as_view(), name='edit_patient'),
    path('api/delete-patient/<int:patient_id>/', DeletePatient.as_view(), name='delete_patient'),
]
