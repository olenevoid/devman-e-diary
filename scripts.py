from datacenter.models import (
    Schoolkid, 
    Mark, 
    Chastisement, 
    Lesson, 
    Commendation,
)


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


def fix_bad_marks(name: str, good_points = 5 ):
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


def get_last_lesson_without_commedation(
        subject_name: str, 
        schoolkid: Schoolkid, 
    ) -> Lesson:

    commedations = Commendation.objects.filter(
        schoolkid=schoolkid,
        subject__title__iregex=subject_name
    ).all()

    commedation_dates = [commedation.created for commedation in commedations]

    last_lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title__iregex=subject_name
    ).exclude(date__in=commedation_dates).order_by('date').last()

    return last_lesson


def create_commedation(
        subject_name: str,
        name: str,
        text: str = 'Хорошо!'
    ):
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return

    lesson = get_last_lesson_without_commedation(subject_name, schoolkid)

    commedation = Commendation()
    commedation.created = lesson.date
    commedation.subject = lesson.subject
    commedation.schoolkid = schoolkid
    commedation.teacher = lesson.teacher
    commedation.text = text
    commedation.save()
    print(f'Похвала успешно создана для {schoolkid.full_name}')
