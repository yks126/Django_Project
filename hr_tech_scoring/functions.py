from django.db.models import Count, Case, When, Value, BooleanField, IntegerField
from django.db.models.aggregates import Sum
from .models import resume_scores_db, user_char_db
import pandas as pd
import ast
import random
import string
import os
from django.conf import settings


# 調用函數
csv_filename = os.path.join(settings.BASE_DIR, 'user_code_password.csv')
user_code_password = pd.read_csv(csv_filename, encoding='utf-8')

###################################################################################################


# 加载CSV文件
csv_file_path = os.path.join(settings.BASE_DIR, '05.csv')
df = pd.read_csv(csv_file_path, encoding='utf-8')
df = df.reset_index(drop=True)
all_row_ids = set(df.index)  # 假设 df 的索引包含所有可能的 row_id
num_rows = len(df)
last_page = num_rows - 1

list_fields = ['edu', 'r_experience', 'experience', 'license', 'license_1', 'license_2', 'license_3']
license_1types = [
    '證券商業務人員', '證券商高級業務人員', '證券投資分析人員', '投信投顧業務員',
    '期貨商業務員', '期貨交易分析人員', '票券商業務人員', '股務人員', '債券人員',
    '資產證券化', '企業內部控制'
]
license_2types = [
    '人身保險業務員', '財產保險業務員', '投資型保險商品業務員', '保險經紀人',
    '保險代理人', '保險公證人', '個人風險管理師', '企業風險管理師', '人壽保險核保理賠人員',
    '財產保險核保理賠人員', '保險精算師'
]
license_3types = [
    '信託業務專業測驗', '銀行內部控制與內部稽核測驗', '債券委外催收人員專業能力測驗', '理財規劃人員測驗',
    '初階授信人員專業測驗', '進階授信人員專業測驗', '授信擔保品估價能力測驗', '初階外匯人員專業測驗', '外匯交易專業能力測驗',
    '金融人員風險管理專業能力','金融科技力知識檢定測驗'
]

################################################
def parse_list_from_string(list_string):
    try:
        return ast.literal_eval(list_string)
    except ValueError as e:
        # 如果字符串不能被解析为列表，打印错误并设置一个默认值
        print(f"Error parsing string as list: {e}")
        return []  # 返回一个空列表作为默认值
#################################################

def get_resume_data(row_id):
    row_data = df.iloc[row_id]

    row_data['age'] = int(row_data['age'])

    # 解析所有的列表字段
    for field in list_fields:
        if row_data[field]:
            row_data[field] = parse_list_from_string(row_data[field])

    max_length = max(len(license_1types), len(license_2types), len(license_3types))

    license_data = []
    for i in range(max_length):
        license_data.append({
            'license_1type': license_1types[i] if i < len(license_1types) else '',
            'license_1highlight': row_data.license_1[i] == '1' if i < len(row_data.license_1) else False,
            'license_2type': license_2types[i] if i < len(license_2types) else '',
            'license_2highlight': row_data.license_2[i] == '1' if i < len(row_data.license_2) else False,
            'license_3type': license_3types[i] if i < len(license_3types) else '',
            'license_3highlight': row_data.license_3[i] == '1' if i < len(row_data.license_3) else False,
        })

    return row_data, license_data
###################################################################################################

def find_next_page(user_code, all_row_ids):
    # 查询数据库，找到当前用户的最后一条评分记录
    latest_record = resume_scores_db.objects.filter(user_code=user_code).order_by('-created').first()

    # 检查是否有最新的未完成评分的记录
    if latest_record:
        has_empty_score = any([
            latest_record.score_1 is None,
            latest_record.score_2 is None,
            latest_record.score_3 is None,
            latest_record.score_4 is None,
            latest_record.score_5 is None,
            latest_record.score_6 is None,
        ])
        if has_empty_score:
            # 如果最新的评分记录中有空的评分字段，意味着当前履历还未评分完毕
            return latest_record.row_id, True

    # 如果没有未完成的评分记录或者所有评分字段都已填写，查找下一个未评分的履历
    row_id_counts = resume_scores_db.objects.values('row_id').annotate(
        count=Count('row_id'),
        is_current_user=Sum(
            Case(
                When(user_code=user_code, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        )
    ).annotate(
        is_current_user=Case(
            When(is_current_user__gt=0, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    ).order_by('count', 'row_id')

    row_id_counts = list(row_id_counts)

    # 将row_id转换为整数
    for item in row_id_counts:
        item['row_id'] = int(item['row_id'])

    # 筛选出未被当前用户评分的履历
    filtered_row_ids = [item['row_id'] for item in row_id_counts if item['count'] == 1 and not item['is_current_user']]
    used_row_ids = set(row['row_id'] for row in row_id_counts)
    unused_row_ids = set(all_row_ids) - used_row_ids

    # 确定下一个未评分的履历
    if filtered_row_ids:
        next_page = filtered_row_ids[0]
    elif unused_row_ids:
        next_page = min(unused_row_ids)
    else:
        next_page_candidates = [item['row_id'] for item in row_id_counts if not item['is_current_user']]
        next_page = next_page_candidates[0] if next_page_candidates else None

    return next_page, False if next_page is not None else True
