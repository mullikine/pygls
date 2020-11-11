# Copyright 2017 Palantir Technologies, Inc.
# pylint: disable=redefined-builtin, unused-argument
from pygls import hookspec


@hookspec
def pygls_code_actions(config, workspace, document, range, context):
    pass


@hookspec
def pygls_code_lens(config, workspace, document):
    pass


@hookspec
def pygls_commands(config, workspace):
    """The list of command strings supported by the server.

    Returns:
        List[str]: The supported commands.
    """


@hookspec
def pygls_completions(config, workspace, document, position):
    pass


@hookspec
def pygls_definitions(config, workspace, document, position):
    pass


@hookspec
def pygls_dispatchers(config, workspace):
    pass


@hookspec
def pygls_document_did_open(config, workspace, document):
    pass


@hookspec
def pygls_document_did_save(config, workspace, document):
    pass


@hookspec
def pygls_document_highlight(config, workspace, document, position):
    pass


@hookspec
def pygls_document_symbols(config, workspace, document):
    pass


@hookspec(firstresult=True)
def pygls_execute_command(config, workspace, command, arguments):
    pass


@hookspec
def pygls_experimental_capabilities(config, workspace):
    pass


@hookspec(firstresult=True)
def pygls_folding_range(config, workspace, document):
    pass


@hookspec(firstresult=True)
def pygls_format_document(config, workspace, document):
    pass


@hookspec(firstresult=True)
def pygls_format_range(config, workspace, document, range):
    pass


@hookspec(firstresult=True)
def pygls_hover(config, workspace, document, position):
    pass


@hookspec
def pygls_initialize(config, workspace):
    pass


@hookspec
def pygls_initialized():
    pass


@hookspec
def pygls_lint(config, workspace, document, is_saved):
    pass


@hookspec
def pygls_references(config, workspace, document, position, exclude_declaration):
    pass


@hookspec(firstresult=True)
def pygls_rename(config, workspace, document, position, new_name):
    pass


@hookspec
def pygls_settings(config):
    pass


@hookspec(firstresult=True)
def pygls_signature_help(config, workspace, document, position):
    pass
