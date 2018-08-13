from django.utils.http import is_safe_url
from django.urls import reverse

class RequestformattachMixin(object):
    def get_form_kwargs(self):    # we have write this funtion to pass the request to the form to be able to read the users inputs
        kwargs=super().get_form_kwargs()
        # kwargs={
        #     'request':self.request
        # }

        kwargs['request']=self.request
        print(kwargs)
        return kwargs

class NextUrlMixin(object):
    def get_next_url(self):
        next_ = self.request.GET.get("next")
        next_post = self.request.POST.get("next")
        redirected_path = next_ or next_post or None
        if is_safe_url(redirected_path,self.request.get_host()):      # self.request.get_host_url() = hosts
            return redirected_path     # we changed the return to be the path only
        return reverse('home')


