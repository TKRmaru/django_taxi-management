from django.views.generic.base import TemplateView
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView, DeleteView, View
from .models import CarInformation, CustomerInformation, PlaceInformation, SalesRecord
from .forms import CarCreateForm, CarSearchForm, CustomerCreateForm, CustomerSearchForm, PlaceCreateForm, \
    PlaceSearchForm, DataInputForm, DataUpdateForm, DataSearchForm, DataSummaryForm, CSVUploadForm
from django.db.models import Q, Sum, Avg, Count, IntegerField
from datetime import datetime, timedelta, date
from django.utils import timezone
import csv, codecs
from django.http import HttpResponse
from django.db.models.functions import Cast
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
import re
from django.http import JsonResponse


class Home(TemplateView):
    template_name = 'myapp/home.html'


class CarCreateView(CreateView):
    model = CarInformation
    form_class = CarCreateForm
    template_name = 'myapp/car_create.html'
    success_url = '/car_list'


class CarListView(ListView):
    model = CarInformation
    form_class = CarSearchForm
    template_name = 'myapp/car_list.html'
    context_object_name = "car_list"
    paginate_by = 10

    def get(self, request, *args, **kwargs):  # 検索条件をセッションに保存
        q_car_number = self.request.GET.get('car_number')
        q_car_type = self.request.GET.get('car_type')
        q_car_mileage_begin = self.request.GET.get('car_mileage_begin')
        q_car_mileage_end = self.request.GET.get('car_mileage_end')
        q_remarks = self.request.GET.get('remarks')
        request.session['q_car_number'] = q_car_number
        request.session['q_car_type'] = q_car_type
        request.session['q_car_mileage_begin'] = q_car_mileage_begin
        request.session['q_car_mileage_end'] = q_car_mileage_end
        request.session['q_remarks'] = q_remarks

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)
        context.update(dict(form=self.form_class(), query_string=self.request.GET.urlencode()))

        q_car_number = self.request.GET.get('car_number')
        q_car_type = self.request.GET.get('car_type')
        q_car_mileage_begin = self.request.GET.get('car_mileage_begin')
        q_car_mileage_end = self.request.GET.get('car_mileage_end')
        q_remarks = self.request.GET.get('remarks')

        context['form'] = CarSearchForm(initial={
            'car_number': q_car_number, 'car_type': q_car_type, 'car_mileage_begin': q_car_mileage_begin,
            'car_mileage_end': q_car_mileage_end, 'remarks': q_remarks})
        return context

    def get_queryset(self):
        q_car_number = self.request.GET.get('car_number')
        q_car_type = self.request.GET.get('car_type')
        q_car_mileage_begin = self.request.GET.get('car_mileage_begin')
        q_car_mileage_end = self.request.GET.get('car_mileage_end')
        q_remarks = self.request.GET.get('remarks')

        carinformation = CarInformation.objects.all()

        if q_car_number:
            carinformation = carinformation.filter(car_number__icontains=q_car_number)
        if q_car_type:
            carinformation = carinformation.filter(car_type__icontains=q_car_type)
        if q_car_mileage_begin:
            carinformation = carinformation.filter(car_mileage_begin__gte=q_car_mileage_begin)
        if q_car_mileage_end:
            carinformation = carinformation.filter(car_mileage_end__lte=q_car_mileage_end)
        if q_remarks:
            carinformation = carinformation.filter(remarks__icontains=q_remarks)

        return carinformation.order_by("id")


class CarCSVExportView(View):
    def get(self, request, *args, **kwargs):  # セッションから検索条件を取得
        q_car_number = request.session.get('q_car_number')
        q_car_type = request.session.get('q_car_type')
        q_car_mileage_begin = request.session.get('q_car_mileage_begin')
        q_car_mileage_end = request.session.get('q_car_mileage_end')
        q_remarks = request.session.get('q_remarks')

        carinformation = CarInformation.objects.all()

        if q_car_number:
            carinformation = carinformation.filter(car_number__icontains=q_car_number)
        if q_car_type:
            carinformation = carinformation.filter(car_type__icontains=q_car_type)
        if q_car_mileage_begin:
            carinformation = carinformation.filter(car_mileage_begin__gte=q_car_mileage_begin)
        if q_car_mileage_end:
            carinformation = carinformation.filter(car_mileage_end__lte=q_car_mileage_end)
        if q_remarks:
            carinformation = carinformation.filter(remarks__icontains=q_remarks)
        # セッションの検索条件を削除
        del request.session['q_car_number']
        del request.session['q_car_type']
        del request.session['q_car_mileage_begin']
        del request.session['q_car_mileage_end']
        del request.session['q_remarks']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="car_list.csv"'
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)
        writer.writerow(
            ['ID', 'ナンバー', '車種', '総走行距離', '備考'])

        for car in carinformation:
            writer.writerow([
                car.id,
                car.car_number,
                car.car_type,
                car.car_mileage,
                car.remarks,
            ])
        return response


class CarUpdateView(UpdateView):
    model = CarInformation
    form_class = CarCreateForm
    template_name = 'myapp/car_update.html'
    success_url = '/car_list'


class CarDeleteView(DeleteView):
    model = CarInformation
    template_name = 'myapp/delete.html'
    success_url = '/car_list'


class CustomerCreateView(CreateView):
    model = CustomerInformation
    form_class = CustomerCreateForm
    template_name = 'myapp/customer_create.html'
    success_url = '/customer_list'


