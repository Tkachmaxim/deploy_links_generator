import datetime
import os
import hashlib
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.views import View
from django.contrib import messages
from app.models import Urls


class Start(View):

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        url = request.POST.get('link')
        if url != '':
            link = hashlib.md5(url.encode()).hexdigest()
            # checking whether this hashlink with same url in database is the or no
            if len(Urls.objects.filter(short_link=link, original_url=url))>=1:
                link_for_display = request.build_absolute_uri() + link[:7]
                messages.success(request, link_for_display)
                return redirect(request.path)

            # next check object with same hash adn if yes - generate new hash for url
            elif len(Urls.objects.filter(short_link=link))>=1:
                print('next')
                salt1 = os.urandom(hashlib.blake2b.SALT_SIZE)
                link = hashlib.blake2b(salt=salt1)
                link.update(url.encode())
                link_for_data = Urls(short_link=link.hexdigest(), original_url=url)
                link_for_data.save()
                link_for_display = request.build_absolute_uri() + link.hexdigest()[:7]
                messages.success(request, link_for_display)
                return redirect(request.path)
            # if we have not any thing generate new object
            else:
                link_for_data = Urls(short_link=link, original_url=url)
                link_for_data.save()
                link_for_display = request.build_absolute_uri() + link[:7]
                messages.success(request, link_for_display)
                return redirect(request.path)
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
