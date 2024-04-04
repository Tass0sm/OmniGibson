# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: environment.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x11\x65nvironment.proto\x12\x0b\x65nvironment"\x1d\n\x0bStepRequest\x12\x0e\n\x06\x61\x63tion\x18\x01 \x02(\x0c"h\n\x0cStepResponse\x12\x13\n\x0bobservation\x18\x01 \x02(\x0c\x12\x0e\n\x06reward\x18\x02 \x02(\x02\x12\x12\n\nterminated\x18\x03 \x02(\x08\x12\x11\n\ttruncated\x18\x04 \x02(\x08\x12\x0c\n\x04info\x18\x05 \x02(\x0c"-\n\x0cResetRequest\x12\x0c\n\x04seed\x18\x01 \x01(\x05\x12\x0f\n\x07options\x18\x02 \x01(\x0c"8\n\rResetResponse\x12\x13\n\x0bobservation\x18\x01 \x02(\x0c\x12\x12\n\nreset_info\x18\x02 \x02(\x0c"\x0f\n\rRenderRequest"%\n\x0eRenderResponse\x12\x13\n\x0brender_data\x18\x01 \x02(\x0c"\x0e\n\x0c\x43loseRequest"\x0f\n\rCloseResponse"\x12\n\x10GetSpacesRequest"D\n\x11GetSpacesResponse\x12\x19\n\x11observation_space\x18\x01 \x02(\x0c\x12\x14\n\x0c\x61\x63tion_space\x18\x02 \x02(\x0c":\n\x10\x45nvMethodRequest\x12\x13\n\x0bmethod_name\x18\x01 \x02(\t\x12\x11\n\targuments\x18\x02 \x02(\x0c"#\n\x11\x45nvMethodResponse\x12\x0e\n\x06result\x18\x01 \x02(\x0c"(\n\x0eGetAttrRequest\x12\x16\n\x0e\x61ttribute_name\x18\x01 \x02(\t"*\n\x0fGetAttrResponse\x12\x17\n\x0f\x61ttribute_value\x18\x01 \x02(\x0c"A\n\x0eSetAttrRequest\x12\x16\n\x0e\x61ttribute_name\x18\x01 \x02(\t\x12\x17\n\x0f\x61ttribute_value\x18\x02 \x02(\x0c"\x11\n\x0fSetAttrResponse"(\n\x10IsWrappedRequest\x12\x14\n\x0cwrapper_type\x18\x01 \x02(\t"\'\n\x11IsWrappedResponse\x12\x12\n\nis_wrapped\x18\x01 \x02(\x08"\x07\n\x05\x45mpty"6\n\x1aRegisterEnvironmentRequest\x12\n\n\x02ip\x18\x01 \x02(\t\x12\x0c\n\x04port\x18\x02 \x02(\x05".\n\x1bRegisterEnvironmentResponse\x12\x0f\n\x07success\x18\x01 \x02(\x08\x32\x84\x05\n\x12\x45nvironmentService\x12;\n\x04Step\x12\x18.environment.StepRequest\x1a\x19.environment.StepResponse\x12>\n\x05Reset\x12\x19.environment.ResetRequest\x1a\x1a.environment.ResetResponse\x12\x41\n\x06Render\x12\x1a.environment.RenderRequest\x1a\x1b.environment.RenderResponse\x12>\n\x05\x43lose\x12\x19.environment.CloseRequest\x1a\x1a.environment.CloseResponse\x12J\n\tGetSpaces\x12\x1d.environment.GetSpacesRequest\x1a\x1e.environment.GetSpacesResponse\x12J\n\tEnvMethod\x12\x1d.environment.EnvMethodRequest\x1a\x1e.environment.EnvMethodResponse\x12\x44\n\x07GetAttr\x12\x1b.environment.GetAttrRequest\x1a\x1c.environment.GetAttrResponse\x12\x44\n\x07SetAttr\x12\x1b.environment.SetAttrRequest\x1a\x1c.environment.SetAttrResponse\x12J\n\tIsWrapped\x12\x1d.environment.IsWrappedRequest\x1a\x1e.environment.IsWrappedResponse2\xd2\x01\n\x1e\x45nvironmentRegistrationService\x12h\n\x13RegisterEnvironment\x12\'.environment.RegisterEnvironmentRequest\x1a(.environment.RegisterEnvironmentResponse\x12\x46\n\x1cRegisterEnvironmentAvailable\x12\x12.environment.Empty\x1a\x12.environment.Empty'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "environment_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_STEPREQUEST"]._serialized_start = 34
    _globals["_STEPREQUEST"]._serialized_end = 63
    _globals["_STEPRESPONSE"]._serialized_start = 65
    _globals["_STEPRESPONSE"]._serialized_end = 169
    _globals["_RESETREQUEST"]._serialized_start = 171
    _globals["_RESETREQUEST"]._serialized_end = 216
    _globals["_RESETRESPONSE"]._serialized_start = 218
    _globals["_RESETRESPONSE"]._serialized_end = 274
    _globals["_RENDERREQUEST"]._serialized_start = 276
    _globals["_RENDERREQUEST"]._serialized_end = 291
    _globals["_RENDERRESPONSE"]._serialized_start = 293
    _globals["_RENDERRESPONSE"]._serialized_end = 330
    _globals["_CLOSEREQUEST"]._serialized_start = 332
    _globals["_CLOSEREQUEST"]._serialized_end = 346
    _globals["_CLOSERESPONSE"]._serialized_start = 348
    _globals["_CLOSERESPONSE"]._serialized_end = 363
    _globals["_GETSPACESREQUEST"]._serialized_start = 365
    _globals["_GETSPACESREQUEST"]._serialized_end = 383
    _globals["_GETSPACESRESPONSE"]._serialized_start = 385
    _globals["_GETSPACESRESPONSE"]._serialized_end = 453
    _globals["_ENVMETHODREQUEST"]._serialized_start = 455
    _globals["_ENVMETHODREQUEST"]._serialized_end = 513
    _globals["_ENVMETHODRESPONSE"]._serialized_start = 515
    _globals["_ENVMETHODRESPONSE"]._serialized_end = 550
    _globals["_GETATTRREQUEST"]._serialized_start = 552
    _globals["_GETATTRREQUEST"]._serialized_end = 592
    _globals["_GETATTRRESPONSE"]._serialized_start = 594
    _globals["_GETATTRRESPONSE"]._serialized_end = 636
    _globals["_SETATTRREQUEST"]._serialized_start = 638
    _globals["_SETATTRREQUEST"]._serialized_end = 703
    _globals["_SETATTRRESPONSE"]._serialized_start = 705
    _globals["_SETATTRRESPONSE"]._serialized_end = 722
    _globals["_ISWRAPPEDREQUEST"]._serialized_start = 724
    _globals["_ISWRAPPEDREQUEST"]._serialized_end = 764
    _globals["_ISWRAPPEDRESPONSE"]._serialized_start = 766
    _globals["_ISWRAPPEDRESPONSE"]._serialized_end = 805
    _globals["_EMPTY"]._serialized_start = 807
    _globals["_EMPTY"]._serialized_end = 814
    _globals["_REGISTERENVIRONMENTREQUEST"]._serialized_start = 816
    _globals["_REGISTERENVIRONMENTREQUEST"]._serialized_end = 870
    _globals["_REGISTERENVIRONMENTRESPONSE"]._serialized_start = 872
    _globals["_REGISTERENVIRONMENTRESPONSE"]._serialized_end = 918
    _globals["_ENVIRONMENTSERVICE"]._serialized_start = 921
    _globals["_ENVIRONMENTSERVICE"]._serialized_end = 1565
    _globals["_ENVIRONMENTREGISTRATIONSERVICE"]._serialized_start = 1568
    _globals["_ENVIRONMENTREGISTRATIONSERVICE"]._serialized_end = 1778
# @@protoc_insertion_point(module_scope)
