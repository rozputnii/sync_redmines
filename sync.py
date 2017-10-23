"""Package for sync redmine projects"""

import sys

from redminelib import Redmine

from settings import *


class Syncer(object):
    """Sync redmine projects by dates"""

    def __init__(self, date_start, date_end):
        self.date_start = date_start.strip()
        self.date_end = date_end.strip()
        self.src = self._get_r(SRC_URL, SRC_KEY, SRC_USERNAME, SRC_PASSWORD)
        self.dst = self._get_r(DST_URL, DST_KEY, DST_USERNAME, DST_PASSWORD)

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

    def _get_time_entries(self, redmine, project):
        """Get project issues"""
        user = redmine.user.get('current')
        return redmine.time_entry.filter(
            project_id=project.id,
            user_id=user.id,
            from_date=self.date_start,
            to_date=self.date_end
        )

    @property
    def src_project(self):
        """Get source project"""
        return self.src.project.get(SRC_PROJECT)

    @property
    def dst_project(self):
        """Get destination project"""
        return self.src.project.get(DST_PROJECT)

    @property
    def src_issues(self):
        """Get source project issues"""
        return self._get_issues(self.src, SRC_PROJECT)

    @property
    def dst_issues(self):
        """Get source project issues"""
        return self._get_issues(self.dst, DST_PROJECT)

    @property
    def src_time_entries(self):
        return self._get_time_entries(self.src, self.src_project)

    @property
    def dst_time_entries(self):
        return self._get_time_entries(self.dst, self.dst_project)

    def sync_time_entries(self):
        dst_entries = tuple((te.spent_on, te.hours, te.comments.strip()) for te in self.dst_time_entries)
        dst_project_id = self.dst_project.id

        for te in self.src_time_entries:
            if (te.spent_on, te.hours, te.comments.strip()) in dst_entries:
                print('exists', te.spent_on, te.comments)
                continue

            new_dst_te = self.dst.time_entry.create(project_id=dst_project_id,
                                                    spent_on=te.spent_on,
                                                    hours=te.hours,
                                                    comments=te.comments.strip())
            print('ok', new_dst_te.spent_on, new_dst_te.comments)


if __name__ == '__main__':
    if not len(sys.argv) > 2:
        print('Please enter dates range. (e.g.: 2017-10-20 2017-10-30)')
        sys.exit()
    s = Syncer(sys.argv[1], sys.argv[2])
    s.sync_time_entries()
    sys.exit()
