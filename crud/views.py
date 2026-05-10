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
            
      Genders.objects.create(gender=gender).save()
      messages.success(request, 'Gender added succesfully!')
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
        'gender':genderObj
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
  

# FIXME: SIDEBAR CHECK
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
        if request.method == 'POST':
            userObj = Users.objects.get(pk=userId)

            userObj.full_name = request.POST.get('full_name')
            userObj.gender = Genders.objects.get(pk=request.POST.get('gender'))
            userObj.birth_date = request.POST.get('birth_date')
            userObj.address = request.POST.get('address')
            userObj.contact_number = request.POST.get('contact_number')
            userObj.email = request.POST.get('email')
            userObj.username = request.POST.get('username')


# TODO:PARA MA CHANGE IMAGE
            if request.FILES.get('profile_pic'):
                userObj.profile_pic = request.FILES.get('profile_pic')

            userObj.save()
            messages.success(request, 'User updated successfully!')

            data = {
                'user': userObj,
                'genders': Genders.objects.all()
            }

            return render(request, 'user/EditUser.html', data)

        else:
            userObj = Users.objects.get(pk=userId)

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
      fullName = request.POST.get('full_name')
      gender = request.POST.get('gender')
      birthDate = request.POST.get('birth_date')
      address = request.POST.get('address')
      contactNumber = request.POST.get('contact_number')
      email = request.POST.get('email')
      username = request.POST.get('username')
      password = request.POST.get('password')
      confirmPassword = request.POST.get('confirm_password')
      profile_pic = request.FILES.get('profile_pic')


# FIXME: password validation CHECK
      if password != confirmPassword:
        messages.error(request, "Password does not match!")
        return redirect('/user/add')
      
 # FIXME: Para indi mag double ang username
      if Users.objects.filter(username=username).exists():
        messages.error(request, "Username already exists!")
        return redirect('/user/add')

      Users.objects.create(
        full_name=fullName,
        gender=Genders.objects.get(pk=gender),
        birth_date=birthDate,
        address=address,
        contact_number=contactNumber,
        email = email,
        username=username,
        password=make_password(password),
        profile_pic=profile_pic
      ).save()

      messages.success(request, 'User added succesfully!')
      return redirect('/user/add')


    else:
      genderObj = Genders.objects.all()

      data = {
        'genders':genderObj
      }
    return render(request, 'user/AddUser.html', data)
  except Exception as e:
    return HttpResponse(f'Error occurred during add user: {e}')
  