class CustomerListView(ListView):
    model = CustomerInformation
    form_class = CustomerSearchForm
    template_name = 'myapp/customer_list.html'
    context_object_name = "customer_list"
    paginate_by = 20

    def get(self, request, *args, **kwargs):  # 検索条件をセッションに保存
        q_customer_name = self.request.GET.get('customer_name')
        q_address = self.request.GET.get('address')
        request.session['q_customer_name'] = q_customer_name
        request.session['q_address'] = q_address

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CustomerListView, self).get_context_data(**kwargs)
        context.update(dict(form=self.form_class(), query_string=self.request.GET.urlencode()))

        q_customer_name = self.request.GET.get('customer_name')
        q_address = self.request.GET.get('address')

        context['form'] = CustomerSearchForm(initial={
            'customer_name': q_customer_name, 'address': q_address})

        return context

    def get_queryset(self):
        q_customer_name = self.request.GET.get('customer_name')
        q_address = self.request.GET.get('address')

        customerinformation = CustomerInformation.objects.all()

        if q_customer_name:
            customerinformation = customerinformation.filter(customer_name__icontains=q_customer_name)
        if q_address:
            words = q_address.split()
            for word in words:
                customerinformation = customerinformation.filter(
                    Q(zip_code__icontains=word) |
                    Q(prefecture__icontains=word) |
                    Q(city__icontains=word) |
                    Q(bldg__icontains=word)
                )
        return customerinformation.order_by('id')


class CustomerCSVExportView(View):
    def get(self, request, *args, **kwargs):  # セッションから検索条件を取得
        q_customer_name = request.session.get('q_customer_name')
        q_address = request.session.get('q_address')

        customerinformation = CustomerInformation.objects.all()

        if q_customer_name:
            customerinformation = customerinformation.filter(customer_name__icontains=q_customer_name)
        if q_address:
            words = q_address.split()
            for word in words:
                customerinformation = customerinformation.filter(
                    Q(zip_code__icontains=word) |
                    Q(prefecture__icontains=word) |
                    Q(city__icontains=word) |
                    Q(bldg__icontains=word)
                )
        # セッションの検索条件を削除
        del request.session['q_customer_name']
        del request.session['q_address']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customer_list.csv"'
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)
        writer.writerow(
            ['ID', '名前', '生年月日', '郵便番号', '都道府県', '市区町村番地', '建物名', '電話番号', '備考'])

        for customer in customerinformation:
            writer.writerow([
                customer.id,
                customer.customer_name,
                customer.birthday.strftime('%Y-%m-%d') if customer.birthday else '',
                customer.zip_code,
                customer.prefecture,
                customer.city,
                customer.bldg,
                customer.tel,
                customer.remarks,
            ])
        return response


class CustomerUpdateView(UpdateView):
    model = CustomerInformation
    form_class = CustomerCreateForm
    template_name = 'myapp/customer_update.html'
    success_url = '/customer_list'


class CustomerDetailView(DetailView):
    model = CustomerInformation
    template_name = 'myapp/customer_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        data_input_count = SalesRecord.objects.filter(customer_name=customer).count()

        context['data_input_count'] = data_input_count
        return context


class CustomerDeleteView(DeleteView):
    model = CustomerInformation
    template_name = 'myapp/delete.html'
    success_url = '/customer_list'


class PlaceCreateView(CreateView):
    model = PlaceInformation
    form_class = PlaceCreateForm
    template_name = 'myapp/place_create.html'
    success_url = '/place_list'


class PlaceListView(ListView):
    model = PlaceInformation
    form_class = PlaceSearchForm
    template_name = 'myapp/place_list.html'
    context_object_name = "place_list"
    paginate_by = 10

    def get(self, request, *args, **kwargs):  # 検索条件をセッションに保存
        q_place_name = self.request.GET.get('place_name')
        q_address = self.request.GET.get('address')
        request.session['q_place_name'] = q_place_name
        request.session['q_address'] = q_address

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlaceListView, self).get_context_data(**kwargs)
        context.update(dict(form=self.form_class(), query_string=self.request.GET.urlencode()))

        q_place_name = self.request.GET.get('place_name')
        q_address = self.request.GET.get('address')

        context['form'] = PlaceSearchForm(initial={
            'place_name': q_place_name, 'address': q_address})
        return context

    def get_queryset(self):
        q_place_name = self.request.GET.get('place_name')
        q_address = self.request.GET.get('address')

        placeinformation = PlaceInformation.objects.all()

        if q_place_name:
            placeinformation = placeinformation.filter(place_name__icontains=q_place_name)
        if q_address:
            words = q_address.split()
            for word in words:
                placeinformation = placeinformation.filter(
                    Q(zip_code__icontains=word) |
                    Q(prefecture__icontains=word) |
                    Q(city__icontains=word) |
                    Q(bldg__icontains=word)
                )
        return placeinformation.order_by("place_name")


class PlaceCSVExportView(View):
    def get(self, request, *args, **kwargs):  # セッションから検索条件を取得
        q_place_name = request.session.get('q_place_name')
        q_address = request.session.get('q_address')

        placeinformation = PlaceInformation.objects.all()

        if q_place_name:
            placeinformation = placeinformation.filter(place_name__icontains=q_place_name)
        if q_address:
            words = q_address.split()
            for word in words:
                placeinformation = placeinformation.filter(
                    Q(zip_code__icontains=word) |
                    Q(prefecture__icontains=word) |
                    Q(city__icontains=word) |
                    Q(bldg__icontains=word)
                )
        # セッションの検索条件を削除
        del request.session['q_place_name']
        del request.session['q_address']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="place_list.csv"'
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)
        writer.writerow(
            ['ID', '施設名', '郵便番号', '都道府県', '市区町村番地', '建物名', '電話番号', '備考'])

        for place in placeinformation:
            writer.writerow([
                place.id,
                place.place_name,
                place.zip_code,
                place.prefecture,
                place.city,
                place.bldg,
                place.tel,
                place.remarks,
            ])
        return response


