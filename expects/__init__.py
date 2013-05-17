# -*- coding: utf-8 -*


class Expectation(object):
    def __init__(self):
        self._parent = None

    @property
    def actual(self):
        return self._parent.actual

    def __get__(self, instance, owner):
        if instance is not None:
            self._parent = instance

        return self


class Equal(Expectation):
    def __call__(self, expected):
        assert self.actual == expected, self.error_message(repr(expected))

    def error_message(self, tail):
        return self._parent.error_message('equal {}'.format(tail))


class Be(Expectation):
    equal = Equal()

    def __call__(self, expected):
        assert self.actual is expected, self.error_message(repr(expected))

    @property
    def true(self):
        assert self.actual, self.error_message(True)

    @property
    def false(self):
        assert not self.actual, self.error_message(False)

    def error_message(self, tail):
        return self._parent.error_message('be {}'.format(tail))


class Have(Expectation):
    def property(self, *args):
        name = args[0]

        def error_message(tail):
            return self.error_message('property {}'.format(tail))

        assert hasattr(self.actual, name), error_message(repr(name))

        try:
            expected = args[1]
        except IndexError:
            pass
        else:
            value = getattr(self.actual, name)

            assert value == expected, error_message('{} with value {} but was {}'.format(
                repr(name), repr(expected), repr(value)))

    def error_message(self, tail):
        return self._parent.error_message('have {}'.format(tail))


class To(Expectation):
    be = Be()
    have = Have()
    equal = Equal()

    def error_message(self, tail):
        return self._parent.error_message('to {}'.format(tail))


class expect(object):
    to = To()

    def __init__(self, actual):
        self.actual = actual

    def error_message(self, tail):
        return 'Expected {} {}'.format(repr(self.actual), tail)
