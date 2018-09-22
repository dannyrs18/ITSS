from django.core.exceptions import ValidationError
 
def valid_extension(value):
    if (not value.name.endswith('.odt') and
        not value.name.endswith('.ods') and 
        not value.name.endswith('.odp') and
        not value.name.endswith('.odg') and
        not value.name.endswith('.docx')):
 
        raise ValidationError("Archivos permitidos: .odt, .ods, .odp, .odg")