class PlaceUpdateView(UpdateView):
    model = PlaceInformation
    form_class = PlaceCreateForm
    template_name = 'myapp/place_update.html'
    success_url = '/place_list'


class PlaceDetailView(DetailView):
    model = PlaceInformation
    form_class = PlaceCreateForm
    template_name = 'myapp/place_detail.html'


class PlaceDeleteView(DeleteView):
    model = PlaceInformation
    template_name = 'myapp/delete.html'
    success_url = '/place_list'


class DataInputView(LoginRequiredMixin, CreateView):
    model = SalesRecord
    form_class = DataInputForm
    template_name = 'myapp/data_input.html'
    success_url = '/data_input'

    def form_valid(self, form):
        # フォームのバリデーションに成功した場合の処理
        user = self.request.user  # ログインユーザーを取得
        sales_record = form.save(commit=False)  # SalesRecord オブジェクトを作成
        sales_record.added_by = user  # ユーザー情報を設定
        sales_record.save()  # オブジェクトを保存

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            error_message1 = '基本データが見つかりませんでした。'
            error_message2 = '搬送車または施設情報を登録してください。'
            return render(request, 'myapp/error_template.html', {'error_message1': error_message1, 'error_message2': error_message2})


def get_car_mileage(request, car_id):
    try:
        car = CarInformation.objects.get(id=car_id)
        car_mileage = car.car_mileage
        return JsonResponse({'car_mileage': car_mileage})
    except CarInformation.DoesNotExist:
        return JsonResponse({'error': 'Car not found'}, status=404)


