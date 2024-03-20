from django.core.management.base import BaseCommand

from myapp.models import ReturnGoods


class Command(BaseCommand):
    help = "Close orders which weren't closed manually"

    def handle(self, *args, **options):
        print("Command work")
        ReturnGoods.objects.all().delete()
        # if return_goods:
        #     self.stdout.write(self.style.SUCCESS('Successfully closed orders'))