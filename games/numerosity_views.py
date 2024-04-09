from django.shortcuts import render, redirect
from .models import tester_numerosity_score_db,tester_char_db
from .functions import operator_functions, distribute_choices


def introduction(request):
    tester_code = request.session.get('tester_code', None)
    if tester_code:
        tester = tester_char_db.objects.get(tester_code=tester_code)
    if request.method == 'POST':
        return redirect('game_numerosity_test_page')
    if tester and tester_numerosity_score_db.objects.filter(tester_code=tester_code).exists():
        # 如果tester已经有了score记录，则重定向到end页面
        return redirect('/games/numerosity/result_page/')  # 替换'end_page_url_name'为你的end页面的URL名称
    return render(request, 'games/numerosity/introduction.html')


def test_page(request):

    tester_code = request.session.get('tester_code', None)
    numerosity_score_entry, created = tester_numerosity_score_db.objects.get_or_create(
        tester_code=tester_code,
    )
    current_score = numerosity_score_entry.score

    if request.method == "POST":
        selected_numbers = request.POST.get('selected_numbers')
        if ',' in selected_numbers:
            selected_numbers = [int(x.strip()) for x in selected_numbers.split(',')]
            print(selected_numbers)

            a, b, c = request.session['selected_rows']
            chosen = request.session['chosen']
            ran_operator = request.session['ran_operator']

            if chosen == 'a':
                b, c = selected_numbers
            elif chosen == 'b':
                a, c = selected_numbers
            else:
                a, b = selected_numbers

            if operator_functions[ran_operator](a, b) == c:
                tester_numerosity_score_db.objects.update_or_create(
                    tester_code=tester_code,
                    defaults={
                        'score': current_score + 1,
                    })

    a, b, c, chosen, ran_operator, random_numbers = distribute_choices()

    request.session['selected_rows'] = [a, b, c]
    request.session['chosen'] = chosen
    request.session['ran_operator'] = ran_operator

    context = {
        "a": a,
        "b": b,
        "c": c,
        "chosen": chosen,
        "operator_path": 'games/numerosity/{}.png'.format(ran_operator),
        "number_1": random_numbers[0],
        "number_2": random_numbers[1],
        "number_3": random_numbers[2],
        "number_4": random_numbers[3],
        "number_5": random_numbers[4],
        "number_6": random_numbers[5],
        "number_7": random_numbers[6],
        "number_8": random_numbers[7],
        "number_9": random_numbers[8],
    }
    return render(request, 'games/numerosity/test_page.html', context)

def result_page(request):
    tester_code = request.session.get('tester_code', None)
    numerosity_score_entry, created = tester_numerosity_score_db.objects.get_or_create(
        tester_code=tester_code,
    )

    if request.method == "POST":
        return redirect('game_select')
    context = {
        'score': numerosity_score_entry.score,
    }
    return render(request, 'games/numerosity/result.html', context)
