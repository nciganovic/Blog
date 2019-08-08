from django.utils.text import slugify

def unique_slug_generator(model_instance, headline, slug_field):
    '''Generating unique slugs for Blog model'''
    slug = slugify(headline)
    model_class = model_instance.__class__

    while model_class._default_manager.filter(blog_slug=slug).exists():
        object_pk = model_class._default_manager.latest('pk')
        object_pk = object_pk.pk + 1

        slug = f'{slug}-{object_pk}'
    return slug