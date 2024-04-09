from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, SelectionForm
from .models import user_char_db, resume_scores_db
from .functions import get_resume_data, find_next_page, df, all_row_ids, num_rows, last_page, user_code_password
import pandas as pd

def login_view(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_code = form.cleaned_data['user_code']
            password = form.cleaned_data['password']

            if  user_code_password.loc[user_code_password['user_code'] == user_code, 'password'].eq(password).any():

                request.session['user_code'] = user_code
                return redirect('scoring_index')
            else:
                messages.error(request, "密碼錯誤")
    
            #users = user_char_db.objects.filter(user_code=user_code)
            #if not users:
            #    messages.error(request, "該帳號不存在")

            #else:
            #    user = users[0]
            #    if user.user_password == password:
                    # 密码匹配，重定向到首页
            #        request.session['user_code'] = user_code
            #        return redirect('scoring_index')
            #    else:
                    # 密码不匹配
            #        messages.error(request, "密碼錯誤")
    else:
        form = LoginForm()

    return render(request, 'scoring/login.html', {'form': form})


# def create_account_view(request):
#     if request.method == 'POST':
#         form = UserCodeForm(request.POST)
#         if form.is_valid():
#             user_code = form.cleaned_data['user_code']
#
#             # 检查数据库中是否已存在相同的 user_code
#             if user_char_db.objects.filter(user_code=user_code).exists():
#                 # 如果存在，显示警告信息
#                 messages.error(request, "該用戶名已被使用，請選擇其他用戶名")
#             else:
#                 # 如果不存在，保存表单数据到数据库
#                 form.save()
#
#                 # 保存用户代码到 session 并重定向到登录页面
#                 request.session['user_code'] = user_code
#                 return redirect('scoring_login')
#
#     else:
#         form = UserCodeForm()
#
#     return render(request, 'scoring/create_account.html', {'form': form})


def index(request):
    user_code = request.session.get('user_code', None)

    #############################################################
    # 優先導向未評分的頁面，都評分了才可以開啟新的頁面
    user_scores = resume_scores_db.objects.filter(user_code=user_code)

    preset_row_id , no_new_page = find_next_page(user_code, all_row_ids)

    ###############################################################

    scores_list = []
    for score_entry in user_scores:
        # 确保 row_id 是整数类型
        try:
            row_id_int = int(score_entry.row_id)
        except ValueError:
            # 如果 row_id 不能转换为整数，则跳过这次循环的后续操作
            continue

        # 现在可以安全地进行比较，因为 row_id_int 和 len(df) 都是整数
        if 0 <= row_id_int < len(df):
            row_data = df.iloc[row_id_int]
            # 从DataFrame中提取需要的信息，例如type
            type_info = row_data['type'] if 'type' in row_data else 'Unknown'
        else:
            type_info = 'Unknown'

        scores_list.append({
            'row_id': score_entry.row_id,  # 保持原样，因为它可能在模板中用作字符串
            'score_1': score_entry.score_1,
            'score_2': score_entry.score_2,
            'score_3': score_entry.score_3,
            'score_4': score_entry.score_4,
            'score_5': score_entry.score_5,
            'score_6': score_entry.score_6,
            'marked': score_entry.marked,
            'notes': score_entry.notes,
        })

    context = {
        'scores_list': scores_list,  # 将分数列表传递给模板
        'preset_row_id': preset_row_id,
    }

    return render(request, 'scoring/index.html', context)


def detail(request, row_id):
    user_code = request.session.get('user_code', None)

    row_data, license_data= get_resume_data(row_id)

    # Try to retrieve an existing entry or create a placeholder one
    resume_score_entry, created = resume_scores_db.objects.get_or_create(
        row_id=row_id, user_code=user_code,
    )
    marked = resume_score_entry.marked

    # 找到前一頁
    row_id_scored = resume_scores_db.objects.filter(user_code=user_code).values('row_id')
    row_id_scored = [int(item['row_id']) for item in row_id_scored]

    row_id_index = row_id_scored.index(row_id)
    len_row_id_scored = len(row_id_scored)

    if request.method == 'POST':
        form = SelectionForm(request.POST)
        marked = True if form.data.get('marked') == "on" else False
        notes = form.data.get('notes')

        expand_edu = int(request.POST.get('expand_edu')) + resume_score_entry.expand_edu
        expand_experience = int(request.POST.get('expand_experience')) + resume_score_entry.expand_experience
        expand_intro = int(request.POST.get('expand_intro')) + resume_score_entry.expand_intro

        resume_scores_db.objects.update_or_create(
            row_id=row_id, user_code=user_code,
            defaults={
                'marked': marked,
                'notes': notes,
                'expand_edu': expand_edu,
                'expand_experience': expand_experience,
                'expand_intro': expand_intro,
            }
        )

        action_page = request.POST.get('action_page')
        if action_page == 'previous':
            previous_page = row_id_scored[row_id_index - 1] if row_id_index != 0 else None
            return redirect('scoring_detail', row_id=previous_page)
        elif action_page == 'home_page':
            return redirect('scoring_index')
        elif action_page == 'next':
            next_page = row_id_scored[row_id_index + 1] if row_id_index < (len_row_id_scored - 1) else None
            return redirect('scoring_detail', row_id=next_page)

        scores = {
            f'score_{i}': form.data.get(f'score_{i}') if form.data.get(f'score_{i}') != '' else None
            for i in range(1, 7)
        }

        # 更新或创建数据库条目，保留原有的标记状态
        resume_scores_db.objects.update_or_create(
            row_id=row_id, user_code=user_code,
            defaults={
                'score_1': scores['score_1'],
                'score_2': scores['score_2'],
                'score_3': scores['score_3'],
                'score_4': scores['score_4'],
                'score_5': scores['score_5'],
                'score_6': scores['score_6'],
            }
        )

        if action_page == 'new_resume':

            new_page , no_new_page= find_next_page(user_code, all_row_ids)
            print(no_new_page)
            if no_new_page:
                messages.error(request, '先填寫完每個分數才會有新履歷')
            return redirect('scoring_detail', row_id=new_page)

    else:
        initial_data = {'score_1': None, 'score_2': None, 'score_3': None, 'score_4': None, 'score_5': None, 'score_6': None}
        if resume_score_entry:
            initial_data.update({
                'score_1': resume_score_entry.score_1,
                'score_2': resume_score_entry.score_2,
                'score_3': resume_score_entry.score_3,
                'score_4': resume_score_entry.score_4,
                'score_5': resume_score_entry.score_5,
                'score_6': resume_score_entry.score_6,
                'marked': resume_score_entry.marked,
                'notes': resume_score_entry.notes,
            })
        form = SelectionForm(initial=initial_data)

    context = {
        'form': form,
        'row_data': row_data,
        'row_id': row_id,
        'num_rows': num_rows,
        'last_page': last_page,
        'marked': marked,
        'license_data': license_data,
        'row_id_index': row_id_index + 1,
        'len_row_id_scored': len_row_id_scored,
    }

    return render(request, 'scoring/detail.html', context)


