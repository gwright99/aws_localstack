# Tied to `factory.py` to work out inner/outer factory model
# https://realpython.com/inner-functions-what-are-they-good-for/

# powers.py

# Define exponent once but let base be variable
def generate_power(exponent):
    def power(base):
        return base ** exponent
    return power

# Set exponent levels
raise_two = generate_power(2)
raise_three = generate_power(3)

# Pass in bases
print(raise_two(4))
print(raise_two(5))

print(raise_three(2))
print(raise_three(3))