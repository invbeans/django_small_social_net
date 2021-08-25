from .models import PostReact
import datetime

def clean_every_week():
    like_recs = PostReact.objects.filter(react_type = 0)
    for rec in like_recs:
        if(datetime.timedelta(datetime.now() - rec.react_time).days > 30):
            rec.delete()
