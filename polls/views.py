from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import messages
from .models import Choice, Question, Voter


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


@login_required
def vote(request, question_id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            Voter.objects.create(question_id=question_id, user_id=request.user.id)
            messages.success(request,f'Your vote is successfully recorded')
            return HttpResponseRedirect(reverse('polls:index'))
    else:
        if Voter.objects.filter(question_id=question_id, user_id=request.user.id).exists():
            question = get_object_or_404(Question, pk=question_id)
            print("yippe")
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You have already voted."
            })
        else:
            question = get_object_or_404(Question, pk=question_id)
            return render(request, 'polls/detail.html', {
                'question': question,
            })
