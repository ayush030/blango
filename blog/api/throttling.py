from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import throttling

class AnonSustainedThrottle(AnonRateThrottle):
  scope= "anon_sustained"

class AnonBurstThrottle(AnonRateThrottle):
  scope = "anon_burst"

class UserSustainedThrottle(UserRateThrottle):
  scope = 'user_sustained'

class UserBurstThrottle(UserRateThrottle):
  scope = 'user_burst'



# custom throttling
# add this to throttling classes in settings.py. Throttle only when generated rand is 1
class RandomRateThrottling(throttling.BaseThrottle):
  def allow_request(self, request, view):
    return random.randint(1, 10) != 1