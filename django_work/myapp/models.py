from django.db import models
from django.core.validators import MaxValueValidator, RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User

class CarInformation(models.Model):
    car_number = models.CharField('ナンバー', max_length=4)
    car_type = models.CharField('車種', max_length=100, blank=True, null=True)
    car_mileage = models.PositiveIntegerField('総走行距離', validators=[MaxValueValidator(1000000000)])
    remarks = models.TextField('備考', blank=True, null=True, max_length=1000)

    def __str__(self):
        return self.car_number


class CustomerInformation(models.Model):
    customer_name = models.CharField('名前', max_length=100)
    birthday = models.DateTimeField('生年月日', blank=True, null=True, default=None)
    zip_code = models.CharField('郵便番号', max_length=8, blank=True, null=True)
    prefecture = models.CharField('都道府県', max_length=40, blank=True, null=True)
    city = models.CharField('市区町村番地', max_length=50, blank=True, null=True)
    bldg = models.CharField('建物名', max_length=50, blank=True, null=True)
    tel = models.CharField('電話番号', blank=True, null=True, max_length=100, validators=[
        RegexValidator(
            regex=r'^\d{2,4}-\d{2,4}-\d{4}$',
            message='電話番号はハイフン区切りの数字で入力してください。',
        ),
    ])
    remarks = models.TextField('備考', blank=True, null=True, max_length=1000)

    def __str__(self):
        return self.customer_name


class PlaceInformation(models.Model):
    place_name = models.CharField('施設名', max_length=100)
    zip_code = models.CharField('郵便番号', max_length=8, blank=True, null=True)
    prefecture = models.CharField('都道府県', max_length=40, blank=True, null=True)
    city = models.CharField('市区町村番地', max_length=50, blank=True, null=True)
    bldg = models.CharField('建物名', max_length=50, blank=True, null=True)
    tel = models.CharField('電話番号', blank=True, null=True, max_length=100, validators=[
        RegexValidator(
            regex=r'^\d{2,4}-\d{2,4}-\d{4}$',
            message='電話番号はハイフン区切りの数字で入力してください。',
        ),
    ])
    remarks = models.TextField('備考', blank=True, null=True, max_length=1000)

    def __str__(self):
        return self.place_name

    @property
    def address(self):
        return self.zip_code + self.prefecture + self.city + self.bldg


class SalesRecord(models.Model):
    CHOICES = [
        ('迎車', '迎車'),
        ('賃走', '賃走'),
        ('回送', '回送'),
    ]
    date = models.DateField('日付', blank=False, null=False, default=timezone.now)
    car = models.ForeignKey(CarInformation, on_delete=models.CASCADE, verbose_name=("搬送車"),
                            related_name='car_records')
    ride_type = models.CharField('乗車タイプ', max_length=10, choices=CHOICES)
    customer_name = models.ForeignKey(CustomerInformation, on_delete=models.CASCADE, verbose_name=("顧客名"), null=True,
                                      blank=True)
    place_from = models.ForeignKey(PlaceInformation, on_delete=models.CASCADE, verbose_name=("出発地"),
                                   related_name='PlaceFrom')
    place_to = models.ForeignKey(PlaceInformation, on_delete=models.CASCADE, verbose_name=("到着地"),
                                 related_name='PlaceTo')
    start_time = models.TimeField('出発時刻', blank=True, null=True, default=timezone.now)
    arrival_time = models.TimeField('到着時刻', blank=True, null=True, default=timezone.now)
    mileage_from = models.PositiveIntegerField('MTR(前)', validators=[MaxValueValidator(1000000000)])
    mileage_to = models.PositiveIntegerField('MTR(後)', validators=[MaxValueValidator(1000000000)])
    distance = models.PositiveIntegerField('走行距離', validators=[MaxValueValidator(1000000000)], blank=True,
                                           null=True)
    fare = models.PositiveIntegerField('料金', validators=[MaxValueValidator(1000000000)], blank=True, null=True)
    at_stretcher = models.BooleanField('ストレッチャー', default=False)
    at_night = models.BooleanField('深夜割増', default=False)
    remarks = models.TextField('備考', blank=True, null=True, max_length=1000)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="登録者", null=True, blank=True, related_name="added_by")
    revised_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="更新者", null=True, blank=True, related_name="revised_by")

    def __str__(self):
        return str(self.date)

    def save(self, *args, **kwargs):
        if not self.mileage_from:
            self.mileage_from = int(self.car.car_mileage)
        self.distance = int(self.mileage_to) - int(self.mileage_from)

        super().save(*args, **kwargs)

        latest_mileage = SalesRecord.objects.filter(car=self.car).order_by('-mileage_to').first()
        if latest_mileage:
            self.car.car_mileage = latest_mileage.mileage_to
        else:
            self.car.car_mileage = self.mileage_to
        self.car.save()

    def delete(self, *args, **kwargs):
        # 削除されるデータのmileage_toの値を取得
        deleted_mileage_to = self.mileage_to

        super().delete(*args, **kwargs)

        latest_mileage = SalesRecord.objects.filter(car=self.car).order_by('-mileage_to').first()
        if latest_mileage:
            self.car.car_mileage = latest_mileage.mileage_to
        else:
            self.car.car_mileage = deleted_mileage_to  # 削除されるデータのmileage_toの値を使用
        self.car.save()

