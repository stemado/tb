
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render

from tb.medications.models import Medication
from tb.feeds.models import Feed
import string
from django.http import HttpResponse
import json
from django.http import JsonResponse
from tb.decorators import ajax_required

@login_required
def GetMedicationSearch(request):
    if request.is_ajax():
        q = request.GET.get('term').strip()
        drugs = Medication.objects.filter(medicationName__icontains=q)
        print(drugs)
        results=[]
        for d in drugs:
            drug = {}
            drug['id'] = d.id
            drug['label'] = d.medicationName
            drug['value'] = d.medicationName
            results.append(drug)
        data = json.dumps(results)
    else:
        data = 'fail'
        mimetype = 'application/json'
        return JsonResponse(data, mimetype)

@login_required
def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        print(querystring)
        if len(querystring) == 0:
            return redirect('/search/')

        try:
            search_type = request.GET.get('type')
            if search_type not in ['feed', 'articles', 'questions', 'users', 'residents']:
                search_type = 'feed'

        except Exception:
            search_type = 'feed'

        count = {}
        results = {}
        results['feed'] = Feed.objects.filter(post__icontains=querystring,
                                              parent=None)
        results['users'] = User.objects.filter(
            Q(username__icontains=querystring) | Q(
                first_name__icontains=querystring) | Q(
                    last_name__icontains=querystring))
        count['feed'] = results['feed'].count()
        count['users'] = results['users'].count()

        return render(request, 'search/results.html', {
            'hide_search': True,
            'querystring': querystring,
            'active': search_type,
            'count': count,
            'results': results[search_type],
        })
    else:
        return render(request, 'search/search.html', {'hide_search': True})

@login_required
def autocomplete(request):
    return render(request, 'search/autocomplete_search.html')

@login_required
def marSearch(request, med_id):
    if 'to' and 'from' in request.GET:
        stringTo = request.GET.get('to').strip()
        stringFrom = request.GET.get('from').strip()
        querystringTo = str.replace(stringTo, '/', ',')
        querystringFrom = str.replace(stringFrom, '/', ',')
        print(quertystringTo)
        print(querystringFrom)
        if len(querystringTo) == 0 and len(querystringFrom) == 0:
            return redirect('/search/')

        try:
            search_type = request.GET.get('type')
            if search_type not in ['users', 'medications']:
                search_type = 'feed'

        except Exception:
            search_type = 'feed'

        count = {}
        results = {}
        medications['medication'] = Medication.objects.select_related().filter(id=med_id, post__icontains=querystring,
                                              parent=None)
        count['users'] = results['users'].count()

        return render(request, 'search/results.html', {
            'hide_search': True,
            'querystring': querystringTo + '|' + querystringFrom,
            'active': search_type,
            'count': count,
            'results': results[search_type],
        })
    else:
        return render(request, 'search/search.html', {'hide_search': True})


    # medication = Medication.objects.filter(medicationUser_id=mar_id).order_by("medicationName", "id")
    # resident = Resident.objects.filter(id=mar_id)[0]
    # paginator = Paginator(medication, 5)
    # page = request.GET.get('page')
    # try:
    #     meds = paginator.page(page)
    # except PageNotAnInteger:
    #     meds = paginator.page(1)
    # except EmptyPage:
    #     meds = paginator.page(paginator.num_pages)


    # return render(request, 'medications/mar.html', {'medication': medication, 'resident': resident, 'meds': meds})