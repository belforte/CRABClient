#!/usr/bin/env python
"""
_ClientMapping_

This allows to have an agnostic client.
For each client command it is possible to define the path of the REST request, the map between
the client configuration and the final request to send to the server. It includes type of the
parameter so that the client can do a basic sanity check on the input data type.
For each server parameter, there can be more than one parameter in the CRAB configuration file.
If that is the case, then the meaning is that any of the parameters in the CRAB configuration
file is used to set the same server parameter.
"""

import copy

## In this dictionary, the definitions of 'type', 'required' and 'default'
## refer to the parameters in the CRAB configuration file.
parametersMapping = {
    'on-server': {'workflow'       : {'default': None,       'config': ['General.requestName'],             'type': 'StringType',  'required': False},
                  'activity'       : {'default': None,       'config': ['General.activity'],                'type': 'StringType',  'required': False},
                  'saveoutput'     : {'default': True,       'config': ['General.transferOutputs'],         'type': 'BooleanType', 'required': False},
                  'savelogsflag'   : {'default': False,      'config': ['General.transferLogs'],            'type': 'BooleanType', 'required': False},
                  'faillimit'      : {'default': None,       'config': ['General.failureLimit'],            'type': 'IntType',     'required': False},
                  'inputdata'      : {'default': None,       'config': ['Data.inputDataset'],               'type': 'StringType',  'required': False},
                  'primarydataset' : {'default': None,       'config': ['Data.outputPrimaryDataset'],       'type': 'StringType',  'required': False},
                  'nonvaliddata'   : {'default': False,      'config': ['Data.allowNonValidInputDataset'],  'type': 'BooleanType', 'required': False},
                  'userfiles'      : {'default': [],         'config': ['Data.userInputFiles'],             'type': 'ListType',    'required': False},
                  'dbsurl'         : {'default': 'global',   'config': ['Data.inputDBS'],                   'type': 'StringType',  'required': False},
                  'useparent'      : {'default': None,       'config': ['Data.useParent'],                  'type': 'BooleanType', 'required': False},
                  'secondarydata'  : {'default': None,       'config': ['Data.secondaryInputDataset'],      'type': 'StringType',  'required': False},
                  'ignorelocality' : {'default': False,      'config': ['Data.ignoreLocality'],             'type': 'BooleanType', 'required': False},
                  'splitalgo'      : {'default': 'Automatic', 'config': ['Data.splitting'],                 'type': 'StringType',  'required': True },
                  'algoargs'       : {'default': 480,        'config': ['Data.unitsPerJob'],                'type': 'IntType',     'required': False},
                  'totalunits'     : {'default': 0,          'config': ['Data.totalUnits'],                 'type': 'IntType',     'required': False},
                  'lfn'            : {'default': None,       'config': ['Data.outLFNDirBase'],              'type': 'StringType',  'required': False},
                  'publication'    : {'default': True,       'config': ['Data.publication'],                'type': 'BooleanType', 'required': False},
                  'publishdbsurl'  : {'default': 'phys03',   'config': ['Data.publishDBS'],                 'type': 'StringType',  'required': False},
                  #the 2 here to the publishname was added because of https://github.com/dmwm/CRABServer/issues/4947
                  'publishname2'   : {'default': None,       'config': ['Data.outputDatasetTag'],           'type': 'StringType',  'required': False},
                  'jobtype'        : {'default': 'Analysis', 'config': ['JobType.pluginName',
                                                                        'JobType.externalPluginFile'],      'type': 'StringType',  'required': False},
                  'generator'      : {'default': 'pythia',   'config': ['JobType.generator'],               'type': 'StringType',  'required': False},
                  'addoutputfiles' : {'default': [],         'config': ['JobType.outputFiles'],             'type': 'ListType',    'required': False},
                  'maxjobruntime'  : {'default': 1250,       'config': ['JobType.maxJobRuntimeMin'],        'type': 'IntType',     'required': False},
                  'numcores'       : {'default': 1,          'config': ['JobType.numCores'],                'type': 'IntType',     'required': False},
                  'maxmemory'      : {'default': 2000,       'config': ['JobType.maxMemoryMB'],             'type': 'IntType',     'required': False},
                  'priority'       : {'default': 10,         'config': ['JobType.priority'],                'type': 'IntType',     'required': False},
                  'nonprodsw'      : {'default': False,      'config': ['JobType.allowUndistributedCMSSW'], 'type': 'BooleanType', 'required': False},
                  'scriptexe'      : {'default': None,       'config': ['JobType.scriptExe'],               'type': 'StringType',  'required': False},
                  'scriptargs'     : {'default': None,       'config': ['JobType.scriptArgs'],              'type': 'ListType',    'required': False},
                  'asyncdest'      : {'default': None,       'config': ['Site.storageSite'],                'type': 'StringType',  'required': False},
                  'sitewhitelist'  : {'default': None,       'config': ['Site.whitelist'],                  'type': 'ListType',    'required': False},
                  'siteblacklist'  : {'default': None,       'config': ['Site.blacklist'],                  'type': 'ListType',    'required': False},
                  'requireaccelerator' : {'default': False,  'config': ['Site.requireAccelerator'],         'type': 'BooleanType', 'required': False},
                  'acceleratorparams'  : {'default': None,   'config': ['Site.acceleratorParams'],          'type': 'DictType',    'required': False},
                  'vorole'         : {'default': None,       'config': ['User.voRole'],                     'type': 'StringType',  'required': False},
                  'vogroup'        : {'default': None,       'config': ['User.voGroup'],                    'type': 'StringType',  'required': False},
                  'oneEventMode'   : {'default': False,      'config': ['Debug.oneEventMode'],              'type': 'BooleanType', 'required': False},
                  'scheddname'     : {'default': None,       'config': ['Debug.scheddName'],                'type': 'StringType',  'required': False},
                  'extrajdl'       : {'default': [],         'config': ['Debug.extraJDL'],                  'type': 'ListType',    'required': False},
                  'collector'      : {'default': None,       'config': ['Debug.collector'],                 'type': 'StringType',  'required': False},
                  'ignoreglobalblacklist':{'default': False, 'config': ['Site.ignoreGlobalBlacklist'],      'type': 'BooleanType', 'required': False},
                  'partialdataset' : {'default': False,      'config': ['Data.partialDataset'],             'type': 'BooleanType', 'required': False},
                  'inputblocks'    : {'default': [],         'config': ['Data.inputBlocks'],                'type': 'ListType',    'required': False},
                # the folllwing one is deprecated in crabConfig, but it must be listed since it is what we send to server
                # the value is obtained from Data.lumisPerFile below and number of jobs (files)
                  'eventsperlumi'  : {'default': None,       'config': ['JobType.eventsPerLumi'],           'type': 'IntType',     'required': False},
                 },
    'other-config-params': [         {'default': None,       'config': ['General.workArea'],                'type': 'StringType',  'required': False},
                                     {'default': 'prod',     'config': ['General.instance'],                'type': 'StringType',  'required': True },
                                     {'default': None,       'config': ['General.restHost'],                'type': 'StringType',  'required': False },
                                     {'default': None,       'config': ['General.dbInstance'],              'type': 'StringType',  'required': False },
                                     {'default': None,       'config': ['General.restHost'],                'type': 'StringType',  'required': False },
                                     {'default': None,       'config': ['General.dbInstance'],              'type': 'StringType',  'required': False },
                                     {'default': None,       'config': ['Data.lumiMask'],                   'type': 'StringType',  'required': False},
                                     {'default': None,       'config': ['Data.runRange'],                   'type': 'StringType',  'required': False},
                                     {'default': None,       'config': ['JobType.psetName'],                'type': 'StringType',  'required': False},
                                     {'default': False,      'config': ['JobType.sendVenvFolder'],          'type': 'BooleanType', 'required': False},
                                     {'default': False,      'config': ['JobType.sendExternalFolder'],      'type': 'BooleanType', 'required': False},
                                     {'default': None,       'config': ['JobType.pyCfgParams'],             'type': 'ListType',    'required': False},
                                     {'default': False,      'config': ['JobType.disableAutomaticOutputCollection'],'type': 'BooleanType', 'required': False},
                                     {'default': None,       'config': ['JobType.copyCatTaskname'],         'type': 'StringType',  'required': False},
                                     {'default': 'prod',     'config': ['JobType.copyCatInstance'],         'type': 'StringType',  'required': False},
                                     {'default': None,       'config': ['JobType.copyCatWorkdir'],          'type': 'StringType',  'required': False},
                                     {'default': [],         'config': ['JobType.inputFiles'],              'type': 'ListType',    'required': False},
                                     {'default': None,       'config': ['Data.lumisPerFile'],               'type': 'IntType',     'required': False},
]
}

