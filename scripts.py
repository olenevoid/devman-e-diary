from datacenter.models import (
    Schoolkid, 
    Mark, 
    Chastisement, 
    Lesson, 

    Teacher
)
from django.db.models.query import QuerySet


BAD_POINTS = (2, 3)


def get_schoolkid(full_name: str) -> Schoolkid | None:
    schoolkids = Schoolkid.objects.filter(full_name__iregex=full_name).all()
    if len(schoolkids) > 1:
        print(f'Найдено несколько школьников с именем {full_name}')
        return None
    if not schoolkids:
        print(f'Не найдено ни одного школьника с именем {full_name}')
        return None
    return schoolkids[0]


def fix_bad_marks(schoolkid: Schoolkid, good_points=5):
    Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=BAD_POINTS
    ).update(points=good_points)


def delete_chastisements(schoolkid: Schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def get_lessons(schoolkid: Schoolkid, subject_name: str):
    return Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title__iregex=subject_name
    ).all()

def get_teacher(full_name: str) -> Teacher | None:
    teachers = Teacher.objects.filter(full_name__iregex=full_name).all()
    if len(teachers) > 1:
        print(f'Найдено несколько учителей с именем {full_name}')
        return None
    if not teachers:
        print(f'Не найдено ни одного учителя с именем {full_name}')
        return None
    return teachers[0]
