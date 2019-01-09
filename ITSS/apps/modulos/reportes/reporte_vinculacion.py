# coding: utf-8
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from reportlab.platypus.flowables import Flowable
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from django.utils import timezone
from functools import partial

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm, Inches, Pt
import jinja2
from jinja2.utils import Markup
from django.shortcuts import get_object_or_404

from ...vinculacion.models import Entidad, Informe_vinculacion

import StringIO
import zipfile

PAGE_HEIGHT=A4[1]; PAGE_WIDTH=A4[0]
styles = getSampleStyleSheet()

def _hb(size, position=TA_LEFT):
    return ParagraphStyle(
        'identificacion',
        fontName='Helvetica-Bold',
        fontSize=size,
        alignment = position,
    )
def _h(size, position=TA_LEFT):
    return ParagraphStyle(
            'identificacion',
            fontName='Helvetica',
            fontSize=size,
            alignment = position,
        )

def primeraPagina(c, doc, titulo):
    c.saveState()
    c.drawImage(settings.STATIC_ROOT+'/images/vinculacion.png', (PAGE_WIDTH/2-240/2), 660, width=280, height=220, preserveAspectRatio=True)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(cm*2, 705, titulo.upper())
    c.drawRightString(PAGE_WIDTH-(cm*2), 705, '{}'.format(timezone.now().date().strftime('%d-%m-%Y')))
    c.setFont('Times-Roman', 11)
    c.drawRightString(PAGE_WIDTH-(cm*2), 0.75*(cm*2), 'Pagina {}'.format(1))
    c.restoreState()

def siguientePagina(c, doc):
    c.saveState()
    c.drawImage(settings.STATIC_ROOT+'/images/logo_vinculacion.png', PAGE_WIDTH-inch*1.2, PAGE_HEIGHT-inch*2.6, width=60, preserveAspectRatio=True)
    c.setFont('Times-Roman', 11)
    c.drawRightString(PAGE_WIDTH-(cm*2), 0.75*(cm*2), 'Pagina {}'.format(doc.page))
    c.restoreState()

def cab_table(story, enc, align=TA_LEFT, size=450):
    data = [
        [Paragraph(enc, _hb(10, align))],
    ]
    t = Table(data, colWidths=size)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.lavender),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    story.append(t)

