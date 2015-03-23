from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import signals
from models import Stream

def save_stream(instance, **kwargs):
  if not instance.id:
    user = instance.user
    raise Exception(user)

if settings.STREAMS_MODEL_COLLECTION:
  for model in settings.STREAMS_MODEL_COLLECTION:
    module_parts = model[0].split('.')
    module = module_parts.pop()
    module_path = '.'.join(module_parts)
    import_string = 'from ' + module_path + ' import ' + module
    exec import_string
    signals.post_save.connect(save_stream, sender=module)
