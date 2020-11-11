# Copyright 2017 Palantir Technologies, Inc.
import os
import sys

import pytest

from pygls import uris

PY2 = sys.version_info.major == 2

if PY2:
    import pathlib2 as pathlib
else:
    import pathlib


DOC_URI = uris.from_fs_path(__file__)


def path_as_uri(path):
    return pathlib.Path(os.path.abspath(path)).as_uri()


def test_local(pygls):
    """ Since the workspace points to the test directory """
    assert pygls.workspace.is_local()


def test_put_document(pygls):
    pygls.workspace.put_document(DOC_URI, 'content')
    assert DOC_URI in pygls.workspace._docs


def test_get_document(pygls):
    pygls.workspace.put_document(DOC_URI, 'TEXT')
    assert pygls.workspace.get_document(DOC_URI).source == 'TEXT'


def test_get_missing_document(tmpdir, pygls):
    source = 'TEXT'
    doc_path = tmpdir.join("test_document.py")
    doc_path.write(source)
    doc_uri = uris.from_fs_path(str(doc_path))
    assert pygls.workspace.get_document(doc_uri).source == 'TEXT'


def test_rm_document(pygls):
    pygls.workspace.put_document(DOC_URI, 'TEXT')
    assert pygls.workspace.get_document(DOC_URI).source == 'TEXT'
    pygls.workspace.rm_document(DOC_URI)
    assert pygls.workspace.get_document(DOC_URI)._source is None


@pytest.mark.parametrize('metafiles', [('setup.py',), ('pyproject.toml',), ('setup.py', 'pyproject.toml')])
def test_non_root_project(pygls, metafiles):
    repo_root = os.path.join(pygls.workspace.root_path, 'repo-root')
    os.mkdir(repo_root)
    project_root = os.path.join(repo_root, 'project-root')
    os.mkdir(project_root)

    for metafile in metafiles:
        with open(os.path.join(project_root, metafile), 'w+') as f:
            f.write('# ' + metafile)

    test_uri = uris.from_fs_path(os.path.join(project_root, 'hello/test.py'))
    pygls.workspace.put_document(test_uri, 'assert True')
    test_doc = pygls.workspace.get_document(test_uri)
    assert project_root in test_doc.sys_path()


def test_root_project_with_no_setup_py(pygls):
    """Default to workspace root."""
    workspace_root = pygls.workspace.root_path
    test_uri = uris.from_fs_path(os.path.join(workspace_root, 'hello/test.py'))
    pygls.workspace.put_document(test_uri, 'assert True')
    test_doc = pygls.workspace.get_document(test_uri)
    assert workspace_root in test_doc.sys_path()


def test_multiple_workspaces(tmpdir, pygls):
    workspace1_dir = tmpdir.mkdir('workspace1')
    workspace2_dir = tmpdir.mkdir('workspace2')
    file1 = workspace1_dir.join('file1.py')
    file2 = workspace2_dir.join('file1.py')
    file1.write('import os')
    file2.write('import sys')

    msg = {
        'uri': path_as_uri(str(file1)),
        'version': 1,
        'text': 'import os'
    }

    pygls.m_text_document__did_open(textDocument=msg)
    assert msg['uri'] in pygls.workspace._docs

    added_workspaces = [{'uri': path_as_uri(str(x))}
                        for x in (workspace1_dir, workspace2_dir)]
    event = {'added': added_workspaces, 'removed': []}
    pygls.m_workspace__did_change_workspace_folders(event)

    for workspace in added_workspaces:
        assert workspace['uri'] in pygls.workspaces

    workspace1_uri = added_workspaces[0]['uri']
    assert msg['uri'] not in pygls.workspace._docs
    assert msg['uri'] in pygls.workspaces[workspace1_uri]._docs

    msg = {
        'uri': path_as_uri(str(file2)),
        'version': 1,
        'text': 'import sys'
    }
    pygls.m_text_document__did_open(textDocument=msg)

    workspace2_uri = added_workspaces[1]['uri']
    assert msg['uri'] in pygls.workspaces[workspace2_uri]._docs

    event = {'added': [], 'removed': [added_workspaces[0]]}
    pygls.m_workspace__did_change_workspace_folders(event)
    assert workspace1_uri not in pygls.workspaces


def test_multiple_workspaces_wrong_removed_uri(pygls, tmpdir):
    workspace = {'uri': str(tmpdir.mkdir('Test123'))}
    event = {'added': [], 'removed': [workspace]}
    pygls.m_workspace__did_change_workspace_folders(event)
    assert workspace['uri'] not in pygls.workspaces


def test_root_workspace_changed(pygls, tmpdir):
    test_uri = str(tmpdir.mkdir('Test123'))
    pygls.root_uri = test_uri
    pygls.workspace._root_uri = test_uri

    workspace1 = {'uri': test_uri}
    workspace2 = {'uri': str(tmpdir.mkdir('NewTest456'))}

    event = {'added': [workspace2], 'removed': [workspace1]}
    pygls.m_workspace__did_change_workspace_folders(event)

    assert workspace2['uri'] == pygls.workspace._root_uri
    assert workspace2['uri'] == pygls.root_uri


