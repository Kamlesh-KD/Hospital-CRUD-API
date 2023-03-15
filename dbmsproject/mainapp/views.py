from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .serializers import UserSerializer, PatientSerializer


class UserSignup(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Ensure both username and password are provided
        if not username or not password:
            return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the username is unique
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM auth_user WHERE username=%s', [username])
            if cursor.fetchone():
                return Response({'error': 'This username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO auth_user (username, password) VALUES (%s, %s)', [username, password])
            user_id = cursor.lastrowid

        # Serialize and return the user data
        user = {'id': user_id, 'username': username}
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.db import connection

class UserSignIn(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Ensure both username and password are provided
        if not username or not password:
            return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Find the user with the provided username
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM auth_user WHERE username=%s', [username])
            user = cursor.fetchone()

        # Ensure the user exists
        if not user:
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

        # # Ensure the provided password matches the user's password
        # if not check_password(password, user[2]):
        #     return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Return the user's data
        user_data = {'id': user[0], 'username': user[1]}
        return Response(user_data, status=status.HTTP_200_OK)
    


class AddPatient(APIView):
    def post(self, request):
        user_id = request.user.id
        data = request.data

        # Add the user_id to the data before serializing it
        data['user_id'] = user_id

        # Serialize the data and validate it
        serializer = PatientSerializer(data=data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Add the new patient to the database using SQL queries
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO patients (name, age, gender, phone, email, address, user_id, doctor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [data['name'], data['age'], data['gender'], data['phone'], data['email'], data['address'], user_id, data['doctor']])
            patient_id = cursor.lastrowid

        # Retrieve the new patient from the database
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, age, gender, phone, email, address, doctor FROM patients WHERE id = %s", [patient_id])
            row = cursor.fetchone()
            patient_data = {'id': row[0], 'name': row[1], 'age': row[2], 'gender': row[3], 'phone': row[4], 'email': row[5], 'address': row[6], 'doctor': row[7]}

        # Return the serialized patient data
        return Response(patient_data, status=status.HTTP_201_CREATED)


class GetPatient(APIView):
    def get(self, request, patient_id):
        user_id = request.user.id

        # Retrieve the patient data from the database using SQL queries
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, age, gender, phone, email, address, doctor FROM patients WHERE id = %s AND user_id = %s", [patient_id, user_id])
            row = cursor.fetchone()

            if row is None:
                return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

            patient_data = {'id': row[0], 'name': row[1], 'age': row[2], 'gender': row[3], 'phone': row[4], 'email': row[5], 'address': row[6], 'doctor': row[7]}

        # Return the patient data in the response
        return Response(patient_data, status=status.HTTP_200_OK)
    

class EditPatient(APIView):
    def put(self, request, patient_id):
        user_id = request.user.id

        # Retrieve the patient data from the database using SQL queries
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, age, gender, phone, email, address, doctor FROM patients WHERE id = %s AND user_id = %s", [patient_id, user_id])
            row = cursor.fetchone()

            if row is None:
                return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update the patient data in the database using SQL queries
        with connection.cursor() as cursor:
            cursor.execute("UPDATE patients SET name = %s, age = %s, gender = %s, phone = %s, email = %s, address = %s, doctor= %s WHERE id = %s AND user_id = %s", [request.data['name'], request.data['age'], request.data['gender'], request.data['phone'], request.data['email'], request.data['address'], request.data['doctor'], patient_id, user_id])

            # Get the number of rows affected by the update query
            num_rows_affected = cursor.rowcount

            if num_rows_affected == 0:
                return Response({'error': 'Patient not found or user does not have permission to edit this patient'}, status=status.HTTP_404_NOT_FOUND)

        # Return a success response
        return Response({'success': 'Patient data updated successfully'}, status=status.HTTP_200_OK)

class DeletePatient(APIView):
    def delete(self, request, patient_id):
        user_id = request.user.id

        # Delete the patient data from the database using SQL queries
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM patients WHERE id = %s AND user_id = %s", [patient_id, user_id])

            # Get the number of rows affected by the delete query
            num_rows_affected = cursor.rowcount

            if num_rows_affected == 0:
                return Response({'error': 'Patient not found or user does not have permission to delete this patient'}, status=status.HTTP_404_NOT_FOUND)

        # Return a success response
        return Response({'success': 'Patient data deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
