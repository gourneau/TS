# Copyright (C) 2012 Ion Torrent Systems, Inc. All Rights Reserved
from iondb.rundb.models import Project, PlannedExperiment, Content
from django.contrib.auth.models import User

from traceback import format_exc

import logging
logger = logging.getLogger(__name__)


def get_projects_helper(projectIdAndNameList):
    found, missing = [], []
    if (isinstance(projectIdAndNameList, basestring)):
        projectIdAndNameList = projectIdAndNameList.split(',')

    for projectIdAndName in projectIdAndNameList:
        projectId = projectIdAndName.split('|')[0]
        try:
            found.append(Project.objects.get(id=int(projectId)))
        except:
            missing.append(projectIdAndName)

    return found, missing


def get_projects(username, json_data):
    # selected projects, projectIdAndNameList is a string if 1 entry; list otherwise
    projectIdAndNameList = json_data.get('projects', '')
    projectObjList = []
    if projectIdAndNameList:
        projectObjList, missings = get_projects_helper(projectIdAndNameList)
        for missing in missings:
            logger.debug("views.editplannedexperiment project= %s is no longer in db" % missing)
    # new projects added
    newProjectNames = json_data.get('newProjects', '')
    if newProjectNames:
        newProjectNames = newProjectNames.split(',')
        projectObjList.extend(Project.bulk_get_or_create(newProjectNames, User.objects.get(username=username)))
    return projectObjList


def dict_bed_hotspot():
    data = {}
    allFiles = Content.objects.filter(publisher__name="BED", path__contains="/unmerged/detail/")
    bedFiles, hotspotFiles = [], []
    bedFileFullPaths, bedFilePaths, hotspotFullPaths, hotspotPaths = [], [], [], []
    for _file in allFiles:
        if _file.meta.get("hotspot", False):
            hotspotFiles.append(_file)
            hotspotFullPaths.append(_file.file)
            hotspotPaths.append(_file.path)
        else:
            bedFiles.append(_file)
            bedFileFullPaths.append(_file.file)
            bedFilePaths.append(_file.path)
    data["bedFiles"] = bedFiles
    data["hotspotFiles"] = hotspotFiles
    data["bedFileFullPaths"] = bedFileFullPaths
    data["bedFilePaths"] = bedFilePaths
    data["hotspotFullPaths"] = hotspotFullPaths
    data["hotspotPaths"] = hotspotPaths
    return data
