def non_private_dict(obj):
    return {k:v for k,v in vars(obj).items() if not k.startswith('_')}
