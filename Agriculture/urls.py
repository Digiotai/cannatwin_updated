from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/', views.testing, name='testing'),
    path('api/register/', views.registerPage, name="register"),
    path('api/login/', views.loginPage, name="login"),
     path('api/googlelogin/', views.googlelogin, name="googlelogin"),
    path('api/fileupload/', views.fileupload, name="fileupload"),
    path('api/logout/', views.logoutUser, name="logout"),
    path('api/getuserdetails/', views.getuserdetails, name="getuserdetails"),
    path('api/getdatawithinrange/', views.getdatawithinrange, name="getdatawithinrange"),
    path('api/getroomsdata/', views.getroomsdata, name="getroomsdata"),
    path('api/harvestfileupload/', views.fileupload_harvest, name="fileuploadharvest"),
    path('api/getharvestdata/', views.getharvestdata, name="getharvestdata"),
    path('api/getlayoutsectionadd/', views.getlayoutsectionadd, name="getlayoutsectionadd"),
    path('api/getlayoutsectionread/', views.getlayoutsectionread, name="getlayoutsectionread"),
    path('api/getlayoutsectionupdate/', views.getlayoutsectionupdate, name="getlayoutsectionupdate"),
    path('api/getlayoutsectiondelete/', views.getlayoutsectiondelete, name="getlayoutsectiondelete"),
    path('api/gethardwareadd/', views.gethardwareadd, name="gethardwareadd"),
    path('api/gethardwareread/', views.gethardwareread, name="gethardwareread"),
    path('api/gethardwareupdate/', views.gethardwareupdate, name="gethardwareupdate"),
    path('api/gethardwaredelete/', views.gethardwaredelete, name="gethardwaredelete"),
    path('api/getsoftwareadd/', views.getsoftwareadd, name="getsoftwareadd"),
    path('api/getsoftwareread/', views.getsoftwareread, name="getsoftwareread"),
    path('api/getsoftwareupdate/', views.getsoftwareupdate, name="getsoftwareupdate"),
    path('api/getsoftwaredelete/', views.getsoftwaredelete, name="getsoftwaredelete"),


    # Password reset request view
    path('api/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    # Email sent confirmation
    path('api/password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # Password reset form link sent to email
    path('api/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Password successfully changed
    path('api/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]
