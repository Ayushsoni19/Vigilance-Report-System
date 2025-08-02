from django.shortcuts import render, redirect
from .forms import MisuseEntryForm
from .models import MisuseEntry
from django.http import HttpResponse
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def index(request):
    form = MisuseEntryForm(request.POST or None)
    entries = MisuseEntry.objects.all().order_by('-id')

    query = request.GET.get('search', '')
    bp_search = request.GET.get('bp_no', '')
    from_date = request.GET.get('from', '')
    to_date = request.GET.get('to', '')

    if query:
        entries = entries.filter(name__icontains=query)
    if bp_search:
        entries = entries.filter(bp_no__icontains=bp_search)
    if from_date and to_date:
        entries = entries.filter(date__gte=from_date, date__lte=to_date)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('index')

    return render(request, 'misuse/index.html', {
        'form': form,
        'entries': entries,
        'search': query,
        'from': from_date,
        'to': to_date,
        'bp_no': bp_search,
    })

def export_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="misuse_entries.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Date', 'Name', 'Address', 'Zone', 'Public DC', 'BP No', 'Purpose', 'Load KW',
        'Meter Make', 'Meter SN', 'Capacity', 'Pulse', 'Reading', 'MD', 'PH', 'Remark'
    ])
    for entry in MisuseEntry.objects.all():
        writer.writerow([
            entry.date, entry.name, entry.address, entry.zone, entry.public_dc,
            f'="{entry.bp_no}"', entry.purpose, entry.load_kw,
            f'="{entry.meter_make}"', f'="{entry.meter_sn}"', entry.capacity,
            f'="{entry.pulse}"', f'="{entry.reading}"',
            f'="{entry.md}"', f'="{entry.ph}"', entry.remark
        ])
    return response

def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="misuse_entries.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 30

    header = "Date | Name | Address | Zone | Public DC | BP No | Purpose | Load KW | Meter Make | Meter SN | Capacity | Pulse | Reading | MD | PH | Remark"
    p.drawString(30, y, header)
    y -= 20

    for entry in MisuseEntry.objects.all():
        line = f"{entry.date} | {entry.name} | {entry.address} | {entry.zone} | {entry.public_dc} | {entry.bp_no} | {entry.purpose} | {entry.load_kw} | {entry.meter_make} | {entry.meter_sn} | {entry.capacity} | {entry.pulse} | {entry.reading} | {entry.md} | {entry.ph} | {entry.remark}"
        p.drawString(30, y, line[:120])
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 30
            p.drawString(30, y, header)
            y -= 20

    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
