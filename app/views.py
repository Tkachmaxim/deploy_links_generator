import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponseRedirect, Http404
from django.views import View
from django.contrib import messages
from app import short_code
from app.models import Urls


class Start(View):

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        url = request.POST.get('link')
        if url != '':
            link = short_code.get_short_code()
            link_for_display = request.build_absolute_uri()+link
            link = Urls(short_link=link, original_url=url)
            link.save()
            messages.success(request, link_for_display)
        return redirect(request.path)


class ReturnShortLink(View):

    def get(self, request, short_id):
        try:
            original_url = get_object_or_404(Urls, short_link=short_id)
        except MultipleObjectsReturned:
            original_url = Urls.objects.filter(short_link=short_id).order_by('-date')[0]

        checktime = datetime.datetime.now() - datetime.timedelta(minutes=60)
        if checktime < original_url.date:
            return HttpResponseRedirect(f'{original_url}')
        else:
            original_url.delete()
            raise Http404
