def preserve(obj):
    """Save updates to obj (including first-write) without
    trashing the publication/revision dates"""
    fpa = obj.first_published_at
    lpa = obj.last_published_at
    lrca = obj.latest_revision_created_at
    rev = obj.save_revision()
    rev.publish()
    obj.first_published_at = fpa
    obj.last_published_at = lpa
    obj.latest_revision_created_at = lrca
    obj.save()
