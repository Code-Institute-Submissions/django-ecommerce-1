from django import template

register = template.Library()


@register.filter(name='rating')
def rating(individual_rating, star_rating=5):
    """Generates rating stars when rating is passed through"""
    output_html = ''
    star = 1
    while True:
        if star <= individual_rating:
            output_html += '<i class="fas fa-star checked" aria-hidden="true">'
            '</i>'
        else:
            output_html += '<i class="fas fa-star" aria-hidden="true"></i>'

        star += 1

        if star > star_rating:
            break

    return output_html
