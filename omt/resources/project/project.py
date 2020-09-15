# -*- coding: utf-8 -*-

from omt.core.resource import Resource


class Project(Resource):
    """
NAME
    project - project resource type

SYNOPSIS
    omt project [<project resource>] [<sub resource>] [action] [action params]

DESCRIPTION
     identify the resources with namespace project, then deal with the resource with further actions

ACTION LIST
    config - sub resource type, to do operation on do operation on project configuration, such as view/edit.
    """