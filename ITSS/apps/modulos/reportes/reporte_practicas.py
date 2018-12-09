# coding: utf-8
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from django.utils import timezone
from functools import partial

# URL: https://docxtpl.readthedocs.io/en/latest/
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm, Inches, Pt
import jinja2
from jinja2.utils import Markup
from django.shortcuts import get_object_or_404
# URL: https://docxtpl.readthedocs.io/en/latest/

from ...practicas.models import Empresa, Informe_practicas

PAGE_HEIGHT=A4[1]; PAGE_WIDTH=A4[0]
styles = getSampleStyleSheet()

def _hb(size):
    return ParagraphStyle(
        'identificacion',
        fontName='Helvetica-Bold',
        fontSize=size
    )
def _h(size):
    return ParagraphStyle(
            'identificacion',
            fontName='Helvetica',
            fontSize=size
        )

def primeraPagina(c, doc, titulo):
    c.saveState()
    c.drawImage(settings.STATIC_ROOT+'/images/institucion.jpg', (PAGE_WIDTH/2-270/2), 660, width=280, height=220, preserveAspectRatio=True)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(cm*2, 705, titulo.upper())
    c.drawRightString(PAGE_WIDTH-(cm*2), 705, '{}'.format(timezone.now().date()))
    c.setFont('Times-Roman', 11)
    c.drawRightString(PAGE_WIDTH-(cm*2), 0.75*(cm*2), 'Pagina {}'.format(1))
    c.restoreState()

def siguientePagina(c, doc):
    c.saveState()
    c.drawImage(settings.STATIC_ROOT+'/images/logo_practicas.jpg', PAGE_WIDTH-inch*1.5, PAGE_HEIGHT-inch*1.5, width=80, preserveAspectRatio=True)
    c.setFont('Times-Roman', 11)
    c.drawRightString(PAGE_WIDTH-(cm*2), 0.75*(cm*2), 'Pagina {}'.format(doc.page))
    c.restoreState()

def encabezado(story, inf):
    data = []
    for i in range(len(inf['data'])):
        data.append([Paragraph(u'{}:'.format(inf['data'][i]), _hb(12)), Paragraph(u'{}'.format(inf['info'][i]), _h(10))])
    t = Table(data, colWidths=inf['dim'])
    t.setStyle(TableStyle([
       ('VALIGN', (0,0), (-1, -1), 'CENTER'),
       ('ALIGN', (0,0), (-1, -1), 'CENTER'),
    ]))
    story.append(t)

def tabla(story, inf):
    aux, data = [], []
    for i in range(len(inf['data'])):
        aux.append(Paragraph(u'{}'.format(inf['data'][i]), _hb(9)))
    data.append(aux)
    for i in range(len(inf['info'])):
        aux = []
        for x in range(len(inf['info'][i])):
            aux.append(Paragraph(u'{}'.format(inf['info'][i][x]), _h(10)))
        data.append(aux)
    t = Table(data, colWidths=inf['dim'])
    t.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('VALIGN',(0,0),(-1,-1),'CENTER'), # eje x
        ('ALIGN',(0,0),(-1,-1),'CENTER'), # eje y
    ]))
    story.append(t)

def estudiantes(estudiante):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte Estudiantes"
    response['Content-Disposition'] = 'attachment; filename={}'.format(pdf_name)
    buff = BytesIO()
    doc = SimpleDocTemplate(
        buff, 
        pagesize=A4,
        title='DR_Reports',
        author='dannyrs'
    ) # Crear un doc

    story = [Spacer(1,inch)]
    inf = {
        'data' :['Nombre','Apellidos','Cedula', 'Carrera'],
        'info' :[
            estudiante.nombres, 
            estudiante.apellidos, 
            estudiante.cedula,
            estudiante.carrera.nombre    
        ],
        'dim'  :[100, 390]
    }
    encabezado(story, inf)

    story.append(Spacer(1, 13))
    inf = {
        'data' :['EMPRESA', 'INICIO', u'CULMINACIÓN', u'CALIFICACIÓN', 'T. HORAS'],
        'info' :[[u'{}'.format(registro.empresa.nombre), u'{}'.format(registro.presentacion), u'{}'.format(registro.fin or '------'), u'{0:.1f}'.format(registro.calificacion), u'{}'.format(registro.horas)] for registro in estudiante.registros_practicas.all() ],
        'dim'  :[160, 80, 80, 80, 80]
    }
    tabla(story, inf)

    doc.build(story, onFirstPage=partial(primeraPagina, titulo='Reporte general del estudiante'), onLaterPages=siguientePagina)
    response.write(buff.getvalue())
    buff.close()
    return response

