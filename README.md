# chess_weaknesses
Find your chess weaknesses

### Setup

- First edit the `config` file to setup your engine path and to edit the file names. You can use the config_example file as a template.
- First execution will be slow as it needs to generate the engine analysis of the last `100` games in the pgn file previously given in the `config` file.
<br>Current rate is at half a second per move.
- That should be it. There are no visualization for now (coming soon) but you can use your debugger to check results.

### Add new MistakesTypes

Each type of mistake is defined as a class inside the folder `MistakeTypes` and which inherits the `MistakeType` class.
<br>
In order to develop a new mistake you must :
- Create a new file with a class inheriting the `MistakeType` class.
- Implement the `has_happened_on_position` function
- Import your class inside the `__init__.py`