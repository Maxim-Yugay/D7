from django import template


register = template.Library()

sens = [
        'article',
    ]

@register.filter()
def censor(text):
    t1 = text.split()
    for t in t1:
        if t == sens:
            return f'***'
        else:
            return text

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


# <form action="" method="get" >
#     {{ filterset.form.non_field_errors }}
#
#     {{ filterset.form.name__icontains.errors }}
#     <label for="{{ filterset.form.name__icontains.id_for_label }}">Search</label>
#     <input
#         id="{{ filterset.form.name__icontains.id }}"
#         name="{{ filterset.form.name__icontains.name }}"
#         value="{{ filterset.form.name__icontains.value }}"
#         class="form-control"
#     >
#     <input type="submit" class="mt-3 btn-primary" value="Найти" />
# </form>
#