def empresas(empresas):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte Empresas"
    response['Content-Disposition'] = 'attachment; filename={}'.format(pdf_name)
    buff = BytesIO()
    doc = SimpleDocTemplate(
        buff, 
        pagesize=A4,
        title='DR_Reports',
        author='dannyrs'
    ) # Crear un doc
    info = []
    for empresa in empresas:
        aux2 = ''
        for carrera in empresa.carreras.all():
            aux2 += u'-{}'.format(carrera.nombre)
        estado = ''
        if empresa.fin < timezone.now().date():
            estado = u'Caducado'
        elif empresa.fin < timezone.now().date()+timezone.timedelta(days=30):
            estado = u'Por vencer'
        elif empresa.fin > timezone.now().date():
            estado = u'Vigente'
        aux = [u'{}'.format(empresa.nombre), u'{}'.format(aux2), u'{}'.format(empresa.inicio), u'{}'.format(empresa.fin), u'{}'.format(estado)]
        info.append(aux)

    story = [Spacer(1,inch*1.3)]
    inf = {
        'data' :['EMPRESA', 'CARRERA','INICIO', u'CULMINA', 'ESTADO'],
        'info' :info,
        'dim'  :[120, 170, 70, 70, 70]
    }
    tabla(story, inf)

    doc.build(story, onFirstPage=partial(primeraPagina, titulo='Reporte general de empresas'), onLaterPages=siguientePagina)
    response.write(buff.getvalue())
    buff.close()
    return response

def periodo(registros, fecha):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte Periodo de Practicas"
    response['Content-Disposition'] = 'attachment; filename={}'.format(pdf_name)
    buff = BytesIO()
    doc = SimpleDocTemplate(
        buff, 
        pagesize=A4,
        title='DR_Reports',
        author='dannyrs'
    ) # Crear un doc

    story = [Spacer(1,inch)]
    inf = {
        'data' :['Periodo'],
        'info' :[
            u'{} - {}'.format(fecha.get('inicio'), fecha.get('fin'))
        ],
        'dim'  :[100, 390]
    }
    encabezado(story, inf)

    inf = {
        'data' :['ESTUDIANTE', u'CÉDULA', 'EMPRESA', u'CALIFICACIÓN', 'HORAS'],
        'info' :[[u'{}'.format(registro.estudiante.get_full_name()), u'{}'.format(registro.estudiante.cedula), u'{}'.format(registro.empresa.nombre), u'{}'.format(registro.calificacion), u'{}'.format(registro.horas)] for registro in registros],
        'dim'  :[190, 70, 115, 80, 45]
    }
    tabla(story, inf)

    doc.build(story, onFirstPage=partial(primeraPagina, titulo='Reporte general de practicas'), onLaterPages=siguientePagina)
    response.write(buff.getvalue())
    buff.close()
    return response

#############################

def convenio(slug):
    empresa = get_object_or_404(Empresa, slug=slug)
    if not Informe_practicas.objects.all().last():
        return False
    informe = Informe_practicas.objects.all().last().convenio
    tpl=DocxTemplate(informe)
    carreras = []
    for carrera in empresa.carreras.all():
        carreras.append({
            'nombre' : carrera.nombre
        })
    logo = ''
    if empresa.logo:
        logo = InlineImage(tpl, empresa.logo, height=Mm(18))
    context = {
        'nombre' : empresa.nombre,
        'logo' : logo,
        'telefono' : empresa.telefono,
        'fecha_inicio_convenio' : empresa.inicio,
        'fecha_fin_convenio' : empresa.fin,
        'correo' : empresa.correo,
        'direccion' : empresa.direccion,
        'gerente' : empresa.gerente,
        'descripcion' : empresa.descripcion,
        'carreras' :  carreras,
        'responsable' : empresa.responsable.get_full_name(),
    }
    jinja_env = jinja2.Environment(autoescape=True)
    tpl.render(context, jinja_env)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=convenio {}.docx'.format(empresa.nombre)
    tpl.save(response)
    return response