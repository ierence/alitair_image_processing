import click
from PIL import Image


@click.command()
@click.option('--i', required=True, type=str,
              help='Имя файла с базовым изображением, расположенного в папке /input')
@click.option('--o', required=True, type=str,
              help='Имя файла с плашкой, расположенного в папке /overlay')
@click.option('--r', required=True, type=str,
              help='Имя для нового файла с результатом, сохраняется в папке /result')
@click.option('--m', default="overlay", type=str,
              help='Решим работы сценария. При overlay плашка накладывается '
                   'на базовое изображение, что может перекрыть товар, при add - присоединяется сверху')
def overlay_images(i, o, r, m):
    # Open images
    base_image, overlay_image = load_images(i, o)
    # Resize the overlay to fit the base
    overlay_image = resize_billet(base_image, overlay_image)
    # Process images
    if m == 'overlay':
        result_image = overlay(base_image, overlay_image)
    else:
        result_image = add(base_image, overlay_image)
    # Save the result
    result_image.save(f"result/{r}")


def resize_billet(base_image, overlay_image):
    width = base_image.width

    overlay_size = overlay_image.size
    width_ratio = (width / float(overlay_size[0]))
    height = int((float(overlay_size[1])*float(width_ratio)))
    new_overlay = overlay_image.resize((width, height), resample=Image.Resampling.NEAREST)

    return new_overlay


def load_images(i, o):
    try:
        base_image = Image.open(f'input/{i}').convert('RGBA')
    except FileNotFoundError:
        raise click.BadParameter(message=f'Базовый файл с именем {i} в папке /input не найден.')

    try:
        overlay_image = Image.open(f'overlay/{o}').convert('RGBA')
    except FileNotFoundError:
        raise click.BadParameter(message=f'Файл с плашкой с именем {o} в папке /overlay не найден.')
    return base_image, overlay_image


def overlay(base_image, overlay_image):
    base_image.paste(overlay_image, (0, 0), overlay_image)
    return base_image


def add(base_image, overlay_image):
    result = Image.new(
        mode='RGBA',
        size=(
            base_image.width, base_image.height + overlay_image.height
        ))

    result.paste(overlay_image, (0, 0), overlay_image)
    result.paste(base_image, (0, overlay_image.height), base_image)

    return result


if __name__ == '__main__':
    overlay_images()
