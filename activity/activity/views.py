from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.template.loader import render_to_string
from django.http import JsonResponse


NEWS_COUNT_PER_PAGE = 3
@login_required
def home(request):
    page = int(request.GET.get('page', 1))
    # # print(page)
    # user = User.objects.get(username = request.user)
    # social = user.social_auth.get(provider="github")
    response = requests.get("https://api.github.com/users/saurav-bot/events")
    response = response.json()
    # print(len(response))
    ctx = {'data':response}
    message = []
    for mess in response:
        message.append(f"{mess['type']} {mess['repo']['name']} at {mess['created_at']}")
        
    # print(len(message))
    ctx = {"data": message[:3]}
    # # print(response[0]["type"], response[0]["repo"]["name"], response[0]["created_at"])
    # print(social.extra_data['access_token'])
    # # print(request.user.password)
    return render(request, 'home.html', ctx)

    # print(len(response))
    # p = paginator.Paginator(response,
    #                         NEWS_COUNT_PER_PAGE)
    # try:
    #     # post_page = p.page(page)
    #     post_page = p.get_page(page)
    # except paginator.EmptyPage:
    #     post_page = paginator.Page([], page, p)

    # if not request.is_ajax():
    #     context = {
    #         'posts': post_page,
    #     }
    #     return render(request,
    #                   'home.html',
    #                   context)
    # else:
    #     content = ''
    #     for post in post_page:
    #         content += render_to_string('item.html',
    #                                     {'post': post},
    #                                     request=request)
    #     return JsonResponse({
    #         "content": content,
    #         "end_pagination": True if page >= p.num_pages else False,
    #     })

    paginator = Paginator(response, 20)


    try:
        act = paginator.page(page)
    except PageNotAnInteger:
        act = paginator.page(1)
    except EmptyPage:
        act = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {"data":act})