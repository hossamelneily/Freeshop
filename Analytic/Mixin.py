from .signals import object_viewed_signal

class ObjectMixinView(object):

    def get_context_data(self,*args,**kwargs):
        context=super(ObjectMixinView,self).get_context_data(*args,**kwargs)
        instance=context.get('object')
        request=self.request

        if instance:
            object_viewed_signal.send(instance.__class__,instance=instance,request=request)

        return context


    # we could use also get_object() to get the object but it will be redunt to repeat it here as we called it in the views.py

