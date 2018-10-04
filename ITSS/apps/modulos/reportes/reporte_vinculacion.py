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

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm, Inches, Pt
import jinja2
from jinja2.utils import Markup
from django.shortcuts import get_object_or_404

from ...vinculacion.models import Entidad, Informe_vinculacion

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
    c.drawImage(settings.STATIC_ROOT+'/images/vinculacion.png', (PAGE_WIDTH/2-240/2), 660, width=280, height=220, preserveAspectRatio=True)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(cm*2, 705, titulo.upper())
    c.drawRightString(PAGE_WIDTH-(cm*2), 705, '{}'.format(timezone.now().date()))
    c.setFont('Times-Roman', 11)
    c.drawRightString(PAGE_WIDTH-(cm*2), 0.75*(cm*2), 'Pagina {}'.format(1))
    c.restoreState()

def siguientePagina(c, doc):
    c.saveState()
    c.drawImage(settings.STATIC_ROOT+'/images/logo_vinculacion.png', PAGE_WIDTH-inch*1.2, PAGE_HEIGHT-inch*2.6, width=60, preserveAspectRatio=True)
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

    registros = []
    for evaluacion in estudiante.evaluaciones.all():
        registros.append(evaluacion.componente.proyecto_vinculacion)
    info = []
    for registro in set(registros):
        calificacion = 0
        horas = 0
        componentes = registro.componentes.filter(evaluacion__estudiante=estudiante)
        for componente in componentes:
            calificacion += componente.evaluacion.promedio
            horas += componente.evaluacion.total_horas
        calificacion /= componentes.count()
        fin = '-----'
        if registro.componentes.all().last().estado == 0:
            fin = registro.componentes.all().last().fin
        info.append(['{}'.format(registro.nombre), '{}'.format(registro.inicio), '{}'.format(fin), '{0:.1f}'.format(calificacion), '{}'.format(horas)])

    story.append(Spacer(1, 13))
    inf = {
        'data' :['PROYECTO', 'INICIO', u'CULMINACIÓN', u'CALIFICACIÓN', 'T. HORAS'],
        'info' :info,
        'dim'  :[190, 70, 80, 80, 60]
    }
    data = tabla(story, inf)

    doc.build(story, onFirstPage=partial(primeraPagina, titulo='Reporte general del estudiante'), onLaterPages=siguientePagina)
    response.write(buff.getvalue())
    buff.close()
    return response

def entidades(entidades):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte Entidades"
    response['Content-Disposition'] = 'attachment; filename={}'.format(pdf_name)
    buff = BytesIO()
    doc = SimpleDocTemplate(
        buff, 
        pagesize=A4,
        title='DR_Reports',
        author='dannyrs'
    ) # Crear un doc
    info = []
    for entidad in entidades:
        aux2 = ''
        for carrera in entidad.carreras.all():
            aux2 += u'-{}'.format(carrera.nombre)
        estado = ''
        if entidad.fin < timezone.now().date():
            estado = u'Caducado'
        elif entidad.fin < timezone.now().date()+timezone.timedelta(days=30):
            estado = u'Por vencer'
        elif entidad.fin > timezone.now().date():
            estado = u'Vigente'
        aux = [u'{}'.format(entidad.nombre), u'{}'.format(aux2), u'{}'.format(entidad.inicio), u'{}'.format(entidad.fin), u'{}'.format(estado)]
        info.append(aux)

    story = [Spacer(1,inch*1.3)]
    inf = {
        'data' :['ENTIDAD', 'CARRERA','INICIO', u'CULMINA', 'ESTADO'],
        'info' :info,
        'dim'  :[120, 170, 70, 70, 70]
    }
    data = tabla(story, inf)

    doc.build(story, onFirstPage=partial(primeraPagina, titulo='Reporte general de entidades'), onLaterPages=siguientePagina)
    response.write(buff.getvalue())
    buff.close()
    return response

#################

def convenio(slug):
    entidad = get_object_or_404(Entidad, slug=slug)
    if not Informe_vinculacion.objects.all().last():
        return False
    informe = Informe_vinculacion.objects.all().last().convenio
    tpl=DocxTemplate(informe)
    carreras = []
    for carrera in entidad.carreras.all():
        carreras.append({
            'nombre' : carrera.nombre
        })
    context = {
        'nombre' : entidad.nombre,
        'logo' : InlineImage(tpl, entidad.logo, height=Mm(10)),
        'telefono' : entidad.telefono,
        'fecha_inicio_convenio' : entidad.inicio,
        'fecha_fin_convenio' : entidad.fin,
        'correo' : entidad.correo,
        'direccion' : entidad.direccion,
        'estado' : entidad.estado,
        'enacargado' : entidad.encargado,
        'cargo' : entidad.cargo,
        'descripcion' : entidad.descripcion,
        'carreras' :  carreras,
        'responsable' : entidad.responsable.get_full_name(),
    }
    jinja_env = jinja2.Environment(autoescape=True)
    tpl.render(context, jinja_env)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=convenio {}.docx'.format(entidad.nombre)
    tpl.save(response)
    return response