"""Package for sync redmine projects"""

import sys
from redminelib import Redmine


SRC_URL = 'http://redmine.expobee.com'
SRC_KEY = '0ac8f69047ca241cfd2e562b13de7c2abe0b7d84'
SRC_PROJECT = 'industry'
SRC_USERNAME = ''
SRC_PASSWORD = ''

DST_URL = 'https://redmine.mifprojects.com'
DST_KEY = 'e31bc16e4864419566bbbd8e688a4c53be44d38f'
DST_PROJECT = 'industry'
DST_USERNAME = ''
DST_PASSWORD = ''


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
    
    def _get_issues(self, redmine):
        """Get project issues"""
        user = redmine.user.get('current')
        return redmine.issue.filter(
            project_id=SRC_PROJECT,
            assigned_to_id=user.id,
            # created_on='><%s|%s' % (self.date_start, self.date_end,),
            created_on=self.date_start
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
        return self._get_issues(self.src)
    
    @property
    def dst_issues(self):
        """Get source project issues"""
        return self._get_issues(self.dst)

    # def sync_issues(self, date_start, date_end)


if __name__ == '__main__':
    print sys.argv
    if not len(sys.argv) > 2:
        sys.exit()
    s = Syncer(sys.argv[1], sys.argv[2])
    for i in s.src_issues:
        print i
    for i in s.dst_issues:
        print i.created_on
    sys.exit()