def test_root_workspace_not_changed(pygls, tmpdir):
    # removed uri != root_uri
    test_uri_1 = str(tmpdir.mkdir('Test12'))
    pygls.root_uri = test_uri_1
    pygls.workspace._root_uri = test_uri_1
    workspace1 = {'uri': str(tmpdir.mkdir('Test1234'))}
    workspace2 = {'uri': str(tmpdir.mkdir('NewTest456'))}
    event = {'added': [workspace2], 'removed': [workspace1]}
    pygls.m_workspace__did_change_workspace_folders(event)
    assert test_uri_1 == pygls.workspace._root_uri
    assert test_uri_1 == pygls.root_uri
    # empty 'added' list
    test_uri_2 = str(tmpdir.mkdir('Test123'))
    new_root_uri = workspace2['uri']
    pygls.root_uri = test_uri_2
    pygls.workspace._root_uri = test_uri_2
    workspace1 = {'uri': test_uri_2}
    event = {'added': [], 'removed': [workspace1]}
    pygls.m_workspace__did_change_workspace_folders(event)
    assert new_root_uri == pygls.workspace._root_uri
    assert new_root_uri == pygls.root_uri
    # empty 'removed' list
    event = {'added': [workspace1], 'removed': []}
    pygls.m_workspace__did_change_workspace_folders(event)
    assert new_root_uri == pygls.workspace._root_uri
    assert new_root_uri == pygls.root_uri
    # 'added' list has no 'uri'
    workspace2 = {'TESTuri': 'Test1234'}
    event = {'added': [workspace2], 'removed': [workspace1]}
    pygls.m_workspace__did_change_workspace_folders(event)
    assert new_root_uri == pygls.workspace._root_uri
    assert new_root_uri == pygls.root_uri


def test_root_workspace_removed(tmpdir, pygls):
    workspace1_dir = tmpdir.mkdir('workspace1')
    workspace2_dir = tmpdir.mkdir('workspace2')
    root_uri = pygls.root_uri

    # Add workspaces to the pygls
    added_workspaces = [{'uri': path_as_uri(str(x))}
                        for x in (workspace1_dir, workspace2_dir)]
    event = {'added': added_workspaces, 'removed': []}
    pygls.m_workspace__did_change_workspace_folders(event)

    # Remove the root workspace
    removed_workspaces = [{'uri': root_uri}]
    event = {'added': [], 'removed': removed_workspaces}
    pygls.m_workspace__did_change_workspace_folders(event)

    # Assert that the first of the workspaces (in alphabetical order) is now
    # the root workspace
    assert pygls.root_uri == path_as_uri(str(workspace1_dir))
    assert pygls.workspace._root_uri == path_as_uri(str(workspace1_dir))


@pytest.mark.skipif(os.name == 'nt', reason="Fails on Windows")
def test_workspace_loads_pycodestyle_config(pygls, tmpdir):
    workspace1_dir = tmpdir.mkdir('Test123')
    pygls.root_uri = str(workspace1_dir)
    pygls.workspace._root_uri = str(workspace1_dir)

    # Test that project settings are loaded
    workspace2_dir = tmpdir.mkdir('NewTest456')
    cfg = workspace2_dir.join("pycodestyle.cfg")
    cfg.write(
        "[pycodestyle]\n"
        "max-line-length = 1000"
    )

    workspace1 = {'uri': str(workspace1_dir)}
    workspace2 = {'uri': str(workspace2_dir)}

    event = {'added': [workspace2], 'removed': [workspace1]}
    pygls.m_workspace__did_change_workspace_folders(event)

    seetings = pygls.workspaces[str(workspace2_dir)]._config.settings()
    assert seetings['plugins']['pycodestyle']['maxLineLength'] == 1000

    # Test that project settings prevail over server ones.
    server_settings = {'pygls': {'plugins': {'pycodestyle': {'maxLineLength': 10}}}}
    pygls.m_workspace__did_change_configuration(server_settings)
    assert seetings['plugins']['pycodestyle']['maxLineLength'] == 1000

    # Test switching to another workspace with different settings
    workspace3_dir = tmpdir.mkdir('NewTest789')
    cfg1 = workspace3_dir.join("pycodestyle.cfg")
    cfg1.write(
        "[pycodestyle]\n"
        "max-line-length = 20"
    )

    workspace3 = {'uri': str(workspace3_dir)}

    event = {'added': [workspace3], 'removed': [workspace2]}
    pygls.m_workspace__did_change_workspace_folders(event)

    seetings = pygls.workspaces[str(workspace3_dir)]._config.settings()
    assert seetings['plugins']['pycodestyle']['maxLineLength'] == 20


def test_settings_of_added_workspace(pygls, tmpdir):
    test_uri = str(tmpdir.mkdir('Test123'))
    pygls.root_uri = test_uri
    pygls.workspace._root_uri = test_uri

    # Set some settings for the server.
    server_settings = {'pygls': {'plugins': {'jedi': {'environment': '/usr/bin/python3'}}}}
    pygls.m_workspace__did_change_configuration(server_settings)

    # Create a new workspace.
    workspace1 = {'uri': str(tmpdir.mkdir('NewTest456'))}
    event = {'added': [workspace1]}
    pygls.m_workspace__did_change_workspace_folders(event)

    # Assert settings are inherited from the server config.
    workspace1_object = pygls.workspaces[workspace1['uri']]
    workspace1_jedi_settings = workspace1_object._config.plugin_settings('jedi')
    assert workspace1_jedi_settings == server_settings['pygls']['plugins']['jedi']
