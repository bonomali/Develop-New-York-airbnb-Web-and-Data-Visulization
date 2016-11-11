from django.shortcuts import render
from django_airbnb_web.models import ItemInfo
from django.core.paginator import Paginator

#============================================== <<<< DATA GENS >>>> ====================================================

# TOP X prices of different ways
def topx(cost,limit):

    pipeline = [

        {'$group':{'_id':'$Place','counts':{'$avg':"$"+str(cost)}}},
        {'$sort':{'counts':-1}},
        {'$limit':limit}

    ]

    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'],
            'data': [i['counts']],
            'type': 'column'
        }
        yield data

series_Total = [i for i in topx('Price',3)]
series_Per = [i for i in topx('Cost_per_guest',3)]
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Post quality of every area
def total_post():
    pipeline = [
        {'$group':{'_id':'$Place','counts':{'$sum':1}}},
    ]

    for i in ItemInfo._get_collection().aggregate(pipeline):

        data = {
            'name':i['_id'],
            'y':i['counts']
        }
        yield data

series_post = [i for i in total_post()]

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def pie_rate():
    pipeline = [
        {'$group':{'_id':'$Place','counts':{'$sum':1}}},
        {'$sort':{'counts':1}}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name':i['_id'],
            'y':i['counts']
        }
        yield data
pie_data = [i for i in pie_rate()]

#============================================== <<<< PAGE VIEWS >>>> ===================================================

def index(request):
    limit = 15
    arti_info = ItemInfo.objects
    paginatior = Paginator(arti_info,limit)
    page = request.GET.get('page',1)
    print(request)
    print(request.GET)
    loaded = paginatior.page(page)

    context = {
        'ItemInfo':loaded,
        'counts':arti_info.count(),
        'count_areas':len(set([i['Place'] for i in arti_info]))

    }
    return render(request,'index_data.html',context)

def chart(request):
    context = {
        'chart_Total':series_Total,
        'chart_Per':series_Per,
        'series_post':series_post,
        'pie_data':pie_data,
    }
    return render(request,'chart2.html',context)

