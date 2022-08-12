from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Notes, Homework, Todo
from .forms import HomeworkForm, NotesForm, DashboardForm, TodoForm, ConversionForm, ConversionLengthForm,ConversionMassForm, UserRegistrationForm
from django.views.generic import DetailView
from youtubesearchpython import VideosSearch
import requests
import wikipedia
import random
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, "dashboard/home.html")

@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST["title"], desciption=request.POST["desciption"])
            notes.save()
        messages.success(request, f"Notes added from {request.user.username} successfully")
        return redirect("notes")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    data = {
        "notes": notes,
        "form": form
    }
    return render(request, "dashboard/notes.html", data)


@login_required
def delete_note(request, pk):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


@login_required
def notedetail(request, pk):
    note = get_object_or_404(Notes, id=pk)
    return render(request, "dashboard/notes_detail.html", {
        "note": note
    })

# class NoteDetailView(DetailView):
#     model = Notes
#     template_name = "dashboard/notes_detail.html"
#     context_object_name = "note"


@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework = Homework(
                user = request.user,
                title = request.POST["title"],
                subject = request.POST["subject"],
                desciption = request.POST["desciption"],
                due = request.POST["due"],
                is_finished = finished
            )
            homework.save()
            messages.success(request, f"Homework added from {request.user.username}")
            return redirect("homework")
    else:
        form = HomeworkForm()

    homeworks = Homework.objects.filter(user=request.user) 
    if len(homeworks) == 0:
        homeworks_done = True
    else:
        homeworks_done = False

    data = {
        "homeworks": homeworks,
        "homeworks_done": homeworks_done,
        'form': form
    }
    return render(request, "dashboard/homework.html", data)


@login_required
def update_homework(request, pk):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect("homework")


@login_required
def delete_homework(request,pk):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")



def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        video = VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()["result"]:
            result_dict = {
                "input": text,
                "title": i["title"],
                "duration": i["duration"],
                "thumbnail": i["thumbnails"][0]["url"],
                "channel": i["channel"]["name"],
                "link": i["link"],
                "views": i["viewCount"]["short"],
                "published": i["publishedTime"],
            }
            desc = ''
            if i["descriptionSnippet"]:
                for j in i["descriptionSnippet"]:
                    desc = j["text"]
            result_dict["description"] = desc
            result_list.append(result_dict)
        data = {
                "form": form,
                "results": result_list
            }
        return render(request, "dashboard/youtube.html", data)
    else:
        form = DashboardForm()
    data = {
        "form": form
    }
    return render(request, "dashboard/youtube.html", data)



@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todo = Todo(user=request.user, title=request.POST["title"],is_finished=finished)
            todo.save()
            messages.success(request, f"Todo added from {request.user.username} successfully")
            return redirect("todo")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    data = {
        "todos": todo,
        "form": form,
        "todos_done": todos_done
    }
    return render(request, "dashboard/todo.html", data)


@login_required
def delete_todo(request, pk):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


@login_required
def update_todo(request, pk):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect("todo")



def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST["text"]       
        url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
        r = requests.get(url)
        answer = r.json()
        if answer.get("totalItems") == 0:
            return redirect("books")
        result_list = []
        for i in range(5):
            result_dict = {
                "title": answer["items"][i]["volumeInfo"].get("title"),
                "subtitle": answer["items"][i]["volumeInfo"].get("subtitle"),
                "description": answer["items"][i]["volumeInfo"].get("description"),
                "count": answer["items"][i]["volumeInfo"].get("pageCount"),
                "obj_id": answer["items"][i].get("id"),
                "rating": answer["items"][i]["volumeInfo"].get("ratingCount"),
                "thumbnail": answer["items"][i]["volumeInfo"].get("imageLinks").get("thumbnail"),
                "preview": answer["items"][i]["volumeInfo"].get("previewLink"),
            }
           
            result_list.append(result_dict)
        data = {
                "form": form,
                "results": result_list
            }
        return render(request, "dashboard/books.html", data)
    else:
        form = DashboardForm()
    data = {
        "form": form
    }
    return render(request, "dashboard/books.html", data)


def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST["text"]
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
        r = requests.get(url)
        
        answer = r.json()
        try:
            phonetics = answer[0]["phonetics"][0]["text"]
            audio = answer[0]["phonetics"][1]["audio"]
            defination = answer[0]["meanings"][0]["definitions"][0]["definition"]
            example = answer[0]["meanings"][0]["definitions"][0]["example"]
            synonyms = answer[0]["meanings"][0]["definitions"][0]["synonyms"]
            data = {
                "form": form,
                "input": text,
                "phonetics": phonetics,
                "audio": audio,
                "definition": defination,
                "example": example,
                "synonyms": synonyms
            }
        except:
            data = {
                "form": form,
                "input": ""
            }
        return render(request, "dashboard/dictionary.html", data)
    else:
        form = DashboardForm()
    data = {
        "form": form
    }
    return render(request, "dashboard/dictionary.html", data)


def wiki(request):
    if request.method == "POST":
        text = request.POST["text"]
        form = DashboardForm(request.POST)
        try:
            search = wikipedia.page(text)
        except wikipedia.DisambiguationError as e:
            s = random.choice(e.options)
            search = wikipedia.page(s)
        except:
            search = None
        data = {
            "form": form,
            "search": search
        }
        return render(request, "dashboard/wiki.html", data)
    else:
        form = DashboardForm()
    data = {
        "form": form,
    }
    return render(request, "dashboard/wiki.html", data)



def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST["measurment"] == "length":
            measurement_form = ConversionLengthForm()
            data = {
                "form": form,
                "m_form": measurement_form,
                "input": True
            }
            if "input" in request.POST:
                first = request.POST["measure1"]
                second = request.POST["measure2"]
                input = request.POST["input"]
                answer = ''
                if input and int(input) >= 0:
                    if first == "yard" and second == "foot":
                        answer = f"{input} yard = {int(input)*3} foot"
                    elif first == "foot" and second == "yard":
                        answer = f"{input} foot = {int(input)/3} yard"
                    data = {
                        "form": form,
                        "m_form": measurement_form,
                        "input": True,
                        "answer": answer
                    }

        
        if request.POST["measurment"] == "mass":
            measurement_form = ConversionMassForm()
            data = {
                "form": form,
                "m_form": measurement_form,
                "input": True
            }
            if "input" in request.POST:
                first = request.POST["measure1"]
                second = request.POST["measure2"]
                input = request.POST["input"]
                answer = ''
                if input and int(input) >= 0:
                    if first == "pound" and second == "kilogram":
                        answer = f"{input} pound = {int(input)*0.453592} kilogram"
                    elif first == "kilogram" and second == "pound":
                        answer = f"{input} kilogram = {int(input)*2.20462} pound"
                    data = {
                        "form": form,
                        "m_form": measurement_form,
                        "input": True,
                        "answer": answer
                    }
        return render(request, "dashboard/conversion.html", data)
            
    else:

        form = ConversionForm()
        data = {
            "form": form,
            "input": False
        }
        return render(request, "dashboard/conversion.html", data)



def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account Created for {username}")
            return redirect("login") 
    else:

        form = UserRegistrationForm()
    data = {
        "form": form
    }
    return render(request, "dashboard/register.html", data)


@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homeworks) == 0:
        homeworks_done = True
    else:
        homeworks_done = False

    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    
    data = {
        "homeworks": homeworks,
        "todos": todos,
        "todos_done": todos_done,
        "homeworks_done": homeworks_done
    }

    return render(request, "dashboard/profile.html", data)