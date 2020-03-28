from docxtpl import DocxTemplate
from typing import Union

import settings as settings


def generate_certificate(volunteer_name: str,
                         hours: Union[int, str],
                         template_file: str):

    doc = DocxTemplate(f"{settings.CERTIFICATE_DIR}/{template_file}.docx")
    context = {'recipient': volunteer_name, 'hours': hours}
    doc.render(context)

    doc.save(f"{settings.CERTIFICATE_DIR}/volunteers/{volunteer_name}.docx")
