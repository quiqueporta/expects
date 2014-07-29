# -*- coding: utf-8 -*

import collections

from .matcher import Matcher
from . import equal as equal_matcher


class _DictMatcher(Matcher):
    def _match(self, subject):
        if self._not_a_dict(subject):
            return False

        return self._matches(subject)

    def _not_a_dict(self, value):
        return not isinstance(value, collections.Mapping)

    def _matches(self, subject):
        args, kwargs = self._expected

        for name in args:
            if not self._has_key(subject, name):
                return False

        for name, value in kwargs.items():
            if not self._has_key(subject, name, value):
                return False

        return True

    def _has_key(self, subject, name, *args):
        if args:
            try:
                value = subject[name]
            except KeyError:
                return False
            else:
                expected_value = args[0]

                if hasattr(expected_value, '_match'):
                    return expected_value._match(value)

                return value == expected_value

        return name in subject

    def _match_negated(self, subject):
        if self._not_a_dict(subject):
            return False

        return not self._matches(subject)

    def _description(self, subject):
        message = '{} {}'.format(type(self).__name__.replace('_', ' '),
                                 plain_enumerate(*self._expected))

        if self._not_a_dict(subject):
            message += ' but is not a dict'

        return message


class have_keys(_DictMatcher):
    def __init__(self, *args, **kwargs):
        try:
            self._expected = (), dict(*args, **kwargs)
        except (TypeError, ValueError):
            self._expected = args, kwargs


class have_key(_DictMatcher):
    def __init__(self, name, *args):
        if args:
            self._expected = (), {name: args[0]}
        else:
            self._expected = (name,), {}


def plain_enumerate(args, kwargs):
    total = len(args) + len(kwargs)

    result = ''
    i = 0
    for i, arg in enumerate(args):
        result += repr(arg)

        if i + 2 == total:
            result += ' and '
        elif i + 1 != total:
            result += ', '

    for i, pair in enumerate(_ordered_items(kwargs), i):
        key, value = pair
        if not isinstance(value, Matcher):
            value = equal_matcher(value)

        result += '{!r} {}'.format(key, value._description(None))

        if i + 2 == total:
            result += ' and '
        elif i + 1 != total:
            result += ', '

    return result


def _ordered_items(dct):
    return sorted(dct.items(), key=lambda args: args[0])