def encabezado(story, inf, hb=12, h=10):
    data = []
    for i in range(len(inf['data'])):
        try:
            data.append([Paragraph(u'{}:'.format(inf['data'][i]), _hb(hb)), Paragraph(u'{}'.format(inf['info'][i]), _h(h))])
        except :
            data.append([Paragraph(u'{}:'.format(inf['data'][i]), _hb(hb)), Paragraph(u'{}'.format('------------'), _h(h))])
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
            try:
                aux.append(Paragraph(u'{}'.format(inf['info'][i][x]), _h(10)))
            except:
                aux.append(Paragraph(u'{}'.format('----------'), _h(10)))
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
    response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(pdf_name)
    buff = BytesIO()
    doc = SimpleDocTemplate(
        buff, 
        pagesize=A4,
        title='Devops',
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

    from django.db.models import Sum, Avg

    registros = []
    for evaluacion in estudiante.evaluaciones.all():
        if evaluacion.componente:
            registros.append(evaluacion.componente.proyecto_vinculacion)

    info = []
    for registro in set(registros):
        horas = 0
        promedio = 0
        contador = 0
        for componente in registro.componentes.filter(estado=0):
            evaluacion = componente.evaluaciones.filter(estudiante=estudiante)
            if evaluacion:
                aux_horas = evaluacion.aggregate(Sum('total_horas'))
                aux_promedio = evaluacion.aggregate(Avg('promedio'))
                horas += aux_horas['total_horas__sum']
                promedio += aux_promedio['promedio__avg']
                contador += 1
        fin = '-----'
        if registro.componentes.all().last().estado == 0:
            fin = registro.componentes.all().last().fin
        info.append([u'{}'.format(registro.nombre), u'{}'.format(registro.inicio), u'{}'.format(fin), u'{0:.1f}'.format(promedio/contador), u'{}'.format(horas)])

    story.append(Spacer(1, 10))
    cab_table(story, 'PROYECTOS', TA_CENTER, 480)
    story.append(Spacer(1, 5))
    inf = {
        'data' :['PROYECTO', 'INICIO', u'CULMINA', u'CALIFICACIÓN', 'T. HORAS'],
        'info' :info,
        'dim'  :[200, 70, 70, 80, 60]
    }
    tabla(story, inf)

    story.append(Spacer(1, 20))
    cab_table(story, 'ACTIVIDADES', TA_CENTER, 480)

    info=[]
    for evaluacion in estudiante.evaluaciones.all():
        if evaluacion.actividad:
            info.append([u'{}'.format(evaluacion.actividad.nombre), u'{}'.format(evaluacion.fecha_inicio.strftime('%d-%m-%Y')), u'{}'.format(evaluacion.fecha_fin.strftime('%d-%m-%Y')), u'{}'.format(evaluacion.promedio), u'{}'.format(evaluacion.total_horas)])

    story.append(Spacer(1, 5))
    inf = {
        'data' :['ACTIVIDAD', 'INICIO', u'CULMINA', u'CALIFICACIÓN', 'T. HORAS'],
        'info' :info,
        'dim'  :[200, 70, 70, 80, 60]
    }
    tabla(story, inf)

    doc.build(story, onFirstPage=partial(primeraPagina, titulo='Reporte general del estudiante'), onLaterPages=siguientePagina)
    response.write(buff.getvalue())
    buff.close()
    return response

def entidades(entidades):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte Entidades"
    response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(pdf_name)
    buff = BytesIO()
    doc = SimpleDocTemplate(
        buff, 
        pagesize=A4,
        title='Devops',
        author='dannyrs'
    ) # Crear un doc
    info = []
    for entidad in entidades:
        aux2 = ''
        for carrera in entidad.carreras.all():
            aux2 += u'-{}'.format(carrera.nombre)
        estado = ''
        if entidad.fin == None or entidad.fin < timezone.now().date():
            estado = u'Caducado'
        elif entidad.fin < timezone.now().date()+timezone.timedelta(days=30):
            estado = u'Por vencer'
        elif entidad.fin > timezone.now().date():
            estado = u'Vigente'
        aux = [u'{}'.format(entidad.nombre), u'{}'.format(aux2), u'{}'.format(entidad.inicio), u'{}'.format(entidad.fin), u'{}'.format(estado)]
        info.append(aux)

    story = [Spacer(1,inch*1.1)]
    inf = {
        'data' :['ENTIDAD', 'CARRERA','INICIO', u'CULMINA', 'ESTADO'],
        'info' :info,
        'dim'  :[120, 170, 70, 70, 70]
    }
    tabla(story, inf)

    doc.build(story, onFirstPage=partial(primeraPagina, titulo='Reporte general de entidades'), onLaterPages=siguientePagina)
    response.write(buff.getvalue())
    buff.close()
    return response

def periodo(registros, actividades):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte Periodo de Practicas"
    response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(pdf_name)
    buff = BytesIO()
    doc = SimpleDocTemplate(
        buff, 
        pagesize=A4,
        title='Devops',
        author='dannyrs'
    ) # Crear un doc

    info = []
    for registro in registros:
        fin = '-----'
        if registro.componentes.all().last().estado == 0:
            fin = registro.componentes.all().last().fin.strftime('%d-%m-%Y')
        info.append([u'{}'.format(registro.nombre), u'{}'.format(registro.entidad.nombre), u'{}'.format(registro.componentes.count()), u'{}'.format(registro.inicio.strftime('%d-%m-%Y')), u'{}'.format(fin), u'{}'.format(registro.carrera.nombre)])

    story = [Spacer(1,inch*1.1)]

    cab_table(story, 'PROYECTOS', TA_CENTER, 505)
    story.append(Spacer(1, 5))

    inf = {
        'data' :['PROYECTO', 'ENTIDAD', 'COMP.', 'INICIO', 'CULMINA', 'CARRERA'],
        'info' :info,
        'dim'  :[140, 100, 45, 65, 65, 90] #400
    }
    tabla(story, inf)
    story.append(Spacer(1, 20))
    cab_table(story, 'ACTIVIDADES', TA_CENTER, 505)
    story.append(Spacer(1, 5))
    info = []
    for actividad in actividades:
        info.append([u'{}'.format(actividad.nombre), u'{}'.format(actividad.entidad.nombre), u'{}'.format(actividad.inicio.strftime('%d-%m-%Y')), u'{}'.format(actividad.fin.strftime('%d-%m-%Y')), u'{}'.format(actividad.carrera.nombre)],)
    inf = {
        'data' :['ACTIVIDAD', 'ENTIDAD', 'INICIO', 'CULMINA', 'CARRERA'],
        'info' :info,
        'dim'  :[160, 125, 65, 65, 90] #400
    }
    tabla(story, inf)

    doc.build(story, onFirstPage=partial(primeraPagina, titulo='Reporte general por periodo'), onLaterPages=siguientePagina)
    response.write(buff.getvalue())
    buff.close()
    return response

#################

def primeraPagina2(c, doc, titulo, fondo=True):
    c.saveState()
    c.setFont('Helvetica-Bold', 12)
    c.drawImage(settings.STATIC_ROOT+'/images/logo_vinculacion.png', inch-10, PAGE_HEIGHT-inch*1.6, width=75, height=70)
    c.drawImage(settings.STATIC_ROOT+'/images/institucion2.png', PAGE_WIDTH-inch*3, PAGE_HEIGHT-inch*1.5, width=150, height=50)
    image_width, image_height = 75*8, 70*8
    if fondo:
        c.drawImage(settings.STATIC_ROOT+'/images/logo_vinculacion.png', PAGE_WIDTH/2-image_width/2, PAGE_HEIGHT/2-image_height/2, width=image_width, height=image_height, mask=[-3,-3,-3,-3,-3,-3])
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT-150, titulo)
    c.setFont('Times-Roman', 11)
    c.drawRightString(PAGE_WIDTH-inch, 0.75*inch, 'Pagina {}'.format(1))
    c.restoreState()

def siguientePagina2(c, doc, fondo=True):
    c.saveState()
    c.setFont('Times-Roman', 11)
    image_width, image_height = 75*8, 70*8
    if fondo:
        c.drawImage(settings.STATIC_ROOT+'/images/logo_vinculacion.png', PAGE_WIDTH/2-image_width/2, PAGE_HEIGHT/2-image_height/2, width=image_width, height=image_height, mask=[-3,-3,-3,-3,-3,-3])
    c.drawRightString(PAGE_WIDTH-inch, 0.75*inch, 'Pagina {}'.format(doc.page))
    c.restoreState()

