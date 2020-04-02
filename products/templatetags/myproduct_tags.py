from django import template

register = template.Library()


@register.filter(name='star_generator')
def star_generator(individual_rating, star_rating=5):
    """Generates rating stars when rating is passed through"""
    output_html = ''
    star = 1

    # html output strings
    checked_star = '<i class="fas fa-star checked" aria-hidden="true"></i>'
    unchecked_star = '<i class="fas fa-star unchecked" aria-hidden="true"></i>'

    # loop until break is called
    while True:
        # make sure that a value exists
        if individual_rating:
            if star <= int(individual_rating):
                output_html += checked_star
            else:
                output_html += unchecked_star
        else:
            # if no value exists, return unchecked
            output_html += unchecked_star

        star += 1

        if star > int(star_rating):
            break

    return output_html
