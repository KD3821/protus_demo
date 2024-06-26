# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from src.proto.compiled import auth_pb2 as auth__pb2


class AuthProtoStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateSession = channel.unary_unary(
            "/AuthProto/CreateSession",
            request_serializer=auth__pb2.SessionRequest.SerializeToString,
            response_deserializer=auth__pb2.SessionResponse.FromString,
        )
        self.CreateCustomer = channel.unary_unary(
            "/AuthProto/CreateCustomer",
            request_serializer=auth__pb2.CustomerRequest.SerializeToString,
            response_deserializer=auth__pb2.CustomerResponse.FromString,
        )
        self.AuthenticateCompany = channel.unary_unary(
            "/AuthProto/AuthenticateCompany",
            request_serializer=auth__pb2.AuthCompanyRequest.SerializeToString,
            response_deserializer=auth__pb2.AuthCompanyResponse.FromString,
        )
        self.IntrospectToken = channel.unary_unary(
            "/AuthProto/IntrospectToken",
            request_serializer=auth__pb2.IntrospectRequest.SerializeToString,
            response_deserializer=auth__pb2.IntrospectResponse.FromString,
        )


class AuthProtoServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateSession(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateCustomer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def AuthenticateCompany(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def IntrospectToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_AuthProtoServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "CreateSession": grpc.unary_unary_rpc_method_handler(
            servicer.CreateSession,
            request_deserializer=auth__pb2.SessionRequest.FromString,
            response_serializer=auth__pb2.SessionResponse.SerializeToString,
        ),
        "CreateCustomer": grpc.unary_unary_rpc_method_handler(
            servicer.CreateCustomer,
            request_deserializer=auth__pb2.CustomerRequest.FromString,
            response_serializer=auth__pb2.CustomerResponse.SerializeToString,
        ),
        "AuthenticateCompany": grpc.unary_unary_rpc_method_handler(
            servicer.AuthenticateCompany,
            request_deserializer=auth__pb2.AuthCompanyRequest.FromString,
            response_serializer=auth__pb2.AuthCompanyResponse.SerializeToString,
        ),
        "IntrospectToken": grpc.unary_unary_rpc_method_handler(
            servicer.IntrospectToken,
            request_deserializer=auth__pb2.IntrospectRequest.FromString,
            response_serializer=auth__pb2.IntrospectResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "AuthProto", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class AuthProto(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateSession(
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
            "/AuthProto/CreateSession",
            auth__pb2.SessionRequest.SerializeToString,
            auth__pb2.SessionResponse.FromString,
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
    def CreateCustomer(
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
            "/AuthProto/CreateCustomer",
            auth__pb2.CustomerRequest.SerializeToString,
            auth__pb2.CustomerResponse.FromString,
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
    def AuthenticateCompany(
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
            "/AuthProto/AuthenticateCompany",
            auth__pb2.AuthCompanyRequest.SerializeToString,
            auth__pb2.AuthCompanyResponse.FromString,
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
    def IntrospectToken(
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
            "/AuthProto/IntrospectToken",
            auth__pb2.IntrospectRequest.SerializeToString,
            auth__pb2.IntrospectResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
