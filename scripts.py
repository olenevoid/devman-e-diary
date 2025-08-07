from datacenter.models import Schoolkid, Mark


BAD_POINTS = (2,3)


def get_schoolkid(full_name: str) -> Schoolkid | None:
    schoolkids = Schoolkid.objects.filter(full_name__contains=full_name).all()
    if len(schoolkids) > 1:
        print(f'Найдено несколько школьников с именем {full_name}')
        return None
    if not schoolkids:
        print(f'Не найдено ни одного школьника с именем {full_name}')
        return None
    return schoolkids[0]


def get_bad_marks_for_schoolkid(schoolkid: Schoolkid):
    return Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=BAD_POINTS
    ).all()
