# Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
# License: GPLv2 or later, see LICENSE for more details.

'''
'''

from logging import getLogger

from django.core.management.base import BaseCommand

from sxconsole.accounts.models import Admin


logger = getLogger(__name__)


class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **kwargs):
        from django.conf import settings
        if not settings.DEMO:
            return

        admin, created = Admin.objects.update_or_create(
            email=settings.DEMO_USER,
            defaults={
                'level': Admin.LEVELS.ROOT_ADMIN,
            })
        if created:
            logger.info('Demo user {} has been created'.format(admin.email))

        if not admin.check_password(settings.DEMO_PASS):
            admin.set_password(settings.DEMO_PASS)
            admin.save()
