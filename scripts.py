from datacenter.models import Schoolkid


def get_schoolkid(full_name: str) -> Schoolkid | None:
    schoolkids = Schoolkid.objects.filter(full_name__contains=full_name).all()
    if len(schoolkids) > 1:
        print(f'Найдено несколько школьников с именем {full_name}')
        return None
    if not schoolkids:
        print(f'Не найдено ни одного школьника с именем {full_name}')
        return None
    return schoolkids[0]
