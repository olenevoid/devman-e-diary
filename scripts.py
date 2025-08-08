from datacenter.models import Schoolkid, Mark, Chastisement
from django.db.models.query import QuerySet


BAD_POINTS = (2, 3)


def get_schoolkid(full_name: str) -> Schoolkid | None:
    schoolkids = Schoolkid.objects.filter(full_name__contains=full_name).all()
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
