from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

        #path('', views.generate_all, name="index"),
        path('', views.index, name="index"),
        path('cars/<str:pk>/',views.cars, name="cars"),
        path('login/', views.loginPage, name="login"),
        path('logout/', views.logoutUser, name="logout"),
        path('register/', views.registerPage, name="register"),
        path('dashboard/<str:pk_test>/', views.dashboard, name="dashboard"),
        path('admindashboard/', views.adminDashboard, name="admin_dashboard"),
        path('create_order/<str:pk>/<str:vid>/', views.createOrder, name="create_order"),
        path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
        path('update_vehicle/<str:pk>/', views.updateVehicle, name="update_vehicle"),
        path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
        path('delete_vehicle/<str:pk>/', views.deleteVehicle, name="delete_vehicle"),
        path('pay_order/<str:pk>/<str:custid>/', views.payOrder, name="pay_order"),
        path('reset_password/', auth_views.PasswordResetView.as_view(template_name="wow/password_reset.html"), name="reset_password"),
        path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="wow/password_reset_sent.html"), name="password_reset_done"),
        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="wow/password_reset_form.html"), name="password_reset_confirm"),
        path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="wow/password_reset_done.html"), name="password_reset_complete"),
        path('create_loc/', views.createRentalLoc, name="createRentalLoc"),
        path('create_vehicle/',  views.createRentalVehicle, name="createRentalVehicle")

]


'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''