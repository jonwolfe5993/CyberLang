upload i with value 10
run diagnostic while i <= 20 holds,
    broadcast i
    upload i with value i + 1.
broadcast "Program done"