class DataListView(ListView):
    model = SalesRecord
    form_class = DataSearchForm
    template_name = 'myapp/data_list.html'
    context_object_name = "salesrecord_list"
    paginate_by = 30

    def get(self, request, *args, **kwargs):  # 検索条件をセッションに保存
        q_date_begin_year = self.request.GET.get('date_begin_year')
        q_date_begin_month = self.request.GET.get('date_begin_month')
        q_date_begin_day = self.request.GET.get('date_begin_day')
        q_date_end_year = self.request.GET.get('date_end_year')
        q_date_end_month = self.request.GET.get('date_end_month')
        q_date_end_day = self.request.GET.get('date_end_day')
        q_car = self.request.GET.get('car')
        q_ride_type = self.request.GET.get('ride_type')
        q_customer_name = self.request.GET.get('customer_name')
        q_place_from = self.request.GET.get('place_from')
        q_place_to = self.request.GET.get('place_to')
        q_distance_begin = self.request.GET.get('distance_begin')
        q_distance_end = self.request.GET.get('distance_end')
        q_at_stretcher = self.request.GET.get('at_stretcher')
        q_at_night = self.request.GET.get('at_night')
        q_added_by = self.request.GET.get('added_by')
        q_revised_by = self.request.GET.get('revised_by')

        request.session['q_date_begin_year'] = q_date_begin_year
        request.session['q_date_begin_month'] = q_date_begin_month
        request.session['q_date_begin_day'] = q_date_begin_day
        request.session['q_date_end_year'] = q_date_end_year
        request.session['q_date_end_month'] = q_date_end_month
        request.session['q_date_end_day'] = q_date_end_day
        request.session['q_car'] = q_car
        request.session['q_ride_type'] = q_ride_type
        request.session['q_customer_name'] = q_customer_name
        request.session['q_place_from'] = q_place_from
        request.session['q_place_to'] = q_place_to
        request.session['q_distance_begin'] = q_distance_begin
        request.session['q_distance_end'] = q_distance_end
        request.session['q_at_stretcher'] = q_at_stretcher
        request.session['q_at_night'] = q_at_night
        request.session['q_added_by'] = q_added_by
        request.session['q_revised_by'] = q_revised_by

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DataListView, self).get_context_data(**kwargs)
        context.update(dict(form=self.form_class(), query_string=self.request.GET.urlencode()))
        salesrecord = self.get_queryset()
        total_dis = salesrecord.aggregate(total_dis=Sum('distance'))['total_dis']
        context['total_dis'] = format(total_dis, ',') if total_dis is not None else 'N/A'
        total_fare = salesrecord.aggregate(total_fare=Sum('fare'))['total_fare']
        context['total_fare'] = format(total_fare, ',') if total_fare is not None else 'N/A'
        av_dis = salesrecord.aggregate(av_dis=Avg('distance'))['av_dis']
        context['av_dis'] = int(av_dis) if av_dis is not None else 'N/A'
        av_fare = salesrecord.aggregate(av_fare=Avg('fare'))['av_fare']
        context['av_fare'] = int(av_fare) if av_fare is not None else 'N/A'

        q_date_begin_year = self.request.GET.get('date_begin_year')
        q_date_begin_month = self.request.GET.get('date_begin_month')
        q_date_begin_day = self.request.GET.get('date_begin_day')
        q_date_end_year = self.request.GET.get('date_end_year', date.today().year)
        q_date_end_month = self.request.GET.get('date_end_month', date.today().month)
        q_date_end_day = self.request.GET.get('date_end_day', date.today().day)
        q_car = self.request.GET.get('car')
        q_ride_type = self.request.GET.get('ride_type')
        q_customer_name = self.request.GET.get('customer_name')
        q_place_from = self.request.GET.get('place_from')
        q_place_to = self.request.GET.get('place_to')
        q_distance_begin = self.request.GET.get('distance_begin')
        q_distance_end = self.request.GET.get('distance_end')
        q_at_stretcher = self.request.GET.get('at_stretcher')
        q_at_night = self.request.GET.get('at_night')
        q_added_by = self.request.GET.get('added_by')
        q_revised_by = self.request.GET.get('revised_by')


        context['form'] = DataSearchForm(initial={
            'date_begin_year': q_date_begin_year, 'date_begin_month': q_date_begin_month,
            'date_begin_day': q_date_begin_day,
            'date_end_year': q_date_end_year, 'date_end_month': q_date_end_month, 'date_end_day': q_date_end_day,
            'car': q_car, 'ride_type': q_ride_type, 'customer_name': q_customer_name, 'place_from': q_place_from,
            'place_to': q_place_to,
            'distance_begin': q_distance_begin, 'distance_end': q_distance_end, 'at_stretcher': q_at_stretcher,
            'at_night': q_at_night, 'added_by': q_added_by, 'revised_by': q_revised_by})
        return context

    def get_queryset(self):
        q_date_begin_year = self.request.GET.get('date_begin_year')
        q_date_begin_month = self.request.GET.get('date_begin_month')
        q_date_begin_day = self.request.GET.get('date_begin_day')
        q_date_end_year = self.request.GET.get('date_end_year')
        q_date_end_month = self.request.GET.get('date_end_month')
        q_date_end_day = self.request.GET.get('date_end_day')
        q_car = self.request.GET.get('car')
        q_ride_type = self.request.GET.get('ride_type')
        q_customer_name = self.request.GET.get('customer_name')
        q_place_from = self.request.GET.get('place_from')
        q_place_to = self.request.GET.get('place_to')
        q_distance_begin = self.request.GET.get('distance_begin')
        q_distance_end = self.request.GET.get('distance_end')
        q_at_stretcher = self.request.GET.get('at_stretcher')
        q_at_night = self.request.GET.get('at_night')
        q_added_by = self.request.GET.get('added_by')
        q_revised_by = self.request.GET.get('revised_by')

        salesrecord = SalesRecord.objects.all()

        if q_date_begin_year and q_date_begin_month and q_date_begin_day:
            date_begin = timezone.make_aware(
                datetime.strptime(f"{q_date_begin_year}-{q_date_begin_month}-{q_date_begin_day}", '%Y-%m-%d'))
            salesrecord = salesrecord.filter(date__gte=date_begin)
        elif q_date_begin_year and q_date_begin_month:
            date_begin = timezone.make_aware(
                datetime.strptime(f"{q_date_begin_year}-{q_date_begin_month}-01", '%Y-%m-%d'))
            salesrecord = salesrecord.filter(date__gte=date_begin)
        elif q_date_begin_year:
            date_begin = timezone.make_aware(datetime.strptime(f"{q_date_begin_year}-01-01", '%Y-%m-%d'))
            salesrecord = salesrecord.filter(date__gte=date_begin)
        if q_date_end_year and q_date_end_month and q_date_end_day:
            date_end = timezone.make_aware(
                datetime.strptime(f"{q_date_end_year}-{q_date_end_month}-{q_date_end_day}", '%Y-%m-%d'))
            salesrecord = salesrecord.filter(date__lte=date_end)
        elif q_date_end_year and q_date_end_month:
            date_end = timezone.make_aware(
                datetime.strptime(f"{q_date_end_year}-{q_date_end_month}-01", '%Y-%m-%d'))
            salesrecord = salesrecord.filter(date__lte=date_end)
        elif q_date_end_year:
            date_end = timezone.make_aware(datetime.strptime(f"{q_date_end_year}-01-01", '%Y-%m-%d'))
            salesrecord = salesrecord.filter(date__lte=date_end)
        if q_car:
            salesrecord = salesrecord.filter(car=q_car)
        if q_ride_type is not None:
            if q_ride_type == '迎車':
                salesrecord = salesrecord.filter(ride_type='迎車')
            elif q_ride_type == '賃走':
                salesrecord = salesrecord.filter(ride_type='賃走')
            elif q_ride_type == '回送':
                salesrecord = salesrecord.filter(ride_type='回送')
        if q_customer_name:
            salesrecord = salesrecord.filter(customer_name__customer_name__icontains=q_customer_name)
        if q_place_from:
            salesrecord = salesrecord.filter(place_from=q_place_from)
        if q_place_to:
            salesrecord = salesrecord.filter(place_to=q_place_to)
        if q_distance_begin:
            salesrecord = salesrecord.filter(distance__gte=q_distance_begin)
        if q_distance_end:
            salesrecord = salesrecord.filter(distance__lte=q_distance_end)
        if q_at_stretcher is not None:
            if q_at_stretcher == 'True':
                salesrecord = salesrecord.filter(at_stretcher=True)
            elif q_at_stretcher == 'False':
                salesrecord = salesrecord.filter(at_stretcher=False)
        if q_at_night is not None:
            if q_at_night == 'True':
                salesrecord = salesrecord.filter(at_night=True)
            elif q_at_night == 'False':
                salesrecord = salesrecord.filter(at_night=False)
        if q_added_by:
            salesrecord = salesrecord.filter(added_by=q_added_by)
        if q_revised_by:
            salesrecord = salesrecord.filter(revised_by=q_revised_by)
        return salesrecord.order_by("-date", "car", "-mileage_to")


