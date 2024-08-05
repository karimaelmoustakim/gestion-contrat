from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def profil(request):
    return render(request, 'profil.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        old_password = request.POST.get('oldPassword')
        new_password = request.POST.get('newPassword')

        user = request.user

        # Update username and email
        user.username = username
        user.email = email
        user.save()

        # Check if old password is correct and change password
        if old_password and new_password:
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Important to update session

                messages.success(request, 'Password changed successfully.')
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Incorrect old password.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Please provide both old and new passwords.'})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})