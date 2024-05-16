# pi
A polyglot opening book generator.

## Dependencies
Run `pip3 install chess torch` to install the dependencies.

## Configuring
Change these parameters in `gen.py`:
- `ENGINE_PATH`: path to your engine
- `FACTOR`: move quality
- `THRESHOLD`: probability threshold, roughly equals to 1/(# of positions)
- `ANALYSE_DEPTH`: analyse depth

## Running
Run `python3 gen.py`.
Running may take a while depending on the parameters.
