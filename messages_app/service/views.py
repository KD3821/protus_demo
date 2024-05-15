import os

from dotenv import load_dotenv
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status

from django.utils import timezone

from .permissions import IsOwner
from .models import Customer, Campaign, Message
from .paginations import CustomPagination
from .utils import (
    create_messages,
    schedule_message,
    schedule_campaign,
    schedule_check_campaign,
    cancel_campaign_schedule,
    cancel_campaign_check,
)
from .reports import (
    get_single_campaign_data,
    get_all_campaigns_data,
)
from .serializers import (
    ReadCampaignSerializer,
    WriteCampaignSerializer,
    CampaignMessagesSerializer,
    SingleCampaignReportSerializer,
    AllCampaignsReportSerializer,
    ReadCustomerSerializer,
    WriteCustomerSerializer,
    CustomerMessagesSerializer,
    MessageSerializer,
)
from protus.permissions import ProtusChargePermission
from protus.payment.processors import PaymentProcessor


load_dotenv()


class CampaignViewSet(ModelViewSet):
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.request.user.campaigns.order_by('id')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadCampaignSerializer
        return WriteCampaignSerializer

    def destroy(self, request, *args, **kwargs):
        campaign = self.get_object()
        if campaign.status != Campaign.SCHEDULED:
            raise serializers.ValidationError({
                'error': ['Удаление возможно только для рассылок со статусом "запланирована".']
            })
        self.perform_destroy(campaign)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=True,
        url_path='campaign-messages',
        url_name='campaign'
    )
    def get_messages(self, request, *args, **kwargs):
        campaign = self.get_object()
        messages = campaign.messages.select_related('customer').order_by('id')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(messages, request)
        serializer = CampaignMessagesSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(
        methods=['get'],
        detail=True,
        url_path='campaign-customers',
        url_name='campaign'
    )
    def get_customers(self, request, *arg, **kwargs):
        campaign = self.get_object()
        carrier = campaign.params.get('carrier')
        tag = campaign.params.get('tag')
        if tag is not None:
            customers = Customer.objects.filter(carrier=carrier, tag=tag).order_by('id')
        else:
            customers = Customer.objects.filter(carrier=carrier).order_by('id')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(customers, request)
        serializer = ReadCustomerSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(
        methods=['post'],
        detail=True,
        url_path='launch',
        url_name='campaign',
        permission_classes=[IsOwner, ProtusChargePermission]  # FIXME <INTEGRATION> Token Introspection: checks 'charge'
    )
    def launch_campaign(self, request, *args, **kwargs):
        campaign = self.get_object()
        if campaign.confirmed_at is not None:
            raise serializers.ValidationError({'error': ['Рассылка уже подтверждена.']})
        now_date = timezone.now()
        if now_date >= campaign.finish_at:
            raise serializers.ValidationError({'error': ['Время завершения рассылки уже наступило.']})
        if campaign.start_at <= now_date < campaign.finish_at:
            msg_list = create_messages(campaign)
            if not msg_list:
                raise serializers.ValidationError({
                    'error': ['Для данного фильтра клиенты не найдены. Измените параметры.']
                })
            campaign.status = Campaign.LAUNCHED
            campaign.confirmed_at = now_date
            campaign.save()
            schedule_check_campaign(campaign.pk)
            for msg in msg_list:
                schedule_message(msg.uuid)

            protus_biller = PaymentProcessor(  # noqa FIXME <INTEGRATION> Charge-Account performed (payload is optional)
                user_uuid=request.user.uuid,
                service_id=os.getenv('LAUNCH_CAMPAIGN_SERVICE_ID'),
                payload={
                    'campaign_id': campaign.pk,
                    'campaign_params': campaign.params,
                    'campaign_text': campaign.text[:20]
                }
            )
            protus_biller.start()  # processing PROTUS payment

        elif now_date < campaign.start_at:  # TODO add check if any customer suits the campaign filter
            campaign.status = Campaign.SCHEDULED
            campaign.confirmed_at = now_date
            campaign.save()
            schedule_campaign(campaign.pk)
        return Response(status=status.HTTP_201_CREATED)

    @action(
        methods=['post'],
        detail=True,
        url_path='cancel',
        url_name='campaign'
    )
    def cancel_campaign(self, request, *args, **kwargs):
        campaign = self.get_object()
        if campaign.status == Campaign.FINISHED:
            raise serializers.ValidationError({
                'error': ['Невозможно отменить рассылку - статус рассылки "завершена"']
            })
        campaign.status = Campaign.CANCELED
        campaign.save()
        cancel_campaign_schedule(campaign.pk)
        cancel_campaign_check(campaign.pk)
        return Response(
            {'cancel_data': 'Рассылка будет остановлена'},
            status=status.HTTP_200_OK
        )


class CustomerViewSet(ModelViewSet):
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.request.user.customers.order_by('id')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadCustomerSerializer
        return WriteCustomerSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [
                ProtusChargePermission()  # FIXME <INTEGRATION> Token Introspection: checks if 'charge' in scope
            ]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        protus_biller = PaymentProcessor(  # noqa FIXME <INTEGRATION> Charge-Account performed (payload is optional arg)
            user_uuid=request.user.uuid,
            service_id=os.getenv('ADD_CUSTOMER_SERVICE_ID'),
            payload=serializer.data
        )
        protus_biller.start()              # processing PROTUS payment

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(
        methods=['get'],
        detail=True,
        url_path='customer-messages',
        url_name='customer'
    )
    def get_messages(self, request, *args, **kwargs):
        customer = self.get_object()
        messages = customer.messages.select_related('campaign').order_by('id')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(messages, request)
        serializer = CustomerMessagesSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        if customer.messages.filter(status=Message.OK).count() != 0:
            raise serializers.ValidationError({
                'error': ['Невозможно удалить клиента, которому были отправлены сообщения.']
            })
        processing_messages = customer.messages.filter(status=Message.PROCESSING)
        for msg in processing_messages:
            msg.status = Message.CANCELED
            msg.save(update_fields=['status'])
        self.perform_destroy(customer)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return self.request.user.messages.order_by('id')


class SingleCampaignReportView(APIView):

    def get(self, request, *args, **kwargs):
        campaign_id = kwargs.get('id')
        try:
            campaign = Campaign.objects.filter(owner=request.user, id=campaign_id)[0:1].get()
        except Campaign.DoesNotExist:
            raise serializers.ValidationError({'error': ['Рассылка не найдена.']})
        report_data = get_single_campaign_data(campaign)
        serializer = SingleCampaignReportSerializer(instance=report_data)
        return Response(serializer.data)


class AllCampaignsReportView(APIView):

    def get(self, request, *args, **kwargs):
        report_data = get_all_campaigns_data(request.user)
        serializer = AllCampaignsReportSerializer(instance=report_data)
        return Response(serializer.data)