class DataListCSVExportView(View):
    def get(self, request, *args, **kwargs):  # セッションから検索条件を取得
        q_date_begin_year = request.session.get('q_date_begin_year')
        q_date_begin_month = request.session.get('q_date_begin_month')
        q_date_begin_day = request.session.get('q_date_begin_day')
        q_date_end_year = request.session.get('q_date_end_year')
        q_date_end_month = request.session.get('q_date_end_month')
        q_date_end_day = request.session.get('q_date_end_day')
        q_car = request.session.get('q_car')
        q_ride_type = request.session.get('q_ride_type')
        q_customer_name = request.session.get('q_customer_name')
        q_place_from = request.session.get('q_place_from')
        q_place_to = request.session.get('q_place_to')
        q_distance_begin = request.session.get('q_distance_begin')
        q_distance_end = request.session.get('q_distance_end')
        q_at_stretcher = request.session.get('q_at_stretcher')
        q_at_night = request.session.get('q_at_night')
        q_added_by = request.session.get('added_by')
        q_revised_by = request.session.get('revised_by')

        salesrecord = SalesRecord.objects.all()

        if q_date_begin_year and q_date_begin_month and q_date_begin_day:
            date_begin = timezone.make_aware(
                datetime.strptime(f"{q_date_begin_year}-{q_date_begin_month}-{q_date_begin_day}", '%Y-%m-%d'))
            salesrecord = salesrecord.filter(date__gte=date_begin)
        elif q_date_begin_year and q_date_begin_month:
            date_begin = timezone.make_aware(
                datetime.strptime(f"{q_date_begin_year}-{q_date_begin_month}-01", '%Y-%m-%d'))
            salesrecord = salesrecord.filter(date__gte=date_begin)
        elif q_date_begin_year:
            date_begin = timezone.make_aware(datetime.strptime(f"{q_date_begin_year}-01-01", '%Y-%m-%d'))
            salesrecord = salesrecord.filter(date__gte=date_begin)
        if q_date_end_year and q_date_end_month and q_date_end_day:
            date_end = timezone.make_aware(
                datetime.strptime(f"{q_date_end_year}-{q_date_end_month}-{q_date_end_day}", '%Y-%m-%d'))
            salesrecord = salesrecord.filter(date__lte=date_end)
        elif q_date_end_year and q_date_end_month:
            date_end = timezone.make_aware(
                datetime.strptime(f"{q_date_end_year}-{q_date_end_month}-01", '%Y-%m-%d'))
            salesrecord = salesrecord.filter(date__lte=date_end)
        elif q_date_end_year:
            date_end = timezone.make_aware(datetime.strptime(f"{q_date_end_year}-01-01", '%Y-%m-%d'))
            salesrecord = salesrecord.filter(date__lte=date_end)
        if q_car:
            salesrecord = salesrecord.filter(car=q_car)
        if q_ride_type is not None:
            if q_ride_type == '迎車':
                salesrecord = salesrecord.filter(ride_type='迎車')
            elif q_ride_type == '賃走':
                salesrecord = salesrecord.filter(ride_type='賃走')
            elif q_ride_type == '回送':
                salesrecord = salesrecord.filter(ride_type='回送')
        if q_customer_name:
            salesrecord = salesrecord.filter(customer_name__customer_name__icontains=q_customer_name)
        if q_place_from:
            salesrecord = salesrecord.filter(place_from=q_place_from)
        if q_place_to:
            salesrecord = salesrecord.filter(place_to=q_place_to)
        if q_distance_begin:
            salesrecord = salesrecord.filter(distance__gte=q_distance_begin)
        if q_distance_end:
            salesrecord = salesrecord.filter(distance__lte=q_distance_end)
        if q_at_stretcher is not None:
            if q_at_stretcher == 'True':
                salesrecord = salesrecord.filter(at_stretcher=True)
            elif q_at_stretcher == 'False':
                salesrecord = salesrecord.filter(at_stretcher=False)
        if q_at_night is not None:
            if q_at_night == 'True':
                salesrecord = salesrecord.filter(at_night=True)
            elif q_at_night == 'False':
                salesrecord = salesrecord.filter(at_night=False)
        if q_added_by:
            salesrecord = salesrecord.filter(added_by=q_added_by)
        if q_revised_by:
            salesrecord = salesrecord.filter(revised_by=q_revised_by)
        # セッションの検索条件を削除
        del request.session['q_date_begin_year']
        del request.session['q_date_begin_month']
        del request.session['q_date_begin_day']
        del request.session['q_date_end_year']
        del request.session['q_date_end_month']
        del request.session['q_date_end_day']
        del request.session['q_car']
        del request.session['q_ride_type']
        del request.session['q_customer_name']
        del request.session['q_place_from']
        del request.session['q_place_to']
        del request.session['q_distance_begin']
        del request.session['q_distance_end']
        del request.session['q_at_stretcher']
        del request.session['q_at_night']
        del request.session['q_added_by']
        del request.session['q_revised_by']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data_list.csv"'
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)
        writer.writerow(
            ['ID', '日付', '搬送車', '乗車タイプ', '顧客名', '出発地', '到着地', '出発時刻', '到着時刻', '運行前(km)',
             '運行後(km)', '走行距離(km)', '金額(円)', 'STR', '深夜割増', '備考', '登録者', '更新者'])

        for record in salesrecord:
            record.at_stretcher = '〇' if record.at_stretcher else '×'
            record.at_night = '〇' if record.at_night else '×'
            writer.writerow([
                record.id,
                record.date,
                int(record.car.car_number),
                record.ride_type,
                record.customer_name,
                record.place_from,
                record.place_to,
                record.start_time.strftime('%H:%M'),
                record.arrival_time.strftime('%H:%M'),
                record.mileage_from,
                record.mileage_to,
                record.distance,
                record.fare,
                record.at_stretcher,
                record.at_night,
                record.remarks,
                record.added_by,
                record.revised_by,
            ])
        return response


