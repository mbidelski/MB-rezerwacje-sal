from django.shortcuts import redirect
from django.http import HttpResponse
from django.views import View
from rooms.models import Room, Reservation
from datetime import date
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

container_html = """
<html>
<body>
<div style="width:40%; margin:auto;">
{}
</div>
</body>
</html>
"""

@csrf_exempt
def home(request):

    if request.method == "POST":
        add_name = request.POST.get("name")
        add_seats = request.POST.get("seats")
        add_projector = request.POST.get("projector")
        if add_projector is not None:
            add_projector = True
        else:
            add_projector = False
        Room.objects.create(name=add_name, seats=add_seats, projector=add_projector)

    response = HttpResponse()
    all_rooms = Room.objects.all()
    rooms_html = """<table width=100%>
    <tr>
        <th scope="col" align="left" width=30%><font color="grey">Nazwa sali</th>
        <th scope="col"><font color="grey">Status</th>
        <th scope="col"></th>
        <th scope="col"></th>
        <th scope="col"></th>
    </tr>"""

    for i in all_rooms:

        if Reservation.objects.filter(room=i).filter(day=date.today()):
            x = """<font color="red">Zajęta</font>"""
        else:
            x="""<font color="green">Wolna</font>"""

        name = """<p><strong>{}</strong></p>""".format(i.name.title())
        mod = """<a href="/home/modify/{}"><font size="2">Modyfikuj</font></a>""".format(i.id)
        del_room_str = """<a href="/home/delete/{}"><font size="2">Usuń</font></a>""".format(i.id)
        rez = """<a href="/home/details/{}"><button>Rezerwacje</button></a>""".format(i.id)
        rooms_html = rooms_html + """<tr align="middle"><td align="left">{}</td>
        <td>{}</td><td>{}</td><td>{}</td>
        <td>{}</td></tr>""".format(name, x, mod, del_room_str, rez)

    rooms_html = rooms_html + """</table>
    <form method="POST" action=#>
        <p><strong><font color="grey">Dodaj salę:</strong></font></p>
        <label>Nazwa: <input type="text" name="name"></label>
        <label>Liczba miejsc: <input type="number" name="seats"></label>
        <label>Projektor: <input type="checkbox" name="projector"></label>
        <button type="submit">Dodaj</button>
    </form>
    """
    response.write(container_html.format(rooms_html))
    return response

@csrf_exempt
def mod_room(request, room_id):

    room = Room.objects.get(pk=room_id)

    if request.method == "POST":
        mod_name = request.POST.get("name")
        mod_seats = request.POST.get("seats")
        mod_projector = request.POST.get("projector")
        if mod_projector is not None:
            mod_projector = True
        else:
            mod_projector = False

        room.name = mod_name
        room.seats = mod_seats
        room.projector = mod_projector
        room.save()

    if room.projector == True:
        chk_box = "checked"
    else:
        chk_box = ""

    html = """
    <form method="POST" action=#>
        <p><strong>Modyfiku dane sali:</strong></p>
        <label>Nazwa: <input type="text" name="name" value="{}"></label>
        <label>Liczba miejsc: <input type="number" name="seats" value="{}"></label>
        <label>Projektor: <input type="checkbox" name="projector" {}></label>
        <button type="submit">Zatwierdź</button>
        <a href="/home/details/{}"><button type="button">Rezerwuj</button></a>
        <a href="/home/"><button type="button">Powrót</button></a>
    </form>
    """.format(room.name, room.seats, chk_box, room.id)

    return HttpResponse(container_html.format(html))

def del_room(request, room_id):
    room = Room.objects.get(pk=room_id)
    name = room.name
    room.delete()
    return HttpResponse("""Usunąłem salę "{}" <a href="/home">Powrót</a>""".format(name))

@csrf_exempt
def details(request, room_id):
    room = Room.objects.get(pk=room_id)
    dbl_book_warning = ""

    if request.method == "POST":
        print(request.POST.get("data"))
        if request.POST.get("data") == "":
            dbl_book_warning = """<br><font color="red">Nie podałeś daty spotkania</font>"""
        elif Reservation.objects.filter(room=room).filter(day=request.POST.get("data")):
            dbl_book_warning = """<br><font color="red">Sala zajęta wybranego dnia</font>"""
        else:
            data_nowego_spotkania = request.POST.get("data")
            komentarz = ""
            if request.POST.get("comment") is not None:
                komentarz = request.POST.get("comment")
            Reservation.objects.create(day=data_nowego_spotkania, comment=komentarz, room=room)

    room_booked = Reservation.objects.filter(room=room)
    if room.projector == True:
        chk_box = "Jest"
    else:
        chk_box = "Brak"

    html = """
    <table width=100%>
    <tr width=100%>
        <td><strong>Dane sali:</strong></td>
        <td colspan=2 align="right">
            <a href="/home/modify/{}"><button type="button">Modyfikuj</button></a>
            <a href="/home/"><button type="button">Powrót</button></a>
        </td>
    </tr>
    
    <tr width=100%>
        <td width=33%>Nazwa: {}</td>
        <td>Liczba miejsc: {}</td>
        <td width=33%>Projektor: {}</td>
    </tr>
    <tr style="height:50px"><td colspan=3></td></tr>
    <tr>
    <form action=# method="POST">
        <td><strong>Rezerwacje</strong>{}</td>
        <td colspan=2 align="right">
            <input type="date" name="data">
            <input type="text" name="comment">
            <a href=#><button type="submit">Dodaj</button></a>
        </td>
    <form>
    </tr>
        <tr style="height:10px"><td colspan=3></td></tr>
    <tr>
        <td><strong>Daty</strong></td>
        <td><strong>Komentarz:</strong></td>
    </tr>
    """.format(room.id, room.name, room.seats, chk_box, dbl_book_warning)

    for rb in room_booked:
        if rb.comment is None:
            komentarz = "-"
        else:
            komentarz = rb.comment

        if rb.day >= date.today():

            html = html + """
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td align="middle"><a href=/res_del/{}/{}><font size=2>Usuń</font></a></td>
            </tr>
            """.format(rb.day, komentarz, rb.room.id, rb.day)

    return HttpResponse(container_html.format(html))

@csrf_exempt
def res_del(request, room_id, res_day):
    r = Room.objects.get(pk=room_id)
    Reservation.objects.filter(room=r, day=res_day).delete()
    return redirect("/home/details/{}".format(room_id))