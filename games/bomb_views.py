from django.shortcuts import render, redirect
from .models import tester_bomb_score_db
from .functions import generate_complex_encoding_map
import random

def introduction(request):

    return render(request, 'games/bomb_risk_test/introduction.html')


complex_encoding_map = generate_complex_encoding_map()

def test_page(request):

    tester_code = request.session.get('tester_code', None)
    bomb_score_entry, created = tester_bomb_score_db.objects.get_or_create(
        tester_code=tester_code,
    )
    current_round = bomb_score_entry.current_round

    if request.method == "POST":
        score = request.POST.get('boxes_collected')

        score_field_name = f'score_{current_round}'
        current_round += 1

        # Update or create the record in the database with dynamic field names
        tester_bomb_score_db.objects.update_or_create(
            tester_code=tester_code,
            defaults={
                score_field_name: score,
                'current_round': current_round,
            }
        )

        if current_round >= 6:
            return redirect('game_bomb_result_page')

    if current_round == 0:
        bomb_exp_time = random.randint(1, 64)
    elif current_round == 6:
        return redirect('game_bomb_result_page')
    else:
        bomb_field = f'bomb_{current_round}'
        bomb_exp_time = getattr(bomb_score_entry, bomb_field)

        # 將爆炸時間進行轉碼
    bomb_exp_time_encoded = complex_encoding_map[bomb_exp_time]

    context = {
        'current_round': current_round,
        'range_8': range(8),
        'bomb_exp_time_encoded': bomb_exp_time_encoded,
        'bomb_exp_time': bomb_exp_time + 1,
        'score_1': bomb_score_entry.score_1,
        'score_2': bomb_score_entry.score_2,
        'score_3': bomb_score_entry.score_3,
        'score_4': bomb_score_entry.score_4,
        'score_5': bomb_score_entry.score_5,
    }
    return render(request, 'games/bomb_risk_test/test_page.html', context)



def result_page(request):
    tester_code = request.session.get('tester_code', None)
    bomb_score_entry, created = tester_bomb_score_db.objects.get_or_create(
        tester_code=tester_code,
    )

    if request.method == "POST":
        return redirect('game_select')

    context = {
        'score_1': bomb_score_entry.score_1,
        'score_2': bomb_score_entry.score_2,
        'score_3': bomb_score_entry.score_3,
        'score_4': bomb_score_entry.score_4,
        'score_5': bomb_score_entry.score_5,
    }
    return render(request, 'games/bomb_risk_test/result.html', context)