def informacionX(story, inf):
    cab_table(story, inf['enc'])
    data = []
    for i in range(len(inf['data'])):
        try:
            data.append([Paragraph(u'{}:'.format(inf['data'][i]), _hb(10)), Paragraph(u'{}'.format(inf['info'][i]), _h(10))])
        except :
            data.append([Paragraph(u'{}:'.format(inf['data'][i]), _hb(10)), Paragraph(u'{}'.format('---------------'), _h(10))])
    t = Table(data, colWidths=inf['dim'])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('VALIGN',(0,0),(-1,-1),'CENTER'), # eje x
        ('ALIGN',(0,0),(-1,-1),'CENTER'), # eje y
    ]))
    story.append(t)

def informacion1(story, inf):
    cab_table(story, inf['enc'])
    try:
        data = [
            [''],
            ['',Paragraph(u'{}'.format(inf['data']), _h(10)), ''],
            ['']
        ]
    except :
        data = [
            [''],
            ['',Paragraph(u'{}'.format('----------'), _h(10)), ''],
            ['']
        ]
    t = Table(data, colWidths=inf['dim'])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    story.append(t)

def informacion2(story, inf):
    cab_table(story, inf['enc'])
    data = [
        ['', Paragraph('4.1 Objetivos a alcanzar en el periodo', _hb(10)), '']
    ]
    for i in range(len(inf['obj'])):
        data.append(['', Paragraph(u'- {}'.format(inf['obj'][i]), _h(10)), ''])
    data.append([''])
    data.append(['', Paragraph('4.2 Resumen de las actividades programadas y realizadas', _hb(10)), ''])
    for i in range(len(inf['rsm'])):
        data.append(['', Paragraph('- {}'.format(inf['rsm'][i]), _h(10))])
    t = Table(data, colWidths=inf['dim'])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    story.append(t)

def informacion3(story, inf):
    if inf.get('align'):
        cab_table(story, inf['enc'], inf['align'])
    else:
        cab_table(story, inf['enc'])
    data = ['']
    for i in range(len(inf['obj'])):
        try:
            data.append(['', Paragraph(u'- {}'.format(inf['obj'][i]), _h(10)), ''])
        except :
            data.append(['', Paragraph(u'- {}'.format('---------------'), _h(10)), ''])
    for i in range(len(inf['rsm'])):
        data.append(['', Paragraph('- {}'.format(inf['rsm'][i]), _h(10))])
    data.append([''])
    t = Table(data, colWidths=inf['dim'])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    story.append(t)

def informacionY(story, inf):
    if inf.get('align'):
        cab_table(story, inf['enc'], inf['align'])
    else:
        cab_table(story, inf['enc'])
    aux, data = [], []
    for i in range(len(inf['data'])):
        aux.append(Paragraph(inf['data'][i], _hb(10)))
    data.append(aux)
    for i in range(len(inf['info'])):
        aux = []
        for x in range(len(inf['info'][i])):
            aux.append(Paragraph(inf['info'][i][x], _h(10)))
        data.append(aux)
    t = Table(data, colWidths=inf['dim'])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('VALIGN', (0,0), (-1, -1), 'CENTER'),
        ('ALIGN',(0,0),(-1, -1),'CENTER'),
    ]))
    story.append(t)

def firmas(story, inf):
    aux, data = [], [['' '', ''],['' '', ''],[Paragraph('...................................................................', _h(9, TA_CENTER)), '', Paragraph('.......................................................................', _h(9, TA_CENTER))]]
    for i in range(len(inf['nombre'])):
        aux = []
        for x in range(len(inf['nombre'][i])):
            aux.append(Paragraph(inf['nombre'][i][x], _hb(9, TA_CENTER)))
        data.append(aux)
    for i in range(len(inf['cargo'])):
        aux = []
        for x in range(len(inf['cargo'][i])):
            aux.append(Paragraph(inf['cargo'][i][x], _h(8, TA_CENTER)))
        data.append(aux)
    t = Table(data, colWidths=inf['dim'])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1, -1), 'TOP'),
        ('ALIGN',(0,-1),(-1,-1),'CENTER'),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
    ]))
    story.append(t)

