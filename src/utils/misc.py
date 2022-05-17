import inspect


def non_private_dict(obj):
    return {k: v for k, v in vars(obj).items() if not k.startswith('_')}


def get_all_classes(module):
    list_of_all_classes = []
    for obj in module.__dict__.values():
        if not inspect.isclass(obj):
            continue
        list_of_all_classes.append(obj)
    return list_of_all_classes
