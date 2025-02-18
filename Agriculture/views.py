from django.shortcuts import render, HttpResponse
from django.http import JsonResponse, request
from django.contrib.auth import authenticate, login, logout
from .form import CreateUserForm
from django.views.decorators.csrf import csrf_exempt
from .database import PostgreSQLDB
import io
from io import StringIO
import pandas as pd
import json
from dotenv import load_dotenv


db = PostgreSQLDB(dbname='test', user='test_owner', password='tcWI7unQ6REA')
load_dotenv()

# db.table_creation()
@csrf_exempt
def testing(request):
    return HttpResponse("Application is up")


from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


@csrf_exempt
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # try:
        #     # Check if the user with the provided email exists
        #     user = User.objects.get(email=email)
        # except User.DoesNotExist:
        #     return JsonResponse({"status": "error", "message": "Invalid email or password"}, status=401)

        # Authenticate the user using the username (retrieved from the email) and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)

            # Prepare the user details to return as a response
            user_details = {
                'username': user.username,
                'email': user.email,
                # Add other fields if needed
            }

            return JsonResponse({"status": "success", "user": user_details})
        else:
            return JsonResponse({"status": "error", "message": "Invalid email or password"}, status=401)

    return JsonResponse({"status": "error", "message": "Login failed"}, status=400)


@csrf_exempt
def registerPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                user_name = request.POST.get('username')
                password1 = request.POST.get('password1')
                # password2 = request.POST.get('password')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                address = request.POST.get('address')
                email = request.POST.get('email')
                mobile = request.POST.get('mobile')
                res = db.add_user(user_name, password1, first_name, last_name, address, email, mobile)
                if res=='Success':
                    return HttpResponse("Success")
                else:
                    return HttpResponse(res)
            else:
                print(form.errors)
                return HttpResponse(str(form.errors))
        except Exception as e:
            print(e)
        return HttpResponse("Registration Failed1")



@csrf_exempt
def getuserdetails(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        if not email:
            return HttpResponse('Email not provided.', status=400)

        user_data = db.get_user_data(email)
        if not user_data:
            return HttpResponse('User not found.', status=404)

        return JsonResponse({"userinfo": list(user_data)}, safe=False)





@csrf_exempt
def googlelogin(request):
    if request.method == 'POST':
        try:
            username = request.POST.get("username")
            user_id = request.POST.get("id")
            email = request.POST.get("email")

            # Generate a password (you might want to handle this differently in production)
            password =  "auto@" + user_id

            # Check if the user already exists
            users = db.get_users()
            if email in [user[0] for user in users]:
                user_details = db.get_user_data(email)
                return JsonResponse({"status": "Success", "user_details": user_details})
            else:
                # Create a new user
                form = CreateUserForm({
                    'username': username,
                    'email': email,
                    'password1': password,
                    'password2': password
                })
                if form.is_valid():
                    form.save()
                    db.add_user(
                        user_name=username,
                        password=password,
                        first_name="",  # You can get these from the request if available
                        last_name="",
                        address="",
                        email=email,
                        mobile=""
                    )
                    user_details = db.get_user_data(email)
                    return JsonResponse({"status": "Success", "user_details": user_details})
                else:
                    return JsonResponse({"status": "Error", "errors": form.errors})
        except Exception as e:
            return JsonResponse({"status": "Error", "message": str(e)})
    else:
        return JsonResponse({"status": "Error", "message": "Invalid request method"})


@csrf_exempt
def logoutUser(request):
    pass



# File upload for rooms data
@csrf_exempt
def fileupload(request):
    try:
        # Check if the request method is POST
        if request.method != 'POST':
            return HttpResponse('Invalid request method. Only POST is allowed.', status=405)

        # Get user email from request data ( it's passed as part of the request)
        email = request.POST.get('email')
        if not email:
            return HttpResponse('User email not provided.', status=400)

        # Get the uploaded file
        files = request.FILES.get('file')
        if not files:
            return HttpResponse('No files uploaded', status=400)

        # Determine the file extension
        file_extension = files.name.split('.')[-1].lower()

        # Read file content based on the file extension
        if file_extension == 'csv':
            content = files.read().decode('utf-8')
            csv_data = io.StringIO(content)
            df = pd.read_csv(csv_data)
        elif file_extension == 'xlsx':
            df = pd.read_excel(files)
        else:
            return HttpResponse('Unsupported file format. Please upload a CSV or XLSX file.', status=400)

        # Save the data to the database using the store_file_data method
        db.store_file_data(email, df)

        # Convert DataFrame to JSON format and return it as a response
        response_data = df.to_dict(orient='records')
        return JsonResponse(response_data, safe=False)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


@csrf_exempt
def getdatawithinrange(request):
    return HttpResponse("Under Dev")



# #Get rooms data
# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# import pandas as pd
# import json

# @csrf_exempt
# def getroomsdata(request):
#     try:
#         # Ensure the request method is POST
#         if request.method != 'POST':
#             return HttpResponse('Invalid request method. Only POST is allowed.', status=405)

#         # Get the user email from the request parameters
#         email = request.POST.get('email')
#         if not email:
#             return HttpResponse('User email not provided.', status=400)

#         # Fetch the uploaded data using the email
#         data = db.get_uploaded_data(email)  # Assumes this returns a list of JSON objects

#         if not data:
#             return HttpResponse('No data found for the provided email.', status=404)

#         # Convert the data to a DataFrame
#         df = pd.DataFrame(data)

#         print(df)

#         # Debugging: Print column names to ensure TimeStamp exists
#         print("Columns in DataFrame:", df.columns)

#         # Check if 'TimeStamp' column exists and is correctly named
#         if 'TimeStamp' not in df.columns:
#             return HttpResponse('Column "TimeStamp" not found in data.', status=400)

#         # Convert 'TimeStamp' to datetime
#         df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])

#         # Extract the date part
#         df['Date'] = df['TimeStamp'].dt.date

#         # Extract filters from the POST data
#         from_date = request.POST.get('from_date')
#         to_date = request.POST.get('to_date')
#         facility = request.POST.get('facility')
#         room = request.POST.get('room')

#         # Convert dates to date objects
#         from_date = pd.to_datetime(from_date).date()
#         to_date = pd.to_datetime(to_date).date()

#         # Filter the DataFrame based on facility, room, and date range
#         df = df[(df["Facility"] == facility) & (df["Rooms"] == room)]

#         # Drop unwanted columns
#         df.drop(["Facility", "Rooms", "TimeStamp"], inplace=True, axis=1)

#         # Group by date and calculate the mean for numerical columns
#         result_df = df.groupby('Date').mean().reset_index()

#         # Filter by the provided date range
#         result_df = result_df[(result_df["Date"] >= from_date) & (result_df["Date"] <= to_date)]

#         # Convert the result to JSON
#         result_json = result_df.to_json(orient='records')

#         # Return the JSON response
#         return HttpResponse(json.dumps({"rooms_data": result_json}), content_type="application/json")

#     except Exception as e:
#         # Return the error message
#         return HttpResponse(f"An error occurred: {str(e)}", status=500)


#Get rooms data api
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def getroomsdata(request):
    try:
        # Ensure the request method is GET
        if request.method != 'GET':
            return HttpResponse('Invalid request method. Only GET is allowed.', status=405)

        # Get the user email from the request parameters
        email = request.GET.get('email')
        if not email:
            return HttpResponse('User email not provided.', status=400)

        # Fetch the uploaded data using the email
        uploaded_data = db.get_uploaded_data(email)

        # Check if any data was found
        if not uploaded_data:
            return JsonResponse({'message': 'No data found for the provided email.'}, status=404)

        # Return the data directly as JSON
        return JsonResponse(uploaded_data, safe=False)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)





