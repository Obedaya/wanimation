from providers import MVVProvider, ClockProvider, AnimationProvider
from providers.matrix import Matrix

size = (32, 8)
m = Matrix(size)
providers = [
    AnimationProvider(m),
    ClockProvider(m)
]

while True:
    for p in providers:
        print(f"Displaying: {type(p)}")
        p.displayContent(10)
