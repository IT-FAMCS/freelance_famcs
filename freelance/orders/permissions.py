from rest_framework.permissions import BasePermission
import sqlite3 as sql

def get_freelancer(request):
    connect = sql.connect('.base/db.sqlite')
    cursor = connect.cursor()
    if cursor.execute('SELECT * FROM users.freelancer WHERE user = ?', (request.user,)).fetchone() is not None:
        True
    else:
        False
    


class FreelacerPermission(BasePermission):
    def has_permission(request):
        return get_freelancer(request)