# coding: utf-8
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm, Inches, Pt
import jinja2
from jinja2.utils import Markup
from django.shortcuts import get_object_or_404

from ...practicas.models import Empresa, Informe_practicas


PAGE_HEIGHT=A4[1]; PAGE_WIDTH=A4[0]
styles = getSampleStyleSheet()

##### Datos De prueba
numero_etapa = 3
nombre_vinculacion = "Identificacion y seleccion de la plataforma MOOCS a implementar"
fecha = '23/09/2018'
#####

_s = ParagraphStyle(
        'identificacion',
        fontName='Helvetica-Bold',
        fontSize=10
    )
_s1 = ParagraphStyle(
        'identificacion',
        fontName='Helvetica',
        fontSize=10
    )

#### Inicio

# Imgagenes = static/plugins/Date_Picker/js/jquery.datepicker.min.js
def primeraPagina(c, doc):
    c.saveState()
    c.setFont('Helvetica-Bold', 14)
    c.drawImage(settings.STATIC_ROOT+'/images/institucion.jpg', (PAGE_WIDTH/2-270/2), 655, width=300, height=240, preserveAspectRatio=True)
    c.drawRightString(PAGE_WIDTH-inch, 0.75*inch, 'Pagina {}'.format(1))
    c.restoreState()

def siguientePagina(c, doc):
    c.saveState()
    c.setFont('Times-Roman', 11)
    image_width, image_height = 75*8, 70*8
    #c.drawImage('logo_vinculacion.png', PAGE_WIDTH/2-image_width/2, PAGE_HEIGHT/2-image_height/2, width=image_width, height=image_height, mask=[-3,-3,-3,-3,-3,-3])
    c.drawRightString(PAGE_WIDTH-inch, 0.75*inch, 'Pagina {}'.format(doc.page))
    c.restoreState()

def encabezado():
    data = [
        [Paragraph('ETAPA DEL INFORME:', _s), Paragraph('{}° Componente: {}'.format(numero_etapa, nombre_vinculacion), _s1)],
        [Paragraph('FECHA:', _s), Paragraph('{}'.format(fecha), _s1)]
    ]
    return data

def lienzo():

    response = HttpResponse(content_type='application/pdf')
    pdf_name = "reporte Vinculacion"
    pdf_author = "dannyrs"
    response['Content-Disposition'] = 'attachment; filename={}'.format(pdf_name)
    buff = BytesIO()
    doc = SimpleDocTemplate(
        buff, 
        pagesize=A4,
        title='DR_Reports',
        author='dannyrs'
    ) # Crear un doc
    story = [Spacer(1,inch*1.3)]
    data = encabezado()
    t = Table(data, colWidths=[125, 325])
    t.setStyle(TableStyle([
       ('VALIGN', (0,0), (-1, -1), 'TOP'),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))
    doc.build(story, onFirstPage=primeraPagina, onLaterPages=siguientePagina)

    response.write(buff.getvalue())
    buff.close()
    return response

#############################

def convenio(slug):
    empresa = get_object_or_404(Empresa, slug=slug)
    if Informe_practicas.objects.filter(pk=1).exists():
        informe = Informe_practicas.objects.get(pk=1).convenio
    else:
        informe = settings.STATIC_ROOT+'/base/Convenio.docx'
    buffer = BytesIO()
    tpl=DocxTemplate(informe)
    carreras = []
    for carrera in empresa.carreras.all():
        carreras.append({
            'nombre' : carrera.nombre
        })
    context = {
        'nombre' : empresa.nombre,
        'logo' : InlineImage(tpl, empresa.logo, height=Mm(10)),
        'telefono' : empresa.telefono,
        'fecha_inicio_convenio' : empresa.inicio,
        'fecha_fin_convenio' : empresa.fin,
        'correo' : empresa.correo,
        'direccion' : empresa.direccion,
        'estado' : empresa.estado,
        'gerente' : empresa.gerente,
        'descripcion' : empresa.descripcion,
        'carreras' :  carreras,
        'responsable' : empresa.responsable.get_full_name(),
    }
    jinja_env = jinja2.Environment(autoescape=True)
    tpl.render(context, jinja_env)
    tpl.save(buffer)
    length = buffer.tell()
    buffer.seek(0)
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=convenio {}.docx'.format(empresa.nombre)
    response['Content-Length'] = length
    return response