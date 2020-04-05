class UserDogStatusConverter:
    regex = 'liked|disliked|undecided'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return '%s' % value