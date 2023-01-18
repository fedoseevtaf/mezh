# Rules:

- Only tabs
- No .gitignore in repo
- Tiny __init__
- Tests segregation

## Indentation policy

You MUST use tabs instead of spaces, 
because tabs can be rescaled and customised easily.

## .gitignore policy

You SHALL NOT push or even commit .gitignore, 
but you SHALL use it to protect repo of unexpected 
info about your work process.

## Constructor policy

You SHALL make tiny minimal __init__.

## Tests policy

You SHALL NOT write tests in the files 
that actualy contains the code (For example `doctest` tests), 
but you can write examples of usage (using `doctest`), if it's correct 
and you can run it without exceptions.

