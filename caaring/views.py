

from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

from caaring.forms import NewCabForm
from .models import Cab, User, Passenger, APPROVED,DECLINED, REQUESTED


def index(request):
    return render(request,'homepage.html')

@login_required
def Home(request):


    passengers=Passenger.objects.filter(user=request.user)
    my_cabs=[]
    for passenger in passengers:
        my_cabs.append(Cab.objects.get(name=passenger.of_cab.name))

    allcabs=list(Cab.objects.all())
    cabs=[x for x in allcabs if x not in my_cabs]


    return render(request,'home.html',{'cabs':cabs,'my_cabs':my_cabs,'user':request.user})

@login_required
def My_Account(request):
    user=request.user
    return render(request,'my_details.html',{'user':user})

@login_required
def Request_pass(request,name):
    cab=Cab.objects.get(name=name)
    passengers=Passenger.objects.filter(of_cab=cab)
    try:
        passenger=passengers.get(user=request.user)
        passenger.approval_status=REQUESTED
        passenger.save()
    except:
        passenger=Passenger.objects.create(is_admin=False,
                                               approval_status=REQUESTED,
                                               user=request.user,
                                               of_cab=cab)

    return HttpResponseRedirect('/cabs/'+name,name)
    #return Cab_detail(request,name)

@login_required
def Accept_pass(request,name,uname):
    cab=Cab.objects.get(name=name)
    passengers=Passenger.objects.filter(of_cab=cab)
    try:
        curr_pass=passengers.get(user=User.objects.get(username=uname))
        curr_pass.approval_status=APPROVED
        curr_pass.save()
        cab.seats_left-=1
        cab.save()
    except:
        raise Http404
    return HttpResponseRedirect('/cabs/'+name,name)

@login_required
def Decline_pass(request,name,uname):
    cab=Cab.objects.get(name=name)
    passengers=Passenger.objects.filter(of_cab=cab)
    try:
        curr_pass=passengers.get(user=User.objects.get(username=uname))
        curr_pass.approval_status=DECLINED
        curr_pass.save()
    except:
        raise Http404
    return HttpResponseRedirect('/cabs/'+name,name)

@login_required
def Cab_detail(request,name):
    try:
        permission=False
        cab = Cab.objects.get(name=name)
        passengers=Passenger.objects.filter(of_cab=cab)
        try:
            curr_pass=passengers.get(user=request.user)
            if curr_pass.approval_status == APPROVED:
                permission=True
                button=False
            elif curr_pass.approval_status == REQUESTED:
                button=False
            else:
                button=True
        except:
            button=True


    except Cab.DoesNotExist:
        raise Http404
    return render(request, 'cab_detail.html', {'cab': cab,'button':button,
                                               'passengers':passengers,
                                               'user':request.user,
                                               'APPROVED':APPROVED,
                                               'REQUESTED':REQUESTED,
                                               'DECLINED':DECLINED,
                                               'permission':permission})

@login_required
def New_cab(request):

    user = request.user
    if request.method == 'POST':

        form=NewCabForm(request.POST)
        if form.is_valid():
            # dep_date=form.cleaned_data['dep_date']
            # allcabs=Cab.objects.filter(dep_date=dep_date)
            # if allcabs.count() > 0:
            #     messages.info(request, 'Cab with same date exists',extra_tags="col-lg-6 offset-lg-6")
            #     #form=NewCabForm()
            cab=form.save(commit=False)
            cab.seats_left=int(form.cleaned_data.get('size'))-1
            cab.cab_admin=user
            cab.save()

            passenger=Passenger.objects.create(is_admin=True,
                                               approval_status=APPROVED,
                                               user=user,
                                               of_cab=cab)
            return redirect('../cabs')
    else:
        form=NewCabForm()
    return render(request,'new_cab.html',{'form':form})
# Create your views here.