renamedParams = {
    'General.transferOutput'          : {'newParam' : 'General.transferOutputs',         'version' : None},
    'General.saveLogs'                : {'newParam' : 'General.transferLogs',            'version' : None},
    'Data.outlfn'                     : {'newParam' : 'Data.outLFNDirBase',              'version' : 'v3.3.16'},
    'Data.outLFN'                     : {'newParam' : 'Data.outLFNDirBase',              'version' : 'v3.3.16'},
    'Data.dbsUrl'                     : {'newParam' : 'Data.inputDBS',                   'version' : None},
    'Data.publishDbsUrl'              : {'newParam' : 'Data.publishDBS',                 'version' : None},
    'Data.userInputFile'              : {'newParam' : 'Data.userInputFiles',             'version' : None},
    'JobType.numcores'                : {'newParam' : 'JobType.numCores',                'version' : None},
    'JobType.maxmemory'               : {'newParam' : 'JobType.maxMemoryMB',             'version' : None},
    'JobType.maxjobruntime'           : {'newParam' : 'JobType.maxJobRuntimeMin',        'version' : None},
    'JobType.allowNonProductionCMSSW' : {'newParam' : 'JobType.allowUndistributedCMSSW', 'version' : 'v3.3.16'},
    'Data.secondaryDataset'           : {'newParam' : 'Data.secondaryInputDataset',      'version' : 'v3.3.1511'},
    'Data.primaryDataset'             : {'newParam' : 'Data.outputPrimaryDataset',       'version' : 'v3.3.1511'},
    'Data.publishDataName'            : {'newParam' : 'Data.outputDatasetTag',           'version' : 'v3.3.1511'},
}

