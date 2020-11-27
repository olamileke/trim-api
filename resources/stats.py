from flask_restful import Resource, fields, marshal
from flask import g
from models import db, Redirect, Url, Group
from utilities.middlewares import authenticate
from datetime import date, timedelta

class Stats(Resource):
    def __init__(self):
        self.method_decorators = [ authenticate ]
        self.redirect_field = {
            'short_url':fields.String(attribute='url.short_path'),
            'url':fields.String(attribute='url.path'),
            'created_at':fields.String(attribute='created_time')
        }

    def get(self):
        totals = self.totals(g.user.id)
        redirect_stats = self.redirect_stats(g.user.id)
        url_stats = self.url_stats(g.user.id)
        data = {'totals':totals, 'redirect_stats':redirect_stats, 'url_stats':url_stats}

        return {'data':data}
    
    def url_stats(self, user_id):
        urls = Url.query.filter((Url.user_id == user_id)).all()
        data = {}
        lengths = [len(url.redirects) for url in urls]
        lengths.sort()
        lengths.reverse()
        count = 5

        if len(urls) < 5:
            count = len(urls)

        for i in range(0, count):
            for url in urls:
                if len(url.redirects) == lengths[0]:
                    data[url.short_path] = lengths[0]
                    lengths.remove(lengths[0])
                    urls.remove(url)
                    break

        return data

    def redirect_stats(self, user_id):
        last_week_date = date.today() - timedelta(days=7)
        start = last_week_date
        redirects = Redirect.query.filter((Redirect.user_id == user_id) & (Redirect.created_at >= last_week_date)).all()
        data = {}
        dates = [redirect.created_at.date() for redirect in redirects]
        count = 7

        while count >= 1:
            dt = start + timedelta(days=count)
            day = dt.strftime('%a')
            data[day] = dates.count(dt)
            count = count - 1

        return data

    def totals(self, user_id):
        total_groups = Group.query.filter((Group.user_id == user_id)).count()
        total_urls = Url.query.filter((Url.user_id == user_id)).count()
        total_redirects = Redirect.query.filter((Redirect.user_id == user_id)).count()

        return {'groups':total_groups, 'urls':total_urls, 'redirects':total_redirects}
