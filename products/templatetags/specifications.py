from django import template
from django.utils.safestring import mark_safe


register = template.Library()


TABLE_HEAD = '''
                <table class="table table-hover">
                    <thead>
                        <tr>
                        <th scope="col">Specifications</th>
                        <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody>
            '''


TABLE_TAIL = '''
                    </tbody>
                </table>
            '''


TABLE_CONTENT = '''
                    <tr>
                        <td>{name}</td>
                        <td>{value}</td>
                    </tr>
                '''


PRODUCT_SPECIFICATIONS = {
    'ant': {
        'Size': 'size',
        'Coloration': 'coloration',
        'Occurrence': 'occurrence',
        'Nesting': 'nesting'
    },
    'formicary': {
        'Size': 'size',
        'Dimensions': 'dimensions',
        'Material': 'formicary_material',
        'Additional info': 'additional_info'
    }
}


def get_product_specification(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPECIFICATIONS[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_specification(product):
    model_name = product.__class__._meta.model_name
    return mark_safe(TABLE_HEAD + get_product_specification(product, model_name) + TABLE_TAIL)
