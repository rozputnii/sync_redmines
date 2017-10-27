"""Package for sync redmine projects"""

import sys
import settings as s
from redminelib import Redmine


class Syncer(object):
    """Sync redmine projects by dates"""

    def __init__(self, date_start, date_end):
        self.date_start = date_start.strip()
        self.date_end = date_end.strip()
        self.src = self._get_r(s.SRC_URL, s.SRC_KEY, s.SRC_USERNAME, s.SRC_PASSWORD)
        self.dst = self._get_r(s.DST_URL, s.DST_KEY, s.DST_USERNAME, s.DST_PASSWORD)

    @staticmethod
    def _get_r(url, key, username, password):
        return Redmine(url, key=key) if key else Redmine(url, username=username, password=password)

    def _get_issues(self, redmine, project_id):
        """Get project issues"""
        user = redmine.user.get('current')
        return redmine.issue.filter(
            project_id=project_id,
            assigned_to_id=user.id,
            # created_on='><%s|%s' % (self.date_start, self.date_end,),
            created_on=self.date_start
        )

    def _get_time_entries(self, redmine, project, user):
        """Get project issues"""
        return redmine.time_entry.filter(
            project_id=project.id,
            user_id=user.id,
            from_date=self.date_start,
            to_date=self.date_end
        )

    @property
    def src_project(self):
        """Source project"""
        return self.src.project.get(s.SRC_PROJECT)

    @property
    def dst_project(self):
        """Destination project"""
        return self.src.project.get(s.DST_PROJECT)

    def sync_time_entries(self):
        """Sync time entries"""
        dst_entries = [(te.spent_on, te.hours, te.comments.strip(), te.activity.id)
                       for te in self._get_time_entries(self.dst, self.dst_project, self.dst.user.get('current'))]
        src_entries = [(te.spent_on, te.hours, te.comments.strip(), te.activity.id)
                       for te in self._get_time_entries(self.src, self.src_project, self.src.user.get('current'))]

        dst_project_id = self.dst_project.id

        for te in src_entries:
            if te in dst_entries:
                print('NO %s %s' % (te[0], te[2]))
                continue
            
            new_te = self.dst.time_entry.create(project_id=dst_project_id,
                                                spent_on=te[0],
                                                hours=te[1],
                                                comments=te[2],
                                                activity_id=te[3])
            print('OK %s %s' % (new_te.spent_on, new_te.comments))


if __name__ == '__main__':
    # Fix Python 2.x.
    try:
        input = raw_input
    except NameError:
        pass
    syncer = Syncer(input('From date: '), input('To date: '))
    syncer.sync_time_entries()
    sys.exit()
