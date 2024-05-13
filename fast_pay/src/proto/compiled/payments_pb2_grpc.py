# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from src.proto.compiled import payments_pb2 as payments__pb2


class PaymentsProtoStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateAccount = channel.unary_unary(
            "/PaymentsProto/CreateAccount",
            request_serializer=payments__pb2.AccountRequest.SerializeToString,
            response_deserializer=payments__pb2.AccountResponse.FromString,
        )
        self.CreateAccounting = channel.unary_unary(
            "/PaymentsProto/CreateAccounting",
            request_serializer=payments__pb2.AccountingRequest.SerializeToString,
            response_deserializer=payments__pb2.AccountResponse.FromString,
        )
        self.ChargeAccount = channel.unary_unary(
            "/PaymentsProto/ChargeAccount",
            request_serializer=payments__pb2.ChargeRequest.SerializeToString,
            response_deserializer=payments__pb2.ChargeResponse.FromString,
        )


class PaymentsProtoServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateAccounting(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ChargeAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_PaymentsProtoServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "CreateAccount": grpc.unary_unary_rpc_method_handler(
            servicer.CreateAccount,
            request_deserializer=payments__pb2.AccountRequest.FromString,
            response_serializer=payments__pb2.AccountResponse.SerializeToString,
        ),
        "CreateAccounting": grpc.unary_unary_rpc_method_handler(
            servicer.CreateAccounting,
            request_deserializer=payments__pb2.AccountingRequest.FromString,
            response_serializer=payments__pb2.AccountResponse.SerializeToString,
        ),
        "ChargeAccount": grpc.unary_unary_rpc_method_handler(
            servicer.ChargeAccount,
            request_deserializer=payments__pb2.ChargeRequest.FromString,
            response_serializer=payments__pb2.ChargeResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "PaymentsProto", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class PaymentsProto(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateAccount(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/PaymentsProto/CreateAccount",
            payments__pb2.AccountRequest.SerializeToString,
            payments__pb2.AccountResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def CreateAccounting(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/PaymentsProto/CreateAccounting",
            payments__pb2.AccountingRequest.SerializeToString,
            payments__pb2.AccountResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def ChargeAccount(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/PaymentsProto/ChargeAccount",
            payments__pb2.ChargeRequest.SerializeToString,
            payments__pb2.ChargeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )