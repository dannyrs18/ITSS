from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from django.http import HttpResponse

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm, Inches, Pt
import jinja2
from jinja2.utils import Markup
from django.shortcuts import get_object_or_404

from ...vinculacion.models import Entidad, Informe_vinculacion

#### Inicio

PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH= defaultPageSize[0]
styles = getSampleStyleSheet()

title = 'Hola mundo'
pageinfo = 'Ejemplo platypus'

def primeraPagina(c, doc):
    c.saveState()
    c.setFont('Times-Bold', 16)
    c.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, title)
    c.setFont('Times-Roman', 9)
    c.drawString(inch, 0.75*inch, 'Primera Pagina / {}'.format(pageinfo))
    c.restoreState()
    f = Frame(cm, cm, PAGE_WIDTH-cm*2, PAGE_HEIGHT-cm*2, showBoundary=1) # Crea margenes
    f.drawBoundary(c) # Lo pinta con el canvas

def siguientePagina(c, doc):
    c.saveState()
    c.setFont('Times-Roman', 9)
    c.drawString(inch, 0.75*inch, 'Pagina {} {}'.format(doc.page, pageinfo))
    c.restoreState()

def go():
    doc = SimpleDocTemplate('phola.pdf') # Crear un doc
    story = [Spacer(1,inch)] # Espaciado de parrafo
    style = styles['Normal'] # Estilo 
    s = ParagraphStyle(
        'parrafo',
        fontName= "Times-Roman",
        fontSize=12,
        leading=14,     

    ) # Aqui crea estios perzonalizados
    for i in range(100):
        bogustext = ('This is Paragraph number {}.  '.format(i))*20
        p = Paragraph(bogustext, s) # otra opcion(bogustext, style)
        story.append(p)
        story.append(Spacer(1, 0.2*inch))
    story.append(Spacer(1, inch))
    data= [
        ['00', '01', '02', '03', '04'],
        ['10', '11', '12', '13', '14'],
        ['20', '21', '22', '23', '24'],
        ['30', '31', '32', '33', '34']
    ]
    t=Table(data, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,1),(-1,-2),colors.green),
        ('TEXTCOLOR',(0,0),(1,0),colors.red)
    ]))
    story.append(t)
    doc.build(story, onFirstPage=primeraPagina, onLaterPages=siguientePagina)

####### Fin

def tabla():
    doc = SimpleDocTemplate('phola.pdf')
    p = ParagraphStyle(
        'parrafo',
        fontName = 'Helvetica',
    )
    story = []
    story.append(Paragraph('Hola mundo', p))
    story.append(Paragraph('Hola mundo', p))
    story.append(Paragraph('Hola mundo', p))
    story.append(Paragraph('Hola mundo', p))
    story.append(Paragraph('Hola mundo', p))
    data = [
        ['Nombre', 'Apellidos', 'Edad', 'CI'],
        ['Danny', 'Romero', '23', Paragraph('0706433141 nlaksdnkasnd', styles['Normal'])],
        ['Anita', 'Collaguazo', '20', '1107827994'],
        ['Andres', 'Romero', '19', '0705676546']
    ]
    t = Table(data, colWidths=[60])
    t.setStyle(TableStyle([
       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
       ('ALIGN', (0,1), (-1, -1), 'CENTER'),
       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    story.append(t)
    story.append(t)
    doc.build(story)


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