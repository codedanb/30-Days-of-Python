# Python_02_INTERMEDIATE

## Building Proficiency in Python

*Target Audience*: Junior Developer / Daily User.  
*Philosophy*: Focus on "Getting things done". Standard patterns and libraries.

### Standard Library Usage

**os module**: path operations (os.path.join for cross-platform paths, os.path.exists to check file existence, os.path.isdir for directory checks); file manipulation (os.rename to rename files, os.remove to delete files, os.mkdir to create directories); environment variables (os.environ.get to access env vars).

**sys module**: command-line arguments (sys.argv list for script arguments); exit codes (sys.exit(0) for success, sys.exit(1) for error); system info (sys.version for Python version).

**json module**: encoding/decoding (json.dumps to serialize dict to string, json.loads to parse string to dict) with error handling (try-except for JSONDecodeError); file operations (json.dump to write to file, json.load to read from file).

**datetime module**: date/time objects (datetime.datetime.now() for current time, datetime.date.today() for today's date); formatting (strftime('%Y-%m-%d') for string conversion); timedelta for date arithmetic (date + timedelta(days=1)).

**collections module**: Counter for counting elements (Counter([1,2,2,3]) -> {2:2, 1:1, 3:1}); defaultdict for default values (defaultdict(list) auto-creates lists); namedtuple for lightweight classes (Point = namedtuple('Point', ['x', 'y'])).

### Common Data Structures

**Lists**: list comprehensions [x**2 for x in range(10) if x % 2 == 0]; slicing operations list[1:5:2] (start:stop:step); built-in methods (append for adding single item, extend for adding multiple, insert(index, item), remove(value), pop(index), sort(key=lambda x: x[1]), reverse()); copying (shallow copy with list[:], deep copy with copy.deepcopy).

**Dictionaries**: dict comprehensions {k: v.upper() for k,v in d.items() if len(v) > 3}; accessing methods (keys() for iteration, values() for values list, items() for key-value pairs); safe access (get(key, default) instead of d[key]); merging (update(other_dict), **d1 | d2 in Python 3.9+); ordered dicts from collections.OrderedDict.

**Tuples and Sets**: tuple packing/unpacking (x, y = 1, 2; *rest = tuple); tuple as immutable dict keys; set operations (union |, intersection &, difference -, symmetric_difference ^); set comprehensions {x for x in range(10) if x % 2 == 0}; frozenset for immutable sets usable as dict keys.

### Modular Programming

**Functions**: default parameters (def greet(name, greeting="Hello")); variable arguments (*args for positional, **kwargs for keyword); lambda functions (sorted(list, key=lambda x: x[1])); recursion basics (factorial with base case); function annotations (def func(x: int) -> int).

**Modules and Packages**: importing patterns (import module, from module import func, import module as alias); __name__ == "__main__" for script execution; relative imports (from .subpackage import module); package structure (__init__.py files).

### Object-Oriented Programming

**Classes and Objects**: __init__ method for initialization (def __init__(self, name): self.name = name); instance methods (def method(self): pass); class variables vs instance variables; property decorator (@property for getters, @setter for setters).

**Inheritance and Polymorphism**: single inheritance (class Child(Parent): pass); method overriding; super() for parent calls; isinstance() and issubclass() checks; duck typing for polymorphism.

### File I/O

**Text Files**: with statement for automatic closing (with open('file.txt', 'r', encoding='utf-8') as f: content = f.read()); reading modes ('r' read, 'w' write, 'a' append); line-by-line reading (for line in f:); writing (f.write(string), f.writelines(list)).

**Binary Files**: 'rb'/'wb' modes; pickle module for object serialization (pickle.dump(obj, file), pickle.load(file)); struct module for binary data packing/unpacking.

**CSV and JSON**: csv.reader/csv.writer for comma-separated values; json.dump/load with indent for pretty printing; pandas.read_csv for dataframes (if using pandas).

### Error Handling

**Try-Except Blocks**: specific exceptions (except ValueError, except FileNotFoundError); multiple excepts; else clause for no-exception code; finally for cleanup; exception chaining (raise from).

**Custom Exceptions**: class CustomError(Exception): pass; raising (raise CustomError("message")); exception hierarchy.

**Context Managers**: with statement usage; implementing __enter__ and __exit__ for custom context managers.

### Next Steps  
Build a command-line task manager using classes, file I/O for persistence, and error handling for user input validation.