class DataSummaryView(ListView):
    model = SalesRecord
    form_class = DataSummaryForm
    template_name = 'myapp/data_summary.html'
    paginate_by = 31

    def get(self, request, *args, **kwargs):  # 検索条件をセッションに保存
        q_year = self.request.GET.get('q_year')
        q_month = self.request.GET.get('q_month')
        q_car = self.request.GET.get('car')
        request.session['q_year'] = q_year
        request.session['q_month'] = q_month
        request.session['q_car'] = q_car

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(form=self.form_class(), query_string=self.request.GET.urlencode()))

        q_year = self.request.GET.get('year', date.today().year)
        q_month = self.request.GET.get('month', date.today().month)
        q_car = self.request.GET.get('car')

        salesrecord = self.get_queryset()

        total_dis = salesrecord.aggregate(total_dis=Sum('distance'))['total_dis']
        context['total_dis'] = format(total_dis, ',') if total_dis is not None else 'N/A'
        total_fare = salesrecord.aggregate(total_fare=Sum('fare'))['total_fare']
        context['total_fare'] = format(total_fare, ',') if total_fare is not None else 'N/A'
        av_dis = salesrecord.aggregate(av_dis=Avg('distance'))['av_dis']
        context['av_dis'] = int(av_dis) if av_dis is not None else 'N/A'
        av_fare = salesrecord.aggregate(av_fare=Avg('fare'))['av_fare']
        context['av_fare'] = int(av_fare) if av_fare is not None else 'N/A'

        summary = salesrecord.values('date', 'car__car_number').annotate(
            count_ride_type_1=Count('ride_type', filter=Q(ride_type='迎車')),
            count_ride_type_2=Count('ride_type', filter=Q(ride_type='賃走')),
            count_ride_type_3=Count('ride_type', filter=Q(ride_type='回送')),
            daily_distance=Sum('distance'),
            daily_fare=Sum('fare'),
            count_at_stretcher=Count('at_stretcher', filter=Q(at_stretcher=True)),
            count_at_night=Count('at_night', filter=Q(at_night=True)),
            average_fare=Cast(Avg('fare'), IntegerField())
        ).order_by('date', 'car__car_number')

        context['summary'] = summary

        context['form'] = DataSummaryForm(initial={
            'year': q_year, 'month': q_month, 'car': q_car})
        return context

    def get_queryset(self):
        q_year = self.request.GET.get('year')
        q_month = self.request.GET.get('month')
        q_car = self.request.GET.get('car')

        salesrecord = SalesRecord.objects.all()

        if q_year and q_month:
            date_begin = datetime(int(q_year), int(q_month), 1)
            if q_month == 12:
                date_end = datetime(int(q_year) + 1, 1, 1) - timedelta(days=1)
            else:
                date_end = datetime(int(q_year), int(q_month) + 1, 1) - timedelta(days=1)
            salesrecord = salesrecord.filter(date__range=[date_begin, date_end])
        if q_car:
            salesrecord = salesrecord.filter(car=q_car)

        return salesrecord.order_by("date", "car")


class DataSummaryCSVExportView(View):
    def get(self, request, *args, **kwargs):  # セッションから検索条件を取得
        q_year = request.session.get('q_year')
        q_month = request.session.get('q_month')
        q_car = request.session.get('q_car')

        salesrecord = SalesRecord.objects.all()

        if q_year and q_month:
            date_begin = datetime(int(q_year), int(q_month), 1)
            if q_month == 12:
                date_end = datetime(int(q_year) + 1, 1, 1) - timedelta(days=1)
            else:
                date_end = datetime(int(q_year), int(q_month) + 1, 1) - timedelta(days=1)
            salesrecord = salesrecord.filter(date__range=[date_begin, date_end])
        if q_car:
            salesrecord = salesrecord.filter(car=q_car)
        # セッションの検索条件を削除
        del request.session['q_year']
        del request.session['q_month']
        del request.session['q_car']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data_summary.csv"'
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)
        writer.writerow(
            ['日付', '搬送車', '迎車', '賃走', '回送', '走行距離(km)', '金額(円)', 'STR', '深割', '平均金額(円)'])

        summary = salesrecord.values('date', 'car__car_number').annotate(
            count_ride_type_1=Count('ride_type', filter=Q(ride_type='迎車')),
            count_ride_type_2=Count('ride_type', filter=Q(ride_type='賃走')),
            count_ride_type_3=Count('ride_type', filter=Q(ride_type='回送')),
            daily_distance=Sum('distance'),
            daily_fare=Sum('fare'),
            count_at_stretcher=Count('at_stretcher', filter=Q(at_stretcher=True)),
            count_at_night=Count('at_night', filter=Q(at_night=True)),
            average_fare=Cast(Avg('fare'), IntegerField())
        ).order_by('date', 'car__car_number')

        for data in summary:
            writer.writerow([
                data['date'],
                int(data['car__car_number']),
                data['count_ride_type_1'],
                data['count_ride_type_2'],
                data['count_ride_type_3'],
                data['daily_distance'],
                data['daily_fare'],
                data['count_at_stretcher'],
                data['count_at_night'],
                data['average_fare'],
            ])
        return response


class DataDetailView(DetailView):
    model = SalesRecord
    form_class = DataInputForm
    template_name = 'myapp/data_detail.html'


class DataUpdateView(UpdateView):
    model = SalesRecord
    form_class = DataUpdateForm
    template_name = 'myapp/data_update.html'
    success_url = '/data_list'

    def form_valid(self, form):
        user = self.request.user
        sales_record = form.save(commit=False)
        sales_record.revised_by = user
        sales_record.save()

        return super().form_valid(form)

class DataDeleteView(DeleteView):
    model = SalesRecord
    template_name = 'myapp/data_delete.html'
    success_url = '/data_list'