def componentes(componente):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte Componente"
    response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(pdf_name)
    buff = BytesIO()
    doc = SimpleDocTemplate(
        buff, 
        pagesize=A4,
        title='Devops',
        author='dannyrs'
    ) # Crear un doc
    story = [Spacer(1,inch*1.3)]
    data = [
        [Paragraph('ETAPA DEL INFORME:', _hb(10)), Paragraph(u'Componente: {}'.format(componente.nombre), _h(10))],
        [Paragraph('FECHA:', _hb(10)), Paragraph(u'{}'.format(componente.fin.strftime('%d/%m/%Y')), _h(10))]
    ]
    t = Table(data, colWidths=[125, 325])
    t.setStyle(TableStyle([
       ('VALIGN', (0,0), (-1, -1), 'TOP'),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))
    entidad = componente.proyecto_vinculacion.entidad
    inf = {
        'enc'  :'I. INFORMACION DE LA ORGANIZACION',
        'data' :['Direccion',u'Teléfono','Fax', 'Email', 'Persona de contacto'],
        'info' :[u'{}'.format(entidad.nombre), u'{}'.format(entidad.telefono), u'{}'.format(entidad.fax or ''), u'{}'.format(entidad.correo), u'{}'.format(entidad.encargado)],
        'dim'  :[120, 330]
    }
    informacionX(story, inf)

    story.append(Spacer(1, 20))
    inf = {
        'enc'  :'II. IDENTIFICACIÓN DEL PROYECTO',
        'data' :['Nombre del Proyecto'],
        'info' :[u'{}'.format(componente.nombre)],
        'dim'  :[120, 330]
    }
    informacionX(story, inf)

    story.append(Spacer(1, 20))
    inf = {
        'enc'  :'III. INTRODUCCIÓN',
        'data' :u'{}'.format(componente.introduccion),
        'dim'  :[30, 390, 30]
    }
    informacion1(story, inf)

    story.append(Spacer(1, 20))
    inf = {
        'enc' :'IV. RESUMEN DE LAS ACTIVIDADES PROGRAMADAS Y REALIZADAS',
        'obj' :[u'{}'.format(actividad.nombre) for actividad in componente.actividades.all()],
        'rsm' :[],
        'dim' :[30, 390, 30]
    }
    informacion2(story, inf)

    story.append(Spacer(1, 20))
    inf = {
        'enc'  :'V. OBSERVACIONES',
        'data' :componente.observacion,
        'dim'  :[30, 390, 30]
    }
    informacion1(story, inf)

    story.append(Spacer(1, 20))
    cab_table(story, 'VI. INFORME FINANCIERO')

    story.append(Spacer(1, 20))
    if componente.recursos_humanos.all():
        inf = {
            'align': TA_CENTER,
            'enc'  :'RECURSOS HUMANOS',
            'data' :['Cant.', 'Nombre del recurso', 'Descripción', 'Valor Unitario', 'Valor Total'],
            'info' :[[u'{}'.format(recurso.cantidad), u'{}'.format(recurso.nombre), u'{}'.format(recurso.descripcion), u'{}'.format(recurso.unitario), u'{}'.format(recurso.total)] for recurso in componente.recursos_humanos.all()],
            'dim'  :[55, 145, 150, 50, 50]
        }
        informacionY(story, inf)

    if componente.recursos_financieros.all():
        inf = {
            'align': TA_CENTER,
            'enc'  :'RECURSOS FINANCIEROS',
            'data' :['Cantidad', 'Nombre del recurso', 'Descripción', 'Valor Unitario', 'Valor Total'],
            'info' :[[u'{}'.format(recurso.cantidad), u'{}'.format(recurso.nombre), u'{}'.format(recurso.descripcion), u'{}'.format(recurso.unitario), u'{}'.format(recurso.total)] for recurso in componente.recursos_financieros.all()],
            'dim'  :[55, 145, 150, 50, 50]
        }
        informacionY(story, inf)

    if componente.recursos_materiales.all():
        inf = {
            'align': TA_CENTER,
            'enc'  :'RECURSOS MATERIALES',
            'data' :['Cantidad', 'Nombre del recurso', 'Descripción', 'Valor Unitario', 'Valor Total'],
            'info' :[[u'{}'.format(recurso.cantidad), u'{}'.format(recurso.nombre), u'{}'.format(recurso.descripcion), u'{}'.format(recurso.unitario), u'{}'.format(recurso.total)] for recurso in componente.recursos_materiales.all()],
            'dim'  :[55, 145, 150, 50, 50]
        }
        informacionY(story, inf)

    if componente.recursos_tecnologicos.all():
        inf = {
            'align': TA_CENTER,
            'enc'  :'RECURSOS TECNOLOGICOS',
            'data' :['Cantidad', 'Nombre del recurso', 'Descripción', 'Valor Unitario', 'Valor Total'],
            'info' :[[u'{}'.format(recurso.cantidad), u'{}'.format(recurso.nombre), u'{}'.format(recurso.descripcion), u'{}'.format(recurso.unitario), u'{}'.format(recurso.total)] for recurso in componente.recursos_tecnologicos.all()],
            'dim'  :[55, 145, 150, 50, 50]
        }
        informacionY(story, inf)

    story.append(Spacer(1, 80))
    coordinador = componente.proyecto_vinculacion.carrera.coordinadores.filter(estado=True).first()
    docente = '-------'
    carrera = '-------'
    if coordinador:
        carrera = coordinador.carrera.nombre
        docente = u'{}'.format(coordinador.docente.get_full_name())
    responsable = componente.responsable.perfil.docente
    inf = {
            'cargo':[[u'COORDINACIÓN DE LA CARRERA DE {}'.format(carrera).upper(), '', u'RESPONSABLE DE VINCULACION CON SOCIEDAD CARRERA DE {}'.format(componente.proyecto_vinculacion.carrera.nombre).upper()]],
            'nombre' :[[u'{}'.format(docente).upper(), '', u'{}'.format(responsable.get_full_name()).upper()]],
            'dim'  :[210, 60, 210] #400
        }
    firmas(story, inf)

    doc.build(story, onFirstPage=partial(primeraPagina2, titulo='INFORMES DE AVANCES DE PROYECTOS DE VINCULACIÓN'), onLaterPages=siguientePagina2)
    response.write(buff.getvalue())
    buff.close()
    return response

#################

def primeraPagina3(c, doc):
    c.saveState()
    c.drawImage(settings.STATIC_ROOT+'/images/logo_vinculacion.png', cm*2, PAGE_WIDTH-inch,  width=110, height=50, preserveAspectRatio=True)
    c.drawImage(settings.STATIC_ROOT+'/images/institucion2.png', PAGE_HEIGHT-inch*2.4, PAGE_WIDTH-inch*1.2,  width=130, height=70, preserveAspectRatio=True)
    c.drawRightString(PAGE_WIDTH-(cm*2), 705, '{}'.format(timezone.now().date()))
    c.setFont('Helvetica-Bold', 12)
    c.drawCentredString(PAGE_HEIGHT/2, PAGE_WIDTH-inch*0.8, u'FICHA DE EVAUACIÓN DE VINCULACIÓN CON LA COLECTIVIDAD')
    c.setFont('Times-Roman', 11)
    c.drawRightString(PAGE_HEIGHT-(cm*2), 0.75*(cm*2), 'Pagina {}'.format(1))
    c.restoreState()

def siguientePagina3(c, doc):
    c.saveState()
    c.drawImage(settings.STATIC_ROOT+'/images/logo_vinculacion.png', cm, PAGE_WIDTH-inch,  width=110, height=50, preserveAspectRatio=True)
    c.drawImage(settings.STATIC_ROOT+'/images/institucion2.png', PAGE_HEIGHT-inch*2.4, PAGE_WIDTH-inch*1.2,  width=130, height=70, preserveAspectRatio=True)
    c.setFont('Times-Roman', 11)
    c.drawRightString(PAGE_HEIGHT-(cm*2), 0.75*(cm*2), 'Pagina {}'.format(doc.page))
    c.restoreState()

class TextRotate(Flowable): #TableTextRotate
    '''Rotates a tex in a table cell.'''
    def __init__(self, text):
        Flowable.__init__(self)
        self.text = text
    def draw(self):
        canvas = self.canv
        canvas.rotate(90)
        fs = canvas._fontsize
        canvas.setFont('Helvetica', 7)
        if self.text.find('<br>') !=-1:
            texto = self.text.partition('<br>')
            salto = -3
            for value in texto:
                if value != '<br>':
                    canvas.drawString(0, salto, value)
                    salto -= 9
        else:
            canvas.drawString(0, -8, self.text)

    def wrap(self, aW, aH):
        canv = self.canv
        fn, fs = canv._fontname, canv._fontsize
        if self.text.find('<br>') !=-1:
            return canv._leading, 1 + canv.stringWidth(self.text.partition('<br>')[0], fn, 7)
        else:
            return canv._leading, 1 + canv.stringWidth(self.text, fn, 7)

def tabla2(story, inf):
    data = []
    data.append([Paragraph(u'NRO', _hb(6, TA_CENTER)), Paragraph(u'APELLIDOS Y NOMBRES', _hb(8, TA_CENTER)), Paragraph(u'CI', _hb(8, TA_CENTER)), Paragraph(u'FECHA', _hb(8, TA_CENTER)), Paragraph(u'H/ENTRADA', _hb(7, TA_CENTER)), Paragraph(u'H/SALIDA', _hb(8, TA_CENTER)), Paragraph(u'T/HORAS', _hb(7, TA_CENTER)), Paragraph(u'PARAMETROS DE CALIFICACIÓN SOBRE 10', _hb(8, TA_CENTER)), '', '', '', '', '', '', Paragraph(u'FIRMA', _hb(8, TA_CENTER))])
    data.append(['', '', '', '', '', '', '',TextRotate('PUNTUALIDAD(1)'), TextRotate('ASISTENCIA(1)'), TextRotate('ACTITUD FRENTE<br>ACTIVIDADES(2)'), TextRotate('CUMPLIMIENTO<br>OBJETIVOS(2)'), TextRotate('        NIVEL DE     <br>SATISFACCIÓN(2)'), TextRotate('ASISTENCIA(1)'), TextRotate('PROMEDIO'), ''])
    for i in range(len(inf)):
        data.append([
            Paragraph(u'{}'.format(inf[i][0]), _h(10, TA_CENTER)),
            Paragraph(u'{}'.format(inf[i][1]), _h(8)),
            Paragraph(u'{}'.format(inf[i][2]), _h(8, TA_CENTER)),
            Paragraph(u'{}'.format(inf[i][3]), _h(8, TA_CENTER)),
            Paragraph(u'{}'.format(inf[i][4]), _h(10, TA_CENTER)),
            Paragraph(u'{}'.format(inf[i][5]), _h(10, TA_CENTER)),
            Paragraph(u'{}'.format(inf[i][6]), _h(10, TA_CENTER)),
            Paragraph(u'{}'.format(inf[i][7]), _h(10, TA_CENTER)),
            Paragraph(u'{}'.format(inf[i][8]), _h(10, TA_CENTER)),
            Paragraph(u'{}'.format(inf[i][9]), _h(10, TA_CENTER)),
            Paragraph(u'{}'.format(inf[i][10]), _h(10, TA_CENTER)),
            Paragraph(u'{}'.format(inf[i][11]), _h(10, TA_CENTER)),
            Paragraph(u'{}'.format(inf[i][12]), _h(10, TA_CENTER)),
            Paragraph(u'{}'.format(inf[i][13]), _h(9, TA_CENTER)),
            Paragraph(u'{}'.format(inf[i][14]), _h(10, TA_CENTER)),
        ])
    t = Table(data, colWidths=[27, 190, 57, 57, 55, 50, 45, 26, 26, 26, 26, 26, 26, 30, 80],) #743
    t.setStyle(TableStyle([
        ('SPAN',(7,0),(13,0)),
        ('SPAN',(0,0),(0,1)),
        ('SPAN',(1,0),(1,1)),
        ('SPAN',(2,0),(2,1)),
        ('SPAN',(3,0),(3,1)),
        ('SPAN',(4,0),(4,1)),
        ('SPAN',(5,0),(5,1)),
        ('SPAN',(6,0),(6,1)),
        ('SPAN',(14,0),(14,1)),
        ('VALIGN', (0,0), (14, 0), 'CENTER'),
        ('VALIGN', (0,0), (6, 0), 'CENTER'),
        ('VALIGN', (7,1), (13, 1), 'CENTER'),
        ('ALIGN', (0,0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 2), (-1, -1), 'CENTER'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    story.append(t)


def evaluacion(componente):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte Componente"
    response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(pdf_name)
    buff = BytesIO()
    doc = SimpleDocTemplate(
        buff, 
        pagesize=landscape(A4),
        title='Devops',
        author='dannyrs'
    ) # Crear un doc
    story = []
    coordinador = componente.proyecto_vinculacion.carrera.coordinadores.filter(estado=True).first()
    if coordinador:
        coordinador = componente.proyecto_vinculacion.carrera.coordinadores.filter(estado=True).first().docente.get_full_name()
    inf = {
        'data' :[u'Nombre del Proyecto/Actividad', u'Institución y/o entidad beneficiaria', u'Responsable Institución y/o entidad beneficiaria', u'Responsable ITSS', u'Carrera', u'Fecha de ejecución'],
        'info' :[
            u'{} (Componente: {})'.format(componente.proyecto_vinculacion.nombre, componente.nombre),
            u'{}'.format(componente.proyecto_vinculacion.entidad.nombre),
            u'{}'.format(componente.proyecto_vinculacion.entidad.encargado),
            u'{}'.format(coordinador or '-----'),
            u'{}'.format(componente.proyecto_vinculacion.carrera.nombre),
            u'{} - {}'.format(componente.inicio.strftime('%d/%m/%Y'), componente.fin.strftime('%d/%m/%Y'))
        ],
        'dim'  :[225, 525]
    }
    encabezado(story, inf, 9, 10)
    
    story.append(Spacer(1, 5))
    inf = []
    i = 0
    for evaluacion in componente.evaluaciones.all():
        i += 1
        inf.append([
            u'{}'.format(i),
            u'{}'.format(evaluacion.estudiante.get_full_name().upper()),
            u'{}'.format(evaluacion.estudiante.cedula),
            u'{} - {}'.format(evaluacion.fecha_inicio.strftime('%d/%m/%Y'), evaluacion.fecha_fin.strftime('%d/%m/%Y')),
            u'{}'.format(evaluacion.hora_entrada.strftime('%H:%M')),
            u'{}'.format(evaluacion.hora_salida.strftime('%H:%M')),
            u'{}'.format(evaluacion.total_horas),
            u'{}'.format(evaluacion.puntualidad),
            u'{}'.format(evaluacion.asistencia),
            u'{}'.format(evaluacion.actitud),
            u'{}'.format(evaluacion.cumplimiento),
            u'{}'.format(evaluacion.aplicacion),
            u'{}'.format(evaluacion.satisfaccion),
            u'{}'.format(evaluacion.promedio),
            u'{}'.format('')
        ])
    tabla2(story, inf)

    story.append(Spacer(1, 60))
    coordinador = componente.proyecto_vinculacion.carrera.coordinadores.filter(estado=True).first()
    carrera = '----------'
    docente = '-------'
    if coordinador:
        carrera = coordinador.carrera.nombre
        docente = coordinador.docente.get_full_name()
    responsable = componente.responsable.perfil.docente
    inf = {
            'cargo':[[u'COORDINACIÓN DE LA CARRERA DE {}'.format(carrera).upper(), '', u'RESPONSABLE DE VINCULACION CON SOCIEDAD CARRERA DE {}'.format(componente.proyecto_vinculacion.carrera.nombre).upper()]],
            'nombre' :[[u'{}'.format(docente).upper(), '', u'{}'.format(responsable.get_full_name()).upper()]],
            'dim'  :[290, 100, 290] #400
        }
    firmas(story, inf)

    doc.build(story, onFirstPage=primeraPagina3, onLaterPages=siguientePagina3)
    response.write(buff.getvalue())
    buff.close()
    return response

def actividad(actividad):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte Componente"
    response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(pdf_name)
    buff = BytesIO()
    doc = SimpleDocTemplate(
        buff, 
        pagesize=A4,
        title='Devops',
        author='dannyrs'
    ) # Crear un doc
    story = [Spacer(1,inch*1.3)]
    try:
        data = [
            [Paragraph('TEMA:', _hb(10)), Paragraph(u'{}'.format(actividad.nombre), _h(10))],
            [Paragraph('CARRERA:', _hb(10)), Paragraph(u'{}'.format(actividad.carrera), _h(10))],
            [Paragraph('RESPONSABLE:', _hb(10)), Paragraph(u'{}'.format(actividad.responsable.perfil.docente.get_full_name()), _h(10))],
            [Paragraph('FECHA:', _hb(10)), Paragraph(u'{} - {}'.format(actividad.inicio.strftime('%d/%m/%Y'), actividad.fin.strftime('%d/%m/%Y')), _h(10))],
        ]
    except :
        data = [
            [Paragraph('TEMA:', _hb(10)), Paragraph(u'{}'.format('--------------'), _h(10))],
            [Paragraph('CARRERA:', _hb(10)), Paragraph(u'{}'.format(actividad.carrera), _h(10))],
            [Paragraph('RESPONSABLE:', _hb(10)), Paragraph(u'{}'.format(actividad.responsable.perfil.docente.get_full_name()), _h(10))],
            [Paragraph('FECHA:', _hb(10)), Paragraph(u'{} - {}'.format(actividad.inicio.strftime('%d/%m/%Y'), actividad.fin.strftime('%d/%m/%Y')), _h(10))],
        ]
        
    t = Table(data, colWidths=[100, 350])
    t.setStyle(TableStyle([
       ('VALIGN', (0,0), (-1, -1), 'TOP'),
       ('BACKGROUND', (0,0), (-1,-1), colors.white),
    ]))
    story.append(t)

    story.append(Spacer(1, 12))
    inf = {
        'enc'  :'I. INFORMACION DE LA ORGANIZACION',
        'data' :['Direccion',u'Teléfono','Fax', 'Email', 'Persona de contacto'],
        'info' :[
            u'{}'.format(actividad.entidad.nombre), 
            u'{}'.format(actividad.entidad.telefono), 
            u'{}'.format(actividad.entidad.fax or ''), 
            u'{}'.format(actividad.entidad.correo), 
            u'{}'.format(actividad.entidad.encargado)
        ],
        'dim'  :[120, 330]
    }
    informacionX(story, inf)

    story.append(Spacer(1, 20))
    inf = {
        'enc'  :'II. IDENTIFICACIÓN DEL PROYECTO',
        'data' :['Nombre de la Actividad'],
        'info' :[u'{}'.format(actividad.nombre)],
        'dim'  :[120, 330]
    }
    informacionX(story, inf)

    story.append(Spacer(1, 20))
    inf = {
        'enc' :'III. ESTUDIANTES INVOLUCRADOS',
        'obj' :[u'{}'.format(evaluacion.estudiante.get_full_name()) for evaluacion in actividad.evaluaciones.all()],
        'rsm' :[],
        'dim' :[30, 390, 30]
    }
    informacion3(story, inf)

    story.append(Spacer(1, 20))
    inf = {
        'enc'  :u'IV. DESCRIPCIÓN',
        'data' :u'{}'.format(actividad.descripcion),
        'dim'  :[30, 390, 30]
    }
    informacion1(story, inf)

    story.append(Spacer(1, 20))
    inf = {
        'enc'  :u'V. JUSTIFICACIÓN',
        'data' :u'{}'.format(actividad.justificacion),
        'dim'  :[30, 390, 30]
    }
    informacion1(story, inf)

    story.append(Spacer(1, 20))
    cab_table(story, u'VI. DESCRIPCIÓN DE LAS ACTIVIDADES PROGRAMADAS  REALIZADAS')

    story.append(Spacer(1, 20))
    inf = {
        'align': TA_CENTER,
        'enc' :u'OBJETIVOS GENERALES',
        'obj' :[u'{}'.format(value.nombre) for value in actividad.objetivos_generales.all()],
        'rsm' :[],
        'dim' :[30, 390, 30]
    }
    informacion3(story, inf)
    inf = {
        'align': TA_CENTER,
        'enc' :u'OBJETIVOS ESPECÍFICOS',
        'obj' :[u'{}'.format(value.nombre) for evaluacion in actividad.objetivos_especificos.all()],
        'rsm' :[],
        'dim' :[30, 390, 30]
    }
    informacion3(story, inf)
    inf = {
        'align': TA_CENTER,
        'enc' :u'ACTIVIDADES',
        'obj' :[u'{}'.format(value.nombre) for evaluacion in actividad.actividades_ac.all()],
        'rsm' :[],
        'dim' :[30, 390, 30]
    }
    informacion3(story, inf)
    
    story.append(Spacer(1, 20))

    inf = {
        'cargo':[[u'RESPONSABLE DE VINCULACION CON LA SOCIEDAD CARRERA DE {}'.format(actividad.carrera.nombre).upper(), '', u'RESPONSABLE DE {}'.format(actividad.carrera.nombre).upper()]],
        'nombre' :[[u'{}'.format(actividad.responsable.get_full_name()).upper(), '', u'{}'.format(actividad.entidad.encargado).upper()]],
        'dim'  :[220, 40, 210] #400
    }
    firmas(story, inf)

    doc.build(story, onFirstPage=partial(primeraPagina2, titulo=u'VINCULACIÓN CON LA COLECTIVIDAD', fondo=False), onLaterPages=partial(siguientePagina2, fondo=False))
    response.write(buff.getvalue())
    buff.close()
    return response

def evaluacion2(actividad):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Reporte Actividad"
    response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(pdf_name)
    buff = BytesIO()
    doc = SimpleDocTemplate(
        buff, 
        pagesize=landscape(A4),
        title='Devops',
        author='dannyrs'
    ) # Crear un doc
    story = []
    coordinador = actividad.carrera.coordinadores.filter(estado=True).first()
    if coordinador:
        coordinador = actividad.carrera.coordinadores.filter(estado=True).first().docente.get_full_name()
    inf = {
        'data' :[u'Nombre del Proyecto/Actividad', u'Institución y/o entidad beneficiaria', u'Responsable Institución y/o entidad beneficiaria', u'Responsable ITSS', u'Carrera', u'Fecha de ejecución'],
        'info' :[
            u'{}'.format(actividad.nombre),
            u'{}'.format(actividad.entidad.nombre),
            u'{}'.format(actividad.entidad.encargado),
            u'{}'.format(coordinador or '-----'),
            u'{}'.format(actividad.carrera.nombre),
            u'{} - {}'.format(actividad.inicio.strftime('%d/%m/%Y'), actividad.fin.strftime('%d/%m/%Y'))
        ],
        'dim'  :[225, 525]
    }
    encabezado(story, inf, 9, 10)
    
    story.append(Spacer(1, 5))
    inf = []
    i = 0
    for evaluacion in actividad.evaluaciones.all():
        i += 1
        inf.append([
            u'{}'.format(i),
            u'{}'.format(evaluacion.estudiante.get_full_name().upper()),
            u'{}'.format(evaluacion.estudiante.cedula),
            u'{} - {}'.format(evaluacion.fecha_inicio.strftime('%d/%m/%Y'), evaluacion.fecha_fin.strftime('%d/%m/%Y')),
            u'{}'.format(evaluacion.hora_entrada.strftime('%H:%M')),
            u'{}'.format(evaluacion.hora_salida.strftime('%H:%M')),
            u'{}'.format(evaluacion.total_horas),
            u'{}'.format(evaluacion.puntualidad),
            u'{}'.format(evaluacion.asistencia),
            u'{}'.format(evaluacion.actitud),
            u'{}'.format(evaluacion.cumplimiento),
            u'{}'.format(evaluacion.aplicacion),
            u'{}'.format(evaluacion.satisfaccion),
            u'{}'.format(evaluacion.promedio),
            u'{}'.format('')
        ])
    tabla2(story, inf)

    story.append(Spacer(1, 60))
    coordinador = actividad.carrera.coordinadores.filter(estado=True).first()
    carrera = '-------'
    docente = '-------'
    if coordinador:
        carrera = coordinador.carrera.nombre
        docente = coordinador.docente.get_full_name()
    responsable = actividad.responsable.perfil.docente
    inf = {
            'cargo':[[u'COORDINACIÓN DE LA CARRERA DE {}'.format(carrera).upper(), '', u'COORDINADOR DE {}'.format(actividad.entidad.nombre), '', u'RESPONSABLE DE VINCULACION CON SOCIEDAD CARRERA DE {}'.format(actividad.carrera.nombre).upper()]],
            'nombre' :[[u'{}'.format(docente).upper(), '', u'{}'.format(actividad.entidad.encargado).upper(), '', u'{}'.format(responsable.get_full_name()).upper()]],
            'dim'  :[220, 30, 220, 30, 220] #400
        }
    firmas(story, inf)

    doc.build(story, onFirstPage=primeraPagina3, onLaterPages=siguientePagina3)
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
        carreras.append(carrera.nombre)
    logo = ''
    if entidad.logo:
        logo = InlineImage(tpl, entidad.logo, height=Mm(18))
    context = {
        'nombre' : entidad.nombre,
        'logo' : logo,
        'telefono' : entidad.telefono,
        'fecha_inicio_convenio' : entidad.inicio,
        'fecha_fin_convenio' : entidad.fin,
        'correo' : entidad.correo,
        'direccion' : entidad.direccion,
        'enacargado' : entidad.encargado,
        'cargo' : entidad.cargo,
        'descripcion' : entidad.descripcion,
        'carreras' :  carreras,
        'responsable' : entidad.responsable.get_full_name(),
    }
    jinja_env = jinja2.Environment(autoescape=True)
    tpl.render(context, jinja_env)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = u'attachment; filename=convenio {}.docx'.format(entidad.nombre)
    tpl.save(response)
    return response

##### Evidencias
def evidencia_proyecto(data):
    s = StringIO.StringIO()
    zf = zipfile.ZipFile(s, "w")
    for evidencia in data.evidencias_proyecto.all():
        name = evidencia.imagen.name.split("/")[-1]
        url = settings.MEDIA_ROOT+'/'+evidencia.imagen.name
        zf.write(url.encode('utf-8').strip(), name)
    zf.close()
    response = HttpResponse(s.getvalue(), content_type="application/zip")
    response['Content-Disposition'] = u'attachment; filename=evidencia_{}.zip'.format(data.nombre)
    return response


def evidencia_actividad(data):
    s = StringIO.StringIO()
    zf = zipfile.ZipFile(s, "w")
    for evidencia in data.evidencias_actividades.all():
        name = evidencia.imagen.name.split("/")[-1]
        url = settings.MEDIA_ROOT+'/'+evidencia.imagen.name
        zf.write(url.encode('utf-8').strip(), name)
    zf.close()
    response = HttpResponse(s.getvalue(), content_type="application/zip")
    response['Content-Disposition'] = u'attachment; filename=evidencia_{}.zip'.format(data.nombre)
    return response