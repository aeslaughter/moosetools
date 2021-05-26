#* This file is part of MOOSETOOLS repository
#* https://www.github.com/idaholab/moosetools
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moosetools/blob/main/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html

from collections import OrderedDict
import re
import enum
import logging
import copy

import mooseutils
from .Parameter import Parameter


class InputParameters(object):
    """
    A warehouse for creating and storing options
    """
    from moosetools import base  # Avoid cyclic imports

    __PARAM_TYPE__ = Parameter

    class ErrorMode(enum.Enum):
        """Defines the error mode for all instances"""
        NONE = 0  # disable errors
        WARNING = 1  # logging.warning
        ERROR = 2  # logging.error
        CRITICAL = 3  # logging.critical
        EXCEPTION = 4  # raises MooseException, the import occurs when raised to avoid cyclic imports

    def __init__(self):
        self.__parameters = OrderedDict()
        self.add(
            '_moose_object',
            private=True,
            doc= "The `MooseObject` that the InputParameter object belongs, if provided the error " \
                 "logging will log via the `MooseObject`."
        )
        self.add('error_mode',
                 default=InputParameters.ErrorMode.EXCEPTION,
                 vtype=InputParameters.ErrorMode)

    def add(self, *args, **kwargs):
        """
        Add a new Parameter to the warehouse

        Inputs:
            see Parameter.py
        """
        if args[0] in self.__parameters:
            self.__errorHelper("Cannot add parameter, the parameter '{}' already exists.", args[0])
            return

        elif '_' in args[0]:
            group, subname = args[0].rsplit('_', 1)
            if (group in self.__parameters) and (
                    isinstance(self.__parameters[group].value, InputParameters) or
                (isinstance(self.__parameters[group].default, InputParameters))):

                self.__errorHelper(
                    "Cannot add a parameter with the name '{}', "
                    "a sub parameter exists with the name '{}'.", args[0], group)
                return

        default = kwargs.get('default', None)
        if isinstance(default, InputParameters):
            kwargs['vtype'] = InputParameters

        self.__parameters[args[0]] = self.__PARAM_TYPE__(*args, **kwargs)

    def __contains__(self, name):
        """
        Allows keys to be tested via "in" keyword.
        """
        return name in self.__parameters

    def __iadd__(self, params):
        """
        Append another Parameter objects options into this container.

        Inputs:
           options[InputParameters]: An instance of an InputParameters object to append.
        """
        for key in params.keys():
            self.__parameters[key] = params._InputParameters__parameters[key]
        return self

    def parameter(self, *args):
        """
        Return the desired `Parameter` object.

        The inputs are as defined in `set` method.
        """
        return self._getParameter(*args)

    def parameters(self):
        """
        Iterate over the `Parameter` objects.
        """
        for name, param in self.__parameters.items():
            if not param.private:
                yield param

    def items(self):
        """
        Provides dict.items() functionality.
        """
        for name, param in self.__parameters.items():
            if not param.private:
                yield name, param.value

    def values(self):
        """
        Provides dict.values() functionality.
        """
        for param in self.__parameters.values():
            if not param.private:
                yield param.value

    def keys(self):
        """
        Provides dict.keys() functionality.
        """
        return [key for key, value in self.__parameters.items() if not value.private]

    def remove(self, name):
        """
        Remove an option from the warehouse.

        Inputs:
            name[str]: The name of the Parameter to remove
        """
        if name not in self.__parameters:
            self.__errorHelper("The parameter '{}' does not exist.", name)
        else:
            self.__parameters.pop(name)

    def isValid(self, *args):
        """
        Test if the given option is valid (i.e., !None). (public)

        Inputs:
            name[str]: The name of the Parameter to retrieve
        """
        opt = self._getParameter(*args)
        if opt is not None:
            return opt.value is not None

    def setRequired(self, *args):
        """
        Set the required status for a parameter.
        """
        opt = self._getParameter(*args[:-1])
        if opt is not None:
            ret, err = opt.setRequired(args[-1])
            if ret > 0:
                self.__errorHelper(err)

    def isRequired(self, *args):
        """
        Return True if the parameter is required.
        """
        opt = self._getParameter(*args)
        if opt is not None:
            return opt.required
        return False

    def setDefault(self, *args):
        """
        Set the default value.
        """
        opt = self._getParameter(*args[:-1])
        if opt is not None:
            ret, err = opt.setDefault(args[-1])
            if ret > 0:
                self.__errorHelper(err)

    def getDefault(self, *args):
        """
        Return the default value
        """
        opt = self._getParameter(*args)
        if opt is not None:
            return opt.default

    def isDefault(self, *args):
        """
        Return True if the supplied option is set to the default value.

        Inputs:
            name[str]: The name of the Parameter to test.
        """
        opt = self._getParameter(*args)
        if opt is not None:
            return opt.value == opt.default

    def isSetByUser(self, *args):
        """
        Return True if the supplied option was set after construction.

        Inputs:
            name[str]: The name of the Parameter to test.
        """
        opt = self._getParameter(*args)
        if opt is not None:
            return opt.is_set_by_user

    def setValue(self, *args):
        """
        Set the value of a parameter or update contents of a sub-parameters.

        If the associated parameter is an InputParameters object and the value is a dict, update
        the parameters via InputParameters.update

        Use:
           params.setValue('foo', 42)            # foo is an 'int'
           params.setValue('bar', 'year', 1980)  # bar is an 'InputParameters' object
           params.setValue('bar', {'year':1980}) # bar is an 'InputParameters' object
           params.setValue('bar_year', 1980)     # bar is an 'InputParameters' object

        Inputs:
            name(s)[str]: The name(s) of the Parameter to modify
            value: The value for setting set the parameter
        """
        param = self._getParameter(*args[:-1])
        if (param is not None) and param.isInstance(InputParameters) and isinstance(args[-1], dict):
            param.value.update(**args[-1])
        elif param is not None:
            ret, err = param.setValue(args[-1])
            if ret > 0:
                self.__errorHelper(err)

    def getValue(self, *args):
        """
        Overload for accessing the parameter value by name with []

        Inputs:
            *args[str]: The name(s) of the Parameter to retrieve, use multiple names for nested parameters
        """
        obj = self._getParameter(*args)
        if obj is not None:
            return obj.value

    def hasParameter(self, name):
        """
        Test that the parameter exists.

        Inputs:
            name[str]: The name of the Parameter to check
        """
        return name in self.__parameters

    def update(self, *args, **kwargs):
        """"
        Update the options given key, value pairs

        Inputs:
            *args: InputParameters objects to use for updating this object.
            **kwargs: key, values pairs to used for updating this object.
        """
        # Update from InputParameters object
        for opt in args:
            if not isinstance(opt, InputParameters):
                self.__errorHelper(
                    "The supplied arguments must be InputParameters objects or key, value pairs.")
            else:
                for key in opt.keys():
                    value = opt.getValue(key)
                    if self.hasParameter(key) and (value is not None):
                        self.setValue(key, value)

        # Update from kwargs
        for k, v in kwargs.items():
            self.setValue(k, v)

    def validate(self):
        """
        Validate that all parameters marked as required are defined
        """
        retcode = 0
        errors = list()
        for param in self.__parameters.values():
            ret, err = param.validate()
            retcode += ret
            if ret: errors.append(err)
        if retcode > 0:
            msg = '\n'.join(errors)
            self.__errorHelper(msg)

    def __str__(self):
        """
        Allows print to work with this class.
        """
        return self.toString()

    def toString(self, *keys, prefix=None, level=0):
        """
        Create a string of all parameters using Parameter.toString
        """
        out = []
        keys = keys or self.keys()
        for key, param in self.__parameters.items():
            if key in keys:
                out.append(param.toString(prefix=prefix, level=level))
        return '\n\n'.join(out)

    def _getParameter(self, *args):
        """
        A helper for returning the a Parameter object that handles nested InputParameters.

        Use:
             _getParameter('foo')
             _getParameter('foo', 'bar')

        Inputs:
            *args[str]: The name(s) of the Parameter to retrieve, use multiple names for nested parameters
        """
        if len(args) < 1:
            self.__errorHelper("One or more names must be supplied.")
            return

        opt = self.__parameters.get(args[0])
        if (opt is None) and ('_' in args[0]):
            group, subname = args[0].split('_', 1)
            sub_args = [group, subname] + list(args[1:]) if len(args) > 1 else [group, subname]
            if self.hasParameter(group):
                return self._getParameter(*sub_args)

        if opt is None:
            self.__errorHelper("The parameter '{}' does not exist.", args[0])
            return None
        elif opt.isInstance(InputParameters) and len(args) > 1:
            value = opt.value or opt.default
            return value._getParameter(*args[1:])
        elif (not opt.isInstance(InputParameters)) and len(args) > 1:
            self.__errorHelper("Extra argument(s) found: {}", ', '.join(str(a) for a in args[1:]))
        else:
            return opt

    def __errorHelper(self, text, *args, **kwargs):
        """
        Produce warning, error, or exception based on operation mode.
        """
        msg = text.format(*args, **kwargs)
        mode = self.getValue('error_mode')
        log = self.getValue('_moose_object') or logging.getLogger(__name__)
        if mode == InputParameters.ErrorMode.WARNING:
            log.warning(msg)
        elif mode == InputParameters.ErrorMode.ERROR:
            log.error(msg)
        elif mode == InputParameters.ErrorMode.CRITICAL:
            log.critical(msg)
        elif mode == InputParameters.ErrorMode.EXCEPTION:
            from moosetools import base
            raise base.MooseException(msg)

    # The following are deprecated
    def addParam(self, name, *args, required=False):
        if len(args) == 1:
            self.add(name, doc=args[0], required=required)
        elif len(args) == 2:
            self.add(name, default=args[0], doc=args[1], required=required)

    def addRequiredParam(self, name, *args):
        self.addParam(name, *args, required=True)

    def __getitem__(self, name):
        return self.getValue(name)

    def __setitem__(self, name, value):
        return self.setValue(name, value)
