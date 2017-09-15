from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.response import Response
from django.db import transaction

from hr.models import EmployeeGradeScale, EmployeeGradeGroup, GradeScaleValidity, EmployeeGrade, AllowanceValidity, \
    AllowanceName, Allowance, DeductionValidity, Deduction, DeductionName
from hr.serializers import EmployeeGradeScaleSerializer, EmployeeGradeGroupSerializer, GradeScaleValiditySerializer, \
    EmployeeGradeSerializer, AllowanceValiditySerializer, AllowanceNameSerializer, AllowanceSerializer, \
    DeductionValiditySerializer, DeductionSerializer, DeductionNameSerializer


class EmployeeGradeScaleViewSet(viewsets.ModelViewSet):
    queryset = EmployeeGradeScale.objects.all()
    serializer_class = EmployeeGradeScaleSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('category', 'in_stock')

    def get_queryset(self):
        if self.request.GET.get('validity_id'):
            return self.queryset.filter(validity_id=self.request.GET.get('validity_id'))
        return self.queryset

    def create(self, request, *args, **kwargs):
        rows = request.data
        if rows:
            validity_id = rows[0]['employee_grades'][0]['scale']['validity_id']
            for row in rows:
                for roow in row['employee_grades']:
                    db_row = {key: value if value else None for key, value in roow['scale'].items()}
                    try:
                        id = db_row.pop('id')
                    except (KeyError):
                        id = None
                    try:
                        with transaction.atomic():
                            EmployeeGradeScale.objects.update_or_create(id=id, defaults=db_row)
                    except IntegrityError:
                        if id:
                            EmployeeGradeScale.objects.get(id=id).delete()
            saved_data = EmployeeGradeScaleSerializer(
                EmployeeGradeScale.objects.filter(validity_id=validity_id),
                many=True
            )
            return Response(saved_data.data)
        else:
            return Response([])


class EmployeeGradeGroupViewSet(viewsets.ModelViewSet):
    queryset = EmployeeGradeGroup.objects.all()
    serializer_class = EmployeeGradeGroupSerializer

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('category', 'in_stock')

    # def get_queryset(self):
    #     if self.request.GET.get('validity_id'):
    #         return self.queryset.filter(employee_grades__grade_scales__validity_id=self.request.GET.get('validity_id'))
    #     return self.queryset

    # def list(self, request, *args, **kwargs):
    #     super(EmployeeGradeGroupViewSet, self).list(request, *args, **kwargs)


class GradeScaleValidityViewSet(viewsets.ModelViewSet):
    queryset = GradeScaleValidity.objects.all()
    serializer_class = GradeScaleValiditySerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)


class EmployeeGradeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeGrade.objects.all()
    serializer_class = EmployeeGradeSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('category', 'in_stock')


# Allowance Viewset

class AllowanceValidityViewSet(viewsets.ModelViewSet):
    queryset = AllowanceValidity.objects.all()
    serializer_class = AllowanceValiditySerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)


class AllowanceNameViewSet(viewsets.ModelViewSet):
    queryset = AllowanceName.objects.all()
    serializer_class = AllowanceNameSerializer


class AllowanceViewSet(viewsets.ModelViewSet):
    queryset = Allowance.objects.all()
    serializer_class = AllowanceSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            validity_id = self.request.GET.get('validity_id')
            name_id = self.request.GET.get('name_id')
            return self.queryset.filter(validity_id=validity_id, name_id=name_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        rows = request.data
        if rows:
            validity_id = rows[0]['employee_grades'][0]['allowance']['validity_id']
            name_id = rows[0]['employee_grades'][0]['allowance']['name_id']
            for row in rows:
                for roow in row['employee_grades']:
                    allowance_dict = {key: value if value else None for key, value in roow['allowance'].items() if key not in ['errors', 'ypcm_disable_edit']}
                    try:
                        id = allowance_dict.pop('id')
                    except (KeyError):
                        id = None
                    try:
                        with transaction.atomic():
                            Allowance.objects.update_or_create(id=id, defaults=allowance_dict)
                    except IntegrityError:
                        if id:
                            Allowance.objects.get(id=id).delete()
            saved_data = AllowanceSerializer(
                Allowance.objects.filter(validity_id=validity_id, name_id=name_id),
                many=True
            )
            return Response(saved_data.data)
        else:
            return Response([])

# End Allowance Viewset

# Deduction ViewSet

class DeductionValidityViewSet(viewsets.ModelViewSet):
    queryset = DeductionValidity.objects.all()
    serializer_class = DeductionValiditySerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)

                # End Deduction ViewSet


class DeductionNameViewSet(viewsets.ModelViewSet):
    queryset = DeductionName.objects.all()
    serializer_class = DeductionNameSerializer


class DeductionViewSet(viewsets.ModelViewSet):
    queryset = Deduction.objects.all()
    serializer_class = DeductionSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            validity_id = self.request.GET.get('validity_id')
            return self.queryset.filter(validity_id=validity_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        rows = request.data
        if rows:
            validity_id = rows[0]['deduction']['validity_id']
            for row in rows:

                row_data = {key: value if value else None for key, value in row['deduction'].items()}
                try:
                    id = row_data.pop('id')
                except (KeyError):
                    id = None
                try:
                    with transaction.atomic():
                        Deduction.objects.update_or_create(id=id, defaults=row_data)
                except IntegrityError:
                    if id:
                        Deduction.objects.get(id=id).delete()
            saved_data = DeductionSerializer(
                Deduction.objects.filter(validity_id=validity_id),
                many=True
            )
            return Response(saved_data.data)
        else:
            return Response([])