# dictionary format: param: reasons
deprecatedParams = {
    'JobType.sendPythonFolder': 'Now pythonFolder is always added to sandbox',
    'JobType.eventsPerLumi': 'Use Data.lumisPerFile instead',
}


"""
---------------------------------------------------------------------------------------------------------------
Parameter Name          |  Parameter Meaning
---------------------------------------------------------------------------------------------------------------
requiresDirOption       -  Whether the command requires the -d/--dir option or not (in the end, if the command
                           requiresa CRAB project directory as input).
useCache                -  Whether to use the CRAB cache file (~/.crab3).
                           Currently only used to get the CRAB project directory in case the command requires
                           it but no directory was given in the -d/--dir option.
requiresREST            -  Whether the command has to contact the CRAB Server REST Interface.
acceptsArguments        -  Whether the command accepts arguments. (To not confuse with options.)
                           For commands requiring the task option, which can be actually given as an argument,
                           do not count it here as an argument. Same thing for the 'submit' command which can
                           take the CRAB configuration file name from the arguments.
requiresRucio           -  Whether the command needs access to Rucio client
requiresProxyVOOptions  -  Whether the command requires the --voGroup and --voRole options or not.
doProxyGroupRoleCheck   -  Whether to check if the VO group and VO role in the proxy are the same as what has
                           been specified either in the CRAB configuration file or in the command options
                           --voGroup/--voRole (or with what is written in the request cache).
---------------------------------------------------------------------------------------------------------------
WARNING: Don't set at the same time acceptsArguments = True and requiresDirOption = True. This is because
         we don't have a way to distinghish the CRAB project directory  name from the other arguments,
         so there is a protection when requiresDirOption = True to not accept more that 1 argument.
---------------------------------------------------------------------------------------------------------------
"""
commandsConfiguration = {
    'createmyproxy' : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': False, 'requiresDirOption': False, 'useCache': False, 'requiresProxyVOOptions': False, 'requiresLocalCache': False},
    'checkusername' : {'acceptsArguments': False, 'requiresREST': False, 'requiresRucio': False, 'requiresDirOption': False, 'useCache': False, 'requiresProxyVOOptions': False, 'requiresLocalCache': False},
    'checkwrite'    : {'acceptsArguments': False, 'requiresREST': False, 'requiresRucio': True,  'requiresDirOption': False, 'useCache': False, 'requiresProxyVOOptions': True,  'requiresLocalCache': False},
    'checkdataset'  : {'acceptsArguments': False, 'requiresREST': False, 'requiresRucio': True,  'requiresDirOption': False, 'useCache': False, 'requiresProxyVOOptions': False, 'requiresLocalCache': False},
    'checkfile'     : {'acceptsArguments': False, 'requiresREST': False, 'requiresRucio': True,  'requiresDirOption': False, 'useCache': False, 'requiresProxyVOOptions': False, 'requiresLocalCache': False},
    'setdatasetstatus' : {'acceptsArguments': False, 'requiresREST': False, 'requiresRucio': False, 'requiresDirOption': False, 'useCache': False, 'requiresProxyVOOptions': False, 'requiresLocalCache': False},
    'setfilestatus' : {'acceptsArguments': False, 'requiresREST': False, 'requiresRucio': False, 'requiresDirOption': False, 'useCache': False, 'requiresProxyVOOptions': False, 'requiresLocalCache': False},
    'getlog'        : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': False, 'requiresDirOption': True,  'useCache': True,  'requiresProxyVOOptions': True,  'requiresLocalCache': True },
    'getoutput'     : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': True,  'requiresDirOption': True,  'useCache': True,  'requiresProxyVOOptions': True,  'requiresLocalCache': True },
    'kill'          : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': False, 'requiresDirOption': True,  'useCache': False, 'requiresProxyVOOptions': False, 'requiresLocalCache': True },
    'proceed'       : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': False, 'requiresDirOption': True,  'useCache': True,  'requiresProxyVOOptions': False, 'requiresLocalCache': True },
    'remake'        : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': False, 'requiresDirOption': False, 'useCache': False, 'requiresProxyVOOptions': False, 'requiresLocalCache': False},
    'remote_copy'   : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': True,  'requiresDirOption': True,  'useCache': True,  'requiresProxyVOOptions': False, 'requiresLocalCache': True },
    'report'        : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': False, 'requiresDirOption': True,  'useCache': True,  'requiresProxyVOOptions': False, 'requiresLocalCache': True },
    'resubmit'      : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': False, 'requiresDirOption': True,  'useCache': True,  'requiresProxyVOOptions': False, 'requiresLocalCache': True },
    'status'        : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': True,  'requiresDirOption': True,  'useCache': True,  'requiresProxyVOOptions': False, 'requiresLocalCache': True },
    'submit'        : {'acceptsArguments': True,  'requiresREST': True,  'requiresRucio': False, 'requiresDirOption': False, 'useCache': False, 'requiresProxyVOOptions': False, 'requiresLocalCache': False},
    'tasks'         : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': False, 'requiresDirOption': False, 'useCache': False, 'requiresProxyVOOptions': False, 'requiresLocalCache': False},
    'uploadlog'     : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': False, 'requiresDirOption': True,  'useCache': True,  'requiresProxyVOOptions': False, 'requiresLocalCache': False},
    'preparelocal'  : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': False, 'requiresDirOption': True,  'useCache': True,  'requiresProxyVOOptions': False, 'requiresLocalCache': True},
    'recover'       : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': False, 'requiresDirOption': True, 'useCache': False, 'requiresProxyVOOptions': False, 'requiresLocalCache': False},
    'getsandbox'    : {'acceptsArguments': False, 'requiresREST': True,  'requiresRucio': False,  'requiresDirOption': True,  'useCache': True,  'requiresProxyVOOptions': False, 'requiresLocalCache': True },
}