class CarCSVImportView(FormView):
    success_url = '/car_list'
    template_name = 'myapp/import.html'
    form_class = CSVUploadForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['file']
        decoded_file = csvfile.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader)

        rows_processed = 0
        for row in reader:
            rows_processed += 1
            instance = CarInformation()
            try:
                if not row[1]:
                    form.add_error(None, "ナンバーが入力されていません")
                else:
                    instance.car_number = row[1]
                    if not re.match(r'^\d{1,4}$', instance.car_number):
                        form.add_error(None, f"ナンバーの形式が正しくありません： {instance.car_number}")

                instance.car_type = row[2]

                if not row[3]:  # 空欄の場合はエラーメッセージを追加
                    form.add_error(None, "総走行距離の入力が必要です")
                else:
                    try:
                        instance.car_mileage = float(row[3])
                    except ValueError:
                        form.add_error(None, f"総走行距離の形式が正しくありません： {row[3]}")
                instance.remarks = row[4]

                if not form.errors:
                    existing_car = CarInformation.objects.filter(car_number=instance.car_number).first()
                    if existing_car:
                        existing_car.car_type = instance.car_type
                        existing_car.car_mileage = instance.car_mileage
                        existing_car.remarks = instance.remarks
                        existing_car.save()
                    else:
                        instance.save()
            except IndexError:
                form = self.get_form()  # 新しいフォームインスタンスを作成
                form.add_error(None, "ファイルのフォーマットが正しくありません")

        if rows_processed < 1:
            form.add_error(None, "ファイルにデータがありません")

        if form.errors:
            return self.form_invalid(form)

        return super().form_valid(form)


class CustomerCSVImportView(FormView):
    template_name = 'myapp/import.html'
    success_url = '/customer_list'
    form_class = CSVUploadForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['file']
        decoded_file = csvfile.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader)

        rows_processed = 0
        for row in reader:
            rows_processed += 1
            instance = CustomerInformation()
            try:
                if not row[1]:
                    form.add_error(None, "名前が入力されていません")
                else:
                    instance.customer_name = row[1]
                if row[2]:
                    try:
                        instance.birthday = datetime.strptime(row[2], '%Y/%m/%d').date()
                    except ValueError:
                        form.add_error(None, f"生年月日の形式が正しくありません： {row[2]}")
                instance.zip_code = row[3]
                if instance.zip_code:  # 郵便番号が入力されている場合は形式チェック
                    if not re.match(r'^\d{3}-?\d{4}$', instance.zip_code):
                        form.add_error(None, f"郵便番号の形式が正しくありません： {instance.zip_code}")
                instance.prefecture = row[4]
                instance.city = row[5]
                instance.bldg = row[6]
                instance.tel = row[7]
                if instance.tel:  # 電話番号が入力されている場合は形式チェック
                    if not re.match(r'^\d{2,4}-\d{2,4}-\d{4}$', instance.tel):
                        form.add_error(None, f"電話番号の形式が正しくありません： {instance.tel}")
                instance.remarks = row[8]

                if not form.errors:
                    existing_customer = CustomerInformation.objects.filter(customer_name=instance.customer_name).first()
                    if existing_customer:
                        existing_customer.birthday = instance.birthday
                        existing_customer.zip_code = instance.zip_code
                        existing_customer.prefecture = instance.prefecture
                        existing_customer.city = instance.city
                        existing_customer.bldg = instance.bldg
                        existing_customer.tel = instance.tel
                        existing_customer.remarks = instance.remarks
                        existing_customer.save()
                    else:
                        instance.save()
            except IndexError:
                form = self.get_form()  # 新しいフォームインスタンスを作成
                form.add_error(None, "ファイルのフォーマットが正しくありません")

        if rows_processed < 1:
            form.add_error(None, "ファイルにデータがありません")

        if form.errors:
            return self.form_invalid(form)

        return super().form_valid(form)


class PlaceCSVImportView(FormView):
    success_url = '/place_list'
    template_name = 'myapp/import.html'
    form_class = CSVUploadForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['file']
        decoded_file = csvfile.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader)

        rows_processed = 0
        for row in reader:
            rows_processed += 1
            instance = PlaceInformation()
            try:
                if not row[1]:
                    form.add_error(None, "施設名が入力されていません")
                else:
                    instance.place_name = row[1]
                instance.zip_code = row[2]
                if instance.zip_code:  # 郵便番号が入力されている場合は形式チェック
                    if not re.match(r'^\d{3}-?\d{4}$', instance.zip_code):
                        form.add_error(None, f"郵便番号の形式が正しくありません： {instance.zip_code}")
                instance.prefecture = row[3]
                instance.city = row[4]
                instance.bldg = row[5]
                instance.tel = row[6]
                if instance.tel:  # 電話番号が入力されている場合は形式チェック
                    if not re.match(r'^\d{2,4}-\d{2,4}-\d{4}$', instance.tel):
                        form.add_error(None, f"電話番号の形式が正しくありません： {instance.tel}")
                instance.remarks = row[7]

                if not form.errors:
                    existing_place = PlaceInformation.objects.filter(place_name=instance.place_name).first()
                    if existing_place:
                        existing_place.zip_code = instance.zip_code
                        existing_place.prefecture = instance.prefecture
                        existing_place.city = instance.city
                        existing_place.bldg = instance.bldg
                        existing_place.tel = instance.tel
                        existing_place.remarks = instance.remarks
                        existing_place.save()
                    else:
                        instance.save()
            except IndexError:
                form = self.get_form()  # 新しいフォームインスタンスを作成
                form.add_error(None, "ファイルのフォーマットが正しくありません")

        if rows_processed < 1:
            form.add_error(None, "ファイルにデータがありません")

        if form.errors:
            return self.form_invalid(form)

        return super().form_valid(form)


