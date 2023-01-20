import cProfile
import LibTests.demo as demo
import pstats


cProfile.run('demo.main()', 'profile.prof')
p = pstats.Stats('profile.prof')
p.strip_dirs().sort_stats('time').print_stats()

# cProfile.runctx('demo.main()', globals(), locals(), 'ctx_profile.prof')
# p = pstats.Stats('ctx_profile.prof')
# p.strip_dirs().sort_stats('time').print_stats()
