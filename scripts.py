from datacenter.models import (
    Schoolkid, 
    Mark, 
    Chastisement, 
    Lesson, 
    Commendation,
)


BAD_POINTS = (2, 3)
GOOD_POINTS = 5
DEFAULT_COMMENDATION_TEXT = 'Хорошо!'


def get_schoolkid(full_name: str) -> Schoolkid | None:
    try:
        schoolkid = Schoolkid.objects.get(full_name__iregex=full_name)
    
    except Schoolkid.MultipleObjectsReturned:
        print(
            f'Найдено несколько школьников с именем {full_name}\n'
            'Уточните имя и еще раз запустите скрипт'
        )
        return None
    
    except Schoolkid.DoesNotExist:
        print(
            f'Не найдено ни одного школьника с именем {full_name}\n'
            'Уточните имя и еще раз запустите скрипт'
        )
        return None

    return schoolkid


def fix_bad_marks(name: str, good_points: int = GOOD_POINTS):
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return

    Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=BAD_POINTS
    ).update(points=good_points)
    print(f'Плохие оценки успешно изменены для {schoolkid.full_name}')


def delete_chastisements(name: str):
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return

    Chastisement.objects.filter(schoolkid=schoolkid).delete()
    print(f'Замечания успешно удалены для {schoolkid.full_name}')


def get_last_lesson_without_commendation(
        subject_name: str, 
        schoolkid: Schoolkid, 
    ) -> Lesson | None:

    commendations = Commendation.objects.filter(
        schoolkid=schoolkid,
        subject__title__iregex=subject_name
    ).all()

    commendation_dates = [commendation.created for commendation in commendations]

    last_lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title__iregex=subject_name
    ).exclude(date__in=commendation_dates).order_by('date').last()

    return last_lesson


def create_commendation(
        name: str,
        subject_name: str,
        text: str = DEFAULT_COMMENDATION_TEXT
    ):
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return

    lesson = get_last_lesson_without_commendation(subject_name, schoolkid)
    if not lesson:
        print(
            f'Не найден ни один урок без похвал для предмета {subject_name}\n'
            'Попробуйте еще раз с другим предметом'
        )
        return

    commendation = Commendation()
    commendation.created = lesson.date
    commendation.subject = lesson.subject
    commendation.schoolkid = schoolkid
    commendation.teacher = lesson.teacher
    commendation.text = text
    commendation.save()
    print(f'Похвала успешно создана для {schoolkid.full_name}')
