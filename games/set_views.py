from django.shortcuts import render, redirect
from .forms import SelectionForm
from .functions import get_sets
from .models import tester_set_score_db,tester_char_db,PageVisit
import json
from datetime import timezone
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime

@csrf_exempt
def leave_page(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        visit_id = data.get('visit_id')
        leave_time_str = data.get('leave_time')
        leave_time = parse_datetime(leave_time_str)

        try:
            visit = PageVisit.objects.get(id=visit_id)
            visit.leave_time = leave_time
            if visit.enter_time and visit.leave_time:
                visit.stay_time = visit.leave_time - visit.enter_time
                # 格式化stay_time为HH:MM:SS格式
                formatted_stay_time = format_duration(visit.stay_time)
            else:
                formatted_stay_time = "00:00:00"
            visit.save()
            # 返回格式化后的stay_time
            return JsonResponse({"status": "success", "stay_time": formatted_stay_time})
        except PageVisit.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Visit not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def format_duration(duration):
    print("format_duration called with:", duration)
    print("Duration object:", duration, "Total seconds:", duration.total_seconds())
    seconds = int(duration.total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def introduction_view(request):
    current_url = request.get_full_path()
    tester_code = request.session.get('tester_code', None)
    if tester_code:
        tester = tester_char_db.objects.get(tester_code=tester_code)

    if tester and tester_set_score_db.objects.filter(tester_code=tester_code).exists():
        # 如果tester已经有了score记录，则重定向到end页面
        return redirect('/games/set/end/')  # 替换'end_page_url_name'为你的end页面的URL名称

    enter_time = timezone.now()
    if tester:
        visit = PageVisit.objects.create(
            tester=tester,
            enter_time=enter_time,
            url=current_url
        )
        context = {'visit_id': visit.id}

    return render(request, 'games/sets/introduction.html', context)

def test_page_view1(request):
    current_url = request.get_full_path()
    tester_code = request.session.get('tester_code', None)
    if tester_code:
        tester = tester_char_db.objects.get(tester_code=tester_code)




    enter_time = timezone.now()
    if tester:
        visit = PageVisit.objects.create(
            tester=tester,
            enter_time=enter_time,
            url=current_url
        )
    context = {'visit_id': visit.id}
    return render(request, 'games/sets/TestPage1.html', context)


def test_page_view2(request):
    current_url = request.get_full_path()
    tester_code = request.session.get('tester_code', None)
    if tester_code:
        tester = tester_char_db.objects.get(tester_code=tester_code)

    enter_time = timezone.now()
    if tester:
        visit = PageVisit.objects.create(
            tester=tester,
            enter_time=enter_time,
            url=current_url
        )
    # 初始化变量以避免UnboundLocalError
    form = SelectionForm(request.POST or None)  # 对于GET请求，form将是一个空表单
    selected_rows, correct_answer = get_sets()

    if request.method == 'POST':
        form = SelectionForm(request.POST)
        if form.is_valid():
            # 只有在表单数据有效的情况下才处理表单数据
            request.session['number_entered_1'] = form.cleaned_data.get('number_entered_1')
            request.session['number_entered_2'] = form.cleaned_data.get('number_entered_2')
            request.session['number_entered_3'] = form.cleaned_data.get('number_entered_3')

            # 可能需要重定向到结果视图
            return redirect('set_results')  # 确保这里使用的是结果视图的URL名称
    # 将selected_rows和correct_answer保存到session中
    request.session['selected_rows'] = selected_rows
    request.session['correct_answer'] = correct_answer

    context = {
        "form": form,  # 将表单对象添加到上下文中
        "number_1": selected_rows[0],
        "number_2": selected_rows[1],
        "number_3": selected_rows[2],
        "number_4": selected_rows[3],
        "number_5": selected_rows[4],
        "number_6": selected_rows[5],
        "number_7": selected_rows[6],
        "number_8": selected_rows[7],
        "number_9": selected_rows[8],
        "image_path_1": 'games/set_game/{}.jpg'.format(selected_rows[0]),
        "image_path_2": 'games/set_game/{}.jpg'.format(selected_rows[1]),
        "image_path_3": 'games/set_game/{}.jpg'.format(selected_rows[2]),
        "image_path_4": 'games/set_game/{}.jpg'.format(selected_rows[3]),
        "image_path_5": 'games/set_game/{}.jpg'.format(selected_rows[4]),
        "image_path_6": 'games/set_game/{}.jpg'.format(selected_rows[5]),
        "image_path_7": 'games/set_game/{}.jpg'.format(selected_rows[6]),
        "image_path_8": 'games/set_game/{}.jpg'.format(selected_rows[7]),
        "image_path_9": 'games/set_game/{}.jpg'.format(selected_rows[8]),
        "visit_id": visit.id,

    }

    return render(request, 'games/sets/TestPage2.html', context)


def results_view(request):
    # 從session中獲取selected_rows和correct_answer
    number_entered_1 = request.session['number_entered_1']
    number_entered_2 = request.session['number_entered_2']
    number_entered_3 = request.session['number_entered_3']
    selected_rows = request.session.get('selected_rows', [])
    correct_answer = request.session.get('correct_answer', [[]])
    user_answer = {str(num) for num in filter(None, [number_entered_1, number_entered_2, number_entered_3])}

    image_paths_2d = []
    for i in range(0, len(selected_rows), 3):
        row = ['games/set_game/{}.jpg'.format(num) for num in selected_rows[i:i + 3]]
        image_paths_2d.append(row)

    user_answer_flat = [f'games/set_game/{num}.jpg' for num in user_answer]
    correct_answer_flat = [f'games/set_game/{num}.jpg' for sublist in correct_answer for num in sublist]

    context = {
        "number_entered_1": number_entered_1,
        "number_entered_2": number_entered_2,
        "number_entered_3": number_entered_3,
        "selected_rows": selected_rows,
        "user_answer_flat": user_answer_flat,
        "image_paths_2d": image_paths_2d,
        "correct_answer_flat": correct_answer_flat,
    }

    # Render the template with the context
    return render(request, 'games/sets/Results.html', context)

def my_page_view(request):
    user_code = request.session.get('tester_code', None)
    number_entered_1 = number_entered_2 = number_entered_3 = None

    # 从数据库中获取用户数据
    if user_code:
        user_data = tester_set_score_db.objects.filter(tester_code=user_code).first()
        if user_data:
            correct = user_data.correct
            wrong = user_data.wrong
            skipped_count = user_data.skipped_count
            answered_count = user_data.answered_count
            score = user_data.score
        else:
            correct = wrong = skipped_count = answered_count = score = 0
    else:
        correct = wrong = skipped_count = answered_count = score = 0

    if request.method == 'POST':
        form = SelectionForm(request.POST)
        if form.is_valid():
            answered_count += 1
            if 'skip' in request.POST:
                skipped_count += 1
            else:
                number_entered_1 = form.cleaned_data.get('number_entered_1')
                number_entered_2 = form.cleaned_data.get('number_entered_2')
                number_entered_3 = form.cleaned_data.get('number_entered_3')

                user_answers = {str(num) for num in filter(None, [number_entered_1, number_entered_2, number_entered_3])}
                correct_answer = request.session.get('correct_answer', [])
                correct_answers_set = {str(num) for num in correct_answer[0]}
                if user_answers.issubset(correct_answers_set):
                    correct += 1
                else:
                    wrong += 1

            # 计算得分
            score = 3 * correct - 1 * wrong - 0.5 * skipped_count

            # 更新用户数据到数据库
            tester_set_score_db.objects.update_or_create(
                tester_code=user_code,
                defaults={
                    'correct': correct,
                    'wrong': wrong,
                    'skipped_count': skipped_count,
                    'answered_count': answered_count,
                    'score': score
                }
            )

        # 获取新的题目集
        selected_rows, correct_answer = get_sets()

        request.session['selected_rows'] = selected_rows
        request.session['correct_answer'] = correct_answer

        return redirect('set_mypage')

    else:
        if 'selected_rows' not in request.session or 'correct_answer' not in request.session:
            selected_rows, correct_answer = get_sets()
            request.session['selected_rows'] = selected_rows
            request.session['correct_answer'] = correct_answer
        else:
            selected_rows = request.session['selected_rows']
            correct_answer = request.session['correct_answer']

    context = {
        "correct": correct,
        "score": score,
        "skipped_count": skipped_count,
        "wrong": wrong,
        "number_1": selected_rows[0],
        "number_2": selected_rows[1],
        "number_3": selected_rows[2],
        "number_4": selected_rows[3],
        "number_5": selected_rows[4],
        "number_6": selected_rows[5],
        "number_7": selected_rows[6],
        "number_8": selected_rows[7],
        "number_9": selected_rows[8],
        "image_path_1": 'games/set_game/{}.jpg'.format(selected_rows[0]),
        "image_path_2": 'games/set_game/{}.jpg'.format(selected_rows[1]),
        "image_path_3": 'games/set_game/{}.jpg'.format(selected_rows[2]),
        "image_path_4": 'games/set_game/{}.jpg'.format(selected_rows[3]),
        "image_path_5": 'games/set_game/{}.jpg'.format(selected_rows[4]),
        "image_path_6": 'games/set_game/{}.jpg'.format(selected_rows[5]),
        "image_path_7": 'games/set_game/{}.jpg'.format(selected_rows[6]),
        "image_path_8": 'games/set_game/{}.jpg'.format(selected_rows[7]),
        "image_path_9": 'games/set_game/{}.jpg'.format(selected_rows[8]),
        "number_entered_1": number_entered_1,
        "number_entered_2": number_entered_2,
        "number_entered_3": number_entered_3,
        "answered_count": answered_count,
    }

    return render(request, 'games/sets/MyPage.html', context)




def end_view(request):
    user_code = request.session.get('tester_code')

    # 尝试从数据库中获取当前用户的得分条目
    if user_code is not None:
        try:
            set_score_entry = tester_set_score_db.objects.get(tester_code=user_code)
            score = set_score_entry.score

        except tester_set_score_db.DoesNotExist:
            # 如果没有找到对应的得分条目，可以在这里处理（例如记录日志）
            pass

    context = {
        "score": score,
    }

    return render(request, 'games/sets/end.html', context)
