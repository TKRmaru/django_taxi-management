from django import forms
from .models import CarInformation, CustomerInformation, PlaceInformation, SalesRecord
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.forms.widgets import SelectDateWidget
from datetime import date, datetime
from django.contrib.auth.models import User

class CarCreateForm(forms.ModelForm):
    class Meta:
        model = CarInformation
        fields = ('car_number', 'car_type', 'car_mileage', 'remarks')
        widgets = {
            'car_number': forms.TextInput(
                attrs={'placeholder': '例：1111', }, ),
        }


class CarSearchForm(forms.Form):
    car_number = forms.CharField(label='ナンバー', required=False)
    car_type = forms.CharField(label='車種', required=False)
    car_mileage_begin = forms.IntegerField(label='総走行距離下限', min_value=0, required=False)
    car_mileage_end = forms.IntegerField(label='総走行距離上限', min_value=0, required=False)
    remarks = forms.CharField(label='備考', required=False)


class CustomerCreateForm(forms.ModelForm):
    birthday = forms.DateField(
        label="生年月日",
        widget=SelectDateWidget(
            empty_label=("年", "月", "日"),
            years=range(date.today().year - 100, date.today().year),
        ),
        initial='',
        required=False,
    )

    class Meta:
        model = CustomerInformation
        fields = ('customer_name', 'birthday', 'zip_code', 'prefecture', 'city', 'bldg', 'tel', 'remarks')
        widgets = {
            'zip_code': forms.TextInput(
                attrs={'class': 'p-postal-code', 'placeholder': '例：1001000', }, ),
            'prefecture': forms.TextInput(
                attrs={'class': 'p-region', 'placeholder': '例：東京都'}, ),
            'city': forms.TextInput(
                attrs={'class': 'p-locality p-street-address p-extended-address',
                       'placeholder': '例：千代田区霞ヶ関1-1-1'}, ),
            'bldg': forms.TextInput(
                attrs={'class': '', 'placeholder': '例：千代田ビル101'}, ),
        }


class CustomerSearchForm(forms.Form):
    customer_name = forms.CharField(label='名前', required=False)
    address = forms.CharField(label='住所', required=False,
                              widget=forms.TextInput(attrs={'placeholder': '例：東京都　新宿区'}))


class PlaceCreateForm(forms.ModelForm):
    class Meta:
        model = PlaceInformation
        fields = ('place_name', 'zip_code', 'prefecture', 'city', 'bldg', 'tel', 'remarks')
        widgets = {
            'zip_code': forms.TextInput(
                attrs={'class': 'p-postal-code', 'placeholder': '例：1001000', }, ),
            'prefecture': forms.TextInput(
                attrs={'class': 'p-region', 'placeholder': '例：東京都'}, ),
            'city': forms.TextInput(
                attrs={'class': 'p-locality p-street-address p-extended-address',
                       'placeholder': '例：千代田区霞ヶ関1-1-1'}, ),
            'bldg': forms.TextInput(
                attrs={'class': '', 'placeholder': '例：千代田ビル101'}, ),
        }


class PlaceSearchForm(forms.Form):
    place_name = forms.CharField(label='施設名', required=False)
    address = forms.CharField(label='住所', required=False,
                              widget=forms.TextInput(attrs={'placeholder': '例：東京都　新宿区'}))


class DataInputForm(forms.ModelForm):
    date = forms.DateField(
        label="日付",
        widget=DatePickerInput(
            format='%Y-%m-%d',
            options={
                'locale': 'ja',
                'dayViewHeaderFormat': 'YYYY年 MMMM',
            }
        )
    )
    car = forms.ModelChoiceField(
        label="搬送車",
        queryset=CarInformation.objects.all()
    )
    start_time = forms.TimeField(
        label="出発時刻",
        widget=forms.TimeInput(attrs={"type": "time"})
    )
    arrival_time = forms.TimeField(
        label="到着時刻",
        widget=forms.TimeInput(attrs={"type": "time"})
    )
    mileage_from = forms.IntegerField(
        label="MTR(前)",
    )
    mileage_to = forms.IntegerField(
        label="MTR(後)",
    )

    class Meta:
        model = SalesRecord
        fields = ('date', 'car', 'ride_type', 'customer_name', 'place_from', 'place_to', 'start_time', 'arrival_time',
                  'mileage_from', 'mileage_to', 'fare', 'at_stretcher', 'at_night', 'remarks')


class DataUpdateForm(DataInputForm):
    class Meta:
        model = SalesRecord
        fields = ('date', 'car', 'ride_type', 'customer_name', 'place_from', 'place_to', 'start_time', 'arrival_time',
                  'mileage_from', 'mileage_to', 'fare', 'at_stretcher', 'at_night', 'remarks')


class DataSearchForm(forms.Form):
    date_begin = forms.DateField(
        label='日付下限',
        widget=SelectDateWidget(
            empty_label=("年", "月", "日"),
            years=range(date.today().year - 5, date.today().year + 1),
        ),
        initial='',
        required=False,
    )
    date_end = forms.DateField(
        label='日付上限',
        widget=SelectDateWidget(
            empty_label=("年", "月", "日"),
            years=range(date.today().year - 5, date.today().year + 1),
        ),
        initial={'date_end_year': date.today().year,
                 'date_end_month': date.today().month,
                 'date_end_day': date.today().day},
        required=False,
    )
    start_time = forms.TimeField(label='出発時刻', required=False)
    arrival_time = forms.TimeField(label='到着時刻', required=False)
    car = forms.ModelChoiceField(queryset=CarInformation.objects, label='搬送車', required=False)
    ride_type = forms.CharField(label='乗車タイプ', required=False, widget=forms.Select(
        choices=[('', '--------'), ('迎車', '迎車'), ('賃走', '賃走'), ('回送', '回送')]))
    customer_name = forms.CharField(label='顧客名', required=False)
    place_from = forms.ModelChoiceField(queryset=PlaceInformation.objects, label='出発地', required=False)
    place_to = forms.ModelChoiceField(queryset=PlaceInformation.objects, label='目的地', required=False)
    at_stretcher = forms.CharField(label='STR', required=False, widget=forms.Select(
        choices=[('', '--------'), ('True', 'あり'), ('False', 'なし')]))
    distance_begin = forms.IntegerField(label='走行距離下限', min_value=0, required=False)
    distance_end = forms.IntegerField(label='走行距離上限', min_value=0, required=False)
    at_night = forms.CharField(label='深夜割増', required=False, widget=forms.Select(
        choices=[('', '--------'), ('True', 'あり'), ('False', 'なし')]))
    added_by = forms.ModelChoiceField(queryset=User.objects, label='登録者', required=False)
    revised_by = forms.ModelChoiceField(queryset=User.objects, label='更新者', required=False)



class DataSummaryForm(forms.Form):
    MONTH_CHOICES = [(i, datetime.strptime(str(i), "%m").strftime("%m")) for i in range(1, 13)]
    year = forms.IntegerField(label='年', min_value=2000, max_value=2099, initial=date.today().year)
    month = forms.ChoiceField(label='月', choices=MONTH_CHOICES, initial='')
    car = forms.ModelChoiceField(queryset=CarInformation.objects, label='搬送車', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CSVUploadForm(forms.Form):
    file = forms.FileField(label='CSVファイル', help_text='※拡張子csvのファイルをアップロードしてください。')