class DataCSVImportView(FormView):
    success_url = '/data_list'
    template_name = 'myapp/import.html'
    form_class = CSVUploadForm

    def form_valid(self, form):
        csvfile = form.cleaned_data['file']
        decoded_file = csvfile.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader)

        rows_processed = 0
        for row in reader:
            rows_processed += 1
            instance = SalesRecord()
            try:
                if not row[1]:
                    form.add_error(None, "日付が指定されていません")
                else:
                    try:
                        instance.date = datetime.strptime(row[1], '%Y/%m/%d').date()
                    except ValueError:
                        form.add_error(None, f"日付の形式が正しくありません： {row[1]}")

                if not row[2]:
                    form.add_error(None, "搬送車が指定されていません")
                else:
                    try:
                        instance.car = CarInformation.objects.get(car_number=row[2])
                    except ObjectDoesNotExist:
                        form.add_error(None, f"搬送車データが存在しません： {row[2]}")

                if not row[3]:
                    form.add_error(None, "乗車タイプが指定されていません")
                else:
                    try:
                        instance.ride_type = row[3]
                    except ValueError:
                        form.add_error(None, f"存在しない乗車タイプです： {row[3]}")

                try:
                    if row[4]:  # データが記載されている場合のみ一致を確認
                        customer = CustomerInformation.objects.filter(customer_name=row[4]).first()
                        if customer:
                            instance.customer_name = customer
                        else:
                            form.add_error(None, f"顧客データが存在しません： {row[4]}")
                except CustomerInformation.DoesNotExist:
                    form.add_error(None, f"顧客データが存在しません： {row[4]}")

                try:
                    instance.place_from = PlaceInformation.objects.get(place_name=row[5])
                except ObjectDoesNotExist:
                    form.add_error(None, f"出発地の施設データが存在しません： {row[5]}")

                try:
                    instance.place_to = PlaceInformation.objects.get(place_name=row[6])
                except ObjectDoesNotExist:
                    form.add_error(None, f"到着地の施設データが存在しません： {row[6]}")

                try:
                    instance.start_time = datetime.strptime(row[7], '%H:%M').time()
                except ValueError:
                    form.add_error(None, "開始時間の形式が正しくありません")

                try:
                    instance.arrival_time = datetime.strptime(row[8], '%H:%M').time()
                except ValueError:
                    form.add_error(None, "到着時間の形式が正しくありません")

                if not row[9]:  # row[9]が空欄の場合はエラーメッセージを追加
                    form.add_error(None, "運行前(km)の値が必要です")
                else:
                    try:
                        instance.mileage_from = float(row[9])
                    except ValueError:
                        form.add_error(None, f"運行前(km)の形式が正しくありません： {row[9]}")

                if not row[10]:  # row[10]が空欄の場合はエラーメッセージを追加
                    form.add_error(None, "運行後(km)の値が必要です")
                else:
                    try:
                        instance.mileage_to = float(row[10])
                    except ValueError:
                        form.add_error(None, f"運行後(km)の形式が正しくありません： {row[10]}")

                if row[3] == '賃走':  # row[3]が"賃走"の場合のみチェック
                    if not row[12]:  # row[12]が空欄の場合はエラーメッセージを追加
                        form.add_error(None, "乗車タイプが賃走の場合は金額の入力が必要です")
                    else:
                        try:
                            instance.fare = float(row[12])
                        except ValueError:
                            form.add_error(None, f"金額の形式が正しくありません： {row[12]}")

                if row[13] == '〇':
                    instance.at_stretcher = True
                elif row[13] == '×' or not row[13]:
                    instance.at_stretcher = False  # 空欄の場合は '×' とみなす
                else:
                    form.add_error(None, f"STRは'〇'か'×'で入力してください： {row[13]}")

                if row[14] == '〇':
                    instance.at_night = True
                elif row[14] == '×' or not row[14]:
                    instance.at_night = False  # 空欄の場合は '×' とみなす
                else:
                    form.add_error(None, f"深夜割増は'〇'か'×'で入力してください： {row[14]}")

                instance.remarks = row[15]

                try:
                    if row[16] and row[17]:
                        instance.added_by = User.objects.get(username=row[16])
                        instance.revised_by = User.objects.get(username=row[17])
                    elif row[16] and not row[17]:
                        instance.added_by = User.objects.get(username=row[16])
                        instance.revised_by = self.request.user  # 空欄の場合は現在のログインユーザーを使用
                    elif not row[16] and not row[17]:
                        instance.added_by = self.request.user  # 空欄の場合は現在のログインユーザーを使用
                    else:
                        instance.revised_by = User.objects.get(username=row[17])
                except User.DoesNotExist:
                    form.add_error(None, "存在しないユーザーが指定されています")

                if not form.errors:
                    if not row[0]:  # `row[0]`が空欄の場合、自動的に採番
                        instance.id = None
                    else:
                        instance.id = row[0]
                    # 既存のデータが存在する場合、値を更新
                    try:
                        existing_data = SalesRecord.objects.get(id=instance.id)
                    except ObjectDoesNotExist:
                        existing_data = None
                    if existing_data:
                        existing_data.date = instance.date
                        existing_data.car = instance.car
                        existing_data.ride_type = instance.ride_type
                        existing_data.customer_name = instance.customer_name
                        existing_data.place_from = instance.place_from
                        existing_data.place_to = instance.place_to
                        existing_data.start_time = instance.start_time
                        existing_data.arrival_time = instance.arrival_time
                        existing_data.mileage_from = instance.mileage_from
                        existing_data.mileage_to = instance.mileage_to
                        existing_data.distance = instance.distance
                        existing_data.fare = instance.fare
                        existing_data.at_stretcher = instance.at_stretcher
                        existing_data.at_night = instance.at_night
                        existing_data.remarks = instance.remarks
                        existing_data.added_by = instance.added_by
                        existing_data.revised_by = instance.revised_by
                        existing_data.save()
                    else:
                        instance.save()

            except IndexError:
                form = self.get_form()  # 新しいフォームインスタンスを作成
                form.add_error(None, "ファイルのフォーマットが正しくありません")

        if rows_processed < 1:
            form.add_error(None, "ファイルにデータがありません")

        if form.errors:
            return self.form_invalid(form)

        return super().form_valid(form)
