from django.core.exceptions import ValidationError
 
def valid_extension(value):
    if (not value.name.endswith('.jpeg') and
        not value.name.endswith('.png')):
 
        raise ValidationError("Archivos permitidos: .jpeg, .png")

def valid_extension_docx(value):
    if (not value.name.endswith('.docx')):
        raise ValidationError("Archivo permitido: .docx")