@csrf_exempt
def getdatawithinrange(request):
    return HttpResponse("Under Dev")



## For Harvest data
# File upload for rooms data
@csrf_exempt
def fileupload_harvest(request):
    try:
        # Check if the request method is POST
        if request.method != 'POST':
            return HttpResponse('Invalid request method. Only POST is allowed.', status=405)

        # Get user email from request data ( it's passed as part of the request)
        email = request.POST.get('email')
        if not email:
            return HttpResponse('User email not provided.', status=400)

        # Get the uploaded file
        files = request.FILES.get('file')
        if not files:
            return HttpResponse('No files uploaded', status=400)

        # Determine the file extension
        file_extension = files.name.split('.')[-1].lower()

        # Read file content based on the file extension
        if file_extension == 'csv':
            content = files.read().decode('utf-8')
            csv_data = io.StringIO(content)
            df = pd.read_csv(csv_data)
        elif file_extension == 'xlsx':
            df = pd.read_excel(files)
        else:
            return HttpResponse('Unsupported file format. Please upload a CSV or XLSX file.', status=400)

        # Save the data to the database using the store_file_data method
        db.store_file_data_for_harvest(email, df)

        # Convert DataFrame to JSON format and return it as a response
        response_data = df.to_dict(orient='records')
        return JsonResponse(response_data, safe=False)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)





#Get harvest data api
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def getharvestdata(request):
    try:
        # Ensure the request method is GET
        if request.method != 'GET':
            return HttpResponse('Invalid request method. Only GET is allowed.', status=405)

        # Get the user email from the request parameters
        email = request.GET.get('email')
        if not email:
            return HttpResponse('User email not provided.', status=400)

        # Fetch the uploaded data using the email
        uploaded_data = db.get_uploaded_data_for_harvest(email)

        # Check if any data was found
        if not uploaded_data:
            return JsonResponse({'message': 'No data found for the provided email.'}, status=404)

        # Return the data directly as JSON
        return JsonResponse(uploaded_data, safe=False)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)





@csrf_exempt
def getlayoutsectionadd(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getlayoutsectionread(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getlayoutsectionupdate(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getlayoutsectiondelete(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def gethardwareadd(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def gethardwareread(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def gethardwareupdate(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def gethardwaredelete(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getsoftwareadd(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getsoftwareread(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getsoftwareupdate(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getsoftwaredelete(request):
    return HttpResponse("Under Dev")
