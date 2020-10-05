from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Question, Choice


#Get questios and display them

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


#Show Specific question and choices

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Quetsion does not exist")
    return render(request, 'polls/detail.html', {'question': question})


# Get question and display result
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


# VOte for a question choice
def vote(request, question_id):
    #print(request.Post['choice])
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExits):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "You did'nt select a choice.",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #Always return an HttpRespomseRedirect after successfully dealling
        #with Post data. this prevents data from being posted twice if a
        #user hits the back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))