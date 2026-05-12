from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

# TODO:GENDER LIST
def gender_list(request):
  try:
    genders = Genders.objects.all()

    data={
      'genders':genders
    }

    return render(request, 'gender/GendersList.html', data)
  except Exception as e:
    return HttpResponse(f'Error occurred during load gender: {e}')
  

#TODO: ADD GENDER
def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')

            # Validation
            if not gender:
                messages.error(request, 'Gender field is required!')
                return render(request, 'gender/AddGender.html')

            Genders.objects.create(gender=gender)
            messages.success(request, 'Gender added successfully!')
            return redirect('/gender/list')

        else:
            return render(request, 'gender/AddGender.html')

    except Exception as e:
        return HttpResponse(f'Error occurred during add gender: {e}')
    
    

# TODO:EDIT GENDER
def edit_gender(request, genderId):
    try:
      if request.method == 'POST':
        genderObj = gender = Genders.objects.get(pk=genderId)
        gender = request.POST.get('gender')

        genderObj.gender = gender
        genderObj.save()
        messages.success(request,'Gender updated succesfully!')

        data = {
          'gender':genderObj
        }

        return render(request, 'gender/EditGender.html', data)
      else:
        genderObj = Genders.objects.get(pk=genderId)

        data = {
          'gender':genderObj
        }
        
        return render(request, 'gender/EditGender.html', data)
    except Exception as e:
      return HttpResponse(f'Error occurred during edit gender: {e}')



# TODO:DELETE GENDER
def delete_gender(request, genderId):
  try:
    if request.method == 'POST':
      genderObj = Genders.objects.get(pk=genderId)
      genderObj.delete()

      messages.success(request, 'Gender deleted succesfully!')
      return redirect('/gender/list')
    else:
      genderObj = Genders.objects.get(pk=genderId)

      data = {
        'gender':genderObj,
        'genders': Genders.objects.all()
      }
      
      return render(request, 'gender/DeleteGender.html', data)
  except Exception as e:
    return HttpResponse(f'Error occurred during delete gender: {e}')
  

  
# TODO:USER LIST
def user_list(request):
  try:
    userObj = Users.objects.select_related('gender')
    data = {
      'users': userObj
    }
    return render(request, 'user/UserList.html', data)
  except Exception as e:
    return HttpResponse(f'Error occurred during  load  users: {e}')
  

# FIXME: SEARCH BAR CHECK
def user_list(request):
    search = request.GET.get('search')

    users = Users.objects.select_related('gender')


    if search:
        users = users.filter(
            Q(full_name__icontains=search) |
            Q(gender__gender__icontains=search) |
            Q(birth_date__icontains=search) |
            Q(address__icontains=search) |
            Q(contact_number__icontains=search) |
            Q(email__icontains=search)
        )

    users = users.order_by('-user_id')


# FIXME: PARA SA PAGINATOR CHECK
    paginator = Paginator(users, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user/UserList.html', {
        'page_obj': page_obj,
        'search': search
    })
  

# TODO: EDIT USER
def edit_user(request, userId):
    try:
        userObj = Users.objects.get(pk=userId)

        if request.method == 'POST':

            username = request.POST.get('username')

            # TODO: username exixt warning
            if Users.objects.filter(username=username).exclude(pk=userId).exists():
                messages.error(request, "Username already exists!")
                return redirect(f'/user/edit/{userId}')

            userObj.full_name = request.POST.get('full_name')
            userObj.gender = Genders.objects.get(pk=request.POST.get('gender'))
            userObj.birth_date = request.POST.get('birth_date')
            userObj.address = request.POST.get('address')
            userObj.contact_number = request.POST.get('contact_number')
            userObj.email = request.POST.get('email')
            userObj.username = username

            # TODO: PARA MA CHANGE IMAGE CHECK
            if request.FILES.get('profile_pic'):
                userObj.profile_pic = request.FILES.get('profile_pic')

            userObj.save()
            messages.success(request, 'User updated successfully!')

            return redirect('/user/list')

        else:
            data = {
                'user': userObj,
                'genders': Genders.objects.all()
            }

            return render(request, 'user/EditUser.html', data)

    except Exception as e:
        return HttpResponse(f'Error occurred during edit user: {e}')
    

# TODO: DELETE USER
def delete_user(request, userId):
    try:
        if request.method == 'POST':
            userObj = Users.objects.get(pk=userId)
            userObj.delete()

            messages.success(request, 'User deleted successfully!')
            return redirect('/user/list')

        else:
            userObj = Users.objects.get(pk=userId)

            data = {
                'user': userObj
            }

            return render(request, 'user/DeleteUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error occurred during delete user: {e}')



# TODO:ADD USER
def add_user(request):
    try:
        if request.method == 'POST':

            fullName = request.POST.get('full_name').strip()
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address').strip()
            contactNumber = request.POST.get('contact_number').strip()
            email = request.POST.get('email').strip()
            username = request.POST.get('username').strip()
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')
            profile_pic = request.FILES.get('profile_pic')


            # FIXME: Required fields validation
            if not fullName:
                messages.error(request, "Full name is required!")
                return redirect('/user/add')

            if not gender:
                messages.error(request, "Gender is required!")
                return redirect('/user/add')

            if not birthDate:
                messages.error(request, "Birth date is required!")
                return redirect('/user/add')

            if not address:
                messages.error(request, "Address is required!")
                return redirect('/user/add')

            if not contactNumber:
                messages.error(request, "Contact number is required!")
                return redirect('/user/add')

            if not email:
                messages.error(request, "Email is required!")
                return redirect('/user/add')

            if not username:
                messages.error(request, "Username is required!")
                return redirect('/user/add')

            if not password:
                messages.error(request, "Password is required!")
                return redirect('/user/add')


            # FIXME: password validation CHECK
            if password != confirmPassword:
                messages.error(request, "Password does not match!")
                return redirect('/user/add')

            # FIXME: Para indi mag double ang username CHECK
            if Users.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
                return redirect('/user/add')

            Users.objects.create(
                full_name=fullName,
                gender=Genders.objects.get(pk=gender),
                birth_date=birthDate,
                address=address,
                contact_number=contactNumber,
                email=email,
                username=username,
                password=make_password(password),
                profile_pic=profile_pic
            )

            messages.success(request, 'User added successfully!')
            return redirect('/user/add')

        else:
            genderObj = Genders.objects.all()

            data = {
                'genders': genderObj
            }

        return render(request, 'user/AddUser.html', data)

    except Exception as e:
        return HttpResponse(f'Error occurred during add user: {e}')