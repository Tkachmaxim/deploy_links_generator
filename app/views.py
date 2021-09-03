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
        # clean all expired links
        checktime = datetime.datetime.now() - datetime.timedelta(minutes=60)
        expired_links=Urls.objects.filter(date__lt=checktime)
        expired_links.delete()
        return render(request, 'index.html')

    def post(self, request):
        url = request.POST.get('link')
        if url != '':
            # generate link using hashfunction
            link = hashlib.md5(url.encode()).hexdigest()[:6]
            # checking whether this hashlink with same url in database is the or no
            if len(Urls.objects.filter(short_link=link, original_url=url))>=1:
                # if no - generate link using standart hash function and show for user
                link_for_display = request.build_absolute_uri() + link
                messages.success(request, link_for_display)
                return redirect(request.path)

            # next check object with same hash
            elif len(Urls.objects.filter(short_link=link))>=1:
                flag_created = True
                # if yes - generate new hash for url using add salt. Doing it while not look for free hash
                while flag_created:
                    salt1 = os.urandom(hashlib.blake2b.SALT_SIZE)

                    link = hashlib.blake2b(salt=salt1)
                    link.update(url.encode())
                    cut_link=link.hexdigest()[:6]
                    # check is there in database object with new generated link. If there is - create example
                    if len(Urls.objects.filter(short_link=cut_link)) == 0:
                        flag_created=False
                        link_for_data = Urls(short_link=cut_link, original_url=url)
                        link_for_data.save()
                        link_for_display = request.build_absolute_uri() + cut_link
                        messages.success(request, link_for_display)
                    # if now - generate new salt
                return redirect(request.path)
            # if we have not any thing generate new object
            else:
                # if we have not any collisions and we have not same link in database
                # - will generate new shortlink and create objecr in daabase
                link_for_data = Urls(short_link=link, original_url=url)
                link_for_data.save()
                link_for_display = request.build_absolute_uri() + link[:6]
                messages.success(request, link_for_display)
                return redirect(request.path)
        return redirect(request.path)


class ReturnShortLink(View):

    def get(self, request, short_id):
        original_url = get_object_or_404(Urls, short_link=short_id)
        checktime = datetime.datetime.now() - datetime.timedelta(minutes=60)
        if checktime < original_url.date:
            return HttpResponseRedirect(f'{original_url}')
        else:
            original_url.delete()
            raise Http404