def revertParamsMapping():
    revertedMapping = {}
    for serverParamName, paramInfo in parametersMapping['on-server'].items():
        info = copy.deepcopy(paramInfo)
        info.pop('config')
        for clientParamName in paramInfo['config']:
            revertedMapping[clientParamName] = {'server': serverParamName}
            revertedMapping[clientParamName].update(info)
    for paramInfo in parametersMapping['other-config-params']:
        info = copy.deepcopy(paramInfo)
        info.pop('config')
        for clientParamName in paramInfo['config']:
            revertedMapping[clientParamName] = {'server': None}
            revertedMapping[clientParamName].update(info)
    return revertedMapping

## This mapping looks like this:
## {'General.requestName'     : {'server': 'workflow',   'default': None,  'type': 'StringType',  'required': False},
##  'General.activity'        : {'server': 'activity',   'default': None,  'type': 'StringType',  'required': False},
##  'General.transferOutputs' : {'server': 'saveoutput', 'default': True,  'type': 'BooleanType', 'required': False},
##  etc, for all CRAB configuration parameters
## }
configParametersInfo = revertParamsMapping()


def getParamServerName(paramName):
    return configParametersInfo.get(paramName, {}).get('server')


def getParamDefaultValue(paramName):
    return configParametersInfo.get(paramName, {}